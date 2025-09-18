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

    Parameters
    -------------
    dRa : float or array of floats
        on sky velocity component in RA*Cos(Dec). [Units: deg/day]

    dDec : float/array of floats
        on sky velocity component in Dec. [Units: deg/day]

    seeing : float or array of floats
        FWHM of the seeing disk. [Units: arcseconds]

    texp : float or array of floats, default=30
        Exposure length. [Units: seconds]

    model : string, optional, default="circularPSF"
        Options: 'circularPSF' or trailedSource'
        'circularPSF': Trailing loss due to the DM detection algorithm. Limit SNR:
        5 sigma in a PSF-convolved image with a circular PSF (no trail fitting). Peak
        fluxes will be lower due to motion of the object.
        'trailedSource': Unavoidable trailing loss due to spreading the PSF
        over more pixels lowering the SNR in each pixel.
        See https://github.com/rhiannonlynne/318-proceedings/blob/master/Trailing%20Losses.ipynb for details.

    a_trail : float, default=0.761
        a fit parameters for trailedSource model. Default parameters from Veres & Chesley (2017).

    b_trail : float, default=1.162
        b fit parameters for trailedSource model. Default parameters from Veres & Chesley (2017).

    a_det : float, default=0.420
        a fit parameters for circularPSF model. Default parameters from Veres & Chesley (2017).

    b_det : float, default=0.003
        b fit parameters for circularPSF model. Default parameters from Veres & Chesley (2017).

    Returns
    -----------
    dmag : float or array of floats
        Loss in detection magnitude due to trailing.

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
    eph_df,
    model="circularPSF",
    dra_cosdec_name="RARateCosDec_deg_day",
    ddec_name="DecRate_deg_day",
    dec_name="Dec_deg",
    seeing_name_survey="seeingFwhmEff_arcsec",
    visit_time_name="visitExposureTime",
):
    """
    Calculates detection trailing losses. Wrapper for calcTrailingLoss.

    Parameters
    -------------
    eph_df : pandas dataframe
        Dataframe of observations for which to calculate trailing losses.

    model : string, default="circularPSF"
        Photometric model. Either 'circularPSF' or 'trailedSource': see docstring for
        calcTrailingLoss for details.

    dra_name : string, default="RARateCosDec_deg_day"
        "eph_df" column name for object RA rate.
        Assumes cos(dec) normalization has already been applied

    ddec_name : string, default="DecRate_deg_day"
        "eph_df" column name for object dec rate.

    dec_name : string, default="Dec_deg"
            "eph_df" column name for object declination.

    seeing_name_survey : string, default="seeingFwhmEff_arcsec"
        "eph_df" column name for seeing.

    visit_time_name : string, default="visitExposureTime"
        "eph_df" column name for exposure length.

    Returns
    -----------
    dmag : float or array of floats
        Loss in detection magnitude due to trailing losses.

    Notes
    --------
    Assumes 'eph_df" has RA and Dec stored in deg/dayrates and the seeing in arcseconds
    """

    dmag = calcTrailingLoss(
        eph_df[dra_cosdec_name],
        eph_df[ddec_name],
        eph_df[seeing_name_survey],
        texp=eph_df[visit_time_name],
        model=model,
    )

    return dmag
