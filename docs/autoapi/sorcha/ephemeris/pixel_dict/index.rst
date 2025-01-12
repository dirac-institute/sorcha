sorcha.ephemeris.pixel_dict
===========================

.. py:module:: sorcha.ephemeris.pixel_dict


Classes
-------

.. autoapisummary::

   sorcha.ephemeris.pixel_dict.PixelDict


Functions
---------

.. autoapisummary::

   sorcha.ephemeris.pixel_dict.lagrange3


Module Contents
---------------

.. py:function:: lagrange3(t0, t1, t2, t)

   Calculate the coefficients for
   second-order Lagrange interpolation
   for measured points at times t0, t1,
   and t2 and for an array of times t.

   These coefficients can be reused for
   any number of input vectors.

   :param t0: Time t0
   :type t0: float
   :param t1: Time t1
   :type t1: float
   :param t2: Time t2
   :type t2: float
   :param t: Times for the interpolation
   :type t: 1D array

   :returns: * **L0** (*1D array*) -- interpolation coefficient at t0
             * **L1** (*1D array*) -- interpolation coefficient at t1
             * **L2** (*1D array*) -- interpolation coefficient at t2


.. py:class:: PixelDict(jd_tdb, sim_dict, ephem, obsCode, observatory, picket_interval=1.0, nside=128, nested=True, n_sub_intervals=101)

   Class with methods needed during the ephemerides generation
   Interfaces directly with the ASSIST+Rebound simulation objects as well as healpix


   .. py:attribute:: nside
      :value: 128



   .. py:attribute:: picket_interval
      :value: 1.0



   .. py:attribute:: n_sub_intervals
      :value: 101



   .. py:attribute:: obsCode


   .. py:attribute:: nested
      :value: True



   .. py:attribute:: sim_dict


   .. py:attribute:: ephem


   .. py:attribute:: observatory


   .. py:attribute:: t0


   .. py:attribute:: r_obs_0


   .. py:attribute:: tp


   .. py:attribute:: r_obs_p


   .. py:attribute:: tm


   .. py:attribute:: r_obs_m


   .. py:attribute:: pixel_dict


   .. py:attribute:: rho_hat_m_dict


   .. py:attribute:: rho_hat_0_dict


   .. py:attribute:: rho_hat_p_dict


   .. py:method:: get_observatory_position(t)

      Computes the barycentric position of the observatory (in au)

      :param t: Epoch for the position vector
      :type t: float

      :returns: Barycentric position of the observatory (x,y,z)
      :rtype: array (3,)



   .. py:method:: get_object_unit_vectors(desigs, r_obs, t, lt0=0.01)

      Computes the unit vector (in the equatorial sphere) that point towards the object - observatory vector
      for a list of objects, at a given time

      :param desigs: List of designations (consistent with the simulation dictionary)
      :type desigs: list
      :param r_obs: Observatory location
      :type r_obs: array (3 entries)
      :param t: Time of the observation
      :type t: float
      :param lt0: Initial guess (in days) for light-time correction (default: 0.01 days)
      :type lt0: float

      :returns: **rho_hat_dict** -- Dictionary of unit vectors
      :rtype: dict



   .. py:method:: get_all_object_unit_vectors(r_obs, t, lt0=0.01)

      Computes the unit vector (in the equatorial sphere) that point towards the object - observatory vector
      for *all* objects, at a given time

      :param r_obs: Observatory location
      :type r_obs: array (3 entries)
      :param t: Time of the observation
      :type t: float
      :param lt0: Initial guess (in days) for light-time correction (default: 0.01 days)
      :type lt0: float

      :returns: **rho_hat_dict** -- Dictionary of unit vectors
      :rtype: dict



   .. py:method:: get_interp_factors(tm, t0, tp, n_sub_intervals)

      Computes the Lagrange interpolation factors at a set of 3 times for an
      equally spaced grid of points with a chosen number of sub-intervals
      :param tm: First reference time
      :type tm: float
      :param t0: Second reference time
      :type t0: float
      :param tp: Third reference time
      :type tp: float
      :param n_sub_intervals: Number of sub-intervals for the Lagrange interpolation (default: 101)
      :type n_sub_intervals: int

      :returns: * **Lm** (*2D array*) -- Lagrange coefficients at tm
                * **L0** (*2D array*) -- Lagrange coefficients at t0
                * **Lp** (*2D array*) -- Lagrange coefficient at tp



   .. py:method:: interpolate_unit_vectors(desigs, jd_tdb)

      Interpolates the unit vectors for a list of designations towards the new target time

      :param desigs: List of designations (consistent with the simulation dictionary)
      :type desigs: list
      :param jd_tdb: Target time
      :type jd_tdb: float

      :returns: **unit_vector_dict** -- Dictionary of unit vectors
      :rtype: dict



   .. py:method:: compute_pixel_traversed()

      Computes the healpix pixels traversed by all the objects during between times tm and tp



   .. py:method:: update_pickets(jd_tdb)

      Updates the picket interpolation vectors for the new reference time

      :param jd_tdb: Target time
      :type jd_tdb: float



   .. py:method:: get_designations(jd_tdb, ra, dec, ang_fov)

      Get the object designations that are within an angular radius of a topocentric unit vector at a
      given time.

      :param jd_tdb: Target time
      :type jd_tdb: float
      :param ra: right ascension (degrees)
      :type ra: float
      :param dec: declination (degrees)
      :type dec: float
      :param ang_fov: Field of view radius
      :type ang_fov: float

      :returns: **desigs** -- List of designations
      :rtype: list



