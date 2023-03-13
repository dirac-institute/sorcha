import pandas as pd
import sys
import logging


def PPReadPhysicalParameters(clr_datafile, beginLoc, chunkSize, filesep):
    """
    Reads in the physical parameters file and puts it into a
    single pandas dataframe for further use downstream by other tasks.

    Parameters:
    -----------
    clr_datafile (string): location/name of physical parameters data file.

    beginLoc (int): location in file where reading begins.

    chunkSize (int): length of chunk to be read in.

    filesep (string): format of input file ("whitespace"/"comma"/"csv").

    Returns:
    -----------
    padafr (Pandas dataframe): dataframe of physical parameters data.

    """

    pplogger = logging.getLogger(__name__)

    if (filesep == "whitespace"):
        padafr = pd.read_csv(clr_datafile, delim_whitespace=True, skiprows=range(1, beginLoc + 1), nrows=chunkSize, header=0)
    elif (filesep == "comma" or filesep == "csv"):
        padafr = pd.read_csv(clr_datafile, skiprows=range(1, beginLoc + 1), nrows=chunkSize, header=0)

    # check for nans or nulls

    if padafr.isnull().values.any():
        pdt = padafr[padafr.isna().any(axis=1)]
        print(pdt)
        inds = str(pdt['ObjID'].values)
        outstr = "ERROR: uninitialised values when reading colour file. ObjID: " + str(inds)
        pplogger.error(outstr)
        sys.exit(outstr)

    try:
        padafr['ObjID'] = padafr['ObjID'].astype(str)
    except KeyError:
        pplogger.error('ERROR: PPReadPhysicalParameters: Cannot find ObjID in column headings. Check input and input format.')
        sys.exit('ERROR: PPReadPhysicalParameters: Cannot find ObjID in column headings. Check input and input format.')

    return padafr
