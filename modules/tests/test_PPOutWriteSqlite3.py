#!/bin/python

import pytest
import pandas as pd
import os, sys
import sqlite3

from ..PPJoinColourPointing import PPJoinColourPointing
from ..PPhookBrightnessWithColour import PPhookBrightnessWithColour
from ..PPReadOif import PPReadOif
from ..PPReadColours import PPReadColours
from ..PPMatchPointing import PPMatchPointing
from ..PPMatchPointingsAndColours import PPMatchPointingsAndColours
from ..PPOutWriteSqlite3 import PPOutWriteSqlite3



def test_PPOutWriteSqlite3():

    padafr=PPReadOif('./data/test/oiftestoutput.txt', " ", 'txt')
    padacl=PPReadColours('./data/test/testcolour.txt', 0, 5, " ")
    
    resdf=PPJoinColourPointing(padafr,padacl)
    
    
    resdf1=PPhookBrightnessWithColour(resdf, 'r', 'i-r', 'i')
    resdf3=PPhookBrightnessWithColour(resdf1, 'r', 'g-r', 'g')
    
    
    pada5=PPMatchPointing('./data/test/baseline_10yrs_10klines.db', ['g', 'r', 'i'])
    pada6=PPMatchPointingsAndColours(resdf3,pada5)
    
    
    pada7=PPOutWriteSqlite3(pada6,'./outtest.db')
    nrows=5
    
    con = sqlite3.connect('./outtest.db')
    cur = con.cursor()
    cur.execute("SELECT COUNT(*) FROM pp_results")
    i=cur.fetchone()[0]
    cmp=int(i)

    os.system("rm ./outtest.db")
    
    
    assert nrows==cmp
    return    