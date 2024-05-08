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
import sys
import logging
from sorcha.modules.PPModuleRNG import PerModuleRNG
from sorcha.modules.PPSNRLimit import PPSNRLimit

import pandas as pd

pd.options.mode.copy_on_write = True

logger = logging.getLogger(__name__)


def randomizeAstrometryAndPhotometry(observations, configs, module_rngs, verbose=False):
    """
    Wrapper function to perform randomisation of astrometry and photometry around
    their uncertainties. Calls randomizePhotometry() and randomizeAstrometry().

    Adds the following columns to the dataframe:
    - trailedSourceMag
    - PSFMag
    - AstRATrue(deg)
    - AstDecTrue(deg)

    Parameters
    -----------
    observations : pandas dataframe
       Dataframe containing observations.

    configs : dict
       Dictionary of config file variables.

    module_rngs : PerModuleRNG
       A collection of random number generators (per module).

    verbose : bool
       Verbosity on or off. Default False.

    Returns
    ---------
    observations : pandas dataframe
       Original input dataframe with RA and Dec columns and trailedSourceMag and PSFMag
       columns randomized around astrometric and photometric sigma. Original RA and Dec/magnitudes
       stored in separate columns.

    """

    verboselog = logger.info if verbose else lambda *a, **k: None

    # default SNR cut can be disabled in the config file under EXPERT
    # at low SNR, high photometric sigma causes randomisation to sometimes
    # grossly inflate/decrease magnitudes.
    if configs.get("default_SNR_cut", False):
        verboselog("Removing all observations with SNR < 2.0...")
        observations = PPSNRLimit(observations.copy(), 2.0)

    verboselog("Randomising photometry...")
    observations["trailedSourceMag"] = randomizePhotometry(
        observations, module_rngs, magName="trailedSourceMagTrue", sigName="trailedSourceMagSigma"
    )

    if configs.get("trailing_losses_on", False):
        observations["PSFMag"] = randomizePhotometry(
            observations, module_rngs, magName="PSFMagTrue", sigName="PSFMagSigma"
        )
    else:
        observations["PSFMag"] = observations["trailedSourceMag"]

    verboselog("Randomizing astrometry...")
    observations = randomizeAstrometry(
        observations, module_rngs, sigName="astrometricSigma_deg", sigUnits="deg"
    )

    return observations


def randomizeAstrometry(
    df,
    module_rngs,
    raName="RA_deg",
    decName="Dec_deg",
    raOrigName="RATrue_deg",
    decOrigName="DecTrue_deg",
    sigName="AstSig(deg)",
    radecUnits="deg",
    sigUnits="mas",
):
    """
    Randomize astrometry with a normal distribution around the actual RADEC pointing.
    The randomized values replace the original astrometry, with the original values
    stored in separate columns.

    Adds the following columns to the observations dataframe:

    - AstRATrue(deg)
    - AstDecTrue(deg)

    Parameters
    -----------
    df : pandas dataframe
        Dataframe containing astrometry and sigma.

    module_rngs : PerModuleRNG
        A collection of random number generators (per module).

    ra_Name : string, optional
        "df" dataframe column name for the right ascension.
        Default = "RA_deg"

    dec_Name : string, optional
        "df" dataframe column name for the declination. Default = "Dec_deg"

    raOrigName : string, optional
        "df" dataframe column name for where to store original right
        ascension. Default = "RATrue_deg"

    decOrigName : string, optional
        "df" dataframe column name for where to store original declination.
        Default = "DecTrue_deg"

    sigName : string, optional
        "df" dataframe column name for the standard deviation, uncertainty in the
        astrometric position.
        Default = "AstSig(deg)"

    radecUnits : string
        Units for RA and Dec ('deg'/'rad'/'mas'). Default = "deg"

    sigUnits : string
        Units for standard deviation ('deg'/'rad'/'mas'). Default = "mas"


    Returns
    ---------
    df : pandas dataframe
       original input dataframe with RA and Dec columns randomized around
       astrometric sigma and original RA and Dec stored in separate columns

    Notes
    -----------
    Covariances in RADEC are currently not supported. The routine calculates
    a normal distribution on the unit sphere, so as to allow for a correct modeling of
    the poles. Distributions close to the poles may look odd in RADEC.

    """
    if radecUnits == "deg":
        center = radec2icrf(df[raName], df[decName]).T
    elif radecUnits == "mas":
        center = radec2icrf(df[raName] / 3600000.0, df[decName] / 3600000.0).T
    elif radecUnits == "rad":
        center = radec2icrf(df[raName], df[decName], deg=False).T
    else:
        logger.error("Bad units were provided for RA and Dec, terminating...")
        sys.exit(1)

    if sigUnits == "deg":
        sigmarad = np.deg2rad(df[sigName])
    elif sigUnits == "mas":
        sigmarad = np.deg2rad(df[sigName] / 3600000.0)
    elif sigUnits == "rad":
        sigmarad = df[sigName]
    else:
        logger.error("Bad units were provided for RA and Dec, terminating...")
        sys.exit(1)

    n = len(df.index)
    xyz = np.zeros([n, 3])

    xyz = sampleNormalFOV(center, sigmarad, module_rngs, ndim=3)

    if radecUnits == "deg":
        [ra, dec] = icrf2radec(xyz[:, 0], xyz[:, 1], xyz[:, 2], deg=True)

    else:
        [ra, dec] = icrf2radec(xyz[:, 0], xyz[:, 1], xyz[:, 2], deg=False)

    df.rename(columns={raName: raOrigName, decName: decOrigName}, inplace=True)

    df[raName] = ra
    df[decName] = dec

    return df


