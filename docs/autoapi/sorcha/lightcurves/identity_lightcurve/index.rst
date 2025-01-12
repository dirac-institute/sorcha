sorcha.lightcurves.identity_lightcurve
======================================

.. py:module:: sorcha.lightcurves.identity_lightcurve


Classes
-------

.. autoapisummary::

   sorcha.lightcurves.identity_lightcurve.IdentityLightCurve


Module Contents
---------------

.. py:class:: IdentityLightCurve(required_column_names: List[str] = ['fieldMJD_TAI'])

   Bases: :py:obj:`sorcha.lightcurves.base_lightcurve.AbstractLightCurve`


   !!! THIS SHOULD NEVER BE USED - FOR TESTING ONLY !!!

   Rudimentary lightcurve model that returns no shift. This class is explicitly
   created for testing purposes.


   .. py:method:: compute(df: pandas.DataFrame) -> numpy.array

      Returns numpy array of 0's with shape equal to the input dataframe
      time column.

      :param df: The ``observations`` dataframe provided by ``Sorcha``.
      :type df: Pandas dataframe

      :returns: Numpy array of 0's with shape equal to the input dataframe time column.
      :rtype: np.array



   .. py:method:: name_id() -> str
      :staticmethod:


      Returns the string identifier for this light curve method. It must be
      unique within all the subclasses of ``AbstractLightCurve``.

      We have chosen the name "identity" here because the input brightness will
      equal the output brightness if this model is applied.

      :returns: Unique identifier for this light curve calculator
      :rtype: string



