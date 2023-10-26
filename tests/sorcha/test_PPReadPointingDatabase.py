import numpy as np
from numpy.testing import assert_equal, assert_almost_equal
import pytest

from sorcha.utilities.dataUtilitiesForTests import get_test_filepath, get_demo_filepath


def test_PPReadPointingDatabase():
    from sorcha.modules.PPReadPointingDatabase import PPReadPointingDatabase

    sql_query = "SELECT observationId, observationStartMJD as observationStartMJD_TAI, visitTime, filter, seeingFwhmGeom, seeingFwhmEff, fiveSigmaDepth, fieldRA, fieldDec, rotSkyPos FROM observations order by observationId"
    filter_list = ["u", "g", "r", "i", "z", "y"]

    pointing_db = PPReadPointingDatabase(
        get_test_filepath("baseline_10klines_2.0.db"), filter_list, sql_query, "lsst"
    )

    expected_first_line = np.array(
        [
            0,
            60218.001805555556,
            34.0,
            "y",
            0.6673703914220546,
            0.7486257803188012,
            22.370556803880852,
            310.02448010095446,
            -60.81292801655155,
            62.75077469249649,
            0,
            60218.00200231482,
        ],
        dtype=object,
    )

    expected_columns = np.array(
        [
            "FieldID",
            "observationStartMJD_TAI",
            "visitTime",
            "optFilter",
            "seeingFwhmGeom",
            "seeingFwhmEff",
            "fiveSigmaDepth",
            "fieldRA",
            "fieldDec",
            "rotSkyPos",
            "observationId_",
            "observationMidpointMJD_TAI",
        ],
        dtype=object,
    )

    assert_equal(pointing_db.iloc[0].values, expected_first_line)
    assert_equal(pointing_db.columns.values, expected_columns)

    assert len(pointing_db) == 10000

    bad_query = "SELECT observationId, observationStartMJD as observationStartMJD_TAI, visitTime, filter, seeingFwhmGeom, seeingFwhmEff, fiveSigmaDepth, fieldRA, fieldDec, rotSkyPos FROM SummaryAllProps order by observationId"

    with pytest.raises(SystemExit) as e:
        pointing_db = PPReadPointingDatabase(
            get_test_filepath("baseline_10klines_2.0.db"), filter_list, bad_query, "lsst"
        )

    assert e.type == SystemExit
    assert (
        e.value.code
        == "ERROR: PPReadPointingDatabase: SQL query on pointing database failed. Check that the query is correct in the config file."
    )

    with pytest.raises(SystemExit) as e:
        pointing_db = PPReadPointingDatabase(
            get_test_filepath("baseline_10klines_2.0.db"), filter_list, sql_query, "totally_fake_survey"
        )

    assert e.type == SystemExit
    assert e.value.code == "ERROR: PPReadPointingDatabase: survey name not recognised."

    return
