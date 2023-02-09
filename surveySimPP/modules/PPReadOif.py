#!/bin/python

import sys
import pandas as pd
import numpy as np
import logging

# Author: Grigori Fedorets


def PPReadOif(oif_output, inputformat):
    """
    PPReadOif.py



    Description: This task reads in the output of oif (objectsInField) and puts it into a
    single pandas dataframe for further use downstream by other tasks.

    This task should be used as the first one in the collection of subsequent tasks
    called recipes.

    Any other relevant data (e.g. magnitudes and colours) are read and amended to the
    main pandas dataframe by separate tasks.



    Mandatory input:      string, oif_output, name of text file including Output from objectsInField (oif)
                         string, inputformat, input format of pointing putput (csv, whitespace, hdf5)



    Output:               pandas dataframe


    usage: padafr=PPReadOif(oif_output,inputformat)
    """

    pplogger = logging.getLogger(__name__)

    if (inputformat == "whitespace"):
        padafr = PPSkipOifHeader(oif_output, 'ObjID', delim_whitespace=True)
    elif (inputformat == "comma") or (inputformat == 'csv'):
        padafr = PPSkipOifHeader(oif_output, 'ObjID', delimiter=',')
    elif (inputformat == 'h5') or (inputformat == 'hdf5') or (inputformat == 'HDF5'):
        padafr = pd.read_hdf(oif_output).reset_index(drop=True)
    else:
        pplogger.error("ERROR: PPReadOif: unknown format for ephemeris simulation results.")
        sys.exit("ERROR: PPReadOif: unknown format for ephemeris simulation results.")

    padafr = padafr.rename(columns=lambda x: x.strip())

    padafr = padafr.drop(['V', 'V(H=0)'], axis=1, errors='ignore')

    oif_cols = np.array(['ObjID', 'FieldID', 'FieldMJD', 'AstRange(km)', 'AstRangeRate(km/s)',
                         'AstRA(deg)', 'AstRARate(deg/day)', 'AstDec(deg)',
                         'AstDecRate(deg/day)', 'Ast-Sun(J2000x)(km)', 'Ast-Sun(J2000y)(km)',
                         'Ast-Sun(J2000z)(km)', 'Ast-Sun(J2000vx)(km/s)',
                         'Ast-Sun(J2000vy)(km/s)', 'Ast-Sun(J2000vz)(km/s)',
                         'Obs-Sun(J2000x)(km)', 'Obs-Sun(J2000y)(km)', 'Obs-Sun(J2000z)(km)',
                         'Obs-Sun(J2000vx)(km/s)', 'Obs-Sun(J2000vy)(km/s)',
                         'Obs-Sun(J2000vz)(km/s)', 'Sun-Ast-Obs(deg)'],
                        dtype='object')

    if not set(padafr.columns.values).issubset(oif_cols):
        pplogger.error("ERROR: PPReadOif: column headings do not match expected OIF column headings.")
        sys.exit("ERROR: PPReadOif: column headings do not match expected OIF column headings.")

    padafr['ObjID'] = padafr['ObjID'].astype(str)

    return padafr


def PPSkipOifHeader(filename, line_start='ObjID', **kwargs):
    """Utility function that scans through the lines of OIF output looking for
    the column names then passes the file object to pandas starting from that
    line, thus skipping the long OIF header.
    """

    with open(filename) as f:

        position = 0
        current_line = f.readline()

        # reads the file line by line looking for the line that starts with
        # the expected string
        while not current_line.startswith(line_start):
            position = f.tell()
            current_line = f.readline()

        # changes the file position to the start of the line that begins
        # with the desired string
        f.seek(position)

        # passes that file object to pandas
        return pd.read_csv(f, **kwargs)
