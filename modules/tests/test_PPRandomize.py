import pytest
import numpy as np
import pandas as pd 

from ..PPRandomize import randomizeAstrometry, randomizePhotometry

def test_randomizeAstrometry():
    # Test randomizeAstrometry function

    np.random.seed(4077)

    ephemsdf = pd.DataFrame({
        "AstRA(mas)"       : [162000000.0],
        "AstDec(mas)"       : [54000000.0],
        "AstRASigma(mas)"  : [10 ** 5],
        "AstDecSigma(mas)" : [10 ** 5]
    })

    randomizeAstrometry(ephemsdf, raSigName="AstRASigma(mas)", decSigName="AstDecSigma(mas)")

    result_nominal = pd.DataFrame({
        "AstRA(mas)"          : [162000000.0],
        "AstDec(mas)"          : [54000000.0],
        "AstRASigma(mas)"     : [10 ** 5],
        "AstDecSigma(mas)"    : [10 ** 5],
        "randAstRASigma(mas)" : [45.007163],
        "randDecSigma(mas)"   : [15.017063]
    })

    assert ephemsdf == result_nominal

    return

def test_randomizePhotometry():
    # Test rendomizePhotometry function

    np.random.seed(4077)

    ephemsdf = pd.DataFrame({
        "Filtermag"             : [20.0],
        "PhotometricSigma(mag)" : [0.1]
    })

    randomizePhotometry(ephemsdf, photSigName="PhotometricSigma(mag)")

    nominal_result = pd.DataFrame({
        "Filtermag"             : [20.0],
        "PhotometricSigma(mag)" : [0.1],
        "randFilterMag"         : [20.025785]
    })

    assert ephemsdf == nominal_result
