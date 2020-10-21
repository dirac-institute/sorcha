import pytest
import numpy as np
import pandas as pd 

from ..PPRandomize import randomizeAstrometry, randomizePhotometry

def test_randomizeAstrometry():
    # Test randomizeAstrometry function

    np.random.seed(4077)

    ephemsdf = pd.DataFrame({
        "AstRA(deg)"       : [45.0],
        "AstDec(deg)"       : [15.0],
        "AstRASigma(mas)"  : [10 ** 5],
        "AstDecSigma(mas)" : [10 ** 5]
    })

    result = randomizeAstrometry(ephemsdf)

    result_nominal = pd.DataFrame({
        "AstRA(deg)"          : [45.0],
        "AstDec(deg"          : [15.0],
        "AstRASigma(mas)"     : [10 ** 5],
        "AstDecSigma(mas)"    : [10 ** 5],
        "randAstRASigma(mas)" : [45.007163],
        "randDecSigma(mas)"   : [15.017063]
    })

    assert result == result_nominal

    return

def test_randomizePhotometry():
    # Test rendomizePhotometry function

    np.random.seed(4077)

    ephemsdf = pd.DataFrame({
        "Filtermag"             : [20.0],
        "PhotometricSigma(mag)" : [0.1]
    })

    result = randomizePhotometry(ephemsdf)

    nominal_result = pd.DataFrame({
        "Filtermag"             : [20.0],
        "PhotometricSigma(mag)" : [0.1],
        "randFilterMag"         : [20.025785]
    })

    assert result == nominal_result