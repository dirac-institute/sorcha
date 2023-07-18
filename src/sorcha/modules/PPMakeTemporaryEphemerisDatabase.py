import sqlite3

from sorcha.readers.OIFReader import OIFDataReader


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
    cnx = sqlite3.connect(out_fn)

    cur = cnx.cursor()

    cmd = "drop table if exists interm"
    cur.execute(cmd)

    reader = OIFDataReader(oif_output, inputformat)

    # Load in chunks. The reader does automatic chunking for all file formats
    # and does all validation.
    startChunk = 0
    lastStartChunk = -1
    while lastStartChunk < startChunk:
        lastStartChunk = startChunk
        interm = reader.read_rows(startChunk, chunksize)
        startChunk = int(startChunk + len(interm))

        interm.to_sql("interm", con=cnx, if_exists="append", index=False)

    return out_fn