def sampleNormalFOV(center, sigma, module_rngs, ndim=3):
    """
    Sample n points randomly (normal distribution) on a region on the unit (hyper-)sphere.

    Parameters
    -----------
    center : float
        Center of hpyer-sphere: can be an [n, ndim] dimensional array,
        but only if n == npoints.

    sigma : n-dimensional array
        1 sigma distance on unit sphere [radians]x

    module_rngs : PerModuleRNG
        A collection of random number generators (per module).

    ndim : integer, optional
        Dimension of hyper-sphere. Default = 3

    Return
    --------
    vec : numpy array
        Size [npoints, ndim]

    """
    rng = module_rngs.getModuleRNG(__name__)

    array = np.array
    normaln = rng.multivariate_normal
    norm = np.linalg.norm
    zeros = np.zeros

    mean = zeros(ndim)
    cov = zeros([ndim, ndim])

    n = len(sigma)

    for i in range(ndim):
        cov[i, i] = 1

    # create a small hypersphere with npoints around center point (e.g. RADEC vector on unit sphere)
    # the small hypersphere will look like a bubble on the unit sphere
    mini_sphere = normaln(mean, cov, n)

    # this step allows for vectorization
    mini_sphere = mini_sphere * array([sigma, sigma, sigma]).T + center

    # project mini_sphere onto celestial sphere
    [x, y, z] = [mini_sphere[:, 0], mini_sphere[:, 1], mini_sphere[:, 2]] / norm(mini_sphere, axis=1)
    vec = array([x, y, z]).T

    return vec


def randomizePhotometry(
    df, module_rngs, magName="Filtermag", magRndName="FiltermagRnd", sigName="FiltermagSig"
):
    """
    Randomize photometry with normal distribution around magName value.

    Parameters
    -----------
    df : pandas dataframe
        Dataframe containing astrometry and sigma.

    module_rngs : PerModuleRNG
        A collection of random number generators (per module).

    magName : string, optional
        'df' column name of apparent magnitude. Default = "Filtermag"

    magRndName : string, optional
       'df' column name for storing randomized apparent magnitude, Default = "FiltermagRnd"

    sigName : float, optional
            'df' column name for magnitude standard deviation. Default = "FiltermagSig"

    Returns
    -----------
     : array of floats
         randomized magnitudes for each row in 'df'


    Notes
    -----------
    The normal distribution here is in magnitudes while it should be in flux. This will fail for large sigmas.
    Should be fixed at some point.

    We assume that apparent magnitudes are stored within 'df' and that 'magName'
    corresponds to the corresponding column within 'df'

     'df' is also modified with added column magRndNam to store the randomize apparent magnitude
    """

    rng = module_rngs.getModuleRNG(__name__)

    normal = rng.normal

    s = normal(0, 1, len(df.index))

    return df[magName] + s * df[sigName]


def flux2mag(f, f0=3631):
    """
    AB ugriz system (f0 = 3631 Jy) to magnitude conversion.

    Parameters
    -----------
    f : float or array of floats
        flux. [Units : Jy].

    f0: float, optional
        Zero point flux. Default = 3631

    Returns
    -----------
    mag : float or array of floats
        pogson magnitude. [Units: mag]

    """

    mag = -2.5 * np.log10(f / f0)

    return mag


def mag2flux(mag, f0=3631):
    """
    AB ugriz system (f0 = 3631 Jy) magnitude to flux conversion.

    Parameters
    -----------
    mag : float or rray of floats
        Pogson magnitude. [Units: mag]

    f0 : float, optional
        Zero point flux. Default = 3631

    Returns
    -----------
    f (float/array of floats): flux [Units: Jy].

    """

    f = f0 * 10 ** (-0.4 * mag)

    return f


def icrf2radec(x, y, z, deg=True):
    """
    Convert ICRF xyz to Right Ascension and Declination.
    Geometric states on unit sphere, no light travel time/aberration correction.

    Parameters
    -----------
    x, y, z : floats/arrays of floats
        3D vector of unit length (ICRF)

    de : boolean, optional
        True for angles in degrees, False for angles in radians. Default = True

    Returns
    -----------
    ra : float or array of floats
        Right Ascension. [Units: deg]

    dec: float or array of floats
        Declination. [Units: deg]

    """

    norm = np.linalg.norm
    array = np.array
    arctan2 = np.arctan2
    arcsin = np.arcsin
    rad2deg = np.rad2deg
    modulo = np.mod
    pix2 = 2.0 * np.pi

    pos = array([x, y, z])
    if pos.ndim > 1:
        r = norm(pos, axis=0)
    else:
        r = norm(pos)

    xu = x / r
    yu = y / r
    zu = z / r

    phi = arctan2(yu, xu)
    delta = arcsin(zu)

    if deg:
        ra = modulo(rad2deg(phi) + 360, 360)
        dec = rad2deg(delta)
    else:
        ra = modulo(phi + pix2, pix2)
        dec = delta

    return ra, dec


def radec2icrf(ra, dec, deg=True):
    """
    Convert Right Ascension and Declination to ICRF xyz unit vector.
    Geometric states on unit sphere, no light travel time/aberration correction.

    Parameters
    -----------
    ra : float or array of floats
        Right Ascension. [Units: deg]

    dec: float or array of floats
        Declination. [Units deg]

    deg : boolean, optional
        True for angles in degrees, False for angles in radians. Default = True

    Returns
    -----------
    array([x, y, z]) : arrays/matrix of floats
        3D vector of unit length (ICRF)
    """

    deg2rad = np.deg2rad
    array = np.array
    cos = np.cos
    sin = np.sin

    if deg:
        a = deg2rad(ra)
        d = deg2rad(dec)
    else:
        a = array(ra)
        d = array(dec)

    cosd = cos(d)
    x = cosd * cos(a)
    y = cosd * sin(a)
    z = sin(d)

    return array([x, y, z])
