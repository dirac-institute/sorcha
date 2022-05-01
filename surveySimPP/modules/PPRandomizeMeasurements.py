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

"""
Calculate Astrometric and Photometric Uncertainties for ground based observations and randomize OIF measurements accordingly.

"""
# Numpy
import numpy as np
import time

#Pandas
import pandas as pd

from . import PPAddUncertainties as uc

#set a default random number generator
#default_rng = np.random.default_rng(int(time.time()))

__all__ = ['randomizeObservations','flux2mag','mag2flux','radec2icrf','icrf2radec',
           'sampleNormalFOV','randomizeAstrometry','randomizePhotometry']

############################################
# MODULE SPECIFIC EXCEPTION
###########################################
class Error(Exception):
    """Vector module specific exception."""

    pass

def randomizeObservations(ephemsdf,obsdf, rng, raName='fieldRA',decName='fieldDec',obsIdName='observationId',
                     obsEpochName='observationStartMJD',
                     raNameEph='AstRA(deg)',decNameEph='AstDec(deg)',
                     obsIdNameEph='observationId',ephEpochName='FieldMJD',
                     limMagName='fiveSigmaDepth',seeingName='seeingFwhmEff',
                     filterMagName='Filtermag'):

    """Add astrometric and photometric errors to observations generated through JPL ephemeris simulator OIF.

    Parameters:
    -----------
    ephemsdf   ... Pandas dataFrame containing output of JPL ephemeris simulator OIF
    obsdf    ... Pandas dataFrame containing survey simulator output such as LSST opsim
    *Name    ... relevant column names in obsdf
    *NameEph ... relevant column names in ephemsdf


    Returns:
    --------
    ephemsOut ... ephems Pandas dataFrame (observations with added uncertainties)
    """

    #Check whether the observations dataframe covers the whole ephemeris time
    tobsmin=obsdf[obsEpochName].min()
    tobsmax=obsdf[obsEpochName].max()
    tephmin=ephemsdf[ephEpochName].min()
    tephmax=ephemsdf[ephEpochName].max()

    if(tephmin<tobsmin or tephmax>tobsmax):
        print('observations tmin, ephemeris tmin:',tobsmin, tephmin)
        print('observations tmax, ephemeris tmax:',tobsmax, tephmax)
        raise Exception('Observations do not cover the entire ephemeris timespan.')

    # Preselect only those observations mentioned in the ephemeris dataframe
    obsdfSel=obsdf[obsdf[obsIdName].isin(ephemsdf[obsIdNameEph])]

    ephemsFiltered=[]
    # Iterate over all selected observations from opsim database
    for index, row in obsdfSel.iterrows():

        selection=ephemsdf[ephemsdf[obsIdNameEph] == row[obsIdName]].reset_index(drop=True)

        #Add astrometric and photometric 1 sigma uncertainties
        astrSig,SNR,rndError = uc.calcAstrometricUncertainty(selection[filterMagName], row[limMagName],
                                                    FWHMeff=row[seeingName]*1000, output_units='mas')
        photSig = uc.magErrorFromSNR(SNR)

        selection['AstRASigma(mas)'] = astrSig
        selection['AstDecSigma(mas)'] = astrSig
        selection['PhotometricSigma(mag)'] = photSig
        selection['AstometrySigma(deg)'] = astrSig/1000/3600/180

        randomizeAstrometry(selection,rng, raName=raNameEph,decName=decNameEph,
                            raRndName='AstRARnd(deg)',decRndName='AstDecRnd(deg)',
                            sigName='AstometrySigma(deg)',units='deg')

        randomizePhotometry(selection,rng, magName=filterMagName,magRndName='FiltermagRnd',sigName='PhotometricSigma(mag)')

        ephemsFiltered.append(selection)

    ephemsOut=pd.concat(ephemsFiltered).reset_index(drop=True)

    return ephemsOut

