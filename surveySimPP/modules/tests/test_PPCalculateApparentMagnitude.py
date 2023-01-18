import pandas as pd
import numpy as np
from numpy.testing import assert_almost_equal, assert_equal
from surveySimPP.tests.data import get_test_filepath


def test_PPCalculateApparentMagnitudeInFilter():

    from surveySimPP.modules.PPCalculateApparentMagnitudeInFilter import PPCalculateApparentMagnitudeInFilter

    test_observations = pd.DataFrame({'MJD': [2459215.5],
                                      'H_r': [7.3],
                                      'GS': [0.19],
                                      'G1': [0.62],
                                      'G2': [0.14],
                                      'G12': [0.68],
                                      'S': [0.04],
                                      'AstRange(km)': [4.899690e+08],
                                      'Ast-Sun(km)': [6.301740e+08],
                                      'Sun-Ast-Obs(deg)': [4.5918]})

    test_observations = PPCalculateApparentMagnitudeInFilter(test_observations.copy(), 'HG', 'r', 'HG_mag')
    test_observations = PPCalculateApparentMagnitudeInFilter(test_observations.copy(), 'HG12', 'r', 'HG12_mag')
    test_observations = PPCalculateApparentMagnitudeInFilter(test_observations.copy(), 'HG1G2', 'r', 'HG1G2_mag')
    test_observations = PPCalculateApparentMagnitudeInFilter(test_observations.copy(), 'linear', 'r', 'linear_mag')

    assert_almost_equal(test_observations['HG_mag'][0], 13.391578, decimal=5)
    assert_almost_equal(test_observations['HG12_mag'][0], 13.387267, decimal=5)
    assert_almost_equal(test_observations['HG1G2_mag'][0], 13.376821, decimal=5)
    assert_almost_equal(test_observations['linear_mag'][0], 13.182563, decimal=5)

    return


def test_PPCalculateSimpleCometaryMagnitude():

    from surveySimPP.modules.PPCalculateSimpleCometaryMagnitude import PPCalculateSimpleCometaryMagnitude

    test_cometary_df = pd.read_csv(get_test_filepath('cometary_test_df.csv'), sep=' ')

    othercolours = ['u-r', 'g-r', 'i-r', 'z-r', 'y-r']

    df_comet = PPCalculateSimpleCometaryMagnitude(test_cometary_df.copy(), 'r', othercolours)

    expected = [15.77970706, 15.89970703, 15.77970697, 15.89970695, 15.89970149,
                15.89970147, 15.89970144, 16.31969998, 15.89969995, 15.77969533,
                15.8996953, 16.31969374, 15.89969371, 15.89969053, 15.7796905,
                16.31969043, 15.8996904, 16.31968699, 15.89968696, 15.89968691,
                15.77968688]

    assert_almost_equal(df_comet["TrailedSourceMag"], expected, decimal=5)

    return


def test_PPApplyColourOffsets():

    from surveySimPP.modules.PPApplyColourOffsets import PPApplyColourOffsets

    objects = np.array(['obj1', 'obj1', 'obj1', 'obj1', 'obj2', 'obj2', 'obj2', 'obj2'])

    optfilter = np.array(['r', 'g', 'i', 'z', 'r', 'g', 'z', 'i'])

    ur = np.array([0.1, 0.1, 0.1, 0.1, 0.2, 0.2, 0.2, 0.2])
    gr = np.array([0.3, 0.3, 0.3, 0.3, 0.4, 0.4, 0.4, 0.4])
    ir = np.array([0.5, 0.5, 0.5, 0.5, 0.6, 0.6, 0.6, 0.6])
    zr = np.array([0.7, 0.7, 0.7, 0.7, 0.8, 0.8, 0.8, 0.8])

    H = np.array([10.0, 10.0, 10.0, 10.0, 12.0, 12.0, 12.0, 12.0])
    G = np.array([0.15, 0.15, 0.15, 0.15, 0.12, 0.12, 0.12, 0.12])

    test_obs = pd.DataFrame({'ObjID': objects, 'optFilter': optfilter,
                             'u-r': ur, 'g-r': gr, 'i-r': ir, 'z-r': zr,
                             'H_r': H, 'GS': G})

    othercolours = ['u-r', 'g-r', 'i-r', 'z-r']
    observing_filters = ['r', 'u', 'g', 'i', 'z']

    func_test = PPApplyColourOffsets(test_obs.copy(), 'HG', othercolours, observing_filters, 'r')

    assert_equal(func_test['H_r'].values, [10., 10.3, 10.5, 10.7, 12., 12.4, 12.8, 12.6])

    Gr = np.array([0.151, 0.151, 0.151, 0.151, 0.121, 0.121, 0.121, 0.121])
    Gu = np.array([0.152, 0.152, 0.152, 0.152, 0.122, 0.122, 0.122, 0.122])
    Gi = np.array([0.153, 0.153, 0.153, 0.153, 0.123, 0.123, 0.123, 0.123])
    Gz = np.array([0.154, 0.154, 0.154, 0.154, 0.124, 0.124, 0.124, 0.124])
    Gg = np.array([0.155, 0.155, 0.155, 0.155, 0.125, 0.125, 0.125, 0.125])

    test_obs["GSr"] = Gr
    test_obs["GSu"] = Gu
    test_obs["GSi"] = Gi
    test_obs["GSz"] = Gz
    test_obs["GSg"] = Gg

    test_obs.drop(["GS"], axis=1, inplace=True)

    func_test_2 = PPApplyColourOffsets(test_obs.copy(), 'HG', othercolours, observing_filters, 'r')

    assert_equal(func_test_2['H_r'].values, [10., 10.3, 10.5, 10.7, 12., 12.4, 12.8, 12.6])
    assert_equal(func_test_2['GS'].values, [0.151, 0.155, 0.153, 0.154, 0.121, 0.125, 0.124, 0.123])

    return


def test_PPCalculateApparentMagnitude():

    from surveySimPP.modules.PPCalculateApparentMagnitude import PPCalculateApparentMagnitude

    othercolours = ['u-r', 'g-r', 'i-r', 'z-r', 'y-r']
    observing_filters = ['r', 'u', 'g', 'i', 'z']

    observations_comet = pd.read_csv(get_test_filepath('cometary_test_df.csv'), sep=' ', nrows=1)
    comet_out = PPCalculateApparentMagnitude(observations_comet.copy(), 'HG', 'r', othercolours, observing_filters, 'comet')

    assert_almost_equal(comet_out['TrailedSourceMag'][0], 15.779707, decimal=6)

    observations_mult = pd.read_csv(get_test_filepath('test_data_mag.csv'), nrows=1)
    mult_out = PPCalculateApparentMagnitude(observations_mult.copy(), 'HG', 'r', othercolours, observing_filters, 'none')

    assert_almost_equal(mult_out['TrailedSourceMag'][0], 22.994074, decimal=6)

    observations_single = pd.read_csv(get_test_filepath('test_data_single.csv'))
    single_out = PPCalculateApparentMagnitude(observations_single.copy(), 'HG', 'r', None, ['r'], 'none')

    assert_almost_equal(single_out['TrailedSourceMag'][0], 22.994074, decimal=6)

    return
