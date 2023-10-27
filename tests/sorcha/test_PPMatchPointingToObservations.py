import pandas as pd
import numpy as np
from pandas.testing import assert_frame_equal

from sorcha.utilities.dataUtilitiesForTests import get_test_filepath


def test_PPMatchPointingToObservations():
    from sorcha.modules.PPMatchPointingToObservations import PPMatchPointingToObservations
    from sorcha.modules.PPJoinEphemeridesAndParameters import PPJoinEphemeridesAndParameters
    from sorcha.modules.PPJoinEphemeridesAndOrbits import PPJoinEphemeridesAndOrbits
    from sorcha.modules.PPReadPointingDatabase import PPReadPointingDatabase

    # note that the test orbit, parameters and oif files already in /tests/data/
    # are not compatible with the current version of the pointing database.
    # instead of replacing them and rewriting several tests, here we simply
    # recreate data that will join with the pointing database.

    test_oif = pd.DataFrame(
        {
            "ObjID": ["356450", "356450"],
            "FieldID": [9212, 9262],
            "FieldMJD_TAI": [60229.28437, 60229.308262],
            "AstRange(km)": [5710968952.677331, 5710979387.71679],
            "AstRangeRate(km/s)": [5.027, 5.082],
            "AstRA(deg)": [11.240711, 11.240231],
            "AstRARate(deg/day)": [-0.020115, -0.020077],
            "AstDec(deg)": [-2.329568, -2.329769],
            "AstDecRate(deg/day)": [-0.008383, -0.00838],
            "Ast-Sun(J2000x)(km)": [5738514267.542, 5738511944.992],
            "Ast-Sun(J2000y)(km)": [1155496538.993, 1155505324.219],
            "Ast-Sun(J2000z)(km)": [-213429030.257, -213426267.84],
            "Ast-Sun(J2000vx)(km/s)": [-1.125, -1.125],
            "Ast-Sun(J2000vy)(km/s)": [4.256, 4.256],
            "Ast-Sun(J2000vz)(km/s)": [1.338, 1.338],
            "Obs-Sun(J2000x)(km)": [141728571.959, 141707497.927],
            "Obs-Sun(J2000y)(km)": [43170140.218, 43223951.125],
            "Obs-Sun(J2000z)(km)": [18707327.816, 18730458.18],
            "Obs-Sun(J2000vx)(km/s)": [-10.186, -10.231],
            "Obs-Sun(J2000vy)(km/s)": [26.095, 26.041],
            "Obs-Sun(J2000vz)(km/s)": [11.206, 11.205],
            "Sun-Ast-Obs(deg)": [0.281093, 0.281579],
        }
    )

    test_orb = pd.DataFrame(
        {
            "ObjID": ["356450"],
            "t_0": [54466.0],
            "t_p_MJD_TDB": [90480.35745],
            "argperi": [7.89],
            "node": [144.25849],
            "incl": [8.98718],
            "e": [0.09654],
            "q": [33.01305],
        }
    )

    test_params = pd.DataFrame(
        {
            "ObjID": ["356450"],
            "H_r": [7.99],
            "u-r": [2.55],
            "g-r": [0.92],
            "i-r": [-0.38],
            "z-r": [-0.59],
            "y-r": [-0.7],
            "GS": [0.15],
        }
    )

    joined_df = PPJoinEphemeridesAndParameters(test_oif, test_params)
    joined_df_2 = PPJoinEphemeridesAndOrbits(joined_df, test_orb)

    dbq = "SELECT observationId, observationStartMJD as observationStartMJD_TAI, visitTime, filter, seeingFwhmGeom, seeingFwhmEff, fiveSigmaDepth, fieldRA, fieldDec, rotSkyPos FROM observations order by observationId"

    # note that surveyname here is "test". this is because this test pointing dataframe doesn't have the visitTime column
    # and thus cannot calculate 'observationMidpointMJD_TAI'. we don't need it here, so that's okay.
    pointing_db = PPReadPointingDatabase(
        get_test_filepath("baseline_10klines_2.0.db"), ["g", "r", "i"], dbq, "lsst"
    )

    # simulate adding extra columns to the pointing db for the precomputed values
    # needed for ephemeris generation. This ensures that the extra columns are not
    # included in the merge in PPMatchPointingToObservations.
    r_sun = np.empty((len(pointing_db), 3))
    pointing_db["r_sun"] = r_sun.tolist()

    final_join = PPMatchPointingToObservations(joined_df_2, pointing_db)

    expected_df = pd.DataFrame(
        {
            "ObjID": ["356450", "356450"],
            "FieldID": [9212, 9262],
            "FieldMJD_TAI": [60229.28437, 60229.308262],
            "AstRange(km)": [5710968952.677331, 5710979387.71679],
            "AstRangeRate(km/s)": [5.027, 5.082],
            "AstRA(deg)": [11.240711, 11.240231],
            "AstRARate(deg/day)": [-0.020115, -0.020077],
            "AstDec(deg)": [-2.329568, -2.329769],
            "AstDecRate(deg/day)": [-0.008383, -0.00838],
            "Ast-Sun(J2000x)(km)": [5738514267.542, 5738511944.992],
            "Ast-Sun(J2000y)(km)": [1155496538.993, 1155505324.219],
            "Ast-Sun(J2000z)(km)": [-213429030.257, -213426267.84],
            "Ast-Sun(J2000vx)(km/s)": [-1.125, -1.125],
            "Ast-Sun(J2000vy)(km/s)": [4.256, 4.256],
            "Ast-Sun(J2000vz)(km/s)": [1.338, 1.338],
            "Obs-Sun(J2000x)(km)": [141728571.959, 141707497.927],
            "Obs-Sun(J2000y)(km)": [43170140.218, 43223951.125],
            "Obs-Sun(J2000z)(km)": [18707327.816, 18730458.18],
            "Obs-Sun(J2000vx)(km/s)": [-10.186, -10.231],
            "Obs-Sun(J2000vy)(km/s)": [26.095, 26.041],
            "Obs-Sun(J2000vz)(km/s)": [11.206, 11.205],
            "Sun-Ast-Obs(deg)": [0.281093, 0.281579],
            "H_r": [7.99, 7.99],
            "u-r": [2.55, 2.55],
            "g-r": [0.92, 0.92],
            "i-r": [-0.38, -0.38],
            "z-r": [-0.59, -0.59],
            "y-r": [-0.7, -0.7],
            "GS": [0.15, 0.15],
            "t_0": [54466.0, 54466.0],
            "t_p_MJD_TDB": [90480.35745, 90480.35745],
            "argperi": [7.89, 7.89],
            "node": [144.25849, 144.25849],
            "incl": [8.98718, 8.98718],
            "e": [0.09654, 0.09654],
            "q": [33.01305, 33.01305],
            "visitTime": [34.0, 34.0],
            "optFilter": ["r", "i"],
            "seeingFwhmGeom": [0.9072793403337696, 0.9738200113477326],
            "seeingFwhmEff": [1.0404858154912038, 1.1214355369193827],
            "fiveSigmaDepth": [23.85277692149377, 23.216004807761653],
            "fieldRA": [10.286608210708128, 10.286608210708128],
            "fieldDec": [-2.177840811640851, -2.177840811640851],
            "rotSkyPos": [298.5944886818567, 302.40143247632597],
            "observationMidpointMJD_TAI": [60229.284567, 60229.308459],
        }
    )

    assert_frame_equal(expected_df, final_join)

    return
