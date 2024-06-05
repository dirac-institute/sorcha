import os
import pandas as pd
import numpy as np
from numpy.testing import assert_equal
import pytest


def test_PPStats(tmp_path):

    from sorcha.modules.PPStats import stats

    # make some simple test data
    ObjID = (["object_one"] * 10) + (["object_two"] * 5)
    Linked = ([True] * 10) + ([False] * 5)
    optFilter = (["r"] * 6) + (["g"] * 4) + (["r"] * 5)
    trailedSourceMag = np.concatenate((np.linspace(18, 21, 10), np.linspace(19, 22, 5)))
    phase_deg = np.concatenate((np.linspace(18, 21, 10), np.linspace(19, 22, 5)))

    test_dict = {
        "ObjID": ObjID,
        "Linked": Linked,
        "optFilter": optFilter,
        "trailedSourceMag": trailedSourceMag,
        "phase_deg": phase_deg,
    }
    test_df = pd.DataFrame(test_dict)

    filepath_stats = os.path.join(tmp_path, "test_stats.csv")
    stats(test_df, filepath_stats, ["r", "g"])

    stats_df = pd.read_csv(filepath_stats)

    # check that the dataframe is just two rows long
    assert len(stats_df) == 2

    # check for correct column names
    expected_columns = np.array(
        [
            "ObjID",
            "isLinked",
            "number_obs_r",
            "med_apparent_mag_r",
            "min_apparent_mag_r",
            "max_apparent_mag_r",
            "max_phase_r",
            "min_phase_r",
            "number_obs_g",
            "med_apparent_mag_g",
            "min_apparent_mag_g",
            "max_apparent_mag_g",
            "max_phase_g",
            "min_phase_g",
        ],
        dtype=object,
    )

    assert_equal(expected_columns, stats_df.columns.values)

    # check correct population
    expected_row_one = np.array(
        [
            "object_one",
            True,
            6,
            18.833333333333336,
            18.0,
            19.666666666666668,
            19.666666666666668,
            18.0,
            4,
            20.5,
            20.0,
            21.0,
            21.0,
            20.0,
        ],
        dtype=object,
    )
    expected_row_two = np.array(
        ["object_two", False, 5, 20.5, 19.0, 22.0, 22.0, 19.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0], dtype=object
    )

    assert_equal(expected_row_one, stats_df.iloc[0].values)
    assert_equal(expected_row_two, stats_df.iloc[1].values)
