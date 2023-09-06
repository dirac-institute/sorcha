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
from numpy.testing import assert_almost_equal, assert_equal

from sorcha.modules.PPModuleRNG import PerModuleRNG


def test_calcAstrometricUncertainty():
    from sorcha.modules.PPAddUncertainties import calcAstrometricUncertainty

    # Test the function calcAstrometricUncertainty
    mag = 20
    m5 = 23.5
    result_nominal = (10.85937575072431, 99.19895320080636, 4.233915645760927)

    result = calcAstrometricUncertainty(mag, m5)

    assert result == result_nominal

    return


def test_calcPhotometricUncertainty():
    from sorcha.modules.PPAddUncertainties import calcPhotometricUncertainty

    # Test the function calcPhotometricUncertainty
    snr = 7
    result_nominal = 0.14497986744421684

    result = calcPhotometricUncertainty(snr)

    assert result == result_nominal

    return


def test_degCos():
    from sorcha.modules.PPAddUncertainties import degCos

    assert_almost_equal(degCos(90), 0)
    assert_almost_equal(degCos(180), -1)
    assert_almost_equal(degCos(0), 1)

    return


def test_degSin():
    from sorcha.modules.PPAddUncertainties import degSin

    assert_almost_equal(degSin(90), 1)
    assert_almost_equal(degSin(180), 0)
    assert_almost_equal(degSin(270), -1)

    return


def test_addUncertainties():
    from sorcha.modules.PPAddUncertainties import addUncertainties

    obj_ids = ["a21", "b22", "c23", "d24"]
    obj_mags = [21.0, 22.0, 23.0, 34.0]
    psf_mags = [21.2, 22.2, 23.2, 34.2]
    sig_limit = [23.0, 23.0, 23.0, 23.0]
    seeing = [1.0, 1.0, 1.0, 1.0]
    astRArate = [0.03, 0.03, 0.03, 0.03]
    astDecrate = [-0.01, -0.01, -0.01, -0.01]
    astRA = [260.0, 260.0, 260.0, 260.0]
    astDec = [-5.0, -5.0, -5.0, -5]

    test_data = pd.DataFrame(
        {
            "ObjID": obj_ids,
            "TrailedSourceMag": obj_mags,
            "PSFMag": psf_mags,
            "fiveSigmaDepthAtSource": sig_limit,
            "seeingFwhmGeom": seeing,
            "AstRARate(deg/day)": astRArate,
            "AstDecRate(deg/day)": astDecrate,
            "AstRA(deg)": astRA,
            "AstDec(deg)": astDec,
        }
    )

    configs = {"trailing_losses_on": True, "default_SNR_cut": False}

    rng = PerModuleRNG(2021)

    obs_uncert = addUncertainties(test_data, configs, rng)

    assert_almost_equal(
        obs_uncert["AstrometricSigma(deg)"],
        [6.27294202e-06, 1.38053193e-05, 3.34595607e-05, 8.27032813e-01],
        decimal=6,
    )
    assert_almost_equal(
        obs_uncert["PhotometricSigmaPSF(mag)"], [0.04268156, 0.10056753, 0.23357527, 9.43936686], decimal=6
    )
    assert_almost_equal(
        obs_uncert["PhotometricSigmaTrailedSource(mag)"],
        [0.03603496, 0.08470267, 0.19801133, 9.23940376],
        decimal=6,
    )
    assert_almost_equal(
        obs_uncert["SNR"], [2.49413372e01, 1.03038085e01, 4.16624919e00, 1.67620081e-04], decimal=6
    )
    assert_almost_equal(
        obs_uncert["observedTrailedSourceMag"],
        [21.0419, 22.0064, 23.1822, 37.3978],
        decimal=4,
    )
    assert_almost_equal(obs_uncert["observedPSFMag"], [21.239301, 22.050202, 23.006519, 37.514547], decimal=6)

    configs_notrail = {"trailing_losses_on": False, "default_SNR_cut": False}

    obs_notrail = addUncertainties(test_data, configs_notrail, rng)

    assert_equal(
        obs_notrail["PhotometricSigmaPSF(mag)"].values,
        obs_notrail["PhotometricSigmaTrailedSource(mag)"].values,
    )

    configs_SNRcut = {"trailing_losses_on": False, "default_SNR_cut": True}

    obs_SNRcut = addUncertainties(test_data, configs_SNRcut, rng)

    assert_equal(obs_SNRcut["ObjID"].values, ["a21", "b22", "c23"])

    return


def test_uncertainties():
    from sorcha.modules.PPAddUncertainties import uncertainties

    observations = pd.DataFrame(
        {
            "ObjID": ["S1000000a"],
            "fiveSigmaDepthAtSource": [23.0],
            "seeingFwhmGeom": [1.0],
            "TrailedSourceMag": [20.0],
            "PSFMag": [20.1],
            "AstRARate(deg/day)": [0.03],
            "AstDecRate(deg/day)": [-0.01],
            "AstDec(deg)": [-5.0],
        }
    )

    configs = {"trailing_losses_on": False}

    ast_sig_deg, photo_sig, SNR = uncertainties(observations, configs)

    assert_almost_equal(ast_sig_deg[0], 0.000004, decimal=6)
    assert_almost_equal(photo_sig[0], 0.015926, decimal=6)
    assert_almost_equal(SNR[0], 67.673075, decimal=6)

    configs_trail = {"trailing_losses_on": True}

    ast_sig_deg_T, photo_sig_T, SNR_T = uncertainties(observations, configs_trail)

    assert_almost_equal(ast_sig_deg_T[0], 0.000004, decimal=6)
    assert_almost_equal(photo_sig_T[0], 0.015931, decimal=6)
    assert_almost_equal(SNR_T[0], 67.654219, decimal=6)

    return


def test_calcRandomAstrometricErrorPerCoord():
    from sorcha.modules.PPAddUncertainties import calcRandomAstrometricErrorPerCoord

    error_rand = calcRandomAstrometricErrorPerCoord(700.0, 160.6781779, 0.60)

    assert_almost_equal(error_rand, 2.6139206)

    return
