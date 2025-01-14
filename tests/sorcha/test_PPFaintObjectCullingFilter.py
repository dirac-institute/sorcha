import pandas as pd
import numpy as np

from sorcha.utilities.dataUtilitiesForTests import get_test_filepath

from numpy.testing import assert_almost_equal


def test_PPFaintObjectCullingFilter():
    from sorcha.modules.PPFaintObjectCullingFilter import PPFaintObjectCullingFilter
    from sorcha.modules.PPReadPointingDatabase import PPReadPointingDatabase

    dbq = "SELECT observationId, observationStartMJD as observationStartMJD_TAI, visitTime, visitExposureTime, filter, seeingFwhmGeom as seeingFwhmGeom_arcsec, seeingFwhmEff as seeingFwhmEff_arcsec, fiveSigmaDepth as fieldFiveSigmaDepth_mag , fieldRA as fieldRA_deg, fieldDec as fieldDec_deg, rotSkyPos as fieldRotSkyPos_deg FROM observations order by observationId"
    filterpointing = PPReadPointingDatabase(
        get_test_filepath("baseline_10klines_2.0.db"), ["u", "g", "r", "i", "z", "y"], dbq, "rubin_sim"
    )

    # mock objects from centaur model (murtagh et al. 2025)

    # test that all objects pass
    aux_df = pd.DataFrame(
        {
            "ObjID": ["a", "b", "c", "d"],
            "FORMAT": ["KEP", "KEP", "KEP", "KEP"],
            "a": [29.153, 12.802, 17.169, 9.228],
            "e": [0.2416, 0.3938, 0.1854, 0.2093],
            "inc": [11.42, 28.88, 33.97, 12.96],
            "node": [256.068, 102.054, 151.078, 238.193],
            "argPeri": [83.499, 233.123, 210.293, 12.545],
            "ma": [291.382, 333.178, 343.568, 286.359],
            "epochMJD_TDB": [60676.0, 60676.0, 60676.0, 60676.0],
            "H_r": [8.5876, 17.6338, 10.4349, 17.8486],
            "u-r": [1.8600, 1.8600, 1.8600, 1.8600],
            "g-r": [0.5620, 0.5620, 0.5620, 0.5620],
            "i-r": [-0.2346, -0.2346, -0.2346, -0.2346],
            "z-r": [
                -0.3290,
                -0.3290,
                -0.3290,
                -0.3290,
            ],
            "y-r": [-0.4134, -0.4134, -0.4134, -0.4134],
        }
    )
    output_df = PPFaintObjectCullingFilter(
        aux_df, filterpointing, "r", ["u", "g", "r", "i", "z", "y"], None, None
    )
    assert len(output_df) == 4

    # test objects that should get dropped do get dropped
    aux_df = pd.DataFrame(
        {
            "ObjID": ["a", "b", "c", "d"],
            "FORMAT": ["KEP", "KEP", "KEP", "KEP"],
            "a": [29.153, 54.802, 67.169, 11.228],
            "e": [0.2416, 0.3938, 0.1854, 0.2093],
            "inc": [11.42, 28.88, 33.97, 12.96],
            "node": [256.068, 102.054, 151.078, 238.193],
            "argPeri": [83.499, 233.123, 210.293, 12.545],
            "ma": [291.382, 333.178, 343.568, 286.359],
            "epochMJD_TDB": [60676.0, 60676.0, 60676.0, 60676.0],
            "H_r": [8.5876, 19.6338, 10.4349, 16.8486],
            "u-r": [1.8600, 1.8600, 1.8600, 1.8600],
            "g-r": [0.5620, 0.5620, 0.5620, 0.5620],
            "i-r": [-0.2346, -0.2346, -0.2346, -0.2346],
            "z-r": [
                -0.3290,
                -0.3290,
                -0.3290,
                -0.3290,
            ],
            "y-r": [-0.4134, -0.4134, -0.4134, -0.4134],
        }
    )
    output_df = PPFaintObjectCullingFilter(
        aux_df, filterpointing, "r", ["u", "g", "r", "i", "z", "y"], None, None
    )
    assert len(output_df) == 2

    # test that no objects pass
    aux_df = pd.DataFrame(
        {
            "ObjID": ["a", "b", "c", "d"],
            "FORMAT": ["KEP", "KEP", "KEP", "KEP"],
            "a": [129.153, 114.802, 117.169, 111.228],
            "e": [0.2416, 0.3938, 0.1854, 0.2093],
            "inc": [11.42, 28.88, 33.97, 12.96],
            "node": [256.068, 102.054, 151.078, 238.193],
            "argPeri": [83.499, 233.123, 210.293, 12.545],
            "ma": [291.382, 333.178, 343.568, 286.359],
            "epochMJD_TDB": [60676.0, 60676.0, 60676.0, 60676.0],
            "H_r": [18.5876, 19.6338, 20.4349, 19.8486],
            "u-r": [1.8600, 1.8600, 1.8600, 1.8600],
            "g-r": [0.5620, 0.5620, 0.5620, 0.5620],
            "i-r": [-0.2346, -0.2346, -0.2346, -0.2346],
            "z-r": [
                -0.3290,
                -0.3290,
                -0.3290,
                -0.3290,
            ],
            "y-r": [-0.4134, -0.4134, -0.4134, -0.4134],
        }
    )
    output_df = PPFaintObjectCullingFilter(
        aux_df, filterpointing, "r", ["u", "g", "r", "i", "z", "y"], None, None
    )
    assert len(output_df) == 0

    return


def test_PPEstimatePerihelion():
    from sorcha.modules.PPFaintObjectCullingFilter import PPEstimatePerihelion

    # mock objects from centaur model (murtagh et al. 2025)

    aux_df = pd.DataFrame(
        {
            "ObjID": ["a", "b", "c", "d"],
            "FORMAT": ["KEP", "KEP", "KEP", "KEP"],
            "a": [29.153, 14.802, 17.169, 11.228],
            "e": [0.2416, 0.3938, 0.1854, 0.2093],
            "inc": [11.42, 28.88, 33.97, 12.96],
            "node": [256.068, 102.054, 151.078, 238.193],
            "argPeri": [83.499, 233.123, 210.293, 12.545],
            "ma": [291.382, 333.178, 343.568, 286.359],
            "epochMJD_TDB": [60676.0, 60676.0, 60676.0, 60676.0],
            "H_r": [8.5876, 19.6338, 10.4349, 19.8486],
            "u-r": [1.8600, 1.8600, 1.8600, 1.8600],
            "g-r": [0.5620, 0.5620, 0.5620, 0.5620],
            "i-r": [-0.2346, -0.2346, -0.2346, -0.2346],
            "z-r": [
                -0.3290,
                -0.3290,
                -0.3290,
                -0.3290,
            ],
            "y-r": [-0.4134, -0.4134, -0.4134, -0.4134],
        }
    )

    # from simple a*(1-e) calc for rough estimate
    q = np.array([22.110, 8.973, 13.986, 8.878])

    est_q = PPEstimatePerihelion(aux_df)

    assert_almost_equal(np.round(est_q, 3), q, decimal=5)

    return
