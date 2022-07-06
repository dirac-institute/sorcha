#!/usr/bin/python

import pandas as pd
import sqlite3

# Author: Grigori fedorets


def PPMakeIntermediateEphemerisDatabase(oif_output, outf, chunkSize):
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

    cnx = sqlite3.connect(outf)

    cur = cnx.cursor()

    cmd = 'drop table if exists interm'
    cur.execute(cmd)

    startChunk = 0
    endChunk = 0

    ii = -1
    with open(oif_output) as f:
        for ii, l in enumerate(f):
            pass
    lenf = ii

    while(endChunk <= lenf):
        endChunk = startChunk + chunkSize
        if (lenf - startChunk >= chunkSize):
            incrStep = chunkSize
        else:
            incrStep = lenf - startChunk

        interm = pd.read_csv(oif_output, delim_whitespace=True, skiprows=range(1, startChunk + 1), nrows=incrStep, header=0)
        interm.to_sql("interm", con=cnx, if_exists="append")

        startChunk = startChunk + chunkSize

    return outf
