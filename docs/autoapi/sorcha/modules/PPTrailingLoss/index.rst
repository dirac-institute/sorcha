sorcha.modules.PPTrailingLoss
=============================

.. py:module:: sorcha.modules.PPTrailingLoss


Functions
---------

.. autoapisummary::

   sorcha.modules.PPTrailingLoss.calcTrailingLoss
   sorcha.modules.PPTrailingLoss.PPTrailingLoss


Module Contents
---------------

.. py:function:: calcTrailingLoss(dRaCosDec, dDec, seeing, texp=30.0, model='circularPSF', a_trail=0.761, b_trail=1.162, a_det=0.42, b_det=0.003)

   Find the trailing loss from trailing and detection (Veres & Chesley 2017)

   :param dRa: on sky velocity component in RA*Cos(Dec). [Units: deg/day]
   :type dRa: float or array of floats
   :param dDec: on sky velocity component in Dec. [Units: deg/day]
   :type dDec: float/array of floats
   :param seeing: FWHM of the seeing disk. [Units: arcseconds]
   :type seeing: float or array of floats
   :param texp: Exposure length. [Units: seconds] Default = 30
   :type texp: float or array of floats, optional
   :param model: Options: 'circularPSF' or trailedSource'
                 'circularPSF': Trailing loss due to the DM detection algorithm. Limit SNR:
                 5 sigma in a PSF-convolved image with a circular PSF (no trail fitting). Peak
                 fluxes will be lower due to motion of the object.
                 'trailedSource': Unavoidable trailing loss due to spreading the PSF
                 over more pixels lowering the SNR in each pixel.
                 See https://github.com/rhiannonlynne/318-proceedings/blob/master/Trailing%20Losses.ipynb for details.
                 Default = "circularPSF"
   :type model: string, optional
   :param a_trail: a fit parameters for trailedSource model. Default parameters from Veres & Chesley (2017).
                   Default = 0.761
   :type a_trail: float, optional
   :param b_trail: b fit parameters for trailedSource model. Default parameters from Veres & Chesley (2017).
                   Default = 1.162
   :type b_trail: float, optional
   :param a_det: a fit parameters for circularPSF model. Default parameters from Veres & Chesley (2017).
                 Default = 0.420
   :type a_det: float, optional
   :param b_det: b fit parameters for circularPSF model. Default parameters from Veres & Chesley (2017).
                 Default = 0.003
   :type b_det: float, optional

   :returns: **dmag** -- Loss in detection magnitude due to trailing.
   :rtype: float or array of floats


.. py:function:: PPTrailingLoss(eph_df, model='circularPSF', dra_cosdec_name='RARateCosDec_deg_day', ddec_name='DecRate_deg_day', dec_name='Dec_deg', seeing_name_survey='seeingFwhmEff_arcsec', visit_time_name='visitExposureTime')

   Calculates detection trailing losses. Wrapper for calcTrailingLoss.

   :param eph_df: Dataframe of observations for which to calculate trailing losses.
   :type eph_df: pandas dataframe
   :param model: Photometric model. Either 'circularPSF' or 'trailedSource': see docstring for
                 calcTrailingLoss for details. Default = "circularPSF"
   :type model: string, optional
   :param dra_name: "eph_df" column name for object RA rate. Default = "RARateCosDec_deg_day"
                    Assumes cos(dec) normalization has already been applied
   :type dra_name: string, optional
   :param ddec_name: "eph_df" column name for object dec rate. Default = "DecRate_deg_day"
   :type ddec_name: string, optional
   :param dec_name: "eph_df" column name for object declination. Default = "Dec_deg"
   :type dec_name: string, default
   :param seeing_name_survey: "eph_df" column name for seeing. Default = "seeingFwhmEff_arcsec"
   :type seeing_name_survey: string, optional
   :param visit_time_name: "eph_df" column name for exposure length. Default = "visitExposureTime"
   :type visit_time_name: string, optional

   :returns: **dmag** -- Loss in detection magnitude due to trailing losses.
   :rtype: float or array of floats

   .. rubric:: Notes

   Assumes 'eph_df" has RA and Dec stored in deg/dayrates and the seeing in arcseconds


