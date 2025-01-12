sorcha.ephemeris.simulation_constants
=====================================

.. py:module:: sorcha.ephemeris.simulation_constants


Attributes
----------

.. autoapisummary::

   sorcha.ephemeris.simulation_constants.RADIUS_EARTH_KM
   sorcha.ephemeris.simulation_constants.AU_M
   sorcha.ephemeris.simulation_constants.AU_KM
   sorcha.ephemeris.simulation_constants.SPEED_OF_LIGHT
   sorcha.ephemeris.simulation_constants.OBLIQUITY_ECLIPTIC
   sorcha.ephemeris.simulation_constants.ECL_TO_EQ_ROTATION_MATRIX


Functions
---------

.. autoapisummary::

   sorcha.ephemeris.simulation_constants.create_ecl_to_eq_rotation_matrix


Module Contents
---------------

.. py:data:: RADIUS_EARTH_KM
   :value: 6378.137


.. py:data:: AU_M
   :value: 149597870700


.. py:data:: AU_KM
   :value: 149597870.7


.. py:data:: SPEED_OF_LIGHT
   :value: 173.1446326742403


.. py:data:: OBLIQUITY_ECLIPTIC

.. py:function:: create_ecl_to_eq_rotation_matrix(ecl)

   Creates a rotation matrix for transforming ecliptical coordinates
   to equatorial coordinates. A rotation matrix based on the solar
   system's ecliptic obliquity is already provided as
   `ECL_TO_EQ_ROTATION_MATRIX`.

   :param ecl: The ecliptical obliquity.
   :type ecl: float

   :returns: **rotmat** -- rotation matrix for transofmring ecliptical coordinates to equatorial coordinates.
             Array has shape (3,3).
   :rtype: numpy array/matrix of floats


.. py:data:: ECL_TO_EQ_ROTATION_MATRIX

