sorcha.modules.PPBrightLimit
============================

.. py:module:: sorcha.modules.PPBrightLimit


Functions
---------

.. autoapisummary::

   sorcha.modules.PPBrightLimit.PPBrightLimit


Module Contents
---------------

.. py:function:: PPBrightLimit(observations, observing_filters, bright_limit)

   Drops observations brighter than the user-defined saturation
   limit. Can take either a single saturation limit for a straight cut, or
   filter-specific saturation limits.

   :param observations: Dataframe of observations.
   :type observations: Pandas dataframe
   :param observing_filters: Observing filters present in the data.
   :type observing_filters: list of strings
   :param bright_limit: Saturation limits: either single value applied to all filters or a list of values for each filter.
   :type bright_limit: float or list of floats

   :returns: **observations_out** -- observations dataframe modified with rows dropped for apparent
             magnitudes brigher than the bright_limit for the given observation's
             filter
   :rtype: Pandas dataframe


