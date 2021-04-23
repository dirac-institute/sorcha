import pytest
import numpy as np
import pandas as pd 

from ..PPMatchFieldConditions import PPMatchFieldConditions
from ..PPTrailingLoss import PPTrailingLoss

def test_PPTrailingLoss():
    #Test calcTrailingLoss function

    test_oif=pd.read_csv('./data/test/oiftestoutput', delim_whitespace=True)
    seeing,_=PPMatchFieldConditions('./data/baseline_10yrs_10klines.db')
    seeing.rename(columns={'seeing': 'seeingFwhmGeom'}, inplace=True)

    test_out=PPTrailingLoss(test_oif, seeing)
    print(test_out)

    #assert test_out['trailing loss'][0]==
    return