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
import astropy.units as u
from sorcha.modules import PPTrailingLoss
from sorcha.modules import PPRandomizeMeasurements
from sorcha.modules.PPSNRLimit import PPSNRLimit


def degCos(x):
    """
    Calculate cosine of an angle in degrees.

    Parameters:
    -----------
    x (float): angle in degrees.

    Returns:
    -----------
    The cosine of x.
    """

    return np.cos(x * np.pi / 180.0)


def degSin(x):
    """
    Calculate sine of an angle in degrees.

    Parameters:
    -----------
    x (float): angle in degrees.

    Returns:
    -----------
    The sine of x.
    """

    return np.sin(x * np.pi / 180.0)


def addUncertainties(detDF, configs, module_rngs, verbose=True):
    """
    Generates astrometric and photometric uncertainties, and SNR. Uses uncertainties
    to randomize the photometry. Accounts for trailing losses.

    Parameters:
    -----------
    detDF (Pandas dataframe): Dataframe of observations.

    configs (dictionary): dictionary of configurations from config file.

    module_rngs (PerModuleRNG): A collection of random number generators (per module).

    Returns:
    -----------
    detDF (Pandas dataframe): dataframe of observations, with new columns for observed
    magnitudes, SNR, and astrometric/photometric uncertainties.

    """

    pplogger = logging.getLogger(__name__)
    verboselog = pplogger.info if verbose else lambda *a, **k: None

    detDF["AstrometricSigma(deg)"], detDF["PhotometricSigmaTrailedSource(mag)"], detDF["SNR"] = uncertainties(
        detDF, configs, filterMagName="TrailedSourceMag"
    )

    if configs.get("trailing_losses_on", False):
        _, detDF["PhotometricSigmaPSF(mag)"], detDF["SNR"] = uncertainties(
            detDF, configs, filterMagName="PSFMag"
        )
    else:
        detDF["PhotometricSigmaPSF(mag)"] = detDF["PhotometricSigmaTrailedSource(mag)"]

    # default SNR cut can be disabled in the config file under EXPERT
    # at low SNR, high photometric sigma causes randomisation to sometimes
    # grossly inflate/decrease magnitudes.
    if configs.get("default_SNR_cut", False):
        verboselog("Removing all observations with SNR < 2.0...")
        detDF = PPSNRLimit(detDF.copy(), 2.0)

    verboselog("Randomising photometry...")
    detDF["observedTrailedSourceMag"] = PPRandomizeMeasurements.randomizePhotometry(
        detDF, module_rngs, magName="TrailedSourceMag", sigName="PhotometricSigmaTrailedSource(mag)"
    )

    if configs.get("trailing_losses_on", False):
        detDF["observedPSFMag"] = PPRandomizeMeasurements.randomizePhotometry(
            detDF, module_rngs, magName="PSFMag", sigName="PhotometricSigmaPSF(mag)"
        )
    else:
        detDF["observedPSFMag"] = detDF["observedTrailedSourceMag"]

    return detDF


def uncertainties(
    detDF,
    configs,
    limMagName="fiveSigmaDepthAtSource",
    seeingName="seeingFwhmGeom",
    filterMagName="TrailedSourceMag",
    dra_name="AstRARate(deg/day)",
    ddec_name="AstDecRate(deg/day)",
    dec_name="AstDec(deg)",
):
    """
    Add astrometric and photometric uncertainties to observations.

    Parameters:
    -----------
    detDF (Pandas dataframe): dataframe containing observations.

    configs (dictionary): dictionary of configurations from config file.

    limMagName, seeingName, filterMagName, dra_name, ddec_name, dec_name (strings): column
    names of the limiting magnitude, seeing, magnitude, RA rate, DEC rate and DEC.

    Returns:
    -----------
    astrSigDeg (numpy array): astrometric uncertainties in degrees.

    photometric_sigma (numpy array): photometric uncertainties in magnitude.

    SNR (numpy array): signal-to-noise ratio.

    """

    if configs.get("trailing_losses_on", False):
        dMag = PPTrailingLoss.calcTrailingLoss(
            detDF[dra_name] * degCos(detDF[dec_name]), detDF[ddec_name], detDF[seeingName]
        )
    else:
        dMag = 0.0

    astrSig, SNR, _ = calcAstrometricUncertainty(
        detDF[filterMagName] + dMag, detDF[limMagName], FWHMeff=detDF[seeingName] * 1000, output_units="mas"
    )
    photometric_sigma = calcPhotometricUncertainty(SNR)
    astrSigDeg = (astrSig.values * u.mas).to(u.deg).value

    return (astrSigDeg, photometric_sigma, SNR)


