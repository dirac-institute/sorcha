import pandas as pd
import numpy as np
from numpy.testing import assert_equal

from sorcha.modules.PPModuleRNG import PerModuleRNG


def test_PPDetectionEfficiency():
    from sorcha.modules.PPDetectionEfficiency import PPDetectionEfficiency

    rng = PerModuleRNG(2021)

    observations = pd.DataFrame({"ObjID": np.arange(0, 100)})

    expected_50 = [
        0,
        2,
        7,
        8,
        9,
        11,
        14,
        17,
        19,
        20,
        21,
        22,
        23,
        24,
        25,
        26,
        27,
        28,
        29,
        31,
        32,
        33,
        34,
        37,
        39,
        42,
        44,
        45,
        48,
        50,
        51,
        53,
        55,
        56,
        61,
        62,
        63,
        66,
        68,
        70,
        71,
        72,
        74,
        75,
        77,
        79,
        81,
        82,
        83,
        85,
        87,
        90,
        98,
    ]

    observations_out = PPDetectionEfficiency(observations, 0.50, rng)
    assert_equal(observations_out["ObjID"].values, expected_50)

    observations_zero = PPDetectionEfficiency(observations, 0.0, rng)
    assert_equal(len(observations_zero), 0)

    observations_all = PPDetectionEfficiency(observations, 1.0, rng)
    assert_equal(len(observations_all), 100)

    return
