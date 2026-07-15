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
from sorcha.utilities.sorchaConfigs import sorchaConfigs, expertConfigs
from sorcha.utilities.sorchaModuleRNG import PerModuleRNG


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
    t_exp = [30.0, 30.0, 30.0, 30.0]

    test_data = pd.DataFrame(
        {
            "ObjID": obj_ids,
            "trailedSourceMagTrue": obj_mags,
            "PSFMagTrue": psf_mags,
            "fiveSigmaDepth_mag": sig_limit,
            "seeingFwhmGeom_arcsec": seeing,
            "RARateCosDec_deg_day": astRArate,
            "DecRate_deg_day": astDecrate,
            "RA_deg": astRA,
            "Dec_deg": astDec,
            "visitExposureTime": t_exp,
        }
    )

    configs = {"trailing_losses_on": True, "default_snr_cut": False}
    configs = expertConfigs(**configs)
    setattr(configs, "expert", configs)

    rng = PerModuleRNG(2021)

    obs_uncert = addUncertainties(test_data, configs, rng)

    assert_almost_equal(
        obs_uncert["astrometricSigma_deg"],
        [6.274079e-06, 1.380843e-05, 3.346751e-05, 8.272333e-01],
        decimal=6,
    )
    assert_almost_equal(obs_uncert["PSFMagSigma"], [0.042669, 0.100537, 0.233508, 9.439013], decimal=6)
    assert_almost_equal(
        obs_uncert["trailedSourceMagSigma"],
        [0.036043, 0.084722, 0.198055, 9.239667],
        decimal=6,
    )
    assert_almost_equal(obs_uncert["SNRPSFMag"], [24.94898, 10.30708, 4.167592, 0.0001676], decimal=6)

    return


def test_calcRandomAstrometricErrorPerCoord():
    from sorcha.modules.PPAddUncertainties import calcRandomAstrometricErrorPerCoord

    error_rand = calcRandomAstrometricErrorPerCoord(700.0, 160.6781779, 0.60)

    assert_almost_equal(error_rand, 2.6139206)

    return