def calcAstrometricUncertainty(
    mag, m5, nvisit=1, FWHMeff=700.0, error_sys=10.0, astErrCoeff=0.60, output_units="mas"
):
    """Calculate the astrometric uncertainty, for object catalog purposes.
    The effective FWHMeff MUST BE given in miliarcsec (NOT arcsec!).
    Systematic error, error_sys, must be given in miliarcsec.
    The result corresponds to a single-coordinate uncertainty.
    Note that the total astrometric uncertainty (e.g. relevant when
    matching two catalogs) will be sqrt(2) times larger.
    Default values for parameters are based on estimates for LSST.

    Parameters:
    -----------
    mag (float/array of floats): magnitude of the observation.

    m5 (float/array of floats): 5-sigma limiting magnitude.

    nvisit (int): number of visits to consider.

    FWHMeff (float): effective Full Width at Half Maximum of Point Spread Function [mas].

    error_sys (float): systematic error [mas].

    output_units (string): 'mas' (default): milliarcseconds, 'arcsec': arcseconds.

    Returns:
    -----------
    astrom_error (float/array of floats): astrometric error.

    SNR (float/array of floats): signal to noise ratio.

    error_rand (float/array of floats): random error.

    Description:
    ------------
    The astrometric error can be applied to parallax or proper motion (for nvisit>1).
    If applying to proper motion, should also divide by the # of years of the survey.
    This is also referenced in the LSST overview paper (arXiv:0805.2366, ls.st/lop)

    - assumes sqrt(Nvisit) scaling, which is the best-case scenario
    - calcRandomAstrometricError assumes maxiumm likelihood solution,
      which is also the best-case scenario
    - the systematic error, error_sys = 10 mas, corresponds to the
      design spec from the LSST Science Requirements Document (ls.st/srd)

    """

    # first compute SNR
    rgamma = 0.039
    xval = np.power(10, 0.4 * (mag - m5))
    SNR = 1.0 / np.sqrt((0.04 - rgamma) * xval + rgamma * xval * xval)
    # random astrometric error for a single visit
    error_rand = calcRandomAstrometricErrorPerCoord(FWHMeff, SNR, astErrCoeff)
    # random astrometric error for nvisit observations
    if nvisit > 1:
        error_rand = error_rand / sqrt(nvisit)
    # add systematic error floor:
    astrom_error = np.sqrt(error_sys * error_sys + error_rand * error_rand)

    if output_units == "arcsec":
        astrom_error = astrom_error / 1000
        error_rand = error_rand / 1000

    return astrom_error, SNR, error_rand


def calcRandomAstrometricErrorPerCoord(FWHMeff, SNR, AstromErrCoeff=0.60):
    """Calculate the random astrometric uncertainty, as a function of
    effective FWHMeff and signal-to-noise ratio SNR
    Returns astrometric uncertainty in the same units as FWHM.
    ** This error corresponds to a single-coordinate error **
    the total astrometric uncertainty (e.g. relevant when matching
    two catalogs) will be sqrt(2) times larger.

    Parameters:
    -----------
    FWHMeff (float/array of floats): Effective Full Width at Half Maximum of Point Spread Function [mas].

    SNR (float/array of floats): Signal-to-noise ratio.

    AstromErrCoeff (float): Astrometric error coefficient (see description below).

    Returns:
    -----------
    RandomAstrometricErrorPerCoord (float/array of floats): random astrometric uncertainty per coordinate.

    Description:
    ------------
    The coefficient AstromErrCoeff for Maximum Likelihood
    solution is given by

       AstromErrCoeff = <P^2> / <|dP/dx|^2> * 1/FWHMeff

    where P is the point spread function, P(x,y).

    For a single-Gaussian PSF, AstromErrCoeff = 0.60
    For a double-Gaussian approximation to Kolmogorov
    seeing, AstromErrCoeff = 0.55; however, given the
    same core seeing (FWHMgeom) as for a single-Gaussian
    PSF, the resulting error will be 36% larger because
    FWHMeff is 1.22 times larger and SNR is 1.22 times
    smaller, compared to error for single-Gaussian PSF.
    Although Kolmogorov seeing is a much better approximation
    of the free atmospheric seeing than single Gaussian seeing,
    the default value of AstromErrCoeff is set to the
    more conservative value.

    Note also that AstromErrCoeff = 1.0 is often used in
    practice to empirically account for other error sources.
    """

    RandomAstrometricErrorPerCoord = AstromErrCoeff * FWHMeff / SNR

    return RandomAstrometricErrorPerCoord


def calcPhotometricUncertainty(snr):
    """
    Convert flux signal to noise ratio to an uncertainty in magnitude.

    Parameters:
    -----------
    snr (float/array of floats): The signal-to-noise-ratio in flux.

    Returns:
    -----------
    magerr (float/array of floats): The resulting uncertainty in magnitude.

    """

    # see e.g. www.ucolick.org/~bolte/AY257/s_n.pdf section 3.1
    magerr = 2.5 * np.log10(1.0 + 1.0 / snr)

    return magerr
