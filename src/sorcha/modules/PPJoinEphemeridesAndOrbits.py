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

    return resdf
