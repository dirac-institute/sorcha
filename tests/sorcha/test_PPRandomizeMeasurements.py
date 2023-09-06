import pandas as pd
import numpy as np
from numpy.testing import assert_almost_equal

from sorcha.modules.PPModuleRNG import PerModuleRNG
from sorcha.utilities.dataUtilitiesForTests import get_test_filepath


def test_randomizePhotometry():
    from sorcha.modules.PPRandomizeMeasurements import randomizePhotometry

    test_data = pd.read_csv(get_test_filepath("test_input_fullobs.csv"))

    test_out = randomizePhotometry(
        test_data[0:1],
        PerModuleRNG(2021),
        magName="TrailedSourceMag",
        sigName="PhotometricSigmaTrailedSource(mag)",
    )

    np.testing.assert_almost_equal(test_out.values[0], 19.663194, decimal=5)

    return


def test_randomizeAstrometry():
    from sorcha.modules.PPRandomizeMeasurements import randomizeAstrometry

    test_data = pd.read_csv(get_test_filepath("test_input_fullobs.csv"))

    test_out = randomizeAstrometry(
        test_data[0:1], PerModuleRNG(2021), sigName="AstrometricSigma(deg)", sigUnits="deg"
    )

    np.testing.assert_almost_equal(test_out[0][0], 164.03771597, decimal=5)
    np.testing.assert_almost_equal(test_out[1][0], -17.58257153, decimal=5)

    return


def test_radec_icrf_conversion():
    from sorcha.modules.PPRandomizeMeasurements import radec2icrf, icrf2radec

    observations = pd.read_csv(get_test_filepath("test_input_fullobs.csv"), nrows=1)

    centre = radec2icrf(observations["AstRA(deg)"], observations["AstDec(deg)"])
    expected_centre = np.array([[-0.91652679], [0.26215707], [-0.30207999]])

    ra, dec = icrf2radec(centre[0, :], centre[1, :], centre[2, :])

    assert_almost_equal(centre, expected_centre)
    assert_almost_equal(ra[0], observations["AstRA(deg)"][0])
    assert_almost_equal(dec[0], observations["AstDec(deg)"][0])

    return


def test_sampleNormalFOV():
    from sorcha.modules.PPRandomizeMeasurements import sampleNormalFOV
    from sorcha.modules.PPRandomizeMeasurements import radec2icrf

    observations = pd.read_csv(get_test_filepath("test_input_fullobs.csv"), nrows=1)

    centre = radec2icrf(observations["AstRA(deg)"], observations["AstDec(deg)"])
    sigmarad = np.deg2rad(observations["AstrometricSigma(deg)"])

    n = len(observations.index)
    xyz = np.zeros([n, 3])

    xyz = sampleNormalFOV(centre, sigmarad, PerModuleRNG(2021), ndim=3)
    expected_xyz = [
        [-0.57735025, -0.57735027, -0.57735028],
        [0.57735032, 0.57735025, 0.57735024],
        [-0.57735022, -0.57735029, -0.5773503],
    ]

    assert_almost_equal(xyz, expected_xyz)

    return


def test_flux_mag_conversion():
    from sorcha.modules.PPRandomizeMeasurements import flux2mag, mag2flux

    observations = pd.read_csv(get_test_filepath("test_input_fullobs.csv"), nrows=1)

    flux_test = mag2flux(observations["observedTrailedSourceMag"])
    mag_test = flux2mag(flux_test)

    expected_flux = 5.02107917e-05

    assert_almost_equal(flux_test.values[0], expected_flux)
    assert_almost_equal(observations["observedTrailedSourceMag"][0], mag_test.values[0])

    return
