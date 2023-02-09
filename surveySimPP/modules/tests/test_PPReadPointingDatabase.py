import numpy as np
from numpy.testing import assert_equal
import pytest

from surveySimPP.tests.data import get_test_filepath


def test_PPReadPointingDatabase():

    from surveySimPP.modules.PPReadPointingDatabase import PPReadPointingDatabase

    sql_query = 'SELECT observationId, observationStartMJD, filter, seeingFwhmGeom, seeingFwhmEff, fiveSigmaDepth, fieldRA, fieldDec, rotSkyPos FROM SummaryAllProps order by observationId'
    filter_list = ['u', 'g', 'r', 'i', 'z', 'y']

    pointing_db = PPReadPointingDatabase(get_test_filepath('baseline_10yrs_10klines.db'), filter_list, sql_query)

    expected_first_line = np.array([1, 59853.01679398148, 'z', 0.620848174727237, 0.6920294096438405,
                                    23.34806600026304, 305.088793, -24.889283, 180.0, 1], dtype=object)

    expected_columns = np.array(['FieldID', 'observationStartMJD', 'optFilter', 'seeingFwhmGeom',
                                 'seeingFwhmEff', 'fiveSigmaDepth', 'fieldRA', 'fieldDec',
                                 'rotSkyPos', 'observationId_'], dtype=object)

    assert_equal(pointing_db.iloc[0].values, expected_first_line)
    assert_equal(pointing_db.columns.values, expected_columns)

    assert len(pointing_db) == 10007

    bad_query = 'SELECT observationId, observationStartMJD, filter, seeingFwhmGeom, seeingFwhmEff, fiveSigmaDepth, fieldRA, fieldDec, rotSkyPos FROM observations order by observationId'

    with pytest.raises(SystemExit) as e:
        pointing_db = PPReadPointingDatabase(get_test_filepath('baseline_10yrs_10klines.db'), filter_list, bad_query)

    assert e.type == SystemExit
    assert e.value.code == 'ERROR: PPReadPointingDatabase: SQL query on pointing database failed. Check that the query is correct in the config file.'

    return
