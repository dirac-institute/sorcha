import pandas as pd
import numpy as np
from numpy.testing import assert_equal


def test_PPDetectionEfficiency():
    from sorcha.modules.PPDetectionEfficiency import PPDetectionEfficiency

    rng = np.random.default_rng(2021)

    observations = pd.DataFrame({"ObjID": np.arange(0, 100)})

    expected_50 = [
        3,
        5,
        6,
        7,
        8,
        12,
        13,
        15,
        20,
        21,
        22,
        23,
        24,
        25,
        28,
        29,
        30,
        31,
        32,
        34,
        41,
        42,
        44,
        45,
        46,
        47,
        48,
        49,
        50,
        53,
        54,
        57,
        59,
        61,
        62,
        63,
        66,
        67,
        68,
        69,
        70,
        74,
        76,
        77,
        78,
        79,
        82,
        83,
        84,
        86,
        89,
        90,
        93,
        94,
        96,
        98,
    ]

    observations_out = PPDetectionEfficiency(observations, 0.50, rng)
    assert_equal(observations_out["ObjID"].values, expected_50)

    observations_zero = PPDetectionEfficiency(observations, 0.0, rng)
    assert_equal(len(observations_zero), 0)

    observations_all = PPDetectionEfficiency(observations, 1.0, rng)
    assert_equal(len(observations_all), 100)

    return
