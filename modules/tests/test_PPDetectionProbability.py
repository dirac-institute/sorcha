import pytest
import numpy as np
import pandas as pd 

from ..PPDetectionProbability import calcDetectionProbability, filterFadingFunction
from ..PPDetectionProbability import filterSimpleSensorArea

def test_calcDetectionProbability():
    # Test caclDetetcionProbabilty function

    mag    = 21.9
    limmag = 22.0
    w      = 0.1

    nominal_result = 0.7310585786300077

    result = calcDetectionProbability(mag, limmag, w)

    assert result == nominal_result

def test_filterFadingFunction():
    # test filterFadingFunction function

    np.random.seed(4077)

    ephemsdf = pd.DataFrame({
        "Filtermag"           : [18, 19],
        "FieldID"             : [0, 1],
        "AstRARate(deg/sec)"  : [0.000035, 0.000028],
        "AstDecRate(deg/sec)" : [0.000035, 0.000028]
    })

    obsdf = pd.DataFrame({
        "fiveSigmaDepth" : [22.0, 22.0],
        "onservationId"  : [0, 1],
        "seeingFwhmEff"  : [1.0, 1.0]
    })

    nominal_result = pd.DataFrame({
        "Filtermag"           : [20.139229, 20.820432],
        "FieldID"             : [0, 1],
        "AstRARate(deg/sec)"  : [0.000035, 0.000028],
        "AstDecRate(deg/sec)" : [0.000035, 0.000028]
    })

    filterFadingFunction(ephemsdf, obsdf)

    assert ephemsdf == nominal_result
