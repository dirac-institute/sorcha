import os
import pandas as pd
import numpy as np
from numpy.testing import assert_equal
import pytest
from sorcha.utilities.sorchaConfigs import linkingfilterConfigs
from sorcha.modules.PPStats import stats


def test_PPStats(tmp_path):
    # make some simple test data
    ObjID = (["object_one"] * 10) + (["object_two"] * 5)
    Linked = ([True] * 10) + ([False] * 5)
    optFilter = (["r"] * 6) + (["g"] * 4) + (["r"] * 5)
    trailedSourceMag = np.concatenate(
        (np.linspace(18, 21, 6), np.linspace(19, 22, 4), np.linspace(20, 23, 5))
    )
    phase_deg = np.concatenate((np.linspace(3, 10, 6), np.linspace(4, 11, 4), np.linspace(5, 10, 5)))
    obj_date = np.array(([666.0] * 10) + ([np.nan] * 5), dtype=object)

    test_dict = {
        "ObjID": ObjID,
        "object_linked": Linked,
        "optFilter": optFilter,
        "trailedSourceMag": trailedSourceMag,
        "phase_deg": phase_deg,
        "date_linked_MJD": obj_date,
    }
    test_df = pd.DataFrame(test_dict)

    configs = linkingfilterConfigs()
    configs.ssp_linking_on = True
    configs.drop_unlinked = False
    setattr(configs, "linkingfilter", configs)
    filename_stats = "test_stats"
    stats(test_df, filename_stats, tmp_path, configs)

    stats_df = pd.read_csv(os.path.join(tmp_path, filename_stats + ".csv"))

    # For comparison purposes, change NaNs to Nones
    stats_df.replace({np.nan: None}, inplace=True)

    # check that the dataframe is just three rows long
    assert len(stats_df) == 3

    # check for correct column names
    expected_columns = np.array(
        [
            "ObjID",
            "optFilter",
            "number_obs",
            "min_apparent_mag",
            "max_apparent_mag",
            "median_apparent_mag",
            "min_phase",
            "max_phase",
            "object_linked",
            "date_linked_MJD",
        ],
        dtype=object,
    )

    assert_equal(expected_columns, stats_df.columns.values)

    # check correct population
    expected_row_one = np.array(
        ["object_one", "g", 4, 19.0, 22.0, 20.5, 4.0, 11.0, True, 666.0], dtype=object
    )
    expected_row_two = np.array(
        ["object_one", "r", 6, 18.0, 21.0, 19.5, 3.0, 10.0, True, 666.0], dtype=object
    )
    expected_row_three = np.array(
        ["object_two", "r", 5, 20.0, 23.0, 21.5, 5.0, 10.0, False, None], dtype=object
    )

    assert_equal(expected_row_one, stats_df.iloc[0].values)
    assert_equal(expected_row_two, stats_df.iloc[1].values)
    assert_equal(expected_row_three, stats_df.iloc[2].values)


def test_PPStats_nolinking(tmp_path):
    ObjID = (["object_one"] * 10) + (["object_two"] * 5)
    optFilter = (["r"] * 6) + (["g"] * 4) + (["r"] * 5)
    trailedSourceMag = np.concatenate(
        (np.linspace(18, 21, 6), np.linspace(19, 22, 4), np.linspace(20, 23, 5))
    )
    phase_deg = np.concatenate((np.linspace(3, 10, 6), np.linspace(4, 11, 4), np.linspace(5, 10, 5)))

    test_dict = {
        "ObjID": ObjID,
        "optFilter": optFilter,
        "trailedSourceMag": trailedSourceMag,
        "phase_deg": phase_deg,
    }

    test_df = pd.DataFrame(test_dict)

    configs = {"SSP_linking_on": False, "drop_unlinked": True}
    configs = linkingfilterConfigs()
    setattr(configs, "linkingfilter", configs)

    filename_stats = "test_stats"
    stats(test_df, filename_stats, tmp_path, configs)

    stats_df = pd.read_csv(os.path.join(tmp_path, filename_stats + ".csv"))

    assert len(stats_df) == 3

    expected_columns = np.array(
        [
            "ObjID",
            "optFilter",
            "number_obs",
            "min_apparent_mag",
            "max_apparent_mag",
            "median_apparent_mag",
            "min_phase",
            "max_phase",
        ],
        dtype="object",
    )

    assert_equal(expected_columns, stats_df.columns.values)

    expected_row_one = np.array(["object_one", "g", 4, 19.0, 22.0, 20.5, 4.0, 11.0], dtype=object)

    # the previous test checks all rows so it's fine to just check one here, this test is mostly to make
    # sure that the stats file works correctly if linking is off
    assert_equal(expected_row_one, stats_df.iloc[0].values)


def test_PPStats_justlinking(tmp_path):
    # tests behaviour when linking is on but drop_unlinked=True

    ObjID = (["object_one"] * 10) + (["object_two"] * 5)
    optFilter = (["r"] * 6) + (["g"] * 4) + (["r"] * 5)
    trailedSourceMag = np.concatenate(
        (np.linspace(18, 21, 6), np.linspace(19, 22, 4), np.linspace(20, 23, 5))
    )
    phase_deg = np.concatenate((np.linspace(3, 10, 6), np.linspace(4, 11, 4), np.linspace(5, 10, 5)))
    obj_date = np.array(([666.0] * 10) + ([np.nan] * 5), dtype=object)

    test_dict = {
        "ObjID": ObjID,
        "optFilter": optFilter,
        "trailedSourceMag": trailedSourceMag,
        "phase_deg": phase_deg,
        "date_linked_MJD": obj_date,
    }
    test_df = pd.DataFrame(test_dict)

    configs = linkingfilterConfigs()
    configs.ssp_linking_on = True
    configs.drop_unlinked = True
    setattr(configs, "linkingfilter", configs)

    filename_stats = "test_stats"
    stats(test_df, filename_stats, tmp_path, configs)

    stats_df = pd.read_csv(os.path.join(tmp_path, filename_stats + ".csv"))

    assert len(stats_df) == 3

    expected_columns = np.array(
        [
            "ObjID",
            "optFilter",
            "number_obs",
            "min_apparent_mag",
            "max_apparent_mag",
            "median_apparent_mag",
            "min_phase",
            "max_phase",
            "date_linked_MJD",
        ],
        dtype=object,
    )

    assert_equal(expected_columns, stats_df.columns.values)

    expected_row_one = np.array(["object_one", "g", 4, 19.0, 22.0, 20.5, 4.0, 11.0, 666.0], dtype=object)

    assert_equal(expected_row_one, stats_df.iloc[0].values)
