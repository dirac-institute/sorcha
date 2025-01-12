sorcha.modules.PPMagnitudeLimit
===============================

.. py:module:: sorcha.modules.PPMagnitudeLimit


Functions
---------

.. autoapisummary::

   sorcha.modules.PPMagnitudeLimit.PPMagnitudeLimit


Module Contents
---------------

.. py:function:: PPMagnitudeLimit(observations, mag_limit)

   Filter that performs a straight cut on apparent PSF magnitude
   based on a defined threshold.

   :param observations: Dataframe of observations. Must have "observedPSFMag" column.
   :type observations: pandas dataframe
   :param mag_limit: Limit for apparent magnitude cut.
   :type mag_limit: float

   :returns: **observations** -- "observations" dataframe modified with apparent PSF mag greater than
             or equal to the limit removed.
   :rtype: pandas dataframe


