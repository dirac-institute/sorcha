sorcha.ephemeris.simulation_geometry
====================================

.. py:module:: sorcha.ephemeris.simulation_geometry


Functions
---------

.. autoapisummary::

   sorcha.ephemeris.simulation_geometry.ecliptic_to_equatorial
   sorcha.ephemeris.simulation_geometry.integrate_light_time
   sorcha.ephemeris.simulation_geometry.get_hp_neighbors
   sorcha.ephemeris.simulation_geometry.ra_dec2vec
   sorcha.ephemeris.simulation_geometry.vec2ra_dec
   sorcha.ephemeris.simulation_geometry.barycentricObservatoryRates


Module Contents
---------------

.. py:function:: ecliptic_to_equatorial(v, rot_mat=ECL_TO_EQ_ROTATION_MATRIX)

   Converts an ecliptic-aligned vector to an equatorially-aligned vector

   :param v: vector
   :type v: array (3 entries)
   :param rot_mat: Rotation matrix. Default is the matrix that computes the ecliptic to equatorial conversion
   :type rot_mat: 2D array (3x3 matrix)

   :returns: **v** -- Rotated vector
   :rtype: array (3 entries)


.. py:function:: integrate_light_time(sim, ex, t, r_obs, lt0=0, iter=3, speed_of_light=SPEED_OF_LIGHT)

   Performs the light travel time correction between object and observatory iteratively for the object at a given reference time

   :param sim: Rebound simulation object
   :type sim: simulation
   :param ex: ASSIST simulation extras
   :type ex: simulation extras
   :param t: Target time
   :type t: float
   :param r_obs: Observatory position at time t
   :type r_obs: array (3 entries)
   :param lt0: First guess for light travel time
   :type lt0: float
   :param iter: Number of iterations
   :type iter: int
   :param speed_of_light: Speed of light for the calculation (default is SPEED_OF_LIGHT constant)
   :type speed_of_light: float

   :returns: * **rho** (*array*) -- Object-observatory vector
             * **rho_mag** (*float*) -- Magnitude of rho vector
             * **lt** (*float*) -- Light travel time
             * **target** (*array*) -- Object position vector at t-lt
             * **vtarget** (*array*) -- Object velocity at t-lt


.. py:function:: get_hp_neighbors(ra_c, dec_c, search_radius, nside=32, nested=True)

   Queries the healpix grid for pixels near the given RA/Dec with a given search radius

   :param ra_c: Target RA
   :type ra_c: float
   :param dec_c: Target dec
   :type dec_c: float
   :param search_radius: Radius for the query
   :type search_radius: float
   :param nside: healpix nside
   :type nside: int
   :param nested: Defines the ordering scheme for the healpix ordering. True (default) means a NESTED ordering
   :type nested: boolean

   :returns: **res** -- List of healpix pixels
   :rtype: list


.. py:function:: ra_dec2vec(ra, dec)

   Converts a RA/Dec pair to a unit vector on the sphere
   :param ra: Target RA
   :type ra: float
   :param dec: Target dec
   :type dec: float

   :returns: Unit vector
   :rtype: array


.. py:function:: vec2ra_dec(vec)

   Decomposes a unit vector on the sphere into a RA/Dec pair
   :param vec: Unit vector
   :type vec: array

   :returns: * **ra** (*float*) -- Target RA
             * **dec** (*float*) -- Target dec


.. py:function:: barycentricObservatoryRates(et, obsCode, observatories, Rearth=RADIUS_EARTH_KM, delta_et=10)

   Computes the position and rate of motion for the observatory in barycentric coordinates

   :param et: JPL ephemeris time
   :type et: float
   :param obsCode: MPC observatory code
   :type obsCode: str
   :param observatories: Observatory object with spherical representations for the obsCode
   :type observatories: Observatory
   :param Rearth: Radius of the Earth (default is RADIUS_EARTH_KM)
   :type Rearth: float
   :param delta_et: Difference in ephemeris time (in days) to derive the rotation matrix from the fixed Earth equatorial frame to J2000 (default: 10)
   :type delta_et: float

   :returns: * *array* -- Position of the observatory (baricentric)
             * *array* -- Velocity of the observatory (baricentric)


