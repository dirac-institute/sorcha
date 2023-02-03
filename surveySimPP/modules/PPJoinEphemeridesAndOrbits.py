#!/usr/bin/python

import sys
import logging

# Author: Grigori Fedorets


def PPJoinEphemeridesAndOrbits(padafr, padaor):
    """
    PPJoinEphemeridesAndOrbits.py



    Description: This task  joins the pointing pandas database with the
    orbital pandas database (including brightness H). Each database has to have same ObjID:s: NaN:s will
    be populate the fields for the missing objects.


    Mandatory input:      oif pandas database and colour/cometary database

    Output:               new joined pandas dataframe


    usage: padafr1=PPJoinEphemeridesAndOrbits(padafr,padaor)
    """

    pplogger = logging.getLogger(__name__)

    resdf = padafr.join(padaor.set_index('ObjID'), on='ObjID')

    # check if there is q in the resulting database
    if 'q' not in resdf.columns:
        if ('a' not in resdf.columns or 'e' not in resdf.columns):
            pplogger.error('ERROR: PPJoinEphemeridesAndOrbits: unable to join ephemeris simulation and orbital parameters: no a or e in input.')
            sys.exit('ERROR: PPJoinEphemeridesAndOrbits: unable to join ephemeris simulation and orbital parameters: no a or e in input.')
        else:
            resdf['q'] = resdf['a'] * (1. - resdf['e'])

    return resdf
