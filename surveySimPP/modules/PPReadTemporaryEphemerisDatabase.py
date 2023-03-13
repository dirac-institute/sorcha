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
    cursor1 = con.execute('select * from interm')
    namespd = list(map(lambda x: x[0], cursor1.description))

    part_objid_list_ = tuple(part_objid_list)
    part_objid_list_ = [(i,) for i in part_objid_list]

    cur = con.cursor()

    padafr = []
    for j in part_objid_list_:
        cur.execute("SELECT * from interm WHERE ObjID IN (?);", j)
        padafrtmp = pd.DataFrame(cur.fetchall(), columns=namespd)
        padafr.append(padafrtmp)
    padafr = pd.concat(padafr)

    padafr = padafr.drop(['V', 'V(H=0)'], axis=1, errors='ignore')

    try:
        padafr['ObjID'] = padafr['ObjID'].astype(str)
    except KeyError:
        pplogger.error("ERROR: ephemeris input file does not have 'ObjID' column.")
        sys.exit("ERROR: ephemeris input file does not have 'ObjID' column.")

    return padafr
