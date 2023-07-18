import pandas as pd
import logging
import sys


def PPCheckInputObjectIDs(orbin, colin, poiin):
    """
    Checks whether orbit and physical parameter files contain the same object IDs, and
    additionally checks if the pointing database object iIDs is a subset of
    all the object id:s found in the orbit/physical parameter files.}

    Parameters:
    -----------
    orbin (Pandas dataframe): dataframe of orbital information.

    colin (Pandas dataframe): dataframe of physical parameters.

    poiin (Pandas dataframe): dataframe of pointing database.

    Returns:
    ----------
    None: will error out if a mismatch is found.

    """

    pplogger = logging.getLogger(__name__)

    oif_objects = pd.unique(poiin["ObjID"]).astype(str)
    orb_objects = pd.unique(orbin["ObjID"]).astype(str)
    col_objects = pd.unique(colin["ObjID"]).astype(str)

    if set(col_objects) == set(orb_objects):
        if set(oif_objects).issubset(orb_objects):
            return
        else:
            pplogger.error("ERROR: PPCheckInputObjectIDs: input pointing and orbit files do not match.")
            sys.exit("ERROR: PPCheckInputObjectIDs: input pointing and orbit files do not match.")
    else:
        pplogger.error("ERROR: PPCheckInputObjectIDs: input physical parameter and orbit files do not match.")
        sys.exit("ERROR: PPCheckInputObjectIDs: input physical parameter and orbit files do not match.")
