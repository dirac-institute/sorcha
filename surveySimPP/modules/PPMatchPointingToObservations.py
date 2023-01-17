#!/usr/bin/python

import pandas as pd
import numpy as np
import logging
import sys

# Author: Steph Merritt (based on Grigori's PPMatchPointingAndColours)


def PPMatchPointingToObservations(padain, pointfildb):
    """
    Description: Merges all relevant columns of each observation from the pointing
    database onto the observations dataframe, then drops all observations which are not
    in one of the requested filters and any duplicate columns.

    Mandatory input:      Output from objectsInField (oif) or similar (pandas dataframe)
                          Pointing and filter dataframe (pandas dataframe)

    Output:               pandas dataframe


    usage: padafr=PPMatchFilterToObservations(padain,pointfildb)

    """

    resdf = pd.merge(padain, pointfildb,
                     left_on="FieldID",
                     right_on="FieldID",
                     how="left")

    colour_values = resdf.optFilter.unique()
    colour_values = pd.Series(colour_values).dropna()

    resdf = resdf.dropna(subset=['optFilter']).reset_index(drop=True)

    chktruemjd = np.isclose(resdf['observationStartMJD'], resdf['FieldMJD'])

    if not chktruemjd.all():
        logging.error('ERROR: PPMatchFilterToObservations: mismatch in pointing database and pointing output times.')
        sys.exit('ERROR:: PPMatchFilterToObservations: mismatch in pointing database and pointing output times.')

    resdf = resdf.drop(columns=['observationStartMJD', "observationId_"])

    return resdf