def randomizeAstrometry(df, rng, raName='AstRA(deg)',decName='AstDec(deg)',
                         raRndName='AstRARnd(deg)',decRndName='AstDecRnd(deg)',
                         sigName='AstSig(deg)',radecUnits='deg', sigUnits='mas'):

    """Randomize astrometry with a normal distribution around the actual RADEC pointing.
    The randomized values are added to the input pandas data frame.

    Parameters:
    ----------
    df    ... pandas DataFrame containing astrometry and sigma.
    rng
    xName ... column names for right ascension, declination,
              randomized right ascension, randomized declination
              standard deviation
    units ... units for angles ('deg'/'rad')


    Returns:
    --------
    df ... pandas DataFrame with randomized RADEC columns added


    Comments:
    ---------
    Covariances in RADEC are currently not supported. The routine calculates
    a normal distribution on the unit sphere, so as to allow for a correct modeling of
    the poles. Distributions close to the poles may look odd in RADEC.

    """

    deg2rad = np.deg2rad
    rad2deg = np.rad2deg
    zeros = np.zeros

    if (radecUnits=='deg'):
        center= radec2icrf(df[raName],df[decName]).T
    elif (radecUnits=='mas'):
        center= radec2icrf(df[raName]/3600000., df[decName]/3600000.).T
    elif (radecUnits='rad'):
        center= radec2icrf(df[raName],df[decName],deg=False).T
    else:
        print("Bad units were provided for RA and Dec.")

    if (sigUnits=='deg'):
        sigmarad= deg2rad(df[sigName])
    elif (sigUnits=='mas'):
        sigmarad= deg2rad(df[sigName]/3600000.)
    elif (sigUnits=='rad'):
        sigmarad=df[sigName]
    else:
        print("Bad units were provided for astrometric uncertainty.")

    n = len(df.index)
    xyz = zeros([n,3])

    xyz = sampleNormalFOV(center, sigmarad, rng, ndim=3)

    if (units=='deg'):
        [ra, dec] = icrf2radec(xyz[:,0], xyz[:,1], xyz[:,2], deg=True)

    else:
        [ra, dec] = icrf2radec(xyz[:,0], xyz[:,1], xyz[:,2], deg=False)

    return ra, dec


def sampleNormalFOV(center, sigma, rng, ndim=3):
    """Sample n points randomly (normal distribution) on a region on the unit (hyper-)sphere.

    Parameters:
    -----------
    center  ... center of hpyer-sphere (float, ndim); can be an [n, ndim] dimensional array, but only if n == npoints

    sigma   ... 1 sigma distance on unit sphere [radians], [n] dimensional array
    ndim    ... dimension of hyper-sphere (int)
    seed    ... random seed (int)

    Returns:
    --------
    vec ... numpy array [npoints, ndim]
    """

    array = np.array
    normaln = rng.multivariate_normal
    norm = np.linalg.norm
    zeros = np.zeros

    mean = zeros(ndim)
    cov = zeros([ndim,ndim])

    n = len(sigma)

    for i in range(ndim):
           cov[i,i] = 1

    # create a small hypersphere with npoints around center point (e.g. RADEC vector on unit sphere)
    # the small hypersphere will look like a bubble on the unit sphere
    mini_sphere = normaln(mean, cov, n)


    # this step allows for vectorization
    mini_sphere = mini_sphere*array([sigma,sigma,sigma]).T + center


    # project mini_sphere onto celestial sphere
    [x,y,z] = [mini_sphere[:,0],mini_sphere[:,1],mini_sphere[:,2]]/norm(mini_sphere, axis=1)
    vec = array([x,y,z]).T
    return vec


def randomizePhotometry(df, rng, magName='Filtermag',magRndName='FiltermagRnd',sigName='FiltermagSig'):

    """Randomize photometry with normal distribution around magName value.

    Parameters:
    -----------
    df         ... pandas DataFrame containing photometric data
    magName    ... column name of photometric data [mag]
    magRndName ... column name of randomized photometric data [mag]
    sigName    ... column name of standard deviation [mag]


    Returns:
    --------
    df        ... returns input pandas DataFrame with added column magRndName


    Comments:
    ---------
    The normal distribution here is in magnitudes while it should be in flux. This will fail for large sigmas.
    Should be fixed at some point.

    """

    normal = rng.normal

    s = normal(0, 1, len(df.index))

    return df[magName] + s*df[sigName]

def flux2mag(f,  f0=3631):
    """AB ugriz system (f0 = 3631 Jy) to magnitude conversion

       Parameters:
       -----------
       f  ... flux [Jy]
       f0 ... zero point flux

       Returns:
       --------
       mag ... pogson magnitude
    """
    mag=-2.5*np.log10(f/f0)

    return mag

def mag2flux(mag,  f0=3631):
    """AB ugriz system (f0 = 3631 Jy) magnitude to flux conversion

       Parameters:
       -----------
       mag ... pogson magnitude
       f0 ... zero point flux

       Returns:
       --------
       f  ... flux [Jy]

    """
    f = f0*10**(-0.4*mag)

    return f


def icrf2radec(x, y, z, deg=True):
    """Convert ICRF xyz to Right Ascension and Declination.
    Geometric states on unit sphere, no light travel time/aberration correction.

    Parameters:
    -----------
    x,y,z ... 3D vector of unit length (ICRF)
    deg ... True: angles in degrees, False: angles in radians

    Returns:
    --------
    ra ... Right Ascension [deg]
    dec ... Declination [deg]
    """

    norm=np.linalg.norm
    array=np.array
    arctan2=np.arctan2
    arcsin=np.arcsin
    rad2deg=np.rad2deg
    modulo=np.mod
    pix2=2.*np.pi

    pos=array([x,y,z])
    if(pos.ndim>1):
        r=norm(pos,axis=0)
    else:
        r=norm(pos)

    xu=x/r
    yu=y/r
    zu=z/r

    phi=arctan2(yu,xu)
    delta=arcsin(zu)

    if(deg):
        ra = modulo(rad2deg(phi)+360,360)
        dec = rad2deg(delta)
    else:
        ra = modulo(phi+pix2,pix2)
        dec = delta

    return ra, dec


