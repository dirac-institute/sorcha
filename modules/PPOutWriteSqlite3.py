#!/usr/bin/pyton

import pandas as pd
import sqlite3

# Author: Grigori Fedorets

def PPOutWriteSqlite3(pp_results,outf):


    """
    PPOutWriteSqlite3.py


    Description: This task reads in the pandas database, and writes out a Sqlite3 database file by a name given by the user. 


    Mandatory input:      name of database, name of output file

    Output:               Sqlite3 database


    usage: padafr=PPOutWriteSqlite3(padain,outf)
    """
    
    #cnx = sqlite3.connect(':memory:')
    cnx = sqlite3.connect(outf)

    pp_results.to_sql("pp_results", con=cnx, if_exists="replace")
    
    #cnx.execute(
    #"""
    #create table ppresults as 
    #select * from padain
    #"""
    #)
    
    return