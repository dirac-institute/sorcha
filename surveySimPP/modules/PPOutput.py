#!/usr/bin/python

import pandas as pd
import os
import sqlite3

#     Author: Grigori Fedorets

__all__ = ['PPOutWriteCSV', 'PPOutWriteHDF5',
          'PPOutWriteSqlite3']

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
    

def PPOutWriteHDF5(pp_results,outf,keyin):


    """
    PPOutWriteHDF5.py


    Description: This task reads in the pandas database, and writes out a HDF5 binary file by a name given by the user. 


    Mandatory input:      name of database, name of output file

    Output:               HDF5 binary database


    usage: padafr=PPOutWriteHDF5(padain,outf)
    """
    
    of=pp_results.astype(str).to_hdf(outf, mode='a', format='table', append=True, key=keyin)
    
    return of
    

def PPOutWriteSqlite3(pp_results,outf):


    """
    PPOutWriteSqlite3.py


    Description: This task reads in the pandas database, and writes out a Sqlite3 database file by a name given by the user. 


    Mandatory input:      name of database, name of output file

    Output:               Sqlite3 database


    usage: padafr=PPOutWriteSqlite3(padain,outf)
    """
    pp_results=pp_results.drop('level_0', 1, errors='ignore')
    
    cnx = sqlite3.connect(outf)

    pp_results.to_sql("pp_results", con=cnx, if_exists="append")
    
    