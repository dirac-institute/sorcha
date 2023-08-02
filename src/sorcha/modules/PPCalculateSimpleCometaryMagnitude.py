from sorcha.lsstcomet import Comet
import numpy as np

# Using lsstcomet code by Mike Kelley
# (C)  LSST Solar System Scientific Collaboration 2019


def PPCalculateSimpleCometaryMagnitude(
    padain, observing_filters, rho, delta, alpha, H_col="H_r", colname="TrailedSourceMag"
):
    """
    This task calculates the brightness of the comet at a given pointing
    according to a simple model by A'Hearn et al. (1984).

    The brightness is calculated first in the main filter, and the colour offset is
    applied afterwards.

    Parameters:
    -----------
    padain (Pandas dataframe): dataframe of observations.

    mainfilter (string): the main filter in which H is given and all colour offsets are calculated against.

    othercolours (list of strings): list of colour offsets present in input files.

    colname (string): column name in which to store calculated magnitude.

    Returns:
    ----------
    padain (Pandas dataframe): dataframe of observations with calculated magnitude column.

    """

    # this instantiates the Comet object with H_r, afrho1 and k
    com = Comet(Hr=padain[H_col], afrho1=padain.afrho1, k=padain.k)

    # this is the geometrical data
    g = {"rh": rho, "delta": delta, "phase": alpha}

    # this calculates the coma magnitude in each filter
    for filt in observing_filters:
        padain.loc[padain["optFilter"] == filt, "coma_magnitude"] = com.mag(
            g, filt, rap=padain["seeingFwhmGeom"], nucleus=False
        )

    padain[colname] = -2.5 * np.log10(
        10 ** (-0.4 * padain["coma_magnitude"]) + 10 ** (-0.4 * padain[colname])
    )

    return padain
