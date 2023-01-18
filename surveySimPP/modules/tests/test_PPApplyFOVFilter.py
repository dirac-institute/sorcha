import pandas as pd
import numpy as np
from numpy.testing import assert_equal, assert_almost_equal
from surveySimPP.tests.data import get_test_filepath


def test_PPSimpleSensorArea():

    from surveySimPP.modules.PPApplyFOVFilter import PPSimpleSensorArea

    test_data = pd.read_csv(get_test_filepath('test_input_fullobs.csv'))

    rng = np.random.default_rng(2021)

    test_out = PPSimpleSensorArea(test_data[0:15], rng, fillfactor=0.9)

    expected = [894816, 897478, 897521, 901987, 902035, 907363, 907416, 907470,
                909426, 910872, 915246]

    assert_equal(expected, test_out['FieldID'].values)

    return


def test_PPCircleFootprint():

    from surveySimPP.modules.PPApplyFOVFilter import PPCircleFootprint

    test_data = pd.read_csv(get_test_filepath('test_input_fullobs.csv'))

    test_out = PPCircleFootprint(test_data[:10].copy(), 1.1)

    expected = [897478, 897521, 901987, 902035, 907363, 907416, 907470]

    assert_equal(expected, test_out['FieldID'].values)

    return


def test_PPGetSeparation():

    from surveySimPP.modules.PPApplyFOVFilter import PPGetSeparation

    sep1 = PPGetSeparation(164.03, -17.58, 163.87, -18.84)
    sep2 = PPGetSeparation(1, 1, 1, 1)

    assert_almost_equal(sep1, 1.269133, decimal=5)
    assert sep2 == 0

    return


def test_PPApplyFOVFilters():

    from surveySimPP.modules.PPApplyFOVFilter import PPApplyFOVFilter

    observations = pd.read_csv(get_test_filepath('test_input_fullobs.csv'), nrows=20)

    rng = np.random.default_rng(2021)

    configs = {'cameraModel': 'circle',
               'fadingFunctionOn': True,
               'circleRadius': 1.1}

    new_obs = PPApplyFOVFilter(observations, configs, rng)
    expected = [897478, 897521, 901987, 902035, 907363, 907416, 907470, 910850,
                910872]

    assert_equal(new_obs['FieldID'].values, expected)

    configs = {'cameraModel': 'circle',
               'fadingFunctionOn': False,
               'fillfactor': 0.5}

    new_obs = PPApplyFOVFilter(observations, configs, rng)
    expected = [897521, 902035, 907363, 907416, 907470, 910872, 915246, 922013]

    assert_equal(new_obs['FieldID'].values, expected)

    configs = {'cameraModel': 'footprint',
               'footprintPath': './data/detectors_corners.csv',
               'fillfactor': 1}

    new_obs = PPApplyFOVFilter(observations, configs, rng)
    expected = [894816, 894838, 897478, 897521, 901987, 902035, 907363, 907416,
                907470, 909426, 909452, 910850, 910872, 915246, 915268, 922013,
                922034, 922035, 926281, 926288]

    assert_equal(new_obs['FieldID'].values, expected)

    return
