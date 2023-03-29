import pandas as pd
import sqlite3
import logging
import sys


def PPReadTemporaryEphemerisDatabase(intermdb, part_objid_list):
    """
    Reads in the temporary pointing sqlite3 database specified
    by a subset of object IDs, and outputs a pandas dataframe.

    Parameters:
    -----------
    intermdb (string): filepath/name of temporary database.

    part_objid_list (list): list of object IDs to read in from temporary database.

    Returns:
    -----------
    padafr (Pandas dataframe): dataframe pulled from temporary database.

    """

    pplogger = logging.getLogger(__name__)

    con = sqlite3.connect(intermdb)

    prm_list = ', '.join('?' for _ in part_objid_list)

    sql = 'SELECT * FROM interm WHERE ObjID IN ({})'.format(prm_list)

    padafr = pd.read_sql(sql, con=con, params=part_objid_list)

    padafr = padafr.drop(['V', 'V(H=0)'], axis=1, errors='ignore')

    try:
        padafr['ObjID'] = padafr['ObjID'].astype(str)
    except KeyError:
        pplogger.error('ERROR: ephemeris input file does not have "ObjID" column.')
        sys.exit('ERROR: ephemeris input file does not have "ObjID" column.')

    return padafr
