#!/bin/python

import pytest
import pandas as pd
import sqlite3

from ..PPMatchPointing import PPMatchPointing

def test_PPMatchPointing():
    
    padapo=PPMatchPointing('./data/baseline_10yrs_10klines.db')
    
    nlines=10001
    
    nlinesdb=len(padapo.index)
    
    assert nlines==nlinesdb
    return