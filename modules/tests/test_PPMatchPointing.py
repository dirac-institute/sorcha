#!/bin/python

import pytest
import pandas as pd
import sqlite3

from ..PPMatchPointing import PPMatchPointing

def test_PPMatchPointing():
    
    padapo=PPMatchPointing('./data/test/baseline_10yrs_10klines.db', ['u', 'g', 'r', 'i', 'z', 'y'])
    
    nlines=10007
    
    nlinesdb=len(padapo.index)
    
    assert nlines==nlinesdb
    return