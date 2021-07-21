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
Calculate Astrometric and Photometric Uncertainties for ground based observations.

"""
# Numpy
import numpy as np

#Pandas
import pandas as pd


__all__ = ['addUncertainties','calcAstrometricUncertainty', 'calcPhotometricUncertainty',
           'calcRandomAstrometricErrorPerCoord', 'magErrorFromSNR']


############################################
# MODULE SPECIFIC EXCEPTION
###########################################
class Error(Exception):
    """Vector module specific exception."""

    pass


############################################


def addUncertainties(ephemsdf,obsdf,raName='fieldRA',decName='fieldDec',obsIdName='observationId',
                     obsEpochName='observationStartMJD',
                     raNameEph='AstRA(deg)',decNameEph='AstDec(deg)',
                     obsIdNameEph='observationId',ephEpochName='FieldMJD',
                     limMagName='fiveSigmaDepth',seeingName='seeingFwhmGeom',
                     filterMagName='MaginFilterTrue'):

    """Add astrometric and photometric uncertainties to observations generated through JPL ephemeris simulator.

    Parameters:
    -----------
    ephemsdf   ... Pandas dataFrame containing output of JPL ephemeris simulator
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
    #obsdfSel=obsdf[obsdf[obsIdName].isin(ephemsdf[obsIdNameEph])][[obsIdName, limMagName, seeingName]]

    #ephemsFiltered=[]
    # Iterate over all selected observations from opsim database
    #for index, row in obsdfSel.iterrows():

    #    selection=ephemsdf[ephemsdf[obsIdNameEph] == row[obsIdName]].reset_index(drop=True)

        #Add astrometric and photometric 1 sigma uncertainties
    #    astrSig,SNR,rndError = calcAstrometricUncertainty(selection[filterMagName], row[limMagName],
    #                                               FWHMeff=row[seeingName]*1000, output_units='mas')
    #    photSig = magErrorFromSNR(SNR)

    #    selection['AstRASigma(mas)'] = astrSig
    #    selection['AstDecSigma(mas)'] = astrSig
    #    selection['PhotometricSigma(mag)'] = photSig

    #    ephemsFiltered.append(selection)

    #ephemsOut=pd.concat(ephemsFiltered).reset_index(drop=True)

    #hopefully faster way to do this
    #ephemsdf=ephemsdf.join(obsdfSel.set_index(obsIdName), on=obsIdNameEph)
    #astrSig,SNR,_=calcAstrometricUncertainty(ephemsdf[filterMagName], ephemsdf[limMagName],
    #                                                FWHMeff=ephemsdf[seeingName]*1000, output_units='mas')
    #ephemsdf.drop(columns=[limMagName, seeingName])
    #ephemsdf['AstRASigma(mas)']=astrSig
    #ephemsdf['AstDecSigma(mas)']=astrSig
    #ephemsdf['PhotometricSigma(mag)']=magErrorFromSNR(SNR)

    #a more memory efficient way
    l = len(ephemsdf.index)
    limMag = obsdf.lookup(ephemsdf[obsIdNameEph], [limMagName]*l)
    seeing = obsdf.lookup(ephemsdf[obsIdNameEph], [seeingName]*l)

    astrSig,SNR,_=calcAstrometricUncertainty(ephemsdf[filterMagName], limMag,
                                            FWHMeff=seeing*1000, output_units='mas')
    photometric_sigma = magErrorFromSNR(SNR)

    return (astrSig, photometric_sigma, SNR)


def calcAstrometricUncertainty(mag, m5, nvisit=1, FWHMeff=700.0, error_sys = 10.0,
                               astErrCoeff=0.60, output_units='mas'):
    """Calculate the astrometric uncertainty, for object catalog purposes.
    The effective FWHMeff MUST BE given in miliarcsec (NOT arcsec!).
    Systematic error, error_sys, must be given in miliarcsec.
    The result corresponds to a single-coordinate uncertainty.
    Note that the total astrometric uncertainty (e.g. relevant when
    matching two catalogs) will be sqrt(2) times larger.
    Default values for parameters are based on estimates for LSST.

    Parameters:
    -----------
        mag            ...    magnitude of the observation
        m5             ...    5-sigma limiting magnitude
        nvisit         ...    number of visits to consider
        FWHMeff        ...    effective Full Width at Half Maximum of Point Spread Function [mas]
        error_sys      ...    sytstematic error [mas]
        output_units   ...    'mas' (default): milliarcseconds, 'arcsec': arcseconds

    Returns:
    ---------
        astrom_error   ...    astrometric error
        SNR            ...    signal to noise ratio
        error_rand     ...    random error

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

    Requirements:
    --------------
    numpy as np
    """

    # external functions
    power=np.power
    sqrt=np.sqrt


    # first compute SNR
    rgamma = 0.039
    xval = power(10, 0.4*(mag-m5))
    SNR = 1./sqrt((0.04-rgamma)*xval + rgamma*xval*xval)
    # random astrometric error for a single visit
    error_rand = calcRandomAstrometricErrorPerCoord(FWHMeff, SNR, astErrCoeff)
    # random astrometric error for nvisit observations
    if (nvisit > 1):
        error_rand = error_rand / sqrt(nvisit)
    # add systematic error floor:
    astrom_error = sqrt(error_sys * error_sys + error_rand*error_rand)

    if (output_units=='arcsec'):
        astrom_error=astrom_error/1000
        error_rand=error_rand/1000

    return astrom_error, SNR, error_rand


def calcPhotometricUncertainty(SNR):
    """Photometric uncertainty in magnitudes from flux signal to noise ratio.

    Parameters:
    -----------
          snr ... is the signal to noise ratio in flux

    Returns:
    --------
          photSig ... photometric uncertainty [mag]

    """

    photSig = magErrorFromSNR(SNR)
    return photSig


def calcRandomAstrometricErrorPerCoord(FWHMeff, SNR, AstromErrCoeff = 0.60):
    """Calculate the random astrometric uncertainty, as a function of
    effective FWHMeff and signal-to-noise ratio SNR
    Returns astrometric uncertainty in the same units as FWHM.
    ** This error corresponds to a single-coordinate error **
    the total astrometric uncertainty (e.g. relevant when matching
    two catalogs) will be sqrt(2) times larger.

    Parameters:
    -----------
         FWHMeff        ...    effective Full Width at Half Maximum of Point Spread Function [mas]
         SNR            ...    signal to noise ratio
         AstromErrCoeff ...    Astrometric error coefficient (see description below)


    Returns:
    --------
         RandomAstrometricErrorPerCoord ... random astrometric uncertainty per coordinate

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

def magErrorFromSNR(snr):
    """
    Convert flux signal to noise ratio to an uncertainty in magnitude.

    Parameters:
    -----------
          snr ... is the signal to noise ratio in flux

    Returns:
    --------
          magerr ... the resulting uncertainty in magnitude

    Requirements:
    --------------
    numpy as np
    """

    # external functions
    log10=np.log10

    # see e.g. www.ucolick.org/~bolte/AY257/s_n.pdf section 3.1
    magerr=2.5*log10(1.0+1.0/snr)
    return magerr
