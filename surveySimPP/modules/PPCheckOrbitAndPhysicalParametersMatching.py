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
    
    pplogger = logging.getLogger(__name__)

    poi = pd.unique(poiin['ObjID'])
    poiobjs = pd.Series(poi, dtype=object)

    orbin = orbin.astype({'ObjID': object})
    colin = colin.astype({'ObjID': object})

    if orbin['ObjID'].equals(colin['ObjID']):
        if poiobjs.isin(orbin['ObjID']).all():
            return
        else:
            pplogger.error('ERROR: PPCheckOrbitAndPhysicalParametersMatching: input pointing and orbit files do not match.')
            sys.exit('ERROR: PPCheckOrbitAndPhysicalParametersMatching: input pointing and orbit files do not match.')
    else:
        pplogger.error('ERROR: PPCheckOrbitAndPhysicalParametersMatching: input physical parameter and orbit files do not match.')
        sys.exit('ERROR: PPCheckOrbitAndPhysicalParametersMatching: input physical parameter and orbit files do not match.')
