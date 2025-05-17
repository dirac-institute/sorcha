import numpy as np
import sorcha.ephemeris.simulation_parsing as sp
from sorcha.utilities.dataUtilitiesForTests import get_test_filepath
from sorcha.utilities.sorchaConfigs import auxiliaryConfigs
import sorcha.ephemeris.simulation_geometry as sg
import sorcha.ephemeris.simulation_setup as ss


def test_observatory_compared_to_original():
    auxconfigs = auxiliaryConfigs()
    observatory = sp.Observatory(
        auxconfigs=auxconfigs, args=None, oc_file=get_test_filepath("ObsCodes_test.json")
    )
    obs = observatory.ObservatoryXYZ

    # Reference tuples were taken from Matt Holman's original notebook
    reference_tuple_1 = (0.8352498991871398, -0.26942906823108936, 0.4785)
    reference_tuple_2 = (-0.37388143680631203, 0.762042035331154, -0.52703)

    assert np.all(np.isclose(reference_tuple_1, obs["Z20"]))
    assert np.all(np.isclose(reference_tuple_2, obs["322"]))


def test_observatory_for_moving_observatories():
    auxconfigs = auxiliaryConfigs()
    observatory = sp.Observatory(
        auxconfigs=auxconfigs, args=None, oc_file=get_test_filepath("ObsCodes_test.json")
    )
    obs = observatory.ObservatoryXYZ

    assert obs["250"] == (None, None, None)


def test_observatory_before_1962():
    auxconfigs = auxiliaryConfigs()
    observatory = sp.Observatory(
        auxconfigs=auxconfigs, args=None, oc_file=get_test_filepath("ObsCodes_test.json")
    )

    et = -1229083166.3680687  # thanks to Rahil Makadia

    pos, _ = sg.barycentricObservatoryRates(et, "Z20", observatory)

    x, y, z = -7.426461821563405e07, 1.177545544454091e08, 5.105719899396534e07  # taken from JPL

    # note these should not match precisely because pre-1962 we're using an approximation
    # but this is good enough
    assert np.isclose(pos[0], x, 5)
    assert np.isclose(pos[1], y, 5)
    assert np.isclose(pos[2], z, 5)
