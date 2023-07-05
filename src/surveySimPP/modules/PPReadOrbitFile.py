import pandas as pd
import sys
import logging


def PPReadOrbitFile(orbin, beginLoc, chunkSize, filesep):
    """Read orbits file, and store in a pandas dataframe.

    Parameters:
    -----------
    orbin (string): location/name of orbits data file.

    beginLoc (int): location in file where reading begins.

    chunkSize (int): length of chunk to be read in.

    filesep (string): format of input file ("whitespace"/"comma"/"csv").

    Returns:
    -----------
    padafr (Pandas dataframe): dataframe of orbital data.

    """

    pplogger = logging.getLogger(__name__)

    if filesep == "whitespace":
        padafr = pd.read_csv(
            orbin, delim_whitespace=True, skiprows=range(1, beginLoc + 1), nrows=chunkSize, header=0
        )
    elif filesep == "csv" or filesep == "comma":
        padafr = pd.read_csv(orbin, delimiter=",", skiprows=range(1, beginLoc + 1), nrows=chunkSize, header=0)

    if "H" in padafr.columns:
        pplogger.error(
            "ERROR: PPReadOrbitFile: H column present in orbits data file. H must be included in physical parameters file only."
        )
        sys.exit(
            "ERROR: PPReadOrbitFile: H column present in orbits data file. H must be included in physical parameters file only."
        )

    padafr = padafr.rename(columns=lambda x: x.strip())

    try:
        padafr["ObjID"] = padafr["ObjID"].astype(str)
    except KeyError:
        pplogger.error(
            "ERROR: PPReadOrbitFile: Cannot find ObjID in column headings. Check input and input format."
        )
        sys.exit(
            "ERROR: PPReadOrbitFile: Cannot find ObjID in column headings. Check input and input format."
        )

    # rename i to incl to avoid confusion with the colour i
    padafr = padafr.rename(columns={"i": "incl"})

    # Check for nans or nulls

    if padafr.isnull().values.any():
        pdt = padafr[padafr.isna().any(axis=1)]
        inds = str(pdt["ObjID"].values)
        outstr = "ERROR: uninitialised values when reading orbit file. ObjID: " + str(inds)
        pplogger.error(outstr)
        sys.exit(outstr)

    padafr = padafr.drop(["INDEX", "N_PAR", "MOID", "COMPCODE", "FORMAT"], axis=1, errors="ignore")

    return padafr
