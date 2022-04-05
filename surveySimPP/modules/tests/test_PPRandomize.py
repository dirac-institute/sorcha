import pytest
import numpy as np
import pandas as pd


def test_randomizeAstrometry():
    # Test randomizeAstrometry function

    from surveySimPP.modules.PPRandomize import randomizeAstrometry, randomizePhotometry

    np.random.seed(4077)

    ephemsdf = pd.DataFrame({
        "AstRA(mas)": [162000000.0, 162000000.0],
        "AstDec(mas)": [54000000.0, 54000000.0],
        "AstRASigma(mas)": [10 ** 5, 10 ** 5],
        "AstDecSigma(mas)": [10 ** 5, 10 ** 5]
    })

    epehemsdf = randomizeAstrometry(ephemsdf, raSigName="AstRASigma(mas)", decSigName="AstDecSigma(mas)", raName="AstRA(mas)", decName='AstDec(mas)')

    result_nominal = pd.DataFrame({
        "AstRA(mas)": [162000000.0, 162000000.0],
        "AstDec(mas)": [54000000.0, 54000000.0],
        "AstRASigma(mas)": [10 ** 5, 10 ** 5],
        "AstDecSigma(mas)": [10 ** 5, 10 ** 5],
        "randAstRA(deg)": [45.00716256402985, 45.00716256402985],
        "randAstDec(deg)": [15.017063, 15.017063]
    })

    assert ephemsdf["randAstRA(deg)"][0] == result_nominal["randAstRA(deg)"][0]

    return


def test_randomizePhotometry():
    # Test rendomizePhotometry function

    from surveySimPP.modules.PPRandomize import randomizeAstrometry, randomizePhotometry

    np.random.seed(4077)

    ephemsdf = pd.DataFrame({
        "Filtermag": [20.0, 20.0],
        "PhotometricSigma(mag)": [0.1, 0.1]
    })

    ephemsdf = randomizePhotometry(ephemsdf, photSigName="PhotometricSigma(mag)")

    nominal_result = pd.DataFrame({
        "Filtermag": [20.0, 20.0],
        "PhotometricSigma(mag)": [0.1, 0.1],
        "randFilterMag": [20.02578523050747, 20.02578523050747]
    })

    assert ephemsdf["randFilterMag"][0] == nominal_result["randFilterMag"][0]
