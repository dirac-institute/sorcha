sorcha.lightcurves
==================

.. py:module:: sorcha.lightcurves


Submodules
----------

.. toctree::
   :maxdepth: 1

   /autoapi/sorcha/lightcurves/base_lightcurve/index
   /autoapi/sorcha/lightcurves/identity_lightcurve/index
   /autoapi/sorcha/lightcurves/lightcurve_registration/index


Attributes
----------

.. autoapisummary::

   sorcha.lightcurves.LC_METHODS


Classes
-------

.. autoapisummary::

   sorcha.lightcurves.AbstractLightCurve
   sorcha.lightcurves.IdentityLightCurve


Functions
---------

.. autoapisummary::

   sorcha.lightcurves.register_lc_subclasses
   sorcha.lightcurves.update_lc_subclasses


Package Contents
----------------

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



.. py:function:: register_lc_subclasses() -> Dict[str, Callable]

   This method will identify all of the subclasses of ``AbstractLightCurve``
   and build a dictionary that maps ``name : subclass``.

   :returns: A dictionary of all of subclasses of ``AbstractLightCurve``. Where
             the string returned from ``subclass.name_id()`` is the key, and the
             subclass is the value.
   :rtype: dict

   :raises ValueError: If a duplicate key is found, a ``ValueError`` is raised. This would
       likely occur if a user copy/pasted an existing subclass but failed to
       update the string returned from ``name_id()``.


.. py:function:: update_lc_subclasses() -> None

   This function is used to register newly created subclasses of the
   `AbstractLightCurve`.


.. py:data:: LC_METHODS

