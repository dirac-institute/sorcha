sorcha.modules.PPDropObservations
=================================

.. py:module:: sorcha.modules.PPDropObservations


Functions
---------

.. autoapisummary::

   sorcha.modules.PPDropObservations.PPDropObservations


Module Contents
---------------

.. py:function:: PPDropObservations(observations, module_rngs, probability='detection probability')

   Drops rows where the probabilty of detection is less than sample drawn
   from a uniform distribution. Used by PPFadingFunctionFilter.

   :param observations: Dataframe of observations with a column containing the probability of detection.
   :type observations: Pandas dataframe
   :param module_rngs: A collection of random number generators (per module).
   :type module_rngs: PerModuleRNG
   :param probability: Name of column containing detection probability.
   :type probability: string

   :returns: **out** -- New dataframe of 'observations' modified to remove observations that could not be observed.
   :rtype: Pandas dataframe


