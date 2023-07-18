import pandas as pd
import numpy as np


def PPreadColoursUser(oif_out, colour, mean, stdev, indataf=None):
    """
    Assigns a designated colour to each object in the
    input file and puts it into a single pandas dataframe for further use
    downstream by other tasks. Only one colour is assigned, for more colours,
    the user may run this function several times with different parameters.

    The user may decide to give a single colour, or a uniform distribution of
    colours.
    In case of a single colour, the stdev parameter should be given as zero.

    They also may also wish to amend the existing dataFrame with colours with
    another colour. In that case, duplicate ObjID columns will be removed.

    Parameters:
    -----------
    oif_out (Pandas dataframe): output from objectsInField

    colour (string): colour

    mean (float): mean colour

    stdev (float): standard deviation

    indataf (Pandas dataframe): existing colour dataframe (optional)

    Returns:
    -----------
    padafr (Pandas dataframe)

    """

    nr = oif_out.shape[0]

    new_padafr = oif_out[["ObjID"]]

    clrsnp = np.random.random(size=nr)
    clrsnp = (clrsnp - 0.5) * stdev + mean
    clrs = pd.DataFrame(clrsnp, columns=[colour])
    padafr = pd.concat([new_padafr, clrs], axis=1, sort=False)
    if indataf is not None:
        padafr = pd.concat([padafr, indataf], axis=1, sort=False)
        padafr = padafr.loc[:, ~padafr.columns.duplicated()]

    return padafr
