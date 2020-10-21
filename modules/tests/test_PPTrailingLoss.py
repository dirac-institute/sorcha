import pytest
import numpy as np
import pandas as pd 

from ..PPTrailingLoss import calcTrailingLoss

def test_calcTrailingLoss():
    #Test calcTrailingLoss function

    dRa = 5.0
    dDec = 7.0
    seeing = 1.0
    nominal_result = 17.372787897241796

    result = calcTrailingLoss(dRa, dDec, seeing)

    assert result == nominal_result
