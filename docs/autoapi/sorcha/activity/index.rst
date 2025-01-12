sorcha.activity
===============

.. py:module:: sorcha.activity


Submodules
----------

.. toctree::
   :maxdepth: 1

   /autoapi/sorcha/activity/activity_registration/index
   /autoapi/sorcha/activity/base_activity/index
   /autoapi/sorcha/activity/identity_activity/index


Attributes
----------

.. autoapisummary::

   sorcha.activity.CA_METHODS


Classes
-------

.. autoapisummary::

   sorcha.activity.AbstractCometaryActivity
   sorcha.activity.IdentityCometaryActivity


Functions
---------

.. autoapisummary::

   sorcha.activity.register_activity_subclasses
   sorcha.activity.update_activity_subclasses


Package Contents
----------------

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



.. py:function:: register_activity_subclasses() -> Dict[str, Callable]

   This method will identify all of the subclasses of ``AbstractCometaryActivity``
   and build a dictionary that maps ``name : subclass``.

   :returns: A dictionary of all of subclasses of ``AbstractCometaryActivity``. Where
             the string returned from ``subclass.name_id()`` is the key, and the
             subclass is the value.
   :rtype: dict

   :raises ValueError: If a duplicate key is found, a ``ValueError`` is raised. This would
       likely occur if a user copy/pasted an existing subclass but failed to
       update the string returned from ``name_id()``.


.. py:function:: update_activity_subclasses() -> None

   This function is used to register newly created subclasses of the
   `AbstractCometaryActivity`.


.. py:data:: CA_METHODS

