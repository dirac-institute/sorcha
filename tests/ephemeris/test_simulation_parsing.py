import pytest
import numpy as np
import sorcha.ephemeris.simulation_parsing as sp
from sorcha.utilities.dataUtilitiesForTests import get_test_filepath


def test_observatory_compared_to_original():
    observatory = sp.Observatory(args=None, oc_file=get_test_filepath("ObsCodes_test.json"))
    obs = observatory.ObservatoryXYZ

    # Reference tuples were taken from Matt Holman's original notebook
    reference_tuple_1 = (0.8352498991871398, -0.26942906823108936, 0.4785)
    reference_tuple_2 = (-0.37388143680631203, 0.762042035331154, -0.52703)

    assert np.all(np.isclose(reference_tuple_1, obs["Z20"]))
    assert np.all(np.isclose(reference_tuple_2, obs["322"]))


def test_observatory_for_moving_observatories():
    observatory = sp.Observatory(args=None, oc_file=get_test_filepath("ObsCodes_test.json"))
    obs = observatory.ObservatoryXYZ

    assert obs["250"] == (None, None, None)
