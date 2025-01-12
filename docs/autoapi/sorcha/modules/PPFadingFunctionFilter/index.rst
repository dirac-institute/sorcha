sorcha.modules.PPFadingFunctionFilter
=====================================

.. py:module:: sorcha.modules.PPFadingFunctionFilter


Functions
---------

.. autoapisummary::

   sorcha.modules.PPFadingFunctionFilter.PPFadingFunctionFilter


Module Contents
---------------

.. py:function:: PPFadingFunctionFilter(observations, fillfactor, width, module_rngs, verbose=False)

   Wrapper function for PPDetectionProbability and PPDropObservations.

   Calculates detection probability based on a fading function, then drops rows where the
   probabilty of detection is less than sample drawn from a uniform distribution.

   :param observations: Dataframe of observations with a column containing the probability of detection.
   :type observations: Pandas dataframe
   :param fillFactor: Fraction of camera field-of-view covered by detectors
   :type fillFactor: float
   :param module_rngs: A collection of random number generators (per module).
   :type module_rngs: PerModuleRNG
   :param verbose: Verbose logging flag. Default = False
   :type verbose: boolean, optional

   :returns: **observations_drop** -- Modified 'observations' dataframe without observations that could not be observed.
   :rtype: Pandas dataframe)


