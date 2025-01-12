sorcha.modules.PPDetectionEfficiency
====================================

.. py:module:: sorcha.modules.PPDetectionEfficiency


Functions
---------

.. autoapisummary::

   sorcha.modules.PPDetectionEfficiency.PPDetectionEfficiency


Module Contents
---------------

.. py:function:: PPDetectionEfficiency(padain, threshold, module_rngs)

   Applies a random cut to the observations dataframe based on an efficiency
   threshold: if the threshold is 0.95, for example, 5% of observations will be
   randomly dropped. Used by PPLinkingFilter.

   :param padain: Dataframe of observations.
   :type padain: Pandas dataframe
   :param threshold: Fraction between 0 and 1 of detections retained in the dataframe.
   :type threshold: float
   :param module_rngs: A collection of random number generators (per module).
   :type module_rngs: PerModuleRNG

   :returns: Dataframe of observations with a fraction equal to 1-threshold randomly dropped.
   :rtype: Pandas dataframe


