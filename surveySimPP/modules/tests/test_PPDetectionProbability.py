import pytest
import numpy as np
import pandas as pd
import sqlite3 as sql


#from ..PPMatchFieldConditions import PPMatchFieldConditions


def test_calcDetectionProbability():
    # Test caclDetetcionProbabilty function

    from surveySimPP.modules.PPDetectionProbability import calcDetectionProbability

    mag = 21.9
    limmag = 22.0

    nominal_result = 0.7310585786300077

    result = calcDetectionProbability(mag, limmag)

    assert result == nominal_result


def test_PPDetectionProbabilty():

    from surveySimPP.modules.PPDetectionProbability import PPDetectionProbability

    # test_in=pd.read_csv('data/test/test_input_PPDetectionProbability')
    # test_target=pd.read_csv('data/test/test_output_PPDetectionProbability')
    # _,limiting_magnitude=PPMatchFieldConditions('./data/baseline_10yrs_10klines.db')
    # con=sql.connect('./data/baseline_10yrs_10klines.db')
    #survey=pd.read_sql_query("SELECT observationId, fiveSigmaDepth FROM SummaryAllProps ORDER BY observationId", con)
    test_in = pd.DataFrame({'FieldID': [0, 0], 'MagnitudeInFilter': [21.9, 21.9], 'fiveSigmaDepth': [22.0, 22.0]})

    survey = pd.DataFrame({'observationId': [0]})

    test_target = pd.DataFrame({'FieldID': [0, 0], 'MagnitudeInFilter': [21.9, 21.9],
                                'detection_probability': [0.7310585786300077, 0.7310585786300077]})

    test_out = test_in.copy()
    test_out['detection_probability'] = PPDetectionProbability(oif_df=test_in)

    assert test_out['detection_probability'][0] == test_target['detection_probability'][0]
    return
