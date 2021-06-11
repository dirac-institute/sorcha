#!/bin/python

import pytest
import pandas as pd
import sqlite3

from ..PPMakeIntermediatePointingDatabase import PPMakeIntermediatePointingDatabase
from ..PPReadIntermDatabase import PPReadIntermDatabase
from ..PPReadColours import PPReadColours

def test_PPReadIntermDatabase():
    
    
    padacl=PPReadColours('./data/test/testcolour', 0, 5, ' ')      
    print(padacl)  
    objid_list = padacl['ObjID'].unique().tolist() 
    
    
    daba=PPMakeIntermediatePointingDatabase('./data/test/oiftestoutput','./data/unittest.db', 10)
    
    padafr=PPReadIntermDatabase('./data/unittest.db', objid_list)
    
    
    nlines=9
    
    nlinesdb=len(padafr.index)
    
    
    assert nlines==nlinesdb
    return