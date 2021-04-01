#!/bin/python

import pytest
import pandas as pd
import sqlite3

from ..PPMakeIntermediatePointingDatabase import PPMakeIntermediatePointingDatabase

def test_PPMakeIntermediatePointingDatabase():
    
    daba=PPMakeIntermediatePointingDatabase('./data/test/oiftestoutput','./data/unittest.db', 10)
    

    
    nlines=9
    
    cnx = sqlite3.connect(daba)
    
    cur=cnx.cursor()
    
    cmd='select count (*) from interm'
    cur.execute(cmd)
    
    nlinesdb=cur.fetchall()
    
    nlinesdb=nlinesdb[0]
    nlinesdb=nlinesdb[0]
    
    print(type(nlinesdb))
    
    assert nlines==nlinesdb
    return