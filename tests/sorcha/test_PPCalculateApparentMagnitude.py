import pandas as pd
import numpy as np
from numpy.testing import assert_almost_equal, assert_equal
from sorcha.modules.PPCalculateApparentMagnitudeInFilter import PPCalculateApparentMagnitudeInFilter


def test_PPCalculateApparentMagnitudeInFilter_default():
    """Baseline test, no phase function"""
    test_observations = pd.DataFrame(
        {
            "FieldMJD_TAI": [2459215.5],
            "H_filter": [7.3],
            "GS": [0.19],
            "G1": [0.62],
            "G2": [0.14],
            "G12": [0.68],
            "S": [0.04],
            "AstRange(km)": [4.899690e08],
            "Ast-Sun(km)": [6.301740e08],
            "Sun-Ast-Obs(deg)": [4.5918],
        }
    )

    test_observations = PPCalculateApparentMagnitudeInFilter(
        test_observations.copy(), "none", "r", colname="output"
    )

    assert_almost_equal(test_observations["output"][0], 12.998891, decimal=5)


def test_PPCalculateApparentMagnitudeInFilterWithIdentityLightcurve():
    """Baseline test, no phase function, but includes the "identity" (for testing only!)
    light curve model
    """
    test_observations = pd.DataFrame(
        {
            "FieldMJD_TAI": [2459215.5],
            "H_filter": [7.3],
            "GS": [0.19],
            "G1": [0.62],
            "G2": [0.14],
            "G12": [0.68],
            "S": [0.04],
            "AstRange(km)": [4.899690e08],
            "Ast-Sun(km)": [6.301740e08],
            "Sun-Ast-Obs(deg)": [4.5918],
        }
    )

    test_observations = PPCalculateApparentMagnitudeInFilter(
        test_observations.copy(), "none", "r", colname="output", lightcurve_choice="identity"
    )

    assert_almost_equal(test_observations["output"][0], 12.998891, decimal=5)


def test_PPCalculateApparentMagnitudeInFilter():
    test_observations = pd.DataFrame(
        {
            "FieldMJD_TAI": [2459215.5],
            "H_filter": [7.3],
            "GS": [0.19],
            "G1": [0.62],
            "G2": [0.14],
            "G12": [0.68],
            "S": [0.04],
            "AstRange(km)": [4.899690e08],
            "Ast-Sun(km)": [6.301740e08],
            "Sun-Ast-Obs(deg)": [4.5918],
        }
    )

    test_observations = PPCalculateApparentMagnitudeInFilter(
        test_observations.copy(), "HG", "r", colname="HG_mag"
    )
    test_observations = PPCalculateApparentMagnitudeInFilter(
        test_observations.copy(), "HG12", "r", colname="HG12_mag"
    )
    test_observations = PPCalculateApparentMagnitudeInFilter(
        test_observations.copy(), "HG1G2", "r", colname="HG1G2_mag"
    )
    test_observations = PPCalculateApparentMagnitudeInFilter(
        test_observations.copy(), "linear", "r", "linear_mag"
    )

    assert_almost_equal(test_observations["HG_mag"][0], 13.391578, decimal=5)
    assert_almost_equal(test_observations["HG12_mag"][0], 13.387267, decimal=5)
    assert_almost_equal(test_observations["HG1G2_mag"][0], 13.376821, decimal=5)
    assert_almost_equal(test_observations["linear_mag"][0], 13.182563, decimal=5)


def test_PPCalculateSimpleCometaryMagnitude_no_activity():
    from sorcha.modules.PPCalculateSimpleCometaryMagnitude import PPCalculateSimpleCometaryMagnitude

    # data is for 67P, taken by Colin Snodgrass, and validated against same
    # abnormally large seeing is to account for Colin's use of an aperture measured at comet distance

    cometary_obs = pd.DataFrame(
        {
            "optFilter": ["r", "r"],
            "TrailedSourceMag": [19.676259, 22.748274],
            "H_r": [15.35, 15.35],
            "afrho1": [1552, 1552],
            "k": [-3.35, -3.35],
            "seeingFwhmEff": [8.064748, 3.206723],
        }
    )

    rho = [1.260000, 4.889116]
    delta = [1.709000, 4.298050]
    alpha = [35.100000, 10.339021]

    df_comet = PPCalculateSimpleCometaryMagnitude(cometary_obs, ["r"], rho, delta, alpha)

    assert_almost_equal(df_comet["TrailedSourceMag"], [19.676259, 22.748274], decimal=3)


