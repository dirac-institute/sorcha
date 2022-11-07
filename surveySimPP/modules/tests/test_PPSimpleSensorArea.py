import pandas as pd
import numpy as np
from numpy.testing import assert_equal
from surveySimPP.tests.data import get_test_filepath


def test_PPSimpleSensorArea():

    from surveySimPP.modules.PPApplyFOVFilter import PPSimpleSensorArea

    test_data = pd.read_csv(get_test_filepath('test_input_fullobs.csv'))

    rng = np.random.default_rng(2021)

    test_out = PPSimpleSensorArea(test_data[0:15], rng, fillfactor=0.9)

    expected = [894816, 897478, 897521, 901987, 902035, 907363, 907416, 907470,
                909426, 910872, 915246]

    assert_equal(expected, test_out['FieldID'].values)

    return
