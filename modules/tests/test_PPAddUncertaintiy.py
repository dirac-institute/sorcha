import pytest
import numpy as np
import pandas as pd


from ..PPAddUncertainties import addUncertainties
from ..PPAddUncertainties import calcAstrometricUncertainty
from ..PPAddUncertainties import calcPhotometricUncertainty


def test_calcAstrometricUncertainty():
    # Test the function calcAstrometricUncertainty
    mag = 20
    m5 = 23.5
    result_nominal = (10.85937575072431, 99.19895320080636, 4.233915645760927)

    result = calcAstrometricUncertainty(mag, m5)
    
    assert result == result_nominal

    return

def test_calcPhotometricUncertainty():
    # Test the function calcPhotometricUncertainty
    snr = 7
    result_nominal = 0.14497986744421684

    result=calcPhotometricUncertainty(snr)
    
    assert result == result_nominal

    return

