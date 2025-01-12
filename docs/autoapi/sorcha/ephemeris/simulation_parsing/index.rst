sorcha.ephemeris.simulation_parsing
===================================

.. py:module:: sorcha.ephemeris.simulation_parsing


Classes
-------

.. autoapisummary::

   sorcha.ephemeris.simulation_parsing.Observatory


Functions
---------

.. autoapisummary::

   sorcha.ephemeris.simulation_parsing.mjd_tai_to_epoch
   sorcha.ephemeris.simulation_parsing.parse_orbit_row


Module Contents
---------------

.. py:function:: mjd_tai_to_epoch(mjd_tai)

   Converts a MJD value in TAI to SPICE ephemeris time

   :param mjd_tai: Input mjd
   :type mjd_tai: float

   :rtype: Ephemeris time


.. py:function:: parse_orbit_row(row, epochJD_TDB, ephem, sun_dict, gm_sun, gm_total)

   Parses the input orbit row, converting it to the format expected by
   the ephemeris generation code later on

   :param row: Row of the input dataframe
   :type row: Pandas dataframe row
   :param epochJD_TDB: epoch of the elements, in JD TDB
   :type epochJD_TDB: float
   :param ephem: ASSIST ephemeris object
   :type ephem: Ephem
   :param sun_dict: Dictionary with the position of the Sun at each epoch
   :type sun_dict: dict
   :param gm_sun: Standard gravitational parameter GM for the Sun
   :type gm_sun: float
   :param gm_total: Standard gravitational parameter GM for the Solar System barycenter
   :type gm_total: float

   :returns: State vector (position, velocity)
   :rtype: tuple


.. py:class:: Observatory(args, auxconfigs, oc_file=None)

   Class containing various utility tools related to the calculation of the observatory position


   .. py:attribute:: observatoryPositionCache


   .. py:attribute:: ObservatoryXYZ


   .. py:method:: convert_to_geocentric(obs_location: dict) -> tuple

      Converts the observatory location to geocentric coordinates

      :param obs_location: Dictionary with Longitude and sin/cos of the observatory Latitude
      :type obs_location: dict

      :returns: Geocentric position (x,y,z)
      :rtype: tuple



   .. py:method:: barycentricObservatory(et, obsCode, Rearth=RADIUS_EARTH_KM)

      Computes the barycentric position of the observatory

      :param et: JPL internal ephemeris time
      :type et: float
      :param obsCode: MPC Observatory code
      :type obsCode: str
      :param Rearth: Radius of the Earth
      :type Rearth: float

      :returns: Barycentric position of the observatory (x,y,z)
      :rtype: array (3,)



