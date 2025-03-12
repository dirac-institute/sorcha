# Developed for the Vera C. Rubin Observatory/LSST Data Management System.
# This product includes software developed by the
# Vera C. Rubin Observatory/LSST Project (https://www.lsst.org).
#
# Copyright 2020 University of Washington
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import logging
import numpy as np
import pandas as pd

import sys
import importlib_resources
from shapely.geometry import Point, Polygon, MultiPolygon
from shapely import STRtree, wkb
import sqlite3
import geopandas as gpd
import matplotlib.pyplot as plt
from scipy.spatial import KDTree
from sklearn.neighbors import KDTree as skKD
from tqdm import tqdm

from numba import njit

deg2rad = np.radians
sin = np.sin
cos = np.cos

logger = logging.getLogger(__name__)


# ==============================================================================
# coordinate transforms
# ==============================================================================


def radec_to_tangent_plane(ra, dec, field_ra, field_dec):
    """
    Converts ra and dec to xy on the plane tangent to image center, in the 2-d coordinate system where y is aligned with the meridian.

    Parameters:
    -----------
    ra (float/array of floats): observation Right Ascension, radians.

    dec (float/array of floats): observation Declination, radians.

    fieldra (float/array of floats): field pointing Right Ascension, radians.

    fielddec (float/array of floats): field pointing Declination, radians.

    fieldID (float/array of floats): Field ID, optional.

    Returns:
    ----------
    x, y (float/array of floats): Coordinates on the focal plane, radians projected
    to the plane tangent to the unit sphere.

    """

    # convert to cartesian coordiantes on unit sphere
    observation_vectors = np.array([cos(ra) * np.cos(dec), sin(ra) * np.cos(dec), sin(dec)])  # x  # y  # z

    field_vectors = np.array(
        [cos(field_ra) * np.cos(field_dec), sin(field_ra) * np.cos(field_dec), sin(field_dec)]
    )

    # make the basis vectors for the fields of view
    # the "x" basis is easy, 90 d rotation of the x, y components
    focalx = np.zeros(field_vectors.shape)
    focalx[0] = -field_vectors[1]
    focalx[1] = field_vectors[0]

    # "y" by taking cross product of field vector and "x"
    focaly = np.cross(field_vectors, focalx, axis=0)

    # normalize
    focalx /= np.linalg.norm(focalx, axis=0)
    focaly /= np.linalg.norm(focaly, axis=0)

    # extend observation vectors to plane tangent to field pointings
    k = 1.0 / np.sum(field_vectors * observation_vectors, axis=0)
    observation_vectors *= k
    observation_vectors -= field_vectors

    # get observation vectors as combinations of focal vectors
    x = np.sum(observation_vectors * focalx, axis=0)
    y = np.sum(observation_vectors * focaly, axis=0)

    return x, y


def radec_to_focal_plane(ra, dec, field_ra, field_dec, field_rot):
    # convert ra, dec to points on focal plane, x pointing to celestial north
    x, y = radec_to_tangent_plane(ra, dec, field_ra, field_dec)
    # rotate focal plane to align with detectors
    xy = x + 1.0j * y
    xy *= np.exp(1.0j * field_rot)  # which direction to rotate?

    x = np.real(xy)
    y = np.imag(xy)

    return x, y


# ==============================================================================
# camera class
# ==============================================================================


