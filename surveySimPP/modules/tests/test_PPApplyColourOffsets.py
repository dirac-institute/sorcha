import pandas as pd
import numpy as np
from numpy.testing import assert_equal


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
