#!/usr/bin/python

import pandas as pd
import sqlite3
import logging
import sys
import os
from datetime import datetime
from .PPReadOif import PPSkipOifHeader

# Author: Grigori fedorets and Steph Merritt


def PPMakeTemporaryEphemerisDatabase(oif_output, outf, inputformat, chunksize=1e6, stemname=None):
    """
    PPMakeTemporaryEphemerisDatabase.py

     Description: This task makes an temporary ephemeris database from the output of
     ObjectsInField/other ephemeris simulation output. This database is done in chunks
     to avoid memory problems.

     Mandatory input:      string, oifoutput, name of output of oif, a tab-separated (later csv) file
                           string, outf, path of output temporary sqlite3 database
                           string, inputformat, string of input format
                           int, chunksize, number of rows to chunk creation by
                           string, stemname, name (without .db) of database

     Output:               sqlite3 temporary database

     usage: intermdb=PPMakeTemporaryEphemerisDatabase(oif_output,outf,chunkSize)

    """

    pplogger = logging.getLogger(__name__)

    if not stemname:
        dstr = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        cpid = os.getpid()
        inter_name = dstr + '-p' + str(cpid) + '-' + 'interim.db'
    else:
        inter_name = stemname + '.db'

    cnx = sqlite3.connect(os.path.join(outf, inter_name))

    cur = cnx.cursor()

    cmd = 'drop table if exists interm'
    cur.execute(cmd)

    if (inputformat == "whitespace"):
        PPChunkedTemporaryDatabaseCreation(cnx, oif_output, chunksize, delimiter='whitespace')
    elif (inputformat == "comma") or (inputformat == 'csv'):
        PPChunkedTemporaryDatabaseCreation(cnx, oif_output, chunksize, delimiter=',')
    elif (inputformat == 'h5') or (inputformat == 'hdf5') or (inputformat == 'HDF5'):
        padafr = pd.read_hdf(oif_output).reset_index(drop=True)
        padafr.to_sql("interm", con=cnx, if_exists="append", index=False)
    else:
        pplogger.error("ERROR: PPMakeTemporaryEphemerisDatabase: unknown format for ephemeris simulation results.")
        sys.exit("ERROR: PPMakeTemporaryEphemerisDatabase: unknown format for ephemeris simulation results.")

    return os.path.join(outf, inter_name)


def PPChunkedTemporaryDatabaseCreation(cnx, oif_output, chunkSize, delimiter):
    """
     Description: This task splits up a .csv into chunks to create the temporary
     ephemeris database, to avoid memory problems for very large ephemeris files.

     Mandatory input:      sqlite3 connection object, cnx, connection to the temporary database
                           string, oif_output, path and name of input ephemeris file
                           int, chunkSize, number of rows to read at once
                           delimiter, string, file delimiter

     Output:               none


    """

    n_rows = -1
    with open(oif_output) as f:
        for n_rows, _ in enumerate(f):
            pass

    startChunk = 0
    endChunk = 0

    while (endChunk <= n_rows):
        endChunk = int(startChunk + chunkSize)

        if (n_rows - startChunk >= chunkSize):
            incrStep = chunkSize
        else:
            incrStep = n_rows - startChunk

        if delimiter == 'whitespace':
            interm = PPSkipOifHeader(oif_output, 'ObjID', delim_whitespace=True, skiprows=range(1, startChunk + 1), nrows=incrStep, header=0)
        elif delimiter == ',':
            interm = PPSkipOifHeader(oif_output, 'ObjID', delimiter=',', skiprows=range(1, startChunk + 1), nrows=incrStep, header=0)

        interm.drop(['V', 'V(H=0)'], axis=1, inplace=True, errors='ignore')
        interm.to_sql("interm", con=cnx, if_exists="append", index=False)

        startChunk = int(startChunk + chunkSize)

    return
