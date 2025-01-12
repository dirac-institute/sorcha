sorcha.modules.PPDetectionProbability
=====================================

.. py:module:: sorcha.modules.PPDetectionProbability


Functions
---------

.. autoapisummary::

   sorcha.modules.PPDetectionProbability.calcDetectionProbability
   sorcha.modules.PPDetectionProbability.PPDetectionProbability


Module Contents
---------------

.. py:function:: calcDetectionProbability(mag, limmag, fillFactor=1.0, w=0.1)

   Find the probability of a detection given a visual magnitude,
   limiting magnitude, and fill factor, determined by the fading function
   from Veres & Chesley (2017).

   :param mag: Magnitude of object in filter used for that field.
   :type mag: float or array of floats
   :param limmag: Limiting magnitude of the field.
   :type limmag: float or array of floats
   :param fillFactor: Fraction of FOV covered by the camera sensor. Default = 1.0
   :type fillFactor: float), optional
   :param w: Distribution parameter. Default = 0.1
   :type w: float

   :returns: **P** -- Probability of detection.
   :rtype: float or array of floats


.. py:function:: PPDetectionProbability(eph_df, trailing_losses=False, trailing_loss_name='dmagDetect', magnitude_name='PSFMag', limiting_magnitude_name='fiveSigmaDepth_mag', field_id_name='FieldID', fillFactor=1.0, w=0.1)

   Find probability of observations being observable for objectInField output.
   Wrapper for calcDetectionProbability which takes into account column names
   and trailing losses. Used by PPFadingFunctionFilter.

   :param eph_df: Dataframe of observations.
   :type eph_df: Pandas dataframe
   :param trailing_losses: Are trailing losses being applied?, Default = False
   :type trailing_losses: Boolean, optional
   :param trailing_loss_name: eph_df column name for trailing losses, Default = dmagDetect
   :type trailing_loss_name: string, optional
   :param magnitude_name: eph_df column name for observation limiting magnitude
                          Default = PSFMag
   :type magnitude_name: string, optional
   :param limiting_magnitude_name: eph_df column used for observation limiting magnitude.
                                   Default = fiveSigmaDepth_mag
   :type limiting_magnitude_name: string, optional
   :param field ID: eph_df column name for observation field_id
                    Default = FieldID
   :type field ID: string, optional
   :param fillFactor: Fraction of FOV covered by the camera sensor. Default = 1.0
   :type fillFactor: float, optional
   :param w: Distribution parameter. Default =0.1
   :type w: float

   :returns: Probability of detection.
   :rtype: float or array of floats


