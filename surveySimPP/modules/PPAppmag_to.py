import numpy as np
from sbpy.data import Obs
from sbpy.photometry import HG12,HG,HG1G2
from astropy.modeling.fitting import LevMarLSQFitter
fitter = LevMarLSQFitter()



def appMagFitterHG12(mag_list,a,weights):
    '''
    Fit visual apparent magnitude values to H-magnitude values using the HG12 system and LevMarLSQFitter

    Parameters
    ----------
    mag_list: array
            visual color corrected (all the same band color/filter) apparent magnitudes to be fitted
    a: array
            corresponding phase angles to the apparent magnitude observations in radians
    weights: array
            weights to be used in the fitting process, used (magSigma)^-2 before, can be optional

    Returns
    -------
    numpy array of values returned by the fit, Values listed in order,

    var.H.value: float
            The fitted H-magnitude value
    var.G12.value: float
            The G12 parameter from the fit
    H_err: float
            Error in fitting the H value
    G12_err: float
            Error in fitting the G12 value
    H_G12_cov: float
            Covariance of the HG12 fit
    '''
    obs = Obs.from_dict({'alpha':a,'mag':mag_list,'weights':weights})
    var = HG12.from_obs(obs,fitter,'mag')
    fi=fitter.fit_info
    param_cov = fi['param_cov']
    #fvec = fi['fvec']
    H_err = np.sqrt(param_cov[0][0])
    G12_err = np.sqrt(param_cov[1][1])
    H_G12_cov = param_cov[0][1]
    return np.array([var.H.value,var.G12.value,H_err,G12_err,H_G12_cov])

def appMagFitterHG(mag_list,a,weights):
    '''
    Fit visual apparent magnitude values to H-magnitude values using the HG system and LevMarLSQFitter

    Parameters
    ----------
    mag_list: array
            visual color corrected (all the same band color/filter) apparent magnitudes to be fitted
    a: array
            corresponding phase angles to the apparent magnitude observations in radians
    weights: array
            weights to be used in the fitting process, used (magSigma)^-2 before, can be optional

    Returns
    -------
    numpy array of values returned by the fit, Values listed in order,

    var.H.value: float
            The fitted H-magnitude value
    var.G.value: float
            The G parameter from the fit
    H_err: float
            Error in fitting the H value
    G_err: float
            Error in fitting the G value
    H_G_cov: float
            Covariance of the HG fit
    '''
    obs = Obs.from_dict({'alpha':a,'mag':mag_list,'weights':weights})
    var = HG.from_obs(obs,fitter,'mag')
    fi=fitter.fit_info
    param_cov = fi['param_cov']
    #fvec = fi['fvec']
    H_err = np.sqrt(param_cov[0][0])
    G_err = np.sqrt(param_cov[1][1])
    H_G_cov = param_cov[0][1]
    return np.array([var.H.value,var.G.value,H_err,G_err,H_G_cov])

def appMagFitterHG1G2(mag_list,a,weights):
    '''
    Fit visual apparent magnitude values to H-magnitude values using the HG1G2 system and LevMarLSQFitter

    Parameters
    ----------
    mag_list: array
            visual color corrected (all the same band color/filter) apparent magnitudes to be fitted
    a: array
            corresponding phase angles to the apparent magnitude observations in radians
    weights: array
            weights to be used in the fitting process, used (magSigma)^-2 before, can be optional

    Returns
    -------
    numpy array of values returned by the fit, Values listed in order,

    var.H.value: float
            The fitted H-magnitude value
    var.G1.value: float
            The G1 parameter from the fit
    var.G2.value: float
            The G2 parameter from the fit
    H_err: float
            Error in fitting the H value
    G1_err: float
            Error in fitting the G1 value
    G2_err: float
            Error in fitting the G2 value
    H_G1G2_cov: float
            Covariance of the HG1G2 fit
    '''
    obs = Obs.from_dict({'alpha':a,'mag':mag_list,'weights':weights})
    var = HG1G2.from_obs(obs,fitter,'mag')
    fi=fitter.fit_info
    param_cov = fi['param_cov']
    #fvec = fi['fvec']
    H_err = np.sqrt(param_cov[0][0])
    G1_err = np.sqrt(param_cov[1][1])
    G2_err = np.sqrt(param_cov[2][2])
    H_G1G2_cov = param_cov[0][2] # assuming this is the correct index for the covariance
    return np.array([var.H.value,var.G1.value,var.G2.value,H_err,G1_err,G2_err,H_G1G2_cov])
