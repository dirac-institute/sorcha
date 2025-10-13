import logging

from shapely.geometry import Point, Polygon
import sqlite3
from scipy.spatial import KDTree
import numpy as np
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)


def PPVisitsFootprint(
    field_df,
    query,
    visits_filename,
    ephermers_buffer=1.5,
    ra_name="RA_deg",
    dec_name="Dec_deg",
    fieldId="FieldID",
    k_num=3,
    plot=False,
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
        SQL query string for visits database. name columns as (llcra, llcdec, lrcra, lrcdec, urcra, urcdec, ulcra, ulcdec, ra_centre, dec_centre, detectorID, fieldFiveSigmaDepth_mag )
    visits_filename : str
        Path to SQLite database containing footprint data.
    ra_name, dec_name, fieldId : str
        Column names in field_df for RA, Dec, and field ID respectively.
    ephermers_buffer : float
        accounts for ar wraping RA points around 0-360, while yhe camera footprint doesnt to avoid the need to create complex shapes
    k_num : int
        number of ccds to check
    plot : boolen
        used to turning on plotting for debugging
    Returns
    -------
    detected_list : list
        List of indices in field_df that fall on a sensor footprint.
    detector_id_list : list
        List of detector IDs corresponding to each detected object.
    """
    detected_indices = set()
    detector_for_index = {}
    lim_mag_list = {}

    # open visits database file
    with sqlite3.connect(visits_filename) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        grouped_fieldId = field_df.groupby(
            fieldId
        )  # group objects by fieldId maybe using np.argsort instead would be faster like in miniDifi?
        for obs_id, points_df in grouped_fieldId:
            rows = cursor.execute(query, (obs_id,)).fetchall()  # execute query on visits database
            if not rows:
                continue  # if no ccds skip

            points_query = np.array(
                list(zip(points_df[ra_name], points_df[dec_name]))
            )  # number list of ra and of objects

            # ephermides wraps points around 0-360. however the ccd ra and decs supplied dont wrap around this point for a given camera footprint to reduce the complexity of creating shapes.
            # therefore to solve this priblem we use the radius from the ar simulations to decide if an object on-sky postion needs to be unwraped for a given camera footprint

            # if the camera footprint is near the boundary i.e the radius of ephermers gen is wrapped round 360-0
            if ephermers_buffer < 180:

                if any(points_df["fieldRA_deg"] + ephermers_buffer > 360):
                    points_query[
                        points_query[:, 0] < 180, 0
                    ] += 360  # use a mask to unwrap points so they are in the same relative coordinates as the footprint
                if any(points_df["fieldRA_deg"] - ephermers_buffer < 0):
                    points_query[points_query[:, 0] > 180, 0] -= 360
            else:
                logger.warning(
                    "Ephemides buffer is too big to account for wrap around. Your footprint will be inaccurate"
                )
                # this might casue issues with objects of massive ephermides (greater than 180). Maybe warn the user of the super extreme case?

            # Kd tree using corners and centres of ccds

            n = len(rows)
            # make an empty array to contain all ccd ra and decs
            all_ccd_points = np.empty((n * 5, 2), dtype=float)
            # make a numpy array for indexing
            point_to_ccd_map = np.repeat(np.arange(n), 5)

            # create the numpy array
            for idx, row in enumerate(rows):
                all_ccd_points[idx * 5 : (idx + 1) * 5] = [
                    (row["ra_centre"], row["dec_centre"]),
                    (row["llcra"], row["llcdec"]),
                    (row["lrcra"], row["lrcdec"]),
                    (row["urcra"], row["urcdec"]),
                    (row["ulcra"], row["ulcdec"]),
                ]
            # Build KDTree with all points
            ccd_tree = KDTree(all_ccd_points)

            if len(rows) > 1:
                k = min(k_num, len(all_ccd_points))
                _, closest_point_indices = ccd_tree.query(points_query, k=k)

                # Map back to unique ccd indices
                unique_ccd_indices = set(point_to_ccd_map[i] for i in closest_point_indices.flatten())
            else:
                unique_ccd_indices = {0}

            polygons = []
            detectors = []
            limmag = []
            # create polygons of only ccds needed
            for idx in unique_ccd_indices:
                row = rows[idx]
                corners = np.array(
                    [
                        (row["llcra"], row["llcdec"]),
                        (row["lrcra"], row["lrcdec"]),
                        (row["urcra"], row["urcdec"]),
                        (row["ulcra"], row["ulcdec"]),
                        (row["llcra"], row["llcdec"]),  # closing polygon
                    ]
                )
                polygons.append(Polygon(corners))
                detectors.append(row["detectorID"])
                limmag.append(row["limMag_perChip"])

            # Create a list of Shapely Point objects for each possible detection
            points = [Point(point) for point in points_query]

            for point_index, point in enumerate(points):  # for every point
                for poly_idx, polygon in enumerate(polygons):  # for every ccd
                    if polygon.contains(point):
                        idx_in_df = points_df.index[point_index]
                        detected_indices.add(idx_in_df)
                        detector_for_index[idx_in_df] = detectors[poly_idx]
                        lim_mag_list[idx_in_df] = limmag[poly_idx]
                        break  # no need to check other polygons for this point if already on one

            # ——————————————————————————————— plotting ———————————————————————————————————
            if plot == True:
                _plotting_camera_footprint(polygons, rows, unique_ccd_indices, points_query, obs_id)
            # ——————————————————————————————— end of plotting ———————————————————————————————————

    detected_list = list(detected_indices)  # list of detected observations
    detector_id_list = [
        detector_for_index[idx] for idx in detected_list
    ]  # list of detector Ids for observation
    lim_mag = [lim_mag_list[idx] for idx in detected_list]
    return detected_list, detector_id_list, lim_mag


def _plotting_camera_footprint(polygons, rows, unique_ccd_indices, points_query, obs_id):

    # Plotting code for each camera footprint use only for debugging (handy for unit tests)
    plt.figure(figsize=(8, 8))
    # Plot ccds with created polygons
    for idx, poly in enumerate(polygons):
        x, y = poly.exterior.xy
        if idx == 0:
            plt.plot(x, y, "b-", linewidth=2, label="Used CCDs")
        else:
            plt.plot(x, y, "b-", linewidth=2)

    polygons_plot = []
    # plot unused ccds for checks
    for j, row in enumerate(rows):
        if j not in unique_ccd_indices:
            corners = np.array(
                [
                    (row["llcra"], row["llcdec"]),
                    (row["lrcra"], row["lrcdec"]),
                    (row["urcra"], row["urcdec"]),
                    (row["ulcra"], row["ulcdec"]),
                    (row["llcra"], row["llcdec"]),  # closing polygon
                ]
            )
            polygons_plot.append(Polygon(corners))
        for poly in polygons_plot:
            x, y = poly.exterior.xy

            if j == 0:
                plt.plot(x, y, "r-", linewidth=2, label="Not Used CCDs")
            else:
                plt.plot(x, y, "r-", linewidth=2)
    # Plot points
    for row in points_query:

        ra = row[0]

        dec = row[1]

        if any(poly.contains(Point(ra, dec)) for poly in polygons):
            plt.scatter(ra, dec, c="g", marker="o", label="Detected")
        else:
            plt.scatter(ra, dec, c="r", marker="o", label="Not Detected")

    handles, labels = plt.gca().get_legend_handles_labels()
    unique = dict(zip(labels, handles))
    plt.legend(unique.values(), unique.keys())
    plt.title(f"Camera Footprint and Detections for obs_id {obs_id}")
    plt.xlabel("RA (deg)")
    plt.ylabel("Dec (deg)")
    plt.tight_layout()
    plt.grid(True)
    plt.show()
