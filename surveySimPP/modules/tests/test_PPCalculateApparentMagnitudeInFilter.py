import pandas as pd
from numpy.testing import assert_almost_equal


def test_PPCalculateApparentMagnitudeInFilter():

    from surveySimPP.modules.PPCalculateApparentMagnitudeInFilter import PPCalculateApparentMagnitudeInFilter

    test_observations = pd.DataFrame({'MJD': [2459215.5],
                                      'H': [7.3],
                                      'GS': [0.19],
                                      'G1': [0.62],
                                      'G2': [0.14],
                                      'G12': [0.68],
                                      'S': [0.04],
                                      'AstRange(km)': [4.899690e+08],
                                      'Ast-Sun(km)': [6.301740e+08],
                                      'Sun-Ast-Obs(deg)': [4.5918]})

    test_observations = PPCalculateApparentMagnitudeInFilter(test_observations.copy(), 'HG', 'HG_mag')
    test_observations = PPCalculateApparentMagnitudeInFilter(test_observations.copy(), 'HG12', 'HG12_mag')
    test_observations = PPCalculateApparentMagnitudeInFilter(test_observations.copy(), 'HG1G2', 'HG1G2_mag')
    test_observations = PPCalculateApparentMagnitudeInFilter(test_observations.copy(), 'linear', 'linear_mag')

    assert_almost_equal(test_observations['HG_mag'][0], 13.391578, decimal=5)
    assert_almost_equal(test_observations['HG12_mag'][0], 13.387267, decimal=5)
    assert_almost_equal(test_observations['HG1G2_mag'][0], 13.376821, decimal=5)
    assert_almost_equal(test_observations['linear_mag'][0], 13.182563, decimal=5)

    return
