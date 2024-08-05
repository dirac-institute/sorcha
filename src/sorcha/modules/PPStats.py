import numpy as np
import pandas as pd
import os


def stats(observations, statsfilename, outpath, configs):
    """
    Write a summary statistics file including whether each object was linked
    or not within miniDifi, their number of observations, min/max phase angles,
    min/max trailed source magnitudes, and median trailed source magnitudes
    per filter

    Parameters
    ----------
    observations : Pandas dataframe
        Pandas dataframe of observations

    statsfilename : string
        Stem filename to write summary stats file to

    Returns
    -------
    None.

    """

    statsfilepath = os.path.join(outpath, statsfilename + ".csv")

    group_by = observations.groupby(["ObjID", "optFilter"], observed=False)

    mag = (
        group_by["trailedSourceMag"]
        .agg(["min", "max", "median"])
        .rename(
            columns={"min": "min_apparent_mag", "max": "max_apparent_mag", "median": "median_apparent_mag"}
        )
    )
    phase_deg = (
        group_by["phase_deg"].agg(["min", "max"]).rename(columns={"min": "min_phase", "max": "max_phase"})
    )
    num_obs = group_by.agg("size").to_frame("number_obs")

    if configs["SSP_linking_on"] and not configs["drop_unlinked"]:
        linked = group_by["object_linked"].agg("all").to_frame("object_linked")
        date_linked = group_by["date_linked_MJD"].agg("first").to_frame("date_linked_MJD")
        joined_stats = num_obs.join([mag, phase_deg, linked, date_linked])
    else:
        joined_stats = num_obs.join([mag, phase_deg])

    joined_stats.to_csv(
        path_or_buf=statsfilepath, mode="a", header=not os.path.exists(statsfilepath), index=True
    )

    return
