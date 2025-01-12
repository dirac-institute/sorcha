sorcha.modules.PPLinkingFilter
==============================

.. py:module:: sorcha.modules.PPLinkingFilter


Functions
---------

.. autoapisummary::

   sorcha.modules.PPLinkingFilter.PPLinkingFilter


Module Contents
---------------

.. py:function:: PPLinkingFilter(observations, detection_efficiency, min_observations, min_tracklets, tracklet_interval, minimum_separation, maximum_time, night_start_utc, survey_name='rubin_sim', drop_unlinked=True)

   A function which mimics the effects of the SSP linking process by looking
   for valid tracklets within valid tracks and only outputting observations
   which would be thus successfully "linked" by SSP.

   Parameters:
   -----------
   detection_efficiency (float): the fractional percentage of successfully linked
   detections.

   min_observations (int): the minimum number of observations in a night required
   to form a tracklet.

   min_tracklets (int): the minimum number of tracklets required to form a valid track.

   tracklet_interval (int): the time window (in days) in which the minimum number of
   tracklets must occur to form a valid track.

   minimum_separation (float): the minimum separation inside a tracklet for it
   to be recognised as motion between images (in arcseconds).

   maximum_time (float): # Maximum time separation (in days) between subsequent observations in a tracklet.

   rng (numpy Generator object): numpy random number generator object.

   survey_name (str): a string with the survey name. used for time-zone purposes.
   Currently only accepts "rubin_sim", "RUBIN_SIM", "lsst", "LSST".

   drop_unlinked (boolean): rejects all observations that are considered to not be linked. Default is True

   Returns:
   -----------
   observations_out (pandas dataframe): a pandas dataframe containing observations
   of linked objects only.