def radec2icrf(ra, dec, deg=True):
    """Convert Right Ascension and Declination to ICRF xyz unit vector.
    Geometric states on unit sphere, no light travel time/aberration correction.
    Parameters:
    -----------
    ra ... Right Ascension [deg]
    dec ... Declination [deg]
    deg ... True: angles in degrees, False: angles in radians

    Returns:
    --------
    x,y,z ... 3D vector of unit length (ICRF)
    """

    deg2rad=np.deg2rad
    array=np.array
    cos=np.cos
    sin=np.sin

    if(deg):
        a = deg2rad(ra)
        d = deg2rad(dec)
    else:
        a = array(ra)
        d = array(dec)

    cosd = cos(d)
    x = cosd*cos(a)
    y = cosd*sin(a)
    z = sin(d)

    return array([x, y, z])


def randomizeAstrometry2(df,raName='AstRA(deg)',decName='AstDec(deg)',
                         raRndName='AstRARnd(deg)',decRndName='AstDecRnd(deg)',
                         sigName='AstSig(deg)',units='deg'):

    """Randomize astrometry with a normal distribution around the actual RADEC pointing.
    The randomized values are added to the input pandas data frame.

    Parameters:
    ----------
    df    ... pandas DataFrame containing astrometry and sigma.
    xName ... column names for right ascension, declination,
              randomized right ascension, randomized declination
              standard deviation
    units ... units for angles ('deg'/'rad')


    Returns:
    --------
    df ... pandas DataFrame with randomized RADEC columns added


    Comments:
    ---------
    Covariances in RADEC are currently not supported. The routine calculates
    a normal distribution on the unit sphere, so as to allow for a correct modeling of
    the poles. Distributions close to the poles may look odd in RADEC.

    """

    deg2rad = np.deg2rad
    rad2deg = np.rad2deg
    zeros = np.zeros

    if (units=='deg'):
        center= radec2icrf(df[raName],df[decName]).T
        sigmarad= deg2rad(df[sigName])
    else:
        center= radec2icrf(df[raName],df[decName],deg=False).T
        sigmarad=df[sigName]

    n = len(df.index)
    xyz = zeros([n,3])

    cov = zeros([n,3,3])
    cov[:,0,0] = sigmarad**2
    cov[:,1,1] = sigmarad**2
    cov[:,2,2] = sigmarad**2

    xyz = sampleNormalFOV2(center, cov, ndim=3, seed=2021)

    if (units=='deg'):
        [ra, dec] = icrf2radec(xyz[:,0], xyz[:,1], xyz[:,2], deg=True)

    else:
        [ra, dec] = icrf2radec(xyz[:,0], xyz[:,1], xyz[:,2], deg=False)

    df[raRndName] = ra
    df[decRndName] = dec

    return



def sampleNormalFOV2(center, cov, npoints=1, ndim=3, seed=2021):
    """Sample n points randomly (normal distribution) on a region on the unit (hyper-)sphere.
    This routine allows for an actual 3D covariance to be taken into account.

    Parameters:
    -----------

    center  ... center of hpyer-sphere (float, ndim); can be an [n, ndim] array, but only if n == npoints
    sigma   ... 1 sigma distance on unit sphere [radians] (fload)
    ndim    ... dimension of hyper-sphere (int)
    npoints ... number of sampled points (int)
    seed    ... random seed (int)

    Returns:
    --------
    vec ... numpy array [npoints, ndim]
    """

    np.random.seed(seed)

    array = np.array
    normaln = np.random.multivariate_normal
    norm = np.linalg.norm
    shape = np.shape
    zeros = np.zeros


    if (shape(center)[0] >= 1):
        n = len(center[:,0])

        if(npoints == 1):
            vec = zeros([n,3])

            for j in range(n):

                # create a small hypersphere with npoints around center point (e.g. RADEC vector on unit sphere)
                # the small hypersphere will look like a bubble on the unit sphere
                # mini_sphere = normaln(mean, cov, npoints)
                mini_sphere = normaln(center[j,:], cov[j,:,:], 1)

                # project mini_sphere onto celestial sphere
                vec[j,:]=array([mini_sphere[:,0],mini_sphere[:,1],mini_sphere[:,2]]/norm(mini_sphere, axis=1)).T

        else:
            vec = []

            for j in range(n):

