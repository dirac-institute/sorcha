import pytest
import numpy as np
import pandas as pd 
import sqlite3 as sql

from ..PPDetectionProbability import calcDetectionProbability, PPDetectionProbability
#from ..PPMatchFieldConditions import PPMatchFieldConditions

def test_calcDetectionProbability():
    # Test caclDetetcionProbabilty function

    mag    = 21.9
    limmag = 22.0

    nominal_result = 0.7310585786300077

    result = calcDetectionProbability(mag, limmag)

    assert result == nominal_result

def test_PPDetectionProbabilty():

    #test_in=pd.read_csv('data/test/test_input_PPDetectionProbability')
    #test_target=pd.read_csv('data/test/test_output_PPDetectionProbability')
    #_,limiting_magnitude=PPMatchFieldConditions('./data/baseline_10yrs_10klines.db')
    #con=sql.connect('./data/baseline_10yrs_10klines.db')
    #survey=pd.read_sql_query("SELECT observationId, fiveSigmaDepth FROM SummaryAllProps ORDER BY observationId", con)
    test_in=pd.DataFrame({'FieldID': [0, 0], 'MaginFil': [21.9, 21.9]})

    survey=pd.DataFrame({'observationId': [0], 'fiveSigmaDepth': [22.0]})

    test_target=pd.DataFrame({'FieldID': [0, 0], 'MaginFil': [21.9, 21.9], 
                              'detection probability': [0.7310585786300077, 0.7310585786300077]})

    test_out=test_in.copy()
    test_out['detection probability']=PPDetectionProbability(test_in, survey)

    assert test_out['detection probability'][0]==test_target['detection probability'][0]
    return
