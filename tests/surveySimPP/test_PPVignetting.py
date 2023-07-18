import pandas as pd
import numpy as np
from numpy.testing import assert_almost_equal


def test_PPVignetting():
    import sorcha.modules.PPVignetting as PPVignetting

    test_data = {
        "ObjID": ["a", "b", "c", "d", "e"],
        "AstRA(deg)": [164.037713, 241.757043, 171.929414, 173.235944, 148.678088],
        "AstDec(deg)": [-17.582575, 0.148175, 5.283073, 4.432855, 13.865548],
        "FieldID": [894816, 1208618, 968937, 997409, 2007672],
        "fieldRA": [163.87542091, 241.90572222, 173.11867794, 172.57401125, 149.09896347],
        "fieldDec": [-18.84327137, -0.93109129, 4.9987505, 3.91623225, 15.34987916],
        "fiveSigmaDepth": [23.86356436, 22.40228655, 23.37658623, 22.38353176, 22.50307379],
    }

    test_df = pd.DataFrame(test_data)

    test_df["fiveSigmaDepthAtSource"] = PPVignetting.vignettingEffects(test_df)
    expected = [23.83940373, 22.39012774, 23.35663436, 22.3797003, 22.44707285]

    assert_almost_equal(test_df["fiveSigmaDepthAtSource"].values, expected, decimal=6)

    return


def test_calcVignettingLosses():
    from sorcha.modules.PPVignetting import calcVignettingLosses

    test_loss = calcVignettingLosses(164.037713, -17.582575, 163.87542091, -18.84327137)
    assert_almost_equal(test_loss, 0.02416062)

    return


def test_haversine():
    from sorcha.modules.PPVignetting import haversine

    test_haversine = haversine(164.037713, -17.582575, 163.87542091, -18.84327137)
    test_haversine_zero = haversine(164.037713, -17.582575, 164.037713, -17.582575)

    assert_almost_equal(test_haversine, 1.2648216)
    assert_almost_equal(test_haversine_zero, 0.0)

    return


def test_vignetFunc():
    from sorcha.modules.PPVignetting import vignetFunc

    test_theta = np.rad2deg(1.2648216148765565)
    test_mag = vignetFunc(test_theta)

    assert_almost_equal(test_mag, 1.2245226)
    assert_almost_equal(vignetFunc(0.0), 0.0)

    return
