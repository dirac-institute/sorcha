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
import matplotlib.pyplot as plt
import sys
import importlib_resources
from shapely.geometry import Point, MultiPolygon, Polygon

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
        # First column is the number of each detector
        # other columns are strings of tuples of the points (I know its dumb gonna change it later)
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

        ccd_names = [
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
            "S30",
            "S31",
        ]

        # creates a polygon of each ccd using their corners
        for detector in ccd_names:
            if detector == "S30":
                continue

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
        self.footprint = MultiPolygon(polys)
        self.detectorId_list = poly_name_list

    def applyDESFootprint(
        self,
        field_df,
        ra_name="RA_deg",
        dec_name="Dec_deg",
        ra_name_field="fieldRA_deg",
        dec_name_field="fieldDec_deg",
        edge_thresh=None,
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

        """

        # convert detections to xyz on unit sphere
        ra = deg2rad(field_df[ra_name])
        dec = deg2rad(field_df[dec_name])

        # convert field pointings to xyz on unit sphere
        fieldra = deg2rad(field_df[ra_name_field])
        fielddec = deg2rad(field_df[dec_name_field])

        points = np.array((radec_to_tangent_plane(ra, dec, fieldra, fielddec)))

        detected = []
        detectorId = []
        for i in range(points.shape[1]):
            point = points[:, i]
            P = Point(point[0], point[1])

            if self.footprint.contains(P):
                detected.append(i)

        # for detector Ids. Takes more time to run as need to loop through 60 polygon contain functions
        # for idx, poly in enumerate(self.footprint.geoms):
        #     if poly.contains(P):
        #         detected.append(i)
        #         detectorId.append(self.detectorId_list[idx])

        # uncomment for plot of camera footprint when running sorcha
        # self.plot(field_df)

        return detected, detectorId

        # check whether they land on the footprint

    def plot(
        self,
        field_df,
        ra_name="RA_deg",
        dec_name="Dec_deg",
        ra_name_field="fieldRA_deg",
        dec_name_field="fieldDec_deg",
    ):
        """
        Shows a plot of DeCam footprint and detections of objects
        """

        # convert detections to xyz on unit sphere
        ra = deg2rad(field_df[ra_name])
        dec = deg2rad(field_df[dec_name])

        # convert field pointings to xyz on unit sphere
        fieldra = deg2rad(field_df[ra_name_field])
        fielddec = deg2rad(field_df[dec_name_field])

        points = np.array((radec_to_tangent_plane(ra, dec, fieldra, fielddec)))

        import geopandas as gpd

        poly = gpd.GeoSeries(self.footprint)
        fig, ax = plt.subplots()
        poly.plot(ax=ax, color="lightblue")
        for i in range(points.shape[1]):
            point = points[:, i]
            P = Point(point[0], point[1])
            if self.footprint.contains(P):
                ax.plot(P.x, P.y, "go", markersize=0.1)
            else:
                ax.plot(P.x, P.y, "ro", markersize=0.1)
        plt.legend(
            ["Detected", "Not Detected"],
            loc="best",
            labels=["Detected", "Not Detected"],
            handles=[
                plt.Line2D([0], [0], marker="o", markersize=5, color="g", lw=0),
                plt.Line2D([0], [0], marker="o", markersize=5, color="r", lw=0),
            ],
        )
        plt.xlabel("ra (radians)")
        plt.ylabel("dec (radians)")
        plt.title("Relative position of objects on DeCam footprint for entire survey")
        # plt.savefig('DeCam_footprint.svg', format='svg', dpi=1200)
        plt.show()
