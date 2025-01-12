sorcha.modules.PPVignetting
===========================

.. py:module:: sorcha.modules.PPVignetting


Attributes
----------

.. autoapisummary::

   sorcha.modules.PPVignetting.deg2rad
   sorcha.modules.PPVignetting.rad2deg
   sorcha.modules.PPVignetting.sin
   sorcha.modules.PPVignetting.cos


Functions
---------

.. autoapisummary::

   sorcha.modules.PPVignetting.vignettingEffects
   sorcha.modules.PPVignetting.calcVignettingLosses
   sorcha.modules.PPVignetting.haversine
   sorcha.modules.PPVignetting.vignetFunc


Module Contents
---------------

.. py:data:: deg2rad

.. py:data:: rad2deg

.. py:data:: sin

.. py:data:: cos

.. py:function:: vignettingEffects(df, raName='RA_deg', decName='Dec_deg', fieldName='FieldID', raNameSurvey='fieldRA_deg', decNameSurvey='fieldDec_deg')

   Calculates effective limiting magnitude at source, taking vignetting into account.
   Wrapper for calcVignettingLosses().

   :param df: dataframe of observations.
   :type df: pandas dataframe
   :param raName: 'df' column name of object RA. Default = "RA_deg"
   :type raName: string, optional
   :param decName: 'df' column name of object declination. Default = "Dec_deg"
   :type decName: string, optional
   :param fieldName: 'df' column name for observation pointing field ID. Default = "FieldID"
   :type fieldName: string, optional
   :param raNameSurvey:     'df' column name for observation pointing RA. Default = "fieldRA_deg"

                        decNameSurvey : string, optional
                            'df' column name for observation pointing declination. Default = "fieldDec_deg"
   :type raNameSurvey: string, optional

   :returns: Five sigma limiting magnitude at object location adjusted for vignetting for each
             row in 'df' dataframe.
   :rtype: list of floats


.. py:function:: calcVignettingLosses(ra, dec, fieldra, fielddec)

   Calculates magnitude loss due to vignetting for a point with the telescope
   centered on fieldra, fielddec.

   :param ra: RA of object(s).
   :type ra: float or aarray of floats
   :param dec: Dec of object(s).
   :type dec: float or array of floats
   :param fieldra: RA of field(s).
   :type fieldra: float or array of floats
   :param fielddec: Dec of field(s).
   :type fielddec: float or array of floats

   :returns: Magnitude loss due to vignetting at object position.
   :rtype: floats or array of floats


.. py:function:: haversine(ra1, dec1, ra2, dec2)

   Calculates angular distance between two points. Can produce floating point
   errors for antipodal points, which are not intended to be encountered within
   the scope of this module.

   :param ra1: RA of first point.
   :type ra1: float or array of floats
   :param dec1  or float or array of floats: Dec of first point.
   :param ra2: RA of second point.
   :type ra2: float or array of floats
   :param dec2: Dec of second point.
   :type dec2: float/array of floats

   :returns: Angular distance between two points.
   :rtype: float or array of floats


.. py:function:: vignetFunc(x)

   Returns the magnitude of dimming caused by the vignetting relative to the
   center of the field.

   :param x: Angular separation of point from field centre.
   :type x: float or array of floats

   :returns: Magnitude of dimming due to vignetting at object position.
   :rtype: float or array of floats

   .. rubric:: Notes

   Grabbed from sims_selfcal. From VignettingFunc_v3.3.TXT. r is in degrees,
   frac is fraction of rays which were not vignetted.


