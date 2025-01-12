sorcha.modules.PPAddUncertainties
=================================

.. py:module:: sorcha.modules.PPAddUncertainties


Functions
---------

.. autoapisummary::

   sorcha.modules.PPAddUncertainties.degCos
   sorcha.modules.PPAddUncertainties.degSin
   sorcha.modules.PPAddUncertainties.addUncertainties
   sorcha.modules.PPAddUncertainties.uncertainties
   sorcha.modules.PPAddUncertainties.calcAstrometricUncertainty
   sorcha.modules.PPAddUncertainties.calcRandomAstrometricErrorPerCoord
   sorcha.modules.PPAddUncertainties.calcPhotometricUncertainty


Module Contents
---------------

.. py:function:: degCos(x)

   Calculate cosine of an angle in degrees.

   :param x: angle in degrees.
   :type x: float

   :returns: The cosine of x.
   :rtype: float


.. py:function:: degSin(x)

   Calculate sine of an angle in degrees.

   :param x: angle in degrees.
   :type x: float

   :returns: The sine of x.
   :rtype: float


.. py:function:: addUncertainties(detDF, sconfigs, module_rngs, verbose=True)

   Generates astrometric and photometric uncertainties, and SNR. Uses uncertainties
   to randomize the photometry. Accounts for trailing losses.

   Adds the following columns to the observations dataframe:

   - astrometricSigma_deg
   - trailedSourceMagSigma
   - PSFMagSigma
   - SNR
   - trailedSourceMag
   - PSFMag

   :param detDF: Dataframe of observations.
   :type detDF: Pandas dataframe)
   :param sconfigs: Dataclass of configuration file arguments.
   :type sconfigs: dataclass
   :param module_rngs: A collection of random number generators (per module).
   :type module_rngs: PerModuleRNG
   :param verbose:
   :type verbose: Boolean, optional
   :param Verbose Logging Flag. Default = True:

   :returns: **detDF** -- dataframe of observations, with new columns for observed
             magnitudes, SNR, and astrometric/photometric uncertainties.
   :rtype: Pandas dataframe


.. py:function:: uncertainties(detDF, sconfigs, limMagName='fiveSigmaDepth_mag', seeingName='seeingFwhmGeom_arcsec', filterMagName='trailedSourceMagTrue', dra_name='RARateCosDec_deg_day', ddec_name='DecRate_deg_day', dec_name='Dec_deg', visit_time_name='visitExposureTime')

   Add astrometric and photometric uncertainties to observations.

   :param detDF: dataframe containing observations.
   :type detDF: Pandas dataframe
   :param sconfigs: Dataclass of configuration file arguments.
   :type sconfigs: dataclass
   :param limMagName: pandas dataframe column name of the limiting magnitude.
                      Default = "fiveSigmaDepth_mag"
   :type limMagName: string, optional
   :param seeingName: pandas dataframe column name of the seeing
                      Default = "seeingFwhmGeom_arcsec"
   :type seeingName: string, optional
   :param filterMagName: pandas dataframe column name of the object magnitude
                         Default = "trailedSourceMagTrue"
   :type filterMagName: string, optional
   :param dra_name: pandas dataframe column name of the object RA rate
                    Default = "RARateCosDec_deg_day"
   :type dra_name: string, optional
   :param ddec_name: pandas dataframe column name of the object declination rate
                     Default = "DecRate_deg_day"
   :type ddec_name: string, optional
   :param dec_name: pandas dataframe column name of the object declination
                    Default = "Dec_deg"
   :type dec_name: string, optional
   :param visit_time_name: pandas dataframe column name for exposure length
                           Default = "visitExposureTime"
   :type visit_time_name: string, optional

   :returns: * **astrSigDeg** (*numpy array*) -- astrometric uncertainties in degrees.
             * **photometric_sigma** (*numpy array*) -- photometric uncertainties in magnitude.
             * **SNR** (*numpy array*) -- signal-to-noise ratio.


.. py:function:: calcAstrometricUncertainty(mag, m5, nvisit=1, FWHMeff=700.0, error_sys=10.0, astErrCoeff=0.6, output_units='mas')

   Calculate the astrometric uncertainty, for object catalog purposes.


   :param mag: magnitude of the observation.
   :type mag: float or array of floats)
   :param m5: 5-sigma limiting magnitude.
   :type m5: float or array of floats
   :param nvisit: number of visits to consider.
                  Default = 1
   :type nvisit: int, optional
   :param FWHMeff: effective Full Width at Half Maximum of Point Spread Function [mas].
                   Default = 700.0
   :type FWHMeff: float, optional
   :param error_sys: systematic error [mas].
                     Default = 10.0
   :type error_sys: float, optional
   :param astErrCoeff: Astrometric error coefficient
                       (see calcRandomAstrometricErrorPerCoord description).
                       Default = 0.60
   :type astErrCoeff: float, optional
   :param output_units:
                        Default: "mas"  (milliarcseconds)
                         other options: "arcsec" (arcseconds)
   :type output_units: string, optional

   :returns: * **astrom_error** (*float or array of floats)*) -- astrometric error.
             * **SNR** (*float or array of floats)*) -- signal to noise ratio.
             * **error_rand** (*float or array of floats*) -- random error.

   .. rubric:: Notes

   The effective FWHMeff MUST BE given in miliarcsec (NOT arcsec!).
   Systematic error, error_sys, must be given in miliarcsec.
   The result corresponds to a single-coordinate uncertainty.
   Note that the total astrometric uncertainty (e.g. relevant when
   matching two catalogs) will be sqrt(2) times larger.
   Default values for parameters are based on estimates for LSST.

   The astrometric error can be applied to parallax or proper motion (for nvisit>1).
   If applying to proper motion, should also divide by the # of years of the survey.
   This is also referenced in the LSST overview paper (arXiv:0805.2366, ls.st/lop)

   - assumes sqrt(Nvisit) scaling, which is the best-case scenario
   - calcRandomAstrometricError assumes maxiumm likelihood solution,
     which is also the best-case scenario
   - the systematic error, error_sys = 10 mas, corresponds to the
     design spec from the LSST Science Requirements Document (ls.st/srd)


.. py:function:: calcRandomAstrometricErrorPerCoord(FWHMeff, SNR, AstromErrCoeff=0.6)

   Calculate the random astrometric uncertainty, as a function of
   effective FWHMeff and signal-to-noise ratio SNR and return
   the astrometric uncertainty in the same units as FWHM.

   This error corresponds to a single-coordinate error
   the total astrometric uncertainty (e.g. relevant when matching
   two catalogs) will be sqrt(2) times larger.

   :param FWHMeff: Effective Full Width at Half Maximum of Point Spread Function [mas].
   :type FWHMeff: float or array of floats
   :param SNR: Signal-to-noise ratio.
   :type SNR: float or array of floats
   :param AstromErrCoeff: Astrometric error coefficient (see description below).
                          Default =0.60
   :type AstromErrCoeff: float, optional

   :returns: * **RandomAstrometricErrorPerCoord** (*float or array of floats*) -- random astrometric uncertainty per coordinate.
             * *Returns astrometric uncertainty in the same units as FWHMeff.*

   .. rubric:: Notes

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


.. py:function:: calcPhotometricUncertainty(snr)

   Convert flux signal to noise ratio to an uncertainty in magnitude.

   :param snr: The signal-to-noise-ratio in flux.
   :type snr: float or array of floats

   :returns: **magerr** -- The resulting uncertainty in magnitude.
   :rtype: float or rray of floats


