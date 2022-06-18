#!/bin/python

import sys
import pandas as pd
import logging

# Author: Grigori Fedorets


def PPReadOif(oif_output, inputformat):
    """
    PPReadOif.py



    Description: This task reads in the output of oif (objectsInField) and puts it into a
    single pandas dataframe for further use downstream by other tasks.

    This task should be used as the first one in the collection of subsequent tasks
    called recipes.

    Any other relevant data (e.g. magnitudes and colours) are read and amended to the
    main pandas dataframe by separate tasks.



    Mandatory input:      string, oif_output, name of text file including Output from objectsInField (oif)
                         string, inputformat, input format of pointing putput (csv, whitespace, hdf5)



    Output:               pandas dataframe


    usage: padafr=PPReadOif(oif_output,inputformat)
    """

    pplogger = logging.getLogger(__name__)

    if (inputformat == "whitespace"):
        padafr = pd.read_csv(oif_output, delim_whitespace=True)
    elif (inputformat == "comma") or (inputformat == 'csv'):
        padafr = pd.read_csv(oif_output, delimiter=',')
    elif (inputformat == 'h5') or (inputformat == 'hdf5') or (inputformat == 'HDF5'):
        padafr = pd.read_hdf(oif_output).reset_index(drop=True)
    else:
        pplogger.error("ERROR: PPReadOif: unknown format for pointing simulation results.")
        sys.exit("ERROR: PPReadOif: unknown format for pointing simulation results.")

    padafr = padafr.rename(columns=lambda x: x.strip())

    # Here, we drop the magnitudes calculated by oif as they are calculated elsewhere
    # as they can be calculated with a variety of phase functions, and in different filters

    padafr = padafr.drop(['V', 'V(H=0)'], axis=1, errors='ignore')
    padafr['ObjID'] = padafr['ObjID'].astype(str)

    return padafr