class DESFootprint:
    """DES Camera footprint class"""

    def __init__(self, path=None):
        """
        Initiates a Footprint object for DES.

        Parameters
        -----------
        path : string, optional
            Path to a .csv file containing detector corners. Default = None


        Returns
        ----------
        Footprint : Footprint
            Footprint object for the provided sensors.

        """

        # file should be a .csv (and should be actually comma seperated)
        # First column is the name of each detector
        # the other two columns are the x, y postion of the detector corner
        # if the user doesn't provide their own version of the footprint,
        # we'll use the default DES version that comes included.
        if path:
            try:
                allcornersdf = pd.read_csv(path)
                logger.info(f"Using CCD Detector file: {path}")
            except IOError:
                logger.error(f"Provided detector footprint file does not exist.")
                sys.exit(1)

        else:
            try:
                default_camera_config_file = "data/DES_detector_corners.csv"
                # stream = pkg_resources.resource_stream(__name__, default_camera_config_file)
                # stream = importlib_resources.as_file( default_camera_config_file )
                stream = importlib_resources.files(__name__).joinpath(default_camera_config_file)
                logger.info(f"Using built-in CCD Detector file: {default_camera_config_file}")
                allcornersdf = pd.read_csv(stream)
            except IOError:
                logger.error(f"Error loading default camera footprint, exiting ...")
                sys.exit(1)

        self.DeCam_footprint(allcornersdf)

    def DeCam_footprint(self, ccd_corners):
        """
        Creates a polygon shape using the package shapely of the DES footprint

        Parameters
        -------------
        ccd_corners : pandas dataframe
            pandas dataframe of the positions of ccd corners

        Returns
        -------------
        footprint : MultiPolygon
            A MultiPolygon of the camera footprint

        """
        polys = []
        poly_name_list = []

        self.ccd_names = [
            "N1",
            "N2",
            "N3",
            "N4",
            "N5",
            "N6",
            "N7",
            "N8",
            "N9",
            "N10",
            "N11",
            "N12",
            "N13",
            "N14",
            "N15",
            "N16",
            "N17",
            "N18",
            "N19",
            "N20",
            "N21",
            "N22",
            "N23",
            "N24",
            "N25",
            "N26",
            "N27",
            "N28",
            "N29",
            "N31",
            "S1",
            "S2",
            "S3",
            "S4",
            "S5",
            "S6",
            "S7",
            "S8",
            "S9",
            "S10",
            "S11",
            "S12",
            "S13",
            "S14",
            "S15",
            "S16",
            "S17",
            "S18",
            "S19",
            "S20",
            "S21",
            "S22",
            "S23",
            "S24",
            "S25",
            "S26",
            "S27",
            "S28",
            "S29",
            "S31",
        ]

        # creates a polygon of each ccd using their corners
        for detector in self.ccd_names:

            corners = ccd_corners[ccd_corners["detectorId"] == detector].reset_index(drop=True)

            p1 = Point(corners["x"][0], corners["y"][0])
            p2 = Point(corners["x"][1], corners["y"][1])
            p3 = Point(corners["x"][2], corners["y"][2])
            p4 = Point(corners["x"][3], corners["y"][3])

            points = [p1, p2, p3, p4, p1]

            poly = Polygon([[np.radians(p.x), np.radians(p.y)] for p in points])
            # list of all the polygons created
            polys.append(poly)
            poly_name_list.append(detector)
        # combines all polygons into a MultiPolygon
        self.footprint = polys
        self.detectorId_list = poly_name_list

    def applyDESFootprint_loadpolygons(
        self, field_df, ra_name="RA_deg", dec_name="Dec_deg", fieldId="FieldID", edge_thresh=None
    ):
        """
        Determine whether detections fall on the sensors defined by the
        footprint. Also returns the an ID for the sensor a detection is made
        on.

        Parameters
        -----------
        field_df : Pandas dataframe
            Dataframe containing detection information with pointings.

        ra_name : string, optional
            "field_df" dataframe's column name for object's RA
             for the given observation. Default = "RA_deg" [units: degrees]

        dec_name : string, optional
            "field_df" dataframe's column name for object's declination
             for the given observation. Default = "Dec_deg" [units: dgrees]

        ra_name_field : string, optional
            "field_df" dataframe's column name for the observation field's RA
             Default = "fieldRA_deg" [units: degrees]

        dec_name_field : string, optional
            "field_df" dataframe's column name for the observation field's declination
             Default = "fieldDec_deg" [Units: degrees]


        edge_thresh: float, optional
            An angular threshold in arcseconds for dropping pixels too close to the edge.
            Default  = None

        Returns
        ----------
        detected : array
            Indices of rows in field_df which fall on the sensor(s).

        detectorID :array
            name of the detector that the object falls on.
        """

        # connecting to visitors database and creating a list of polygons
        with sqlite3.connect("/Users/ryanlyttle/Documents/Workstation/Dark energy survey /visits.db") as conn:
            cursor = conn.cursor()
            query = "SELECT geom FROM polygons_table WHERE observationId = ?"
            index_ = set()
            field_df_no_duplicates = field_df.drop_duplicates(subset=[fieldId], keep="first")
            for obs_id in tqdm(field_df_no_duplicates[fieldId], desc="Processing Observations"):

                row = cursor.execute(query, (obs_id,)).fetchone()

                polygon = wkb.loads(row[0])
                check_points = field_df[field_df[fieldId] == obs_id]

                points = [
                    Point(ra_val, dec_val)
                    for ra_val, dec_val in zip(check_points[ra_name], check_points[dec_name])
                ]

                for point_index, point in enumerate(points):
                    if polygon.contains(point):
                        index_.add(check_points.index[point_index])

        detected = list(index_)
        detectorID = []

        return detected, detectorID

    def applyDESFootprint_KDpolygons_test(
        self, field_df, ra_name="RA_deg", dec_name="Dec_deg", fieldId="FieldID", edge_thresh=None
    ):
        """
        Determine whether detections fall on the sensors defined by the
        footprint. Also returns the an ID for the sensor a detection is made
        on.

        Parameters
        -----------
        field_df : Pandas dataframe
            Dataframe containing detection information with pointings.

        ra_name : string, optional
            "field_df" dataframe's column name for object's RA
            for the given observation. Default = "RA_deg" [units: degrees]

        dec_name : string, optional
            "field_df" dataframe's column name for object's declination
            for the given observation. Default = "Dec_deg" [units: dgrees]

        ra_name_field : string, optional
            "field_df" dataframe's column name for the observation field's RA
            Default = "fieldRA_deg" [units: degrees]

        dec_name_field : string, optional
            "field_df" dataframe's column name for the observation field's declination
            Default = "fieldDec_deg" [Units: degrees]


        edge_thresh: float, optional
            An angular threshold in arcseconds for dropping pixels too close to the edge.
            Default  = None

        Returns
        ----------
        detected : array
            Indices of rows in field_df which fall on the sensor(s).

        detectorID :array
            name of the detector that the object falls on.
        """

        detected_index = set()

        # SQLite Database Connection
        with sqlite3.connect(
            "/Users/ryanlyttle/Documents/Workstation/Dark energy survey /visits_cent.db"
        ) as conn:
            cursor = conn.cursor()
            query = "SELECT ra1,dec1,ra2,dec2,ra3,dec3,ra4,dec4,racenter,deccenter FROM observations WHERE observationId = ?"
        # taking all non duplicate exposure ids (Some footprints have a chance of no objects in them and so polygons won't be made of them when using the ids from the detection pd)
        field_df_no_duplicates = field_df.drop_duplicates(subset=[fieldId], keep="first")
        # going through each polygon in a loop

        flag = 0
        for obs_id in tqdm(field_df_no_duplicates[fieldId], desc="Processing Observations"):

            # executing query for this observation id
            rows = cursor.execute(query, (obs_id,)).fetchall()

            # filtering points for given observation Id
            check_points = field_df[field_df[fieldId] == obs_id]
            points_query = [
                list([ra_val, dec_val])
                for ra_val, dec_val in zip(check_points[ra_name], check_points[dec_name])
            ]

            # attampt using sklearn Kdtree
            ccd_index = skKD(list(zip([row[8] for row in rows], [row[9] for row in rows])))
            max_diff = max(abs(row[0] - row[8]) for row in rows)
            polygon_index_to_create = ccd_index.query_radius(
                points_query, max_diff, count_only=False, return_distance=False
            )
            polygon_index_to_create = list(set(np.concatenate(polygon_index_to_create)))
            if not polygon_index_to_create:
                continue

            polys = []
            for index in polygon_index_to_create:

                row = rows[index]
                polys.append(
                    Polygon([[row[i], row[i + 1]] for i in range(0, len(row) - 2, 2)] + [[row[0], row[1]]])
                )
            polygon = MultiPolygon(polys)

            pol = gpd.GeoSeries(polygon)
            pol.plot()

            plt.scatter(list(zip([row[8] for row in rows])), list(zip([row[9] for row in rows])))
            for p in points_query:

                plt.scatter(p[0], p[1])
            plt.title("defined range")

            # Build KDTree for ra_center and dec_center and query the 3 nearest points for each ccd
            ccd_index = KDTree(list(zip([row[8] for row in rows], [row[9] for row in rows])))
            _, polygon_index_to_create = ccd_index.query(points_query, k=3)
            polygon_index_to_create = list(set(polygon_index_to_create.flatten()))  # removes duplicate ccds.

            polys = []
            for index in polygon_index_to_create:

                row = rows[index]
                polys.append(
                    Polygon([[row[i], row[i + 1]] for i in range(0, len(row) - 2, 2)] + [[row[0], row[1]]])
                )
            polygon = MultiPolygon(polys)

            pol = gpd.GeoSeries(polygon)
            pol.plot()

            plt.scatter(list(zip([row[8] for row in rows])), list(zip([row[9] for row in rows])))
            for p in points_query:

                plt.scatter(p[0], p[1])
            plt.title("3 closest ccds for each point")
            plt.show()

            # creation of camera footprint for this ob id
            # will only create the ccds near possible detections

            flag += 1

            # Create a list of Shapely Point objects for each query point
            points = [Point(point) for point in points_query]

            # Check if points are within any of the polygons
            for point_index, point in enumerate(points):
                if polygon.contains(point):
                    # Add the index to a set if it is inside the polygon
                    detected_index.add(check_points.index[point_index])
            print(detected_index)
            if flag > 30:

                sys.exit()

        detected = list(detected_index)
        detectorID = []

        return detected, detectorID

    def applyDESFootprint_createallpolygons(
        self, field_df, ra_name="RA_deg", dec_name="Dec_deg", fieldId="FieldID", edge_thresh=None
    ):
        """
        Determine whether detections fall on the sensors defined by the
        footprint. Also returns the an ID for the sensor a detection is made
        on.

        Parameters
        -----------
        field_df : Pandas dataframe
            Dataframe containing detection information with pointings.

        ra_name : string, optional
            "field_df" dataframe's column name for object's RA
            for the given observation. Default = "RA_deg" [units: degrees]

        dec_name : string, optional
            "field_df" dataframe's column name for object's declination
            for the given observation. Default = "Dec_deg" [units: dgrees]

        ra_name_field : string, optional
            "field_df" dataframe's column name for the observation field's RA
            Default = "fieldRA_deg" [units: degrees]

        dec_name_field : string, optional
            "field_df" dataframe's column name for the observation field's declination
            Default = "fieldDec_deg" [Units: degrees]


        edge_thresh: float, optional
            An angular threshold in arcseconds for dropping pixels too close to the edge.
            Default  = None

        Returns
        ----------
        detected : array
            Indices of rows in field_df which fall on the sensor(s).

        detectorID :array
            name of the detector that the object falls on.
        """
        index_ = set()
        with sqlite3.connect("/Users/ryanlyttle/Documents/Workstation/Dark energy survey /visits.db") as conn:
            cursor = conn.cursor()
            query = "SELECT ra1,dec1,ra2,dec2,ra3,dec3,ra4,dec4 FROM observations WHERE observationId = ?"

        field_df_no_duplicates = field_df.drop_duplicates(subset=[fieldId], keep="first")
        for obs_id in tqdm(field_df_no_duplicates[fieldId], desc="Processing Observations"):

            rows = cursor.execute(query, (obs_id,)).fetchall()

            polys = [
                Polygon([[row[i], row[i + 1]] for i in range(0, len(row), 2)] + [[row[0], row[1]]])
                for row in rows
            ]
            polygon = MultiPolygon(polys)

            check_points = field_df[field_df[fieldId] == obs_id]

            points = [
                Point(ra_val, dec_val)
                for ra_val, dec_val in zip(check_points[ra_name], check_points[dec_name])
            ]

            for point_index, point in enumerate(points):
                if polygon.contains(point):
                    index_.add(check_points.index[point_index])
        detected = list(index_)
        detectorID = []

        return detected, detectorID



    def applyDESFootprint_KDpolygons(
            self, field_df, ra_name="RA_deg", dec_name="Dec_deg", fieldId="FieldID", edge_thresh=None
        ):
            """
            Determine whether detections fall on the sensors defined by the
            footprint. Also returns the an ID for the sensor a detection is made
            on.

            Parameters
            -----------
            field_df : Pandas dataframe
                Dataframe containing detection information with pointings.

            ra_name : string, optional
                "field_df" dataframe's column name for object's RA
                for the given observation. Default = "RA_deg" [units: degrees]

            dec_name : string, optional
                "field_df" dataframe's column name for object's declination
                for the given observation. Default = "Dec_deg" [units: dgrees]

            ra_name_field : string, optional
                "field_df" dataframe's column name for the observation field's RA
                Default = "fieldRA_deg" [units: degrees]

            dec_name_field : string, optional
                "field_df" dataframe's column name for the observation field's declination
                Default = "fieldDec_deg" [Units: degrees]


            edge_thresh: float, optional
                An angular threshold in arcseconds for dropping pixels too close to the edge.
                Default  = None

            Returns
            ----------
            detected : array
                Indices of rows in field_df which fall on the sensor(s).

            detectorID :array
                name of the detector that the object falls on.
            """

            detected_index = set()

            # SQLite Database Connection
            with sqlite3.connect(
                "/Users/ryanlyttle/Documents/Workstation/Dark energy survey /visits_cent.db"
            ) as conn:
                cursor = conn.cursor()
                query = "SELECT ra1,dec1,ra2,dec2,ra3,dec3,ra4,dec4,racenter,deccenter FROM observations WHERE observationId = ?"
            # taking all non duplicate exposure ids (Some footprints have a chance of no objects in them and so polygons won't be made of them when using the ids from the detection pd)
            field_df_no_duplicates = field_df.drop_duplicates(subset=[fieldId], keep="first")
            # going through each polygon in a loop


            for obs_id in tqdm(field_df_no_duplicates[fieldId], desc="Processing Observations"):

                # executing query for this observation id
                rows = cursor.execute(query, (obs_id,)).fetchall()

                # filtering points for given observation Id
                check_points = field_df[field_df[fieldId] == obs_id]
                points_query = [
                    list([ra_val, dec_val])
                    for ra_val, dec_val in zip(check_points[ra_name], check_points[dec_name])
                ]

                # attampt using sklearn Kdtree
                ccd_index = skKD(list(zip([row[8] for row in rows], [row[9] for row in rows])))
                max_diff = max(abs(row[0] - row[8]) for row in rows)
                polygon_index_to_create = ccd_index.query_radius(
                    points_query, max_diff, count_only=False, return_distance=False
                )
                polygon_index_to_create = list(set(np.concatenate(polygon_index_to_create)))
                if not polygon_index_to_create:
                    continue

                polys = []
                for index in polygon_index_to_create:

                    row = rows[index]
                    polys.append(
                        Polygon([[row[i], row[i + 1]] for i in range(0, len(row) - 2, 2)] + [[row[0], row[1]]])
                    )
                polygon = MultiPolygon(polys)

            
                # Create a list of Shapely Point objects for each query point
                points = [Point(point) for point in points_query]

                # Check if points are within any of the polygons
                for point_index, point in enumerate(points):
                    if polygon.contains(point):
                        # Add the index to a set if it is inside the polygon
                        detected_index.add(check_points.index[point_index])

                

            detected = list(detected_index)
            detectorID = []

            return detected, detectorID