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

import numpy as np
import logging
import sys


def calcTrailingLoss(
    dRaCosDec,
    dDec,
    seeing,
    texp=30.0,
    model="circularPSF",
    a_trail=0.761,
    b_trail=1.162,
    a_det=0.420,
    b_det=0.003,
):
    """
    Find the trailing loss from trailing and detection (Veres & Chesley 2017)

    Parameters:
    -----------
    dRa (float/array of floats): on sky velocity component in RA*Cos(Dec), deg/day.

    dDec (float/array of floats): on sky velocity component in Dec, deg/day.

    seeing (float/array of floats): FWHM of the seeing disk, arcseconds.

    texp (float): exposure length in seconds, defaults to 30 seconds.

    model (str):
        - 'circularPSF': Trailing loss due to the DM detection algorithm. Limit SNR:
        5 sigma in a PSF-convolved image with a circular PSF (no trail fitting). Peak
        fluxes will be lower due to motion of the object.
        -'trailedSource': Unavoidable trailing loss due to spreading the PSF
        over more pixels lowering the SNR in each pixel.
        See https://github.com/rhiannonlynne/318-proceedings/blob/master/Trailing%20Losses.ipynb for details.

    *_trail (float): fit parameters for trailedSource model. Default parameters from Veres & Chesley (2017).

    *_det (float): fit parameters for circularPSF model. Default parameters from Veres & Chesley (2017).

    Returns:
    -----------
    dmag (float/array of floats): loss in detection magnitude due to trailing.

    """

    pplogger = logging.getLogger(__name__)

    vel = np.sqrt(dRaCosDec**2 + dDec**2)
    vel = vel / 24.0  # convert to arcsec / sec

    x = vel * texp / seeing

    if model == "trailedSource":
        dmagTrail = 1.25 * np.log10(1.0 + a_trail * x**2 / (1.0 + b_trail * x))
        dmag = dmagTrail
    elif model == "circularPSF":
        dmagDetect = 1.25 * np.log10(1.0 + a_det * x**2 / (1.0 + b_det * x))
        dmag = dmagDetect
    else:
        pplogger.error("PPTrailingLoss.calcTrailingLoss: model unknown.")
        sys.exit("PPTrailingLoss.calcTrailingLoss: model unknown.")

    return dmag


def PPTrailingLoss(
    oif_df,
    model="circularPSF",
    dra_name="AstRARate(deg/day)",
    ddec_name="AstDecRate(deg/day)",
    dec_name="AstDec(deg)",
    seeing_name_survey="seeingFwhmEff",
):
    """
    Calculates detection trailing losses. Wrapper for calcTrailingLoss.

    Parameters:
    -----------
    oif_df (Pandas dataframe): dataframe of observations for which to calculate trailing losses.

    model (string): Either 'circularPSF' or 'trailedSource': see docstring for calcTrailingLoss for details.

    *_name (string): Column names for object RA rate, Dec rate and Dec respectively.

    seeing_name_survey (string): Column name for seeing.

    Returns:
    -----------
    dmag (float/array of floats): loss in detection magnitude due to trailing.

    """

    dmag = calcTrailingLoss(
        oif_df[dra_name] * np.cos(oif_df[dec_name] * np.pi / 180),
        oif_df[ddec_name],
        oif_df[seeing_name_survey],
        model=model,
    )

    return dmag
