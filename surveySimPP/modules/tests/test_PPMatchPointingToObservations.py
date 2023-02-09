import numpy as np
from numpy.testing import assert_equal

from surveySimPP.tests.data import get_test_filepath


def test_PPMatchPointingToObservations():

    from surveySimPP.modules.PPMatchPointingToObservations import PPMatchPointingToObservations
    from surveySimPP.modules.PPJoinEphemeridesAndParameters import PPJoinEphemeridesAndParameters
    from surveySimPP.modules.PPJoinEphemeridesAndOrbits import PPJoinEphemeridesAndOrbits
    from surveySimPP.modules.PPReadOif import PPReadOif
    from surveySimPP.modules.PPReadOrbitFile import PPReadOrbitFile
    from surveySimPP.modules.PPReadPhysicalParameters import PPReadPhysicalParameters
    from surveySimPP.modules.PPReadPointingDatabase import PPReadPointingDatabase

    oif_file = PPReadOif(get_test_filepath('oiftestoutput.txt'), 'whitespace')
    orbit_file = PPReadOrbitFile(get_test_filepath('testorb.des'), 0, 5, 'whitespace')
    params_file = PPReadPhysicalParameters(get_test_filepath('testcolour.txt'), 0, 5, 'whitespace')

    joined_df = PPJoinEphemeridesAndParameters(oif_file, params_file)
    joined_df_2 = PPJoinEphemeridesAndOrbits(joined_df, orbit_file)

    dbq = 'SELECT observationId, observationStartMJD, filter, seeingFwhmGeom, seeingFwhmEff, fiveSigmaDepth, fieldRA, fieldDec, rotSkyPos FROM SummaryAllProps order by observationId'

    pointing_db = PPReadPointingDatabase(get_test_filepath('baseline_10yrs_10klines.db'), ['g', 'r', 'i'], dbq)

    final_join = PPMatchPointingToObservations(joined_df_2, pointing_db)

    first_row = np.array(['S00002b', 572, 59853.293877, 160327206.556, -19.492, 47.088061,
                          0.053874, -15.880194, -0.417293, 253410404.834, 131561171.922,
                          -35804271.497, -21.325, 11.966, 4.031, 148413942.971, 18618735.009,
                          8065543.09, -4.814, 27.264, 11.697, 21.12101, 18.155, 0.3, 0.0,
                          0.1, 0.15, 1.086765486292, 0.624200488727, 21.686676144508,
                          157.115012852228, 325.25491242303, 54590.14887269, 54466.0, 'g',
                          0.9368643954246213, 1.0764773666966196, 24.526447854044683,
                          47.438515, -15.756291, 179.4914282799895], dtype='object')

    assert_equal(final_join.iloc[0].values, first_row)
    assert len(final_join.columns) == 41
    assert len(final_join) == 5

    return
