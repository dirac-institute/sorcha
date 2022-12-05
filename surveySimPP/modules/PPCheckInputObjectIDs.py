#!/usr/bin/python

import pandas as pd
import logging
import sys

# Author: Grigori Fedorets


def PPCheckInputObjectIDs(orbin, colin, poiin):
    """
    PPCheckInputObjectIDs

    Description: Checks whether orbit and physical parameter files contain the same object id:s, and
               additionally checks if the pointing database object id:s is a subset of
               all the object id:s found in the orbit/physical parameter files.


    Mandatory input:   pandas dataframe: orbin -- orbits
                      pandas dataframe: colin -- physical parameters
                      pandas dataframe: poiin -- pointing database

    Output:            None; return if there is a match, throw error and quit if mismatch.



    Usage: PPCheckInputObjectIDs(orbin,colin,poiin)

    """

    pplogger = logging.getLogger(__name__)

    oif_objects = pd.unique(poiin['ObjID']).astype(str)
    orb_objects = pd.unique(orbin['ObjID']).astype(str)
    col_objects = pd.unique(colin['ObjID']).astype(str)

    if set(col_objects) == set(orb_objects):
        if set(oif_objects).issubset(orb_objects):
            return
        else:
            pplogger.error('ERROR: PPCheckInputObjectIDs: input pointing and orbit files do not match.')
            sys.exit('ERROR: PPCheckInputObjectIDs: input pointing and orbit files do not match.')
    else:
        pplogger.error('ERROR: PPCheckInputObjectIDs: input physical parameter and orbit files do not match.')
        sys.exit('ERROR: PPCheckInputObjectIDs: input physical parameter and orbit files do not match.')
