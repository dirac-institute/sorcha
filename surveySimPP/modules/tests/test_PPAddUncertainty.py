# Developed for the Vera C. Rubin Observatory/LSST Data Management System.
# This product includes software developed by the
# Vera C. Rubin Observatory/LSST Project (https://www.lsst.org).
#
# Copyright 2020 University of Washington
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# NB: the above applies to the first two tests only, the rest were written by SM

import numpy as np
import pandas as pd
from numpy.testing import assert_almost_equal
from surveySimPP.tests.data import get_test_filepath


def test_calcAstrometricUncertainty():

    from surveySimPP.modules.PPAddUncertainties import calcAstrometricUncertainty
    # Test the function calcAstrometricUncertainty
    mag = 20
    m5 = 23.5
    result_nominal = (10.85937575072431, 99.19895320080636, 4.233915645760927)

    result = calcAstrometricUncertainty(mag, m5)

    assert result == result_nominal

    return


def test_calcPhotometricUncertainty():

    from surveySimPP.modules.PPAddUncertainties import calcPhotometricUncertainty
    # Test the function calcPhotometricUncertainty
    snr = 7
    result_nominal = 0.14497986744421684

    result = calcPhotometricUncertainty(snr)

    assert result == result_nominal

    return


def test_degCos():

    from surveySimPP.modules.PPAddUncertainties import degCos

    assert_almost_equal(degCos(90), 0)
    assert_almost_equal(degCos(180), -1)
    assert_almost_equal(degCos(0), 1)

    return


def test_degSin():

    from surveySimPP.modules.PPAddUncertainties import degSin

    assert_almost_equal(degSin(90), 1)
    assert_almost_equal(degSin(180), 0)
    assert_almost_equal(degSin(270), -1)

    return


def test_addUncertainties():

    from surveySimPP.modules.PPAddUncertainties import addUncertainties

    observations = pd.read_csv(get_test_filepath('test_input_fullobs.csv'), nrows=1)

    configs = {'trailingLossesOn': True}
    rng = np.random.default_rng(2021)

    test_obs = addUncertainties(observations, configs, rng)

    expected_astrosig = 0.000003
    expected_photosig_trailed = 0.006756
    expected_photosig_psf = 0.006776
    expected_trailed_mag = 19.65488
    expected_psf_mag = 19.655059
    expected_snr = 159.741315

    assert_almost_equal(test_obs.loc[0, 'AstrometricSigma(deg)'], expected_astrosig, decimal=6)
    assert_almost_equal(test_obs.loc[0, 'PhotometricSigmaTrailedSource(mag)'], expected_photosig_trailed, decimal=6)
    assert_almost_equal(test_obs.loc[0, 'PhotometricSigmaPSF(mag)'], expected_photosig_psf, decimal=6)
    assert_almost_equal(test_obs.loc[0, 'SNR'], expected_snr, decimal=6)
    assert_almost_equal(test_obs.loc[0, 'observedTrailedSourceMag'], expected_trailed_mag, decimal=6)
    assert_almost_equal(test_obs.loc[0, 'observedPSFMag'], expected_psf_mag, decimal=6)

    rng = np.random.default_rng(2021)

    configs = {'trailingLossesOn': False}
    test_obs = addUncertainties(observations, configs, rng)

    expected_astrosig = 0.000003
    expected_photosig_trailed = 0.006736
    expected_trailed_mag = 19.654882
    expected_snr = 160.678178

    assert_almost_equal(test_obs.loc[0, 'AstrometricSigma(deg)'], expected_astrosig, decimal=6)
    assert_almost_equal(test_obs.loc[0, 'PhotometricSigmaTrailedSource(mag)'], expected_photosig_trailed, decimal=6)
    assert_almost_equal(test_obs.loc[0, 'PhotometricSigmaPSF(mag)'], expected_photosig_trailed, decimal=6)
    assert_almost_equal(test_obs.loc[0, 'SNR'], expected_snr, decimal=6)
    assert_almost_equal(test_obs.loc[0, 'observedTrailedSourceMag'], expected_trailed_mag, decimal=6)
    assert_almost_equal(test_obs.loc[0, 'observedPSFMag'], expected_trailed_mag, decimal=6)

    return


def test_uncertainties():

    from surveySimPP.modules.PPAddUncertainties import uncertainties

    observations = pd.read_csv(get_test_filepath('test_input_fullobs.csv'), nrows=1)
    configs = {'trailingLossesOn': False}

    ast_sig_deg, photo_sig, SNR = uncertainties(observations, configs)

    assert_almost_equal(ast_sig_deg[0], 0.000003, decimal=6)
    assert_almost_equal(photo_sig[0], 0.006736, decimal=6)
    assert_almost_equal(SNR[0], 160.6781779, decimal=6)

    configs = {'trailingLossesOn': True}
    ast_sig_deg, photo_sig, SNR = uncertainties(observations, configs)

    assert_almost_equal(ast_sig_deg[0], 0.000003, decimal=6)
    assert_almost_equal(photo_sig[0], 0.006756, decimal=6)
    assert_almost_equal(SNR[0], 160.20922231, decimal=6)

    return


def test_calcRandomAstrometricErrorPerCoord():

    from surveySimPP.modules.PPAddUncertainties import calcRandomAstrometricErrorPerCoord

    error_rand = calcRandomAstrometricErrorPerCoord(700.0, 160.6781779, 0.60)

    assert_almost_equal(error_rand, 2.6139206)

    return