#             # create a small hypersphere with npoints around center point (e.g. RADEC vector on unit sphere)
#             # the small hypersphere will look like a bubble on the unit sphere
#             # mini_sphere = normaln(mean, cov, npoints)
              mini_sphere = normaln(center[j,:], cov[j,:,:], npoints)

#             # project mini_sphere onto celestial sphere
              vec.extend(array([mini_sphere[:,0],mini_sphere[:,1],mini_sphere[:,2]]/norm(mini_sphere, axis=1)).T)
              vec = array(vec)
    else:

        mini_sphere = normaln(center[:], cov[:,:], npoints)
        vec = array([mini_sphere[:,0],mini_sphere[:,1],mini_sphere[:,2]]/norm(mini_sphere, axis=1)).T

    return vec


# def sampleNormalFOV(npoints, center, sigma=0.01, ndim=3, seed=2021):
#     """Sample n points randomly (normal distribution) on a region on the unit (hyper-)sphere.

#     Parameters:
#     -----------
#     npoints ... number of sampled points (int)
#     center  ... center of hpyer-sphere (float, ndim); can be an [n, ndim] array, but only if n == npoints

#     sigma   ... 1 sigma distance on unit sphere [radians] (fload)
#     ndim    ... dimension of hyper-sphere (int)
#     seed    ... random seed (int)

#     Returns:
#     --------
#     vec ... numpy array [npoints, ndim]
#     """

#     np.random.seed(seed)
#     normaln = np.random.multivariate_normal
#     norm = np.linalg.norm
#     zeros = np.zeros

#     mean = zeros(ndim)
#     cov = zeros([ndim,ndim])

#     for i in range(ndim):
#            cov[i,i] = sigma

#     # create a small hypersphere with npoints around center point (e.g. RADEC vector on unit sphere)
#     # the small hypersphere will look like a bubble on the unit sphere
#     mini_sphere = normaln(mean, cov, npoints)


#     # this step allows for vectorization
#     mini_sphere = mini_sphere + center


#     # project mini_sphere onto celestial sphere
#     [x,y,z] = [mini_sphere[:,0],mini_sphere[:,1],mini_sphere[:,2]]/norm(mini_sphere, axis=1)
#     vec=np.array([x,y,z])
#     return vec.T

# def randomizeAstrometryCD(df,sigma,raName='AstRA(deg)',decName='AstDec(deg)',
#                         raRndName='AstRARnd(deg)',decRndName='AstDecRnd(deg)',units='deg'):

#     """This cheap and dirty method to randomize astrometry around nominal pointing is fast but fails at the poles.

#     Parameters:
#     ----------
#     df    ... pandas DataFrame containing astrometry and sigma.
#     xName ... column names for right ascension, declination,
#               randomized right ascension, randomized declination
#               standard deviation
#     units ... units for angles ('deg'/'rad')

#     """

#     deg2rad = np.deg2rad
#     rad2deg = np.rad2deg
#     mod = np.mod
#     where = np.where
#     cos = np.cos
#     normal = np.random.multivariate_normal

#     n = len(df.index)

#     if (units == 'deg'):
#         sigmarad = deg2rad(sigma)
#     else:
#         sigmarad = sigma

#     mean = [0,0]
#     cov = [[sigmarad**2,0],[0,sigmarad**2]]

#     dRAcosDec, dDec = normal(mean, cov, n).T

#     if(n > 1):

#         if(units == 'deg'):
#             dec = rad2deg(deg2rad(df[decName].values) + dDec)
#             ra = rad2deg(deg2rad(df[raName].values) + dRAcosDec)
#         else:
#             dec = rad2deg(df[decName].values + dDec)
#             ra = rad2deg(df[raName].values + dRAcosDec)

#         idx = where(dec > 90)
#         dec[idx] = 90 - abs(mod(dec[idx],90))
#         ra[idx] = ra[idx] + 180

#         idx = where(dec < -90)
#         dec[idx] = -90 + abs(mod(dec[idx],-90) )
#         ra[idx] = ra[idx] + 180



#     elif(n == 1):

#         if(units == 'deg'):
#             dec = rad2deg(deg2rad(df[decName]) + dDec)
#             ra = rad2deg(deg2rad(df[raName]) + dRAcosDec)
#         else:
#             dec = rad2deg(df[decName] + dDec)
#             ra = rad2deg(df[raName] + dRAcosDec)

#         if (dec > 90):
#             dec = 90 - abs(mod(dec,90))
#             ra = ra + 180

#         if (dec < -90):
#             dec = -90 + abs(mod(dec,90) )
#             ra = ra + 180

#     else:
#         raise Exception('Observations data frame is empty.')

#     ra = mod(ra + 360,360)


#     if (units =='deg'):
#         df[raRndName] = ra
#         df[decRndName] = dec
#     else:
#         df[raRndName] = deg2rad(ra)
#         df[decRndName] = deg2rad(dec)


#     return

#
