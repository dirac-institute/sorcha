import logging
import sys
import numpy as np
import fnmatch


def PPApplyColourOffsets(observations, function, othercolours, observing_filters, mainfilter):
    """
    Adds the correct colour offset to H based on the filter of each observation,
    then checks to make sure the appropriate columns exist for each phase function model.
    If phase model variables exist for each colour, this function also selects the
    correct variables for each observation based on filter.

    Parameters:
    -----------
    observations (Pandas dataframe): dataframe of observations.

    function (string): string of desired phase function model. Options are HG, HG12, HG1G2, linear, H.

    othercolours (list of strings): list of colour offsets present in input files.

    observing_filters (list of strings): list of observation filters of interest.

    mainfilter (string): the main filter in which H is given and all colour offsets are calculated against.

    Returns:
    -----------
    observations (Pandas dataframe): dataframe of observations with H calculated in relevant filter.

    """

    pplogger = logging.getLogger(__name__)

    H_col = "H_" + mainfilter

    # save original H column: useful for other functions.
    observations["H_original"] = observations[H_col].copy()

    # create a zero-offset column for mainfilter-mainfilter
    observations[mainfilter + "-" + mainfilter] = np.zeros(len(observations))

    # first apply the correct colour offset to H for every observation
    try:
        unique_opt_filters = observations["optFilter"].unique()
        for filter in unique_opt_filters:
            mask = observations["optFilter"] == filter
            diff_column_name = f"{filter}-{mainfilter}"
            observations.loc[mask, H_col] = observations[H_col] + observations[diff_column_name]

    except KeyError:
        pplogger.error("ERROR: PPApplyColourOffsets: H column missing!")
        sys.exit("ERROR: PPApplyColourOffsets: H column missing!")

    # then check the columns for the phase function variables
    # if colour-specific terms exist, pick the columns with the appropriate colour
    # if only one value specified, assume same value for all filters

    if function == "HG1G2":
        G1list = ["G1" + filt for filt in observing_filters]
        G2list = ["G2" + filt for filt in observing_filters]
        col_list = [H_col] + G1list + G2list

        if set([H_col, "G1", "G2"]).issubset(observations.columns):
            pass
        elif set(col_list).issubset(observations.columns):
            observations["G1"] = observations.apply(lambda row: row["G1" + row["optFilter"]], axis=1)
            observations["G2"] = observations.apply(lambda row: row["G2" + row["optFilter"]], axis=1)
            observations.drop(col_list[1:], axis=1, inplace=True)
        else:
            pplogger.error(
                "ERROR: PPApplyColourOffsets: HG1G2 function requires the following input data columns: H, G1, G2."
            )
            sys.exit(
                "ERROR: PPApplyColourOffsets: HG1G2 function requires the following input data columns: H, G1, G2."
            )

    elif function == "HG":
        Glist = ["GS" + filt for filt in observing_filters]
        col_list = [H_col] + Glist

        if set([H_col, "GS"]).issubset(observations.columns):
            pass
        elif set(col_list).issubset(observations.columns):
            observations["GS"] = observations.apply(lambda row: row["GS" + row["optFilter"]], axis=1)
            observations.drop(col_list[1:], axis=1, inplace=True)
        else:
            pplogger.error(
                "ERROR: PPApplyColourOffsets: HG function requires the following input data columns: H, GS."
            )
            sys.exit(
                "ERROR: PPApplyColourOffsets: HG function requires the following input data columns: H, GS."
            )

    elif function == "HG12":
        G12list = ["G12" + filt for filt in observing_filters]
        col_list = [H_col] + G12list

        if set([H_col, "G12"]).issubset(observations.columns):
            pass
        elif set(col_list).issubset(observations.columns):
            observations["G12"] = observations.apply(lambda row: row["G12" + row["optFilter"]], axis=1)
            observations.drop(col_list[1:], axis=1, inplace=True)
        else:
            pplogger.error(
                "ERROR: PPApplyColourOffsets: HG12 function requires the following input data columns: H, G12."
            )
            sys.exit(
                "ERROR: PPApplyColourOffsets: HG12 function requires the following input data columns: H, G12."
            )

    elif function == "linear":
        Slist = ["S" + filt for filt in observing_filters]
        col_list = [H_col] + Slist

        if set([H_col, "S"]).issubset(observations.columns):
            pass
        elif set(col_list).issubset(observations.columns):
            observations["S"] = observations.apply(lambda row: row["S" + row["optFilter"]], axis=1)
            observations.drop(col_list[1:], axis=1, inplace=True)
        else:
            pplogger.error(
                "ERROR: PPApplyColourOffsets: linear function requires the following input data columns: H, S."
            )
            sys.exit(
                "ERROR: PPApplyColourOffsets: linear function requires the following input data columns: H, S."
            )

    elif function == "none":
        pass

    else:
        pplogger.error(
            "ERROR: PPApplyColourOffsets: unknown phase function. Should be HG1G2, HG, HG12 or linear."
        )
        sys.exit("ERROR: PPApplyColourOffsets: unknown phase function. Should be HG1G2, HG, HG12 or linear.")

    # drop colour offset columns
    ks = observations.keys().tolist()
    obsolete_colours = fnmatch.filter(ks, str("?-" + mainfilter))
    observations.drop(obsolete_colours, axis=1, inplace=True)

    # rename H columns to H_filter (for H in filter) and H_mainfilter (for original H)
    observations.rename(columns={H_col: "H_filter", "H_original": H_col}, inplace=True)

    return observations
