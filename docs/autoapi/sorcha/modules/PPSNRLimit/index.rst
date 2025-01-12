sorcha.modules.PPSNRLimit
=========================

.. py:module:: sorcha.modules.PPSNRLimit


Functions
---------

.. autoapisummary::

   sorcha.modules.PPSNRLimit.PPSNRLimit


Module Contents
---------------

.. py:function:: PPSNRLimit(observations, sigma_limit=2.0)

   Filter that performs a straight SNR cut based on a limit, removing
   observations that are less than a SNR limit

   :param observations: Dataframe of observations. Must have "SNR" column.
   :type observations: pandas dataframe
   :param sigma_limit: Limit for SNR cut.
   :type sigma_limit: float, optional.

   :returns: **observations** -- "observations" dataframed modified with entries with SNR < the limit removed.
   :rtype: pandas dataframe


