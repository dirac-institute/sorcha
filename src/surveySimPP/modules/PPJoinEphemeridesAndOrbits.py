import sys
import logging


def PPJoinEphemeridesAndOrbits(padafr, padaor):
    """
    Joins the ephemerides pandas dataframe with the orbital pandas dataframe. Each
    dataframe has to have same ObjIDs: NaNs will populate the fields for the
    missing objects.

    Parameters:
    -----------
    padafr (Pandas dataframe): dataframe of ephemerides/OIF output.

    padaor (Pandas dataframe): dataframe of orbital information.

    Returns:
    ----------
    resdf (Pandas dataframe): joined dataframe.

    """

    pplogger = logging.getLogger(__name__)

    resdf = padafr.join(padaor.set_index("ObjID"), on="ObjID")

    # check if there is q in the resulting database
    if "q" not in resdf.columns:
        if "a" not in resdf.columns or "e" not in resdf.columns:
            pplogger.error(
                "ERROR: PPJoinEphemeridesAndOrbits: unable to join ephemeris simulation and orbital parameters: no a or e in input."
            )
            sys.exit(
                "ERROR: PPJoinEphemeridesAndOrbits: unable to join ephemeris simulation and orbital parameters: no a or e in input."
            )
        else:
            resdf["q"] = resdf["a"] * (1.0 - resdf["e"])

    return resdf
