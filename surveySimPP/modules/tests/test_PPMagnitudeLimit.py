import pandas as pd
import numpy as np
from numpy.testing import assert_equal


def test_PPMagnitudeLimit():
    from surveySimPP.modules.PPMagnitudeLimit import PPMagnitudeLimit

    test_input = pd.DataFrame({'observedPSFMag': np.arange(15, 25)})

    test_output = PPMagnitudeLimit(test_input, 18.)
    assert_equal(test_output['observedPSFMag'].values, [15, 16, 17])

    test_zero = PPMagnitudeLimit(test_input, 14.)
    assert len(test_zero) == 0

    test_all = PPMagnitudeLimit(test_input, 25.)
    assert len(test_all) == 10
