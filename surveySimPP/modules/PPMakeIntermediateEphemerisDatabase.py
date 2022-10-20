#!/usr/bin/python

import pandas as pd
import sqlite3
import logging
import sys
from .PPReadOif import PPSkipOifHeader

# Author: Grigori fedorets and Steph Merritt


def PPMakeIntermediateEphemerisDatabase(oif_output, outf, inputformat):
    """
    PPMakeIntermediateEphemerisDatabase.py

     Description: This task makes an intermediate ephemeris database from the output of
     ObjectsInField/other ephemeris simulation output. This database is done in chunks
     to avoid memory problems.

     Mandatory input:      string, oifoutput, name of output of oif, a tab-separated (later csv) file
                           string, outf, path and name of output intermediate sqlite3 database
                           int, chunkSize

     Output:               sqlite3 intermediate database

     usage: intermdb=PPReadIntermDatabase(oif_output,outf,chunkSize)

    """

    pplogger = logging.getLogger(__name__)

    cnx = sqlite3.connect(outf)

    cur = cnx.cursor()

    cmd = 'drop table if exists interm'
    cur.execute(cmd)

    if (inputformat == "whitespace"):
        padafr = PPSkipOifHeader(oif_output, 'ObjID', delim_whitespace=True)
    elif (inputformat == "comma") or (inputformat == 'csv'):
        padafr = PPSkipOifHeader(oif_output, 'ObjID', delimiter=',')
    elif (inputformat == 'h5') or (inputformat == 'hdf5') or (inputformat == 'HDF5'):
        padafr = pd.read_hdf(oif_output).reset_index(drop=True)
    else:
        pplogger.error("ERROR: PPMakeIntermediateEphemerisDatabase: unknown format for ephemeris simulation results.")
        sys.exit("ERROR: PPMakeIntermediateEphemerisDatabase: unknown format for ephemeris simulation results.")

    padafr.to_sql("interm", con=cnx, if_exists="append", index=False)

    return outf
