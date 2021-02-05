import pytest
import numpy as np
import pandas as pd 

from ..PPDetectionProbability import calcDetectionProbability, PPDetectionProbability
from ..PPMatchFieldConditions import PPMatchFieldConditions

def test_calcDetectionProbability():
    # Test caclDetetcionProbabilty function

    mag    = 21.9
    limmag = 22.0
    w      = 0.1

    nominal_result = 0.7310585786300077

    result = calcDetectionProbability(mag, limmag, w)

    assert result == nominal_result

def test_PPDetectionProbabilty():

    test_in=pd.read_csv('data/test/test_input_PPDetectionProbability')
    test_target=pd.read_csv('data/test/test_output_PPDetectionProbability')
    _,limiting_magnitude=PPMatchFieldConditions('./data/baseline_10yrs_10klines.db')

    test_out=PPDetectionProbability(test_in, limiting_magnitude)

    assert test_out['detection probability'][0]==test_target['detection probability'][0]
    return
