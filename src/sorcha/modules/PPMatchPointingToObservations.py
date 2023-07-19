import pandas as pd
import numpy as np
import logging
import sys


def PPMatchPointingToObservations(padain, pointfildb):
    """
    Merges all relevant columns of each observation from the pointing
    database onto the observations dataframe, then drops all observations which are not
    in one of the requested filters and any duplicate columns.

    Parameters:
    -----------
    padain (Pandas dataframe): dataframe of observations.

    pointfildb (Pandas dataframe): dataframe of the pointing database.

    Returns:
    -----------
    res_df (Pandas dataframe): Merged dataframe of observations with pointing
    database, with all superfluous observations dropped.

    """

    resdf = pd.merge(padain, pointfildb, left_on="FieldID", right_on="FieldID", how="left")

    colour_values = resdf.optFilter.unique()
    colour_values = pd.Series(colour_values).dropna()

    resdf = resdf.dropna(subset=["optFilter"]).reset_index(drop=True)

    chktruemjd = np.isclose(resdf["observationStartMJD"], resdf["FieldMJD"])

    if not chktruemjd.all():
        logging.error(
            "ERROR: PPMatchPointingToObservations: mismatch in pointing database and pointing output times."
        )
        sys.exit(
            "ERROR:: PPMatchPointingToObservations: mismatch in pointing database and pointing output times."
        )

    resdf = resdf.drop(columns=["observationStartMJD", "observationId_"])

    return resdf
