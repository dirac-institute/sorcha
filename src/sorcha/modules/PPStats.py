import numpy as np
import pandas as pd
import os


def stats(observations, statsfilepath):
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

    Returns
    -------
    None.

    """

    group_by = observations.groupby(["ObjID", "optFilter"])

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
    linked = group_by["object_linked"].agg("all").to_frame("object_linked")
    date_linked = group_by["date_linked_MJD"].agg("first").to_frame("date_linked_MJD")

    joined_stats = num_obs.join([mag, phase_deg, linked, date_linked])
    joined_stats.to_csv(
        path_or_buf=statsfilepath, mode="a", header=not os.path.exists(statsfilepath), index=True
    )

    return
