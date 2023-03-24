import pandas as pd
import numpy as np
from numpy.testing import assert_equal


def test_PPSNRLimit():

    from surveySimPP.modules.PPSNRLimit import PPSNRLimit

    observations = pd.DataFrame({'SNR': np.arange(1., 15.)})

    new_obs = PPSNRLimit(observations, 9.)
    expected_SNR = np.array([10., 11., 12., 13., 14.])
    assert_equal(new_obs['SNR'].values, expected_SNR)

    zero_obs = PPSNRLimit(observations, 15.)
    assert len(zero_obs) == 0

    all_obs = PPSNRLimit(observations, 0.5)
    assert len(all_obs) == 14

    return
