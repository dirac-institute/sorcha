#!/usr/bin/python

import pandas as pd
import os
import sqlite3
import logging

#     Author: Grigori Fedorets

__all__ = ['PPOutWriteCSV', 'PPOutWriteHDF5',
           'PPOutWriteSqlite3']


def PPOutWriteCSV(padain, outf):
    """
    PPOutWriteCSV.py


    Description: This task reads in the pandas database, and writes out a CSV file by a name given by the user.


    Mandatory input:      name of database, name of output file

    Output:               CSV file


    usage: padafr=PPOutWriteCSV(padain,outf)
    """

    padain = padain.to_csv(path_or_buf=outf, mode='a', header=not os.path.exists(outf), index=False)

    return


def PPOutWriteHDF5(pp_results, outf, keyin):
    """
    PPOutWriteHDF5.py


    Description: This task reads in the pandas database, and writes out a HDF5 binary file by a name given by the user.


    Mandatory input:      name of database, name of output file

    Output:               HDF5 binary database


    usage: padafr=PPOutWriteHDF5(padain,outf)
    """

    of = pp_results.astype(str).to_hdf(outf, mode='a', format='table', append=True, key=keyin)

    return of


def PPOutWriteSqlite3(pp_results, outf):
    """
    PPOutWriteSqlite3.py


    Description: This task reads in the pandas database, and writes out a Sqlite3 database file by a name given by the user.


    Mandatory input:      name of database, name of output file

    Output:               Sqlite3 database


    usage: padafr=PPOutWriteSqlite3(padain,outf)
    """
    pp_results = pp_results.drop('level_0', 1, errors='ignore')

    cnx = sqlite3.connect(outf)

    pp_results.to_sql("pp_results", con=cnx, if_exists="append")


def PPWriteOutput(cmd_args, configs, observations_in, endChunk, verbose=False):
    """
    Author: Steph Merritt

    Description: Writes out the output in the format specified in the config file.

    Mandatory input:    dict, configs, dictionary of config variables created by PPConfigFileParser
                        pandas DataFrame, observations, table of observations for output
    """

    pplogger = logging.getLogger(__name__)
    verboselog = pplogger.info if verbose else lambda *a, **k: None

    if configs['outputsize'] == 'default':
        observations = observations_in[['ObjID', 'FieldMJD', 'fieldRA', 'fieldDec', 
                                        'AstRA(deg)', 'AstDec(deg)', 'AstrometricSigma(deg)', 
                                        'optFilter', 'observedPSFMag', 'observedTrailedSourceMag', 
                                        'PhotometricSigmaPSF(mag)', 'PhotometricSigmaTrailedSource(mag)', 
                                        'fiveSigmaDepth', 'fiveSigmaDepthAtSource']]
    #else:
        #observations = observations_in

    verboselog('Constructing output path...')

    if (configs['outputformat'] == 'csv'):
        outputsuffix = '.csv'
        out = cmd_args['outpath'] + cmd_args['outfilestem'] + outputsuffix
        verboselog('Output to CSV file...')
        observations = PPOutWriteCSV(observations, out)

    elif (configs['outputformat'] == 'separatelycsv'):
        outputsuffix = '.csv'
        objid_list = observations['ObjID'].unique().tolist()
        verboselog('Output to ' + str(len(objid_list)) + ' separate output CSV files...')

        i = 0
        while(i < len(objid_list)):
            single_object_df = pd.DataFrame(observations[observations['ObjID'] == objid_list[i]])
            out = cmd_args['outpath'] + str(objid_list[i]) + '_' + cmd_args['outfilestem'] + outputsuffix
            observations = PPOutWriteCSV(single_object_df, out)
            i = i + 1

    elif (configs['outputformat'] == 'sqlite3'):
        outputsuffix = '.db'
        out = cmd_args['outpath'] + cmd_args['outfilestem'] + outputsuffix
        verboselog('Output to sqlite3 database...')
        observations = PPOutWriteSqlite3(observations, out)

    elif (configs['outputformat'] == 'hdf5' or configs['outputformat'] == 'h5'):
        outputsuffix = ".h5"
        out = cmd_args['outpath'] + cmd_args['outfilestem'] + outputsuffix
        verboselog('Output to HDF5 binary file...')
        observations = PPOutWriteHDF5(observations, out, str(endChunk))
