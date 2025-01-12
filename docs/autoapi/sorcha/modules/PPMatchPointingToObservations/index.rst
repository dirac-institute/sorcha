sorcha.modules.PPMatchPointingToObservations
============================================

.. py:module:: sorcha.modules.PPMatchPointingToObservations


Functions
---------

.. autoapisummary::

   sorcha.modules.PPMatchPointingToObservations.PPMatchPointingToObservations


Module Contents
---------------

.. py:function:: PPMatchPointingToObservations(padain, pointfildb)

   Merges all relevant columns of each observation from the pointing
   database onto the observations dataframe, then drops all observations which are not
   in one of the requested filters and any duplicate columns.

   Adds the following columns to the dataframe of observations:

       - visitTime
       - visitExposureTime
       - optFilter
       - seeingFwhmGeom_arcsec
       - seeingFwhmEff_arcsec
       - fieldFiveSigmaDepth_mag
       - fieldRA_deg
       - fieldDec_deg
       - fieldRotSkyPos_deg
       - observationMidpointMJD_TAI

   :param padain: Dataframe of observations.
   :type padain: pandas dataframe
   :param pointfildb: Dataframe of the pointing database.
   :type pointfildb: pandas dataframe

   :returns: **res_df** -- Merged dataframe of observations ("padain") with pointing
             database ("pointfildb"), with all superfluous observations dropped.
   :rtype: Pandas dataframe


