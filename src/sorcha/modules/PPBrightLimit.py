import logging
import sys


def PPBrightLimit(observations, observing_filters, bright_limit):
    """
    Drops observations brighter than the user-defined saturation
    limit. Can take either a single saturation limit for a straight cut, or
    filter-specific saturation limits.

    Parameters:
    -----------
    observations (Pandas dataframe): dataframe of observations.

    observing_filters (list of strings): observing filters present in the data.

    bright_limit (float or list of floats): saturation limits: either single or per-filter.

    Returns:
    ----------
    observations_out (Pandas dataframe): dataframe of filtered observations.

    """

    if type(bright_limit) is float:
        observations_out = observations.drop(
            observations[observations["observedPSFMag"] < bright_limit].index
        )

    elif type(bright_limit) is list:
        drop_index = []

        # get the index of everything brighter than its designated saturation limit in filter
        for i, filt in enumerate(observing_filters):
            ind = observations[
                (observations["optFilter"] == filt) & (observations["observedPSFMag"] < bright_limit[i])
            ].index.values
            drop_index.append(ind.tolist())

        # then drop all at once (it's probably faster this way)
        flat_index = [x for xs in drop_index for x in xs]
        observations_out = observations.drop(flat_index)

    else:
        logging.error("ERROR: PPBrightLimit: expected a float or list of floats for bright_limit.")
        sys.exit("ERROR: PPBrightLimit: expected a float or list of floats for bright_limit.")

    observations_out.reset_index(drop=True, inplace=True)

    return observations_out
