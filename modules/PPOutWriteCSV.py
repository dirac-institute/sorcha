#!/usr/bin/python

import pandas as pd
import os

#     Author: Grigori Fedorets

def PPOutWriteCSV(padain, outf):
    """
    PPOutWriteCSV.py


    Description: This task reads in the pandas database, and writes out a CSV file by a name given by the user. 


    Mandatory input:      name of database, name of output file

    Output:               CSV file


    usage: padafr=PPOutWriteCSV(padain,outf)
    """


    padain=padain.to_csv(path_or_buf=outf, mode='a', header=not os.path.exists(outf), index=False)

    return