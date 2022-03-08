#!/usr/bin/pyton

import numpy as np
import pandas as pd
import sqlite3
import os

#     Authors: Grigori Fedorets, Samuel Cornwall

# wraps a few common output formats to one function, including some logic to 
# capture various ways to specify formats and handle appending.

def PPWriteOut(oifDF, file_name, format, logger=None, mode='w', keyin=0):

    """ Writes a pandas dataframe to a file. Appends a file suffix (i.e. ".csv") to the name 
    when writing.

    INPUT
    -----
    oifDF               ... Pandas dataframe
    file_name           ... Path + file name
    format              ... file format
    mode                ... write or append
    keyin               ... hdf5 key
    """

    csv_aliases = ["csv", "CSV"]
    hdf_asliases = ["hdf", "h5", "hdf5", "HDF"]
    sql_aliases = ["sql", "SQL"]
    
    if (mode != 'a') and (mode != 'w'):
        # Maybe move this to the logger? Or add to logger and keep print 
        # statement to maximize visibility
        print("Invalid write mode specified. Terminating without writing.")
        return

    # match format to file suffix

    # check if file exists

    if np.isin(format, csv_aliases):
        outf = file_name + ".csv"
        if os.path.exists(outf) and (mode != 'a'):
            try:
                logger.error("ERROR: File already exists, exiting without saving.")
            except NameError:
                print("File already exists, exiting without saving.")
        oifDF.to_csv(path_or_buf=outf, mode=mode, header=not os.path.exists(outf), index=False)
        return

    elif np.isin(format, hdf_asliases):
        outf = file_name + ".h5"
        if os.path.exists(outf) and (mode != 'a'):
            try:
                logger.error("ERROR: File already exists, exiting without saving.")
            except NameError:
                print("File already exists, exiting without saving.")
        oifDF.astype(str).to_hdf(outf, mode=mode, format='table', append=True, key=keyin)
        return

    elif np.isin(format, sql_aliases):
        outf = file_name + '.db'
        if os.path.exists(outf) and (mode != 'a'):
            try:
                logger.error("ERROR: File already exists, exiting without saving.")
            except NameError:
                print("File already exists, exiting without saving.")
        outcon = sql.connect(outf)
        if mode = 'a':
            whatdo = "append"
        elif mode = 'w':
            whatdo = "replace"
        else:
            whatdo = "fail"
        oifDF.to_sql("detections", con=outcon, if_exists=whatdo)
        return