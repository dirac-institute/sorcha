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
            "fieldMJD_TAI": [60229.28437, 60229.308262],
            "Range_LTC_km": [5710968952.677331, 5710979387.71679],
            "RangeRate_LTC_km_s": [5.027, 5.082],
            "RA_deg": [11.240711, 11.240231],
            "RARateCosDec_deg_day": [-0.020115, -0.020077],
            "Dec_deg": [-2.329568, -2.329769],
            "DecRate_deg_day": [-0.008383, -0.00838],
            "Obj_Sun_x_LTC_km": [5738514267.542, 5738511944.992],
            "Obj_Sun_y_LTC_km": [1155496538.993, 1155505324.219],
            "Obj_Sun_z_LTC_km": [-213429030.257, -213426267.84],
            "Obj_Sun_vx_LTC_km_s": [-1.125, -1.125],
            "Obj_Sun_vy_LTC_km_s": [4.256, 4.256],
            "Obj_Sun_vz_LTC_km_s": [1.338, 1.338],
            "Obs_Sun_x_km": [141728571.959, 141707497.927],
            "Obs_Sun_y_km": [43170140.218, 43223951.125],
            "Obs_Sun_z_km": [18707327.816, 18730458.18],
            "Obs_Sun_vx_km_s": [-10.186, -10.231],
            "Obs_Sun_vy_km_s": [26.095, 26.041],
            "Obs_Sun_vz_km_s": [11.206, 11.205],
            "phase_deg": [0.281093, 0.281579],
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

    dbq = "SELECT observationId, observationStartMJD as observationStartMJD_TAI, visitTime, visitExposureTime, filter, seeingFwhmGeom as seeingFwhmGeom_arcsec, seeingFwhmEff as seeingFwhmEff_arcsec, fiveSigmaDepth as fieldFiveSigmaDepth_mag , fieldRA as fieldRA_deg, fieldDec as fieldDec_deg, rotSkyPos as fieldRotSkyPos_deg FROM observations order by observationId"

    pointing_db = PPReadPointingDatabase(
        get_test_filepath("baseline_10klines_2.0.db"), ["g", "r", "i"], dbq, "rubin_sim"
    )

    # simulate adding extra columns to the pointing db for the precomputed values
    # needed for ephemeris generation. This ensures that the extra columns are not
    # included in the merge in PPMatchPointingToObservations.
    r_sun = np.empty((len(pointing_db), 3))
    pointing_db["r_sun_x"] = r_sun[:, 0]
    pointing_db["r_sun_y"] = r_sun[:, 1]
    pointing_db["r_sun_z"] = r_sun[:, 2]

    final_join = PPMatchPointingToObservations(joined_df_2, pointing_db)

    expected_df = pd.DataFrame(
        {
            "ObjID": ["356450", "356450"],
            "FieldID": [9212, 9262],
            "fieldMJD_TAI": [60229.28437, 60229.308262],
            "Range_LTC_km": [5710968952.677331, 5710979387.71679],
            "RangeRate_LTC_km_s": [5.027, 5.082],
            "RA_deg": [11.240711, 11.240231],
            "RARateCosDec_deg_day": [-0.020115, -0.020077],
            "Dec_deg": [-2.329568, -2.329769],
            "DecRate_deg_day": [-0.008383, -0.00838],
            "Obj_Sun_x_LTC_km": [5738514267.542, 5738511944.992],
            "Obj_Sun_y_LTC_km": [1155496538.993, 1155505324.219],
            "Obj_Sun_z_LTC_km": [-213429030.257, -213426267.84],
            "Obj_Sun_vx_LTC_km_s": [-1.125, -1.125],
            "Obj_Sun_vy_LTC_km_s": [4.256, 4.256],
            "Obj_Sun_vz_LTC_km_s": [1.338, 1.338],
            "Obs_Sun_x_km": [141728571.959, 141707497.927],
            "Obs_Sun_y_km": [43170140.218, 43223951.125],
            "Obs_Sun_z_km": [18707327.816, 18730458.18],
            "Obs_Sun_vx_km_s": [-10.186, -10.231],
            "Obs_Sun_vy_km_s": [26.095, 26.041],
            "Obs_Sun_vz_km_s": [11.206, 11.205],
            "phase_deg": [0.281093, 0.281579],
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
            "visitExposureTime": [30.0, 30.0],
            "optFilter": ["r", "i"],
            "seeingFwhmGeom_arcsec": [0.9072793403337696, 0.9738200113477326],
            "seeingFwhmEff_arcsec": [1.0404858154912038, 1.1214355369193827],
            "fieldFiveSigmaDepth_mag": [23.85277692149377, 23.216004807761653],
            "fieldRA_deg": [10.286608210708128, 10.286608210708128],
            "fieldDec_deg": [-2.177840811640851, -2.177840811640851],
            "fieldRotSkyPos_deg": [298.5944886818567, 302.40143247632597],
        }
    )
    expected_df["optFilter"] = expected_df["optFilter"].astype("category")

    assert_frame_equal(expected_df, final_join, check_categorical=False)

    return
