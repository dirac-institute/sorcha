#!/bin/python

import pytest
import pandas as pd

from ..PPMatchPointing import PPMatchPointing

def test_PPMatchPointing():
    
    padapo=PPMatchPointing('baseline_10yrs_10klines.db')
    
    nlines=10000
    
    nlinessdb=len(padapo.index)
    
    assert nlines==nlinesdb
    return