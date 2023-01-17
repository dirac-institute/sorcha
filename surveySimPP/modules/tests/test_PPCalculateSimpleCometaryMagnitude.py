import pandas as pd
from numpy.testing import assert_almost_equal
from surveySimPP.tests.data import get_test_filepath


def test_PPCalculateSimpleCometaryMagnitude():

    from surveySimPP.modules.PPCalculateSimpleCometaryMagnitude import PPCalculateSimpleCometaryMagnitude

    test_cometary_df = pd.read_csv(get_test_filepath('cometary_test_df.csv'), sep=' ')

    othercolours = ['u-r', 'g-r', 'i-r', 'z-r', 'y-r']

    df_comet = PPCalculateSimpleCometaryMagnitude(test_cometary_df.copy(), 'r', othercolours)

    expected = [15.77970706, 15.89970703, 15.77970697, 15.89970695, 15.89970149,
                15.89970147, 15.89970144, 16.31969998, 15.89969995, 15.77969533,
                15.8996953, 16.31969374, 15.89969371, 15.89969053, 15.7796905,
                16.31969043, 15.8996904, 16.31968699, 15.89968696, 15.89968691,
                15.77968688]

    assert_almost_equal(df_comet["TrailedSourceMag"], expected, decimal=5)

    return
