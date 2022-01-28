#!/bin/python

import pytest
import pandas as pd
import sqlite3

from ..PPMakeIntermediatePointingDatabase import PPMakeIntermediatePointingDatabase
from ..PPReadIntermDatabase import PPReadIntermDatabase
from ..PPReadColours import PPReadColours

def test_PPReadIntermDatabase():
    
    
    padacl=PPReadColours('./data/test/testcolour.txt', 0, 5, 'whitespace')      
    print(padacl)  
    objid_list = padacl['ObjID'].unique().tolist() 
    
    
    daba=PPMakeIntermediatePointingDatabase('./data/test/oiftestoutput.txt','./data/test/testdb_PPIntermDB.db', 10)
    
    padafr=PPReadIntermDatabase('./data/test/testdb_PPIntermDB.db', objid_list)
    
    
    nlines=9
    
    nlinesdb=len(padafr.index)
    
    
    assert nlines==nlinesdb
    return