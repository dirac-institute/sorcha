import pandas as pd
import sqlite3
import logging
import sys
from .PPReadOif import PPSkipOifHeader


def PPMakeTemporaryEphemerisDatabase(oif_output, out_fn, inputformat, chunksize=1e6):
    """
    Makes an temporary ephemeris database from the output of ObjectsInField/other
    ephemeris simulation output. This database is done in chunks to avoid memory problems.

    Parameters:
    -----------
    oif_output (string): location of OIF/other output to be converted to database.

    out_fn (string): filepath where the temporary database should be saved.

    inputformat (string): format of OIF/other output. Should be "whitespace", "comma"/"csv",
    or "h5"/"hdf5"/"HDF5".

    chunksize (int): number of rows in which to chunk database creation.

    Returns:
    -----------
    out_fn (string): as input.

    """

    pplogger = logging.getLogger(__name__)

    cnx = sqlite3.connect(out_fn)

    cur = cnx.cursor()

    cmd = "drop table if exists interm"
    cur.execute(cmd)

    if inputformat == "whitespace":
        PPChunkedTemporaryDatabaseCreation(cnx, oif_output, chunksize, delimiter="whitespace")
    elif (inputformat == "comma") or (inputformat == "csv"):
        PPChunkedTemporaryDatabaseCreation(cnx, oif_output, chunksize, delimiter=",")
    elif (inputformat == "h5") or (inputformat == "hdf5") or (inputformat == "HDF5"):
        padafr = pd.read_hdf(oif_output).reset_index(drop=True)
        padafr.to_sql("interm", con=cnx, if_exists="append", index=False)
    else:
        pplogger.error(
            "ERROR: PPMakeTemporaryEphemerisDatabase: unknown format for ephemeris simulation results."
        )
        sys.exit("ERROR: PPMakeTemporaryEphemerisDatabase: unknown format for ephemeris simulation results.")

    return out_fn


def PPChunkedTemporaryDatabaseCreation(cnx, oif_output, chunkSize, delimiter):
    """
    Splits up a .csv into chunks to create the temporary ephemerides database,
    to avoid memory problems for very large ephemerides files.

    Parameters:
    -----------
    cnx (sqlite3 connection object): the connection object of the SQLite database.

    oif_output (string): the location of OIF/other output to be converted to database.

    chunkSize (int): number of rows in which to chunk database creation.

    delimiter (string): character used as delimiter in OIF/other output.

    Returns:
    -----------
    None.

    """

    n_rows = -1
    with open(oif_output) as f:
        for n_rows, _ in enumerate(f):
            pass

    startChunk = 0
    endChunk = 0

    while endChunk <= n_rows:
        endChunk = int(startChunk + chunkSize)

        if n_rows - startChunk >= chunkSize:
            incrStep = chunkSize
        else:
            incrStep = n_rows - startChunk

        if delimiter == "whitespace":
            interm = PPSkipOifHeader(
                oif_output, "ObjID", delim_whitespace=True, skiprows=range(1, startChunk + 1), nrows=incrStep
            )
        elif delimiter == ",":
            interm = PPSkipOifHeader(
                oif_output, "ObjID", delimiter=",", skiprows=range(1, startChunk + 1), nrows=incrStep
            )

        interm.drop(["V", "V(H=0)"], axis=1, inplace=True, errors="ignore")
        interm.to_sql("interm", con=cnx, if_exists="append", index=False)

        startChunk = int(startChunk + chunkSize)

    return
