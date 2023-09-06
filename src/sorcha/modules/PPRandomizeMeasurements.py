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
from sorcha.modules.PPModuleRNG import PerModuleRNG


def randomizeAstrometry(
    df,
    module_rngs,
    raName="AstRA(deg)",
    decName="AstDec(deg)",
    raRndName="AstRARnd(deg)",
    decRndName="AstDecRnd(deg)",
    sigName="AstSig(deg)",
    radecUnits="deg",
    sigUnits="mas",
):
    """
    Randomize astrometry with a normal distribution around the actual RADEC pointing.
    The randomized values are added to the input pandas data frame.

    Parameters:
    -----------
    df (Pandas dataframe): dataframe containing astrometry and sigma.

    module_rngs (PerModuleRNG): A collection of random number generators (per module).

    *Name (string): column names for right ascension, declination,
    randomized right ascension, randomized declination, and standard deviation.

    *Units (string): units for RA and Dec and sigma ('deg'/'rad'/'mas').

    Returns:
    -----------
    df (Pandas dataframe): as input, with randomized RADEC columns added

    Comments:
    -----------
    Covariances in RADEC are currently not supported. The routine calculates
    a normal distribution on the unit sphere, so as to allow for a correct modeling of
    the poles. Distributions close to the poles may look odd in RADEC.

    """

    deg2rad = np.deg2rad
    zeros = np.zeros

    if radecUnits == "deg":
        center = radec2icrf(df[raName], df[decName]).T
    elif radecUnits == "mas":
        center = radec2icrf(df[raName] / 3600000.0, df[decName] / 3600000.0).T
    elif radecUnits == "rad":
        center = radec2icrf(df[raName], df[decName], deg=False).T
    else:
        print("Bad units were provided for RA and Dec.")

    if sigUnits == "deg":
        sigmarad = deg2rad(df[sigName])
    elif sigUnits == "mas":
        sigmarad = deg2rad(df[sigName] / 3600000.0)
    elif sigUnits == "rad":
        sigmarad = df[sigName]
    else:
        print("Bad units were provided for astrometric uncertainty.")

    n = len(df.index)
    xyz = zeros([n, 3])

    xyz = sampleNormalFOV(center, sigmarad, module_rngs, ndim=3)

    if radecUnits == "deg":
        [ra, dec] = icrf2radec(xyz[:, 0], xyz[:, 1], xyz[:, 2], deg=True)

    else:
        [ra, dec] = icrf2radec(xyz[:, 0], xyz[:, 1], xyz[:, 2], deg=False)

    return ra, dec


def sampleNormalFOV(center, sigma, module_rngs, ndim=3):
    """
    Sample n points randomly (normal distribution) on a region on the unit (hyper-)sphere.

    Parameters:
    -----------
    center (float, ndim): center of hpyer-sphere: can be an [n, ndim] dimensional array, but only if n == npoints.

    sigma (n-dimensional array): 1 sigma distance on unit sphere [radians]x

    module_rngs (PerModuleRNG): A collection of random number generators (per module).

    ndim (int): dimension of hyper-sphere.

    Returns:
    --------
    vec ... numpy array [npoints, ndim]

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

    Parameters:
    -----------
    df (Pandas dataframe): dataframe containing astrometry and sigma.

    module_rngs (PerModuleRNG): A collection of random number generators (per module).

    magName (string): column name of photometric data [mag]

    magRndName (string): column name of randomized photometric data [mag].

    sigName (string): column name of standard deviation [mag].

    Returns:
    -----------
    df (Pandas dataframe): as input pandas dataframe, with added column magRndName.

    Comments:
    -----------
    The normal distribution here is in magnitudes while it should be in flux. This will fail for large sigmas.
    Should be fixed at some point.

    """

    rng = module_rngs.getModuleRNG(__name__)

    normal = rng.normal

    s = normal(0, 1, len(df.index))

    return df[magName] + s * df[sigName]


def flux2mag(f, f0=3631):
    """
    AB ugriz system (f0 = 3631 Jy) to magnitude conversion.

    Parameters:
    -----------
    f (float/array of floats): flux [Jy].

    f0 (float): zero point flux.

    Returns:
    -----------
    mag (float/array of floats: pogson magnitude.

    """

    mag = -2.5 * np.log10(f / f0)

    return mag


def mag2flux(mag, f0=3631):
    """
    AB ugriz system (f0 = 3631 Jy) magnitude to flux conversion.

    Parameters:
    -----------
    mag (float/array of floats): pogson magnitude.

    f0 (float): zero point flux.

    Returns:
    -----------
    f (float/array of floats): flux [Jy].

    """

    f = f0 * 10 ** (-0.4 * mag)

    return f


def icrf2radec(x, y, z, deg=True):
    """
    Convert ICRF xyz to Right Ascension and Declination.
    Geometric states on unit sphere, no light travel time/aberration correction.

    Parameters:
    -----------
    x, y, z (floats/arrays of floats): 3D vector of unit length (ICRF)

    deg (Boolean): True for angles in degrees, False for angles in radians.

    Returns:
    -----------
    ra (float/array of floats): Right Ascension [deg].

    dec(float/array of floats): Declination [deg].

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

    Parameters:
    -----------
    ra (float/array of floats): Right Ascension [deg].

    dec(float/array of floats): Declination [deg].

    deg (Boolean): True for angles in degrees, False for angles in radians.

    Returns:
    -----------
    array([x, y, z]) (arrays of floats/arrays): 3D vector of unit length (ICRF)
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
