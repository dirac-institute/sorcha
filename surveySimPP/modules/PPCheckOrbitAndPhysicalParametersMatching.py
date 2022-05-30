#!/usr/bin/python

import pandas as pd
import logging
import sys

# Author: Grigori Fedorets


def PPCheckOrbitAndPhysicalParametersMatching(orbin, colin, poiin):
    """
    PPCheckOrbitAndPhysicalParametersMatching

    Description: Checks whether orbit and physical parameter files contain the same object id:s, and
               additionally checks if the pointing database object id:s is a subset of
               all the object id:s found in the orbit/physical parameter files.


    Mandatory input:   pandas dataframe: orbin -- orbits
                      pandas dataframe: colin -- physical parameters
                      pandas dataframe: poiin -- pointing database

    Output:            None; return if there is a match, throw error and quit if mismatch.



    Usage: PPCheckOrbitAndPhysicalParametersMatching(orbin,colin,poiin)

    """

    poi = pd.unique(poiin['ObjID'])
    poiobjs = pd.Series(poi, dtype=object)

    orbin = orbin.astype({'!!OID': object})
    colin = colin.astype({'ObjID': object})

    if orbin['!!OID'].equals(colin['ObjID']):
        if poiobjs.isin(orbin['!!OID']).all():
            return
        else:
            logging.error('ERROR: PPCheckOrbitAndPhysicalParametersMatching: input pointing and orbit files do not match.')
            sys.exit('ERROR: PPCheckOrbitAndPhysicalParametersMatching: input pointing and orbit files do not match.')
    else:
        logging.error('ERROR: PPCheckOrbitAndPhysicalParametersMatching: input physical parameter and orbit files do not match.')
        sys.exit('ERROR: PPCheckOrbitAndPhysicalParametersMatching: input physical parameter and orbit files do not match.')
