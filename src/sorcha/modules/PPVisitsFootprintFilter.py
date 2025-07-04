import logging

from shapely.geometry import Point, Polygon
import sqlite3
from scipy.spatial import KDTree
import numpy as np
logger = logging.getLogger(__name__)


def applyVisitsFootprint(
    field_df, query, visits_filename, ra_name="RA_deg", dec_name="Dec_deg", fieldId="FieldID"
):
    """
    Determine whether detections fall on the sensors defined by the
    footprint. Also returns the ID for the sensor a detection is made
    on.

    Parameters
    ----------
    field_df : pandas.DataFrame
        DataFrame containing detection information with pointings.
    query : str
        SQL query string for visits database. name columns as (llcra, llcdec, lrcra, lrcdec, urcra, urcdec, ulcra, ulcdec, ra_centre, dec_centre, detector)
    visits_filename : str
        Path to SQLite database containing footprint data.
    ra_name, dec_name, fieldId : str
        Column names in field_df for RA, Dec, and field ID respectively.

    Returns
    -------
    detected_list : list
        List of indices in field_df that fall on a sensor footprint.
    detector_id_list : list
        List of detector IDs corresponding to each detected object.
    """
    detected_indices = set()
    detector_for_index = {}

# open visits database file
    with sqlite3.connect(visits_filename) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        grouped_fieldId = field_df.groupby(fieldId) #group objects by fieldId maybe using np.argsort instead would be faster like in miniDifi?
        for obs_id, points_df in grouped_fieldId:
            rows = cursor.execute(query, (obs_id,)).fetchall() # execute query on visits database
            if not rows:
                continue # if no ccds skip

            points_query = np.array(list(zip(points_df[ra_name], points_df[dec_name]))) # number list of ra and of objects

            ccd_centers = [(row["ra_centre"], row["dec_centre"]) for row in rows]
            ccd_tree = KDTree(ccd_centers)
            if len(ccd_centers) > 1:                
                k = min(3, len(ccd_centers)) # making sure theirs no error with 2 ccds
                _, closest_ccd_indices = ccd_tree.query(points_query, k=k)
                unique_ccd_indices = set(closest_ccd_indices.flatten()) #remove duplicates
            else:
                unique_ccd_indices = [0]
            # create polygons for closest ccds to points and record detector name/id
            polygons = []
            detectors = []
            for idx in unique_ccd_indices:
                row = rows[idx]
                corners = np.array([
                    (row["llcra"], row["llcdec"]),
                    (row["lrcra"], row["lrcdec"]),
                    (row["urcra"], row["urcdec"]),
                    (row["ulcra"], row["ulcdec"]),
                    (row["llcra"], row["llcdec"])  # closing polygon
                ])
                polygons.append(Polygon(corners))
                detectors.append(row["detector"])


            # Create a list of Shapely Point objects for each possible detection
            points = [Point(point) for point in points_query]

            for point_index, point in enumerate(points): # for every point
                for poly_idx, polygon in enumerate(polygons): # for every ccd
                    if polygon.contains(point):
                        idx_in_df = points_df.index[point_index]
                        detected_indices.add(idx_in_df)
                        detector_for_index[idx_in_df] = detectors[poly_idx]
                        break  # no need to check other polygons for this point if already on one


    detected_list = list(detected_indices) # list of detected observations
    detector_id_list = [detector_for_index[idx] for idx in detected_list] # list of detector Ids for observation

    return detected_list, detector_id_list
