import numpy as np
import pandas as pd
import os


def stats(observations, statsfilepath, filters):
    """
    Write a summary statistics file including whether each object was linked
    or not within miniDifi, their number of observations, min/max phase angles,
    min/max trailed source magnitudes, and median trailed source magnitudes
    per filter

    Parameters
    ----------
    observations : Pandas dataframe
        Pandas dataframe of observations

    statsfilepath : string
        Path to write summary stats file to

    filters : list of strings
        List of observation filters of interest

    Returns
    -------
    None.

    """

    ssObjects = np.unique(observations["ObjID"])
    stats_dict = {"ObjID": [], "isLinked": []}

    for filter_name in filters:
        stats_dict["number_obs_" + filter_name] = []
        stats_dict["med_apparent_mag_" + filter_name] = []
        stats_dict["min_apparent_mag_" + filter_name] = []
        stats_dict["max_apparent_mag_" + filter_name] = []
        stats_dict["max_phase_" + filter_name] = []
        stats_dict["min_phase_" + filter_name] = []

    for obj in ssObjects:
        df = observations[observations["ObjID"] == obj]
        stats_dict["ObjID"].append(obj)
        stats_dict["isLinked"].append(any(df["Linked"]))

        filter_value_counts = df.value_counts("optFilter")

        for filter_name in filters:

            try:
                stats_dict["number_obs_" + filter_name].append(filter_value_counts[filter_name])
                stats_dict["max_phase_" + filter_name].append(
                    np.max(df[df["optFilter"] == filter_name]["phase_deg"])
                )
                stats_dict["min_phase_" + filter_name].append(
                    np.min(df[df["optFilter"] == filter_name]["phase_deg"])
                )
                stats_dict["med_apparent_mag_" + filter_name].append(
                    np.median(df[df["optFilter"] == filter_name]["trailedSourceMag"])
                )
                stats_dict["max_apparent_mag_" + filter_name].append(
                    np.max(df[df["optFilter"] == filter_name]["trailedSourceMag"])
                )
                stats_dict["min_apparent_mag_" + filter_name].append(
                    np.min(df[df["optFilter"] == filter_name]["trailedSourceMag"])
                )

            except KeyError:
                stats_dict["number_obs_" + filter_name].append(0)
                stats_dict["max_phase_" + filter_name].append(0)
                stats_dict["min_phase_" + filter_name].append(0)
                stats_dict["med_apparent_mag_" + filter_name].append(0)
                stats_dict["max_apparent_mag_" + filter_name].append(0)
                stats_dict["min_apparent_mag_" + filter_name].append(0)

    stats_df = pd.DataFrame(stats_dict)
    stats_df.to_csv(
        path_or_buf=statsfilepath, mode="a", header=not os.path.exists(statsfilepath), index=False
    )

    return
