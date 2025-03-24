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

from shapely.geometry import Point, Polygon, MultiPolygon
import sqlite3
from scipy.spatial import KDTree


deg2rad = np.radians
sin = np.sin
cos = np.cos

logger = logging.getLogger(__name__)


# ==============================================================================
# camera class
# ==============================================================================


class DESFootprint:
    """DES Camera footprint class"""

    def __init__(self, query=None, visits=None):
        """
        Initiates a Footprint object for DES.

        Parameters
        -----------
        query : sting, optional
            query for visits database. Default = None

        visits : string, optional
            Path to a sql database containing detector corners and centers. Default = None


        Returns
        ----------
        None

        """
        # currently hard coded in.
        # next step would be either to make them config.fov.attributes and cmdline args

        self.filename = visits
        self.query = query

    def applyDESFootprint(self, field_df, ra_name="RA_deg", dec_name="Dec_deg", fieldId="FieldID"):
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



        Returns
        ----------
        detected : array
            Indices of rows in field_df which fall on the sensor(s).

        detectorID :array
            name of the detector that the object falls on.
        """

        detected_index = set()

        # SQLite Database Connection
        with sqlite3.connect(self.filename) as conn:
            cursor = conn.cursor()
            query = self.query
        # taking all non duplicate exposure ids (Some footprints have a chance of no objects in them and so polygons won't be made of them when using the ids from the detection pd)
        field_df_no_duplicates = field_df.drop_duplicates(subset=[fieldId], keep="first")
        # going through each polygon in a loop

        for obs_id in field_df_no_duplicates[fieldId]:

            # executing query for this observation id
            rows = cursor.execute(query, (obs_id,)).fetchall()

            # filtering points for given observation Id
            check_points = field_df[field_df[fieldId] == obs_id]
            points_query = [
                list([ra_val, dec_val])
                for ra_val, dec_val in zip(check_points[ra_name], check_points[dec_name])
            ]
            # creating kd tree of center of each ccd and finding 3 closest ccds to each point
            ccd_index = KDTree(list(zip([row[8] for row in rows], [row[9] for row in rows])))
            _, ccds_to_create = ccd_index.query(points_query, k=3)

            ccds_to_create = list(set(ccds_to_create.flatten()))  # removes duplicate ccds.

            # creates shapely Multipolygon of only selected ccds
            polys = []
            for index in ccds_to_create:

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

        return detected
