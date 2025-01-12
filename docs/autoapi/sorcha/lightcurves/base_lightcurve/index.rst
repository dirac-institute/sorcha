sorcha.lightcurves.base_lightcurve
==================================

.. py:module:: sorcha.lightcurves.base_lightcurve


Attributes
----------

.. autoapisummary::

   sorcha.lightcurves.base_lightcurve.logger


Classes
-------

.. autoapisummary::

   sorcha.lightcurves.base_lightcurve.AbstractLightCurve


Module Contents
---------------

.. py:data:: logger

.. py:class:: AbstractLightCurve(required_column_names: List[str] = [])

   Bases: :py:obj:`abc.ABC`


   Abstract base class for lightcurve models


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

      :param exception: The exception with a string to appended to the error log
      :type exception: Exception



   .. py:method:: _log_error_message(error_msg: str) -> None

      Log a specific error string to the error log file

      :param error_msg: The string to be appended to the error log
      :type error_msg: string



   .. py:method:: name_id() -> str
      :staticmethod:

      :abstractmethod:


      This method will return the unique name of the LightCurve Model



