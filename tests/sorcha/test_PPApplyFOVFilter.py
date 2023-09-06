import pandas as pd
import numpy as np
from numpy.testing import assert_equal, assert_almost_equal

from sorcha.modules.PPModuleRNG import PerModuleRNG
from sorcha.utilities.dataUtilitiesForTests import get_test_filepath


def test_PPSimpleSensorArea():
    from sorcha.modules.PPApplyFOVFilter import PPSimpleSensorArea

    test_data = pd.read_csv(get_test_filepath("test_input_fullobs.csv"), nrows=15)

    test_out = PPSimpleSensorArea(test_data, PerModuleRNG(2022), fillfactor=0.9)

    expected = [
        894816,
        894838,
        897478,
        901987,
        902035,
        907363,
        907416,
        907470,
        909426,
        909452,
        910850,
        910872,
    ]

    assert_equal(expected, test_out["FieldID"].values)


def test_PPCircleFootprint():
    from sorcha.modules.PPApplyFOVFilter import PPCircleFootprint

    test_data = pd.read_csv(get_test_filepath("test_input_fullobs.csv"), nrows=10)

    test_out = PPCircleFootprint(test_data, 1.1)

    expected = [897478, 897521, 901987, 902035, 907363, 907416, 907470]

    assert_equal(expected, test_out["FieldID"].values)

    return


def test_PPGetSeparation():
    from sorcha.modules.PPApplyFOVFilter import PPGetSeparation

    sep1 = PPGetSeparation(164.03, -17.58, 163.87, -18.84)
    sep2 = PPGetSeparation(1, 1, 1, 1)

    assert_almost_equal(sep1, 1.269133, decimal=5)
    assert sep2 == 0

    return


def test_PPApplyFOVFilters():
    from sorcha.modules.PPApplyFOVFilter import PPApplyFOVFilter
    from sorcha.modules.PPFootprintFilter import Footprint

    observations = pd.read_csv(get_test_filepath("test_input_fullobs.csv"), nrows=20)

    rng = PerModuleRNG(2021)

    configs = {
        "camera_model": "circle",
        "circle_radius": 1.1,
        "fill_factor": None,
        "footprint_edge_threshold": None,
    }

    new_obs = PPApplyFOVFilter(observations, configs, rng)
    expected = [897478, 897521, 901987, 902035, 907363, 907416, 907470, 910850, 910872]

    assert_equal(new_obs["FieldID"].values, expected)

    configs = {
        "camera_model": "circle",
        "fill_factor": 0.5,
        "circle_radius": None,
        "footprint_edge_threshold": None,
    }

    new_obs = PPApplyFOVFilter(observations, configs, rng)
    expected = [894816, 894838, 897478, 897521, 901987, 907416, 907470, 910850, 922034, 922035, 926281]

    assert_equal(new_obs["FieldID"].values, expected)

    configs = {
        "camera_model": "footprint",
        "footprint_path": get_test_filepath("detectors_corners.csv"),
        "footprint_edge_threshold": 0.0,
    }
    footprint = Footprint(configs["footprint_path"])
    new_obs = PPApplyFOVFilter(observations, configs, rng, footprint=footprint)
    expected = [
        894816,
        894838,
        897478,
        897521,
        901987,
        902035,
        907363,
        907416,
        907470,
        909426,
        909452,
        910850,
        910872,
        915246,
        915268,
        922013,
        922034,
        922035,
        926281,
        926288,
    ]

    assert_equal(new_obs["FieldID"].values, expected)

    return
