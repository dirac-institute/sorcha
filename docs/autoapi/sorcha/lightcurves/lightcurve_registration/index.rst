sorcha.lightcurves.lightcurve_registration
==========================================

.. py:module:: sorcha.lightcurves.lightcurve_registration


Attributes
----------

.. autoapisummary::

   sorcha.lightcurves.lightcurve_registration.LC_METHODS


Functions
---------

.. autoapisummary::

   sorcha.lightcurves.lightcurve_registration.register_lc_subclasses
   sorcha.lightcurves.lightcurve_registration.update_lc_subclasses


Module Contents
---------------

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

