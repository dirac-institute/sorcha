import numpy as np
import pandas as pd
import pytest


def test_calcTrailingLoss():
    from sorcha.modules.PPTrailingLoss import calcTrailingLoss

    assert 0.45347433560262895 == calcTrailingLoss(1.0, 1.0, 1.0)
    return


def test_PPTrailingLoss():
    from sorcha.modules.PPTrailingLoss import PPTrailingLoss

    testoifdf = pd.DataFrame(
        {
            "FieldID": np.arange(0, 10),
            "AstRARate(deg/day)": [
                0.2302361,
                0.59039849,
                0.51966227,
                0.35292237,
                0.34375913,
                0.29833637,
                0.28306961,
                0.16266355,
                0.23515252,
                0.49184532,
            ],
            "AstDecRate(deg/day)": [
                0.07060338,
                0.63168302,
                0.90364059,
                0.69532128,
                0.39521156,
                0.43196356,
                0.47147488,
                0.72890365,
                0.38174909,
                0.03332251,
            ],
            "AstDec(deg)": [
                0.45697193,
                0.39612113,
                0.91493552,
                0.21664349,
                0.2001591,
                0.8722614,
                0.08539993,
                0.07318935,
                0.74395827,
                0.47139718,
            ],
            "seeingFwhmEff": [
                0.96801413,
                0.35969965,
                0.33634724,
                0.43889922,
                0.97841924,
                0.54296975,
                0.99666377,
                0.95417028,
                0.41872633,
                0.85249683,
            ],
        }
    )

    np.testing.assert_array_almost_equal(0.25893924959480374, PPTrailingLoss(oif_df=testoifdf)[5], decimal=14)

    # Check that we give an error for an unknown model.
    with pytest.raises(SystemExit) as err:
        PPTrailingLoss(oif_df=testoifdf, model="FAKE")
    assert err.value.args[0] == "PPTrailingLoss.calcTrailingLoss: model unknown."
