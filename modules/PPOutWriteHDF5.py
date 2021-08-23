#!/usr/bin/pyton

import pandas as pd

# Author: Grigori Fedorets

def PPOutWriteHDF5(pp_results,outf,keyin):


    """
    PPOutWriteSqlite3.py


    Description: This task reads in the pandas database, and writes out a HDF5 binary file by a name given by the user. 


    Mandatory input:      name of database, name of output file

    Output:               HDF5 binary database


    usage: padafr=PPOutWriteHDF5(padain,outf)
    """
    #pp_results=pp_results.drop('level_0', 1, errors='ignore')
    
    #pp_results=pp_results.applymap(str)
    
    of=pp_results.astype(str).to_hdf(outf, mode='a', format='table', append=True, key=keyin)
    

    
    return of