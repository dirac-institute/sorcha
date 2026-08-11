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


def test_convert_to_geocentric_zero_parallax_constants():
    """A parallax constant that is legitimately 0.0 must not be mistaken for a
    missing position (e.g. geocenter 500, Greenwich 000, equatorial station 782)."""
    auxconfigs = auxiliaryConfigs()
    observatory = sp.Observatory(
        auxconfigs=auxconfigs, args=None, oc_file=get_test_filepath("ObsCodes_test.json")
    )

    # Geocenter: every constant is 0.0 -> a finite (0, 0, 0) offset, not (None, None, None).
    assert observatory.convert_to_geocentric({"Longitude": 0.0, "cos": 0.0, "sin": 0.0}) == (0.0, 0.0, 0.0)

    # Greenwich: Longitude == 0.0, but cos/sin are nonzero -> finite position.
    x, y, z = observatory.convert_to_geocentric({"Longitude": 0.0, "cos": 0.62411, "sin": 0.77873})
    assert np.allclose((x, y, z), (0.62411, 0.0, 0.77873))

    # Equatorial station: sin == 0.0 -> finite position with z == 0.
    x, y, z = observatory.convert_to_geocentric({"Longitude": 281.65, "cos": 0.999, "sin": 0.0})
    assert z == 0.0
    assert not np.isnan([x, y, z]).any()

    # A genuinely position-less observatory (no parallax keys) still returns None.
    assert observatory.convert_to_geocentric({"Name": "Roving Observer"}) == (None, None, None)


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
