sorcha.activity.base_activity
=============================

.. py:module:: sorcha.activity.base_activity


Attributes
----------

.. autoapisummary::

   sorcha.activity.base_activity.logger


Classes
-------

.. autoapisummary::

   sorcha.activity.base_activity.AbstractCometaryActivity


Module Contents
---------------

.. py:data:: logger

.. py:class:: AbstractCometaryActivity(required_column_names: List[str] = [])

   Bases: :py:obj:`abc.ABC`


   Abstract base class for cometary activity models


   .. py:attribute:: required_column_names
      :value: []



   .. py:method:: compute(df: pandas.DataFrame) -> numpy.array
      :abstractmethod:


      User implemented calculation based on the input provided by the
      pandas dataframe ``df``.

      :param df: The ``observations`` dataframe provided by ``Sorcha``.
      :type df: Pandas dataframe



   .. py:method:: _validate_column_names(df: pandas.DataFrame) -> None

      Private method that checks that the provided pandas dataframe contains
         the required columns defined in ``self.required_column_names``.

      :param df: The ``observations`` dataframe provided by ``Sorcha``.
      :type df: Pandas dataframe



   .. py:method:: _log_exception(exception: Exception) -> None

      Log an error message from an exception to the error log file

      :param exception: The exception with a value string to appended to the error log
      :type exception: Exception



   .. py:method:: _log_error_message(error_msg: str) -> None

      Log a specific error string to the error log file

      :param error_msg: The string to be appended to the error log
      :type error_msg: str



   .. py:method:: name_id() -> str
      :staticmethod:

      :abstractmethod:


      This method will return the unique name of the LightCurve Model



