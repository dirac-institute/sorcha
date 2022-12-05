#!/usr/bin/python

import pandas as pd
import sqlite3
import logging
import sys
import os
from datetime import datetime
from .PPReadOif import PPSkipOifHeader

# Author: Grigori fedorets and Steph Merritt


def PPMakeTemporaryEphemerisDatabase(oif_output, outf, inputformat):
    """
    PPMakeTemporaryEphemerisDatabase.py

     Description: This task makes an temporary ephemeris database from the output of
     ObjectsInField/other ephemeris simulation output. This database is done in chunks
     to avoid memory problems.

     Mandatory input:      string, oifoutput, name of output of oif, a tab-separated (later csv) file
                           string, outf, path and name of output temporary sqlite3 database
                           int, chunkSize

     Output:               sqlite3 temporary database

     usage: intermdb=PPMakeTemporaryEphemerisDatabase(oif_output,outf,chunkSize)

    """

    pplogger = logging.getLogger(__name__)

    dstr = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    cpid = os.getpid()

    inter_name = dstr + '-p' + str(cpid) + '-' + 'interim.db'

    cnx = sqlite3.connect(outf + inter_name)

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
        pplogger.error("ERROR: PPMakeTemporaryEphemerisDatabase: unknown format for ephemeris simulation results.")
        sys.exit("ERROR: PPMakeTemporaryEphemerisDatabase: unknown format for ephemeris simulation results.")

    padafr.to_sql("interm", con=cnx, if_exists="append", index=False)

    return outf + inter_name
