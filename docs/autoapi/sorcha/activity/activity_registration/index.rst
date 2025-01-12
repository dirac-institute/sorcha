sorcha.activity.activity_registration
=====================================

.. py:module:: sorcha.activity.activity_registration


Attributes
----------

.. autoapisummary::

   sorcha.activity.activity_registration.CA_METHODS


Functions
---------

.. autoapisummary::

   sorcha.activity.activity_registration.register_activity_subclasses
   sorcha.activity.activity_registration.update_activity_subclasses


Module Contents
---------------

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

