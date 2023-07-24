import pandas as pd
import numpy as np
from numpy.testing import assert_equal


def test_PPSNRLimit():
    from sorcha.modules.PPSNRLimit import PPSNRLimit

    observations = pd.DataFrame({"SNR": np.arange(1.0, 15.0)})

    new_obs = PPSNRLimit(observations, 9.0)
    expected_SNR = np.array([10.0, 11.0, 12.0, 13.0, 14.0])
    assert_equal(new_obs["SNR"].values, expected_SNR)

    zero_obs = PPSNRLimit(observations, 15.0)
    assert len(zero_obs) == 0

    all_obs = PPSNRLimit(observations, 0.5)
    assert len(all_obs) == 14

    return
