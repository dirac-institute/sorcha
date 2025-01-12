sorcha.activity.identity_activity
=================================

.. py:module:: sorcha.activity.identity_activity


Classes
-------

.. autoapisummary::

   sorcha.activity.identity_activity.IdentityCometaryActivity


Module Contents
---------------

.. py:class:: IdentityCometaryActivity

   Bases: :py:obj:`sorcha.activity.base_activity.AbstractCometaryActivity`


   !!! THIS SHOULD NEVER BE USED - FOR TESTING ONLY !!!

   Rudimentary cometary activity model that returns no change to the input ``observation``
   dataframe.
   This class is explicitly created for testing purposes.


   .. py:method:: compute(df: pandas.DataFrame) -> pandas.DataFrame

      Returns numpy array of 0's with shape equal to the input dataframe
      time column.

      :param df: The ``observations`` dataframe provided by ``Sorcha``.
      :type df: pd.DataFrame

      :returns: The original ``observations`` dataframe, unchanged.
      :rtype: pd.DataFrame



   .. py:method:: name_id() -> str
      :staticmethod:


      Returns the string identifier for this cometary activity method. It
      must be unique within all the subclasses of ``AbstractCometaryActivity``.

      We have chosen the name "identity" here because the input dataframe is
      returned unchanged.

      :returns: Unique identifier for this cometary activity model
      :rtype: str