def test_PPApplyColourOffsets():
    from sorcha.modules.PPApplyColourOffsets import PPApplyColourOffsets

    objects = np.array(["obj1", "obj1", "obj1", "obj1", "obj2", "obj2", "obj2", "obj2"])

    optfilter = np.array(["r", "g", "i", "z", "r", "g", "z", "i"])

    ur = np.array([0.1, 0.1, 0.1, 0.1, 0.2, 0.2, 0.2, 0.2])
    gr = np.array([0.3, 0.3, 0.3, 0.3, 0.4, 0.4, 0.4, 0.4])
    ir = np.array([0.5, 0.5, 0.5, 0.5, 0.6, 0.6, 0.6, 0.6])
    zr = np.array([0.7, 0.7, 0.7, 0.7, 0.8, 0.8, 0.8, 0.8])

    H = np.array([10.0, 10.0, 10.0, 10.0, 12.0, 12.0, 12.0, 12.0])
    G = np.array([0.15, 0.15, 0.15, 0.15, 0.12, 0.12, 0.12, 0.12])

    test_obs = pd.DataFrame(
        {
            "ObjID": objects,
            "optFilter": optfilter,
            "u-r": ur,
            "g-r": gr,
            "i-r": ir,
            "z-r": zr,
            "H_r": H,
            "GS": G,
        }
    )

    othercolours = ["u-r", "g-r", "i-r", "z-r"]
    observing_filters = ["r", "u", "g", "i", "z"]

    func_test = PPApplyColourOffsets(test_obs.copy(), "HG", othercolours, observing_filters, "r")

    assert_equal(func_test["H_filter"].values, [10.0, 10.3, 10.5, 10.7, 12.0, 12.4, 12.8, 12.6])

    Gr = np.array([0.151, 0.151, 0.151, 0.151, 0.121, 0.121, 0.121, 0.121])
    Gu = np.array([0.152, 0.152, 0.152, 0.152, 0.122, 0.122, 0.122, 0.122])
    Gi = np.array([0.153, 0.153, 0.153, 0.153, 0.123, 0.123, 0.123, 0.123])
    Gz = np.array([0.154, 0.154, 0.154, 0.154, 0.124, 0.124, 0.124, 0.124])
    Gg = np.array([0.155, 0.155, 0.155, 0.155, 0.125, 0.125, 0.125, 0.125])

    test_obs["GSr"] = Gr
    test_obs["GSu"] = Gu
    test_obs["GSi"] = Gi
    test_obs["GSz"] = Gz
    test_obs["GSg"] = Gg

    test_obs.drop(["GS"], axis=1, inplace=True)

    func_test_2 = PPApplyColourOffsets(test_obs.copy(), "HG", othercolours, observing_filters, "r")

    assert_equal(func_test_2["H_filter"].values, [10.0, 10.3, 10.5, 10.7, 12.0, 12.4, 12.8, 12.6])
    assert_equal(func_test_2["GS"].values, [0.151, 0.155, 0.153, 0.154, 0.121, 0.125, 0.124, 0.123])


def test_PPCalculateApparentMagnitude():
    from sorcha.modules.PPCalculateApparentMagnitude import PPCalculateApparentMagnitude

    asteroid_obs = pd.DataFrame(
        {
            "MJD": [2459215.5],
            "H_r": [7.3],
            "GS": [0.19],
            "G1": [0.62],
            "G2": [0.14],
            "G12": [0.68],
            "S": [0.04],
            "AstRange(km)": [4.899690e08],
            "Ast-Sun(km)": [6.301740e08],
            "Sun-Ast-Obs(deg)": [4.5918],
            "optFilter": ["i"],
            "i-r": [-0.11],
        }
    )

    asteroid_obs_single = pd.DataFrame(
        {
            "MJD": [2459215.5],
            "H_r": [7.3],
            "GS": [0.19],
            "G1": [0.62],
            "G2": [0.14],
            "G12": [0.68],
            "S": [0.04],
            "AstRange(km)": [4.899690e08],
            "Ast-Sun(km)": [6.301740e08],
            "Sun-Ast-Obs(deg)": [4.5918],
            "optFilter": ["r"],
        }
    )

    asteroid_out = PPCalculateApparentMagnitude(asteroid_obs, "HG", "r", ["i-r"], ["r", "i"], "none")
    asteroid_single = PPCalculateApparentMagnitude(asteroid_obs_single, "HG", "r", ["r-r"], ["r"], "none")

    assert_almost_equal(asteroid_out["TrailedSourceMag"].values[0], 13.281578, decimal=6)
    assert_almost_equal(asteroid_out["H_filter"].values[0], 7.19, decimal=6)

    assert_almost_equal(asteroid_single["TrailedSourceMag"].values[0], 13.391578, decimal=6)
    assert_almost_equal(asteroid_single["H_filter"].values[0], 7.3, decimal=6)
