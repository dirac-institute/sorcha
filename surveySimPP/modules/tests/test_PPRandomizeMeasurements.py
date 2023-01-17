import pandas as pd
import numpy as np

from surveySimPP.tests.data import get_test_filepath


def test_randomizePhotometry():

    from surveySimPP.modules.PPRandomizeMeasurements import randomizePhotometry

    rng = np.random.default_rng(2021)

    test_data = pd.read_csv(get_test_filepath('test_input_fullobs.csv'))

    test_out = randomizePhotometry(test_data[0:1], rng, magName="TrailedSourceMag", sigName="PhotometricSigmaTrailedSource(mag)")

    np.testing.assert_almost_equal(test_out.values[0], 19.654880, decimal=5)

    return


def test_randomizeAstrometry():

    from surveySimPP.modules.PPRandomizeMeasurements import randomizeAstrometry

    rng = np.random.default_rng(2021)

    test_data = pd.read_csv(get_test_filepath('test_input_fullobs.csv'))

    test_out = randomizeAstrometry(test_data[0:1], rng, sigName='AstrometricSigma(deg)', sigUnits='deg')

    np.testing.assert_almost_equal(test_out[0][0], 164.03771597, decimal=5)
    np.testing.assert_almost_equal(test_out[1][0], -17.58257153, decimal=5)

    return
