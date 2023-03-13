import sys
import pandas as pd
import numpy as np
import logging


def PPReadOif(oif_output, inputformat):
    """
    Reads in the output of OIF (objectsInField) and puts it into a
    single pandas dataframe for further use downstream by other tasks.

    Any other relevant data (e.g. magnitudes and colours) are read and amended to the
    main pandas dataframe by separate tasks.

    Parameters:
    -----------
    oif_output (string): location/name of OIF output file.

    inputformat (string): format of input file ("whitespace"/"comma"/"csv"/"h5"/"hdf5").

    Returns:
    -----------
    padafr (Pandas dataframe): dataframe of OIF output.

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

    Parameters:
    -----------
    filename (string): location/name of OIF output file.

    line_start (string): Column heading of first column.

    **kwargs: keyword arguments to pass to pd.read_csv.

    Returns:
    -----------
    padafr (Pandas dataframe): dataframe of OIF output.

    """

    pplogger = logging.getLogger(__name__)

    found = 'no'

    with open(filename) as fh:
        for i, line in enumerate(fh):
            if line.startswith('ObjID'):
                found = i
                break
            if i > 100:  # because we don't want to scan infinitely - OIF headers are ~30 lines long.
                pplogger.error('ERROR: PPReadOif: column headings not found. Ensure column headings exist in OIF output and first column is ObjID.')
                sys.exit('ERROR: PPReadOif: column headings not found. Ensure column headings exist in OIF output and first column is ObjID.')

    if found == 'no':
        pplogger.error('ERROR: PPReadOif: column headings not found. Ensure column headings exist in OIF output and first column is ObjID.')
        sys.exit('ERROR: PPReadOif: column headings not found. Ensure column headings exist in OIF output and first column is ObjID.')

    return pd.read_csv(filename, header=found, **kwargs)
