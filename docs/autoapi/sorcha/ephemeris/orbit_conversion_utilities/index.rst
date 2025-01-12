sorcha.ephemeris.orbit_conversion_utilities
===========================================

.. py:module:: sorcha.ephemeris.orbit_conversion_utilities


Classes
-------

.. autoapisummary::

   sorcha.ephemeris.orbit_conversion_utilities.halley_result


Functions
---------

.. autoapisummary::

   sorcha.ephemeris.orbit_conversion_utilities.stumpff
   sorcha.ephemeris.orbit_conversion_utilities.root_function
   sorcha.ephemeris.orbit_conversion_utilities.halley_safe
   sorcha.ephemeris.orbit_conversion_utilities.universal_cartesian
   sorcha.ephemeris.orbit_conversion_utilities.principal_value
   sorcha.ephemeris.orbit_conversion_utilities.universal_keplerian


Module Contents
---------------

.. py:class:: halley_result

   Bases: :py:obj:`tuple`


   .. py:attribute:: root


   .. py:attribute:: iterations


   .. py:attribute:: function_calls


   .. py:attribute:: converged


   .. py:attribute:: flag


   .. py:attribute:: f


   .. py:attribute:: fp


   .. py:attribute:: fpp


.. py:function:: stumpff(x)

   Computes the Stumpff function c_k(x) for k = 0, 1, 2, 3

   :param x: Argument of the Stumpff function
   :type x: float

   :returns: * **c_0(x)** (*float*)
             * **c_1(x)** (*float*)
             * **c_2(x)** (*float*)
             * **c_3(x)** (*float*)


.. py:function:: root_function(s, mu, alpha, r0, r0dot, t)

   Root function used in the Halley minimizer
   Computes the zeroth, first, second, and third derivatives
   of the universal Kepler equation f

   :param s: Eccentric anomaly
   :type s: float
   :param mu: Standard gravitational parameter GM
   :type mu: float
   :param alpha: Total energy
   :type alpha: float
   :param r0: Initial position
   :type r0: float
   :param r0dot: Initial velocity
   :type r0dot: float
   :param t: Time
   :type t: float

   :returns: * **f** (*float*) -- universal Kepler equation)
             * **fp** (*float*) -- (first derivative of f
             * **fpp** (*float*) -- second derivative of f
             * **fppp** (*float*) -- third derivative of f


.. py:function:: halley_safe(x1, x2, mu, alpha, r0, r0dot, t, xacc=1e-14, maxit=100)

   Applies the Halley root finding algorithm on the universal Kepler equation

   :param x1: Previous guess used in minimization
   :type x1: float
   :param x2: Current guess for minimization
   :type x2: float
   :param mu: Standard gravitational parameter GM
   :type mu: float
   :param alpha: Total energy
   :type alpha: float
   :param r0: Initial position
   :type r0: float
   :param r0dot: Initial velocity
   :type r0dot: float
   :param t: Time
   :type t: float
   :param xacc: Accuracy in x before algorithm declares convergence
   :type xacc: float
   :param maxit: Maximum number of iterations
   :type maxit: int

   :returns: * *boolean* -- True if minimization converged, False otherwise
             * *float* -- Solution
             * *float* -- First derivative of solution


.. py:function:: universal_cartesian(mu, q, e, incl, longnode, argperi, tp, epochMJD_TDB)

   Converts from a series of orbital elements into state vectors
   using the universal variable formulation

   The output vector will be oriented in the same system as
   the positional angles (i, Omega, omega)

   Note that mu, q, tp and epochMJD_TDB must have compatible units
   As an example, if q is in au and tp/epoch are in days, mu must
   be in (au^3)/days^2

   :param mu: Standard gravitational parameter GM (see note above about units)
   :type mu: float
   :param q: Perihelion (see note above about units)
   :type q: float
   :param e: Eccentricity
   :type e: float
   :param incl: Inclination (radians)
   :type incl: float
   :param longnode: Longitude of ascending node (radians)
   :type longnode: float
   :param argperi: Argument of perihelion (radians)
   :type argperi: float
   :param tp: Time of perihelion passage in TDB scale (see note above about units)
   :type tp: float
   :param epochMJD_TDB: Epoch (in TDB) when the elements are defined (see note above about units)
   :type epochMJD_TDB: float

   :returns: * *float* -- x coordinate
             * *float* -- y coordinate
             * *float* -- z coordinate
             * *float* -- x velocity
             * *float* -- y velocity
             * *float* -- z velocity


.. py:function:: principal_value(theta)

   Computes the principal value of an angle

   :param theta: Angle
   :type theta: float

   :returns: Principal value of angle
   :rtype: float


.. py:function:: universal_keplerian(mu, x, y, z, vx, vy, vz, epochMJD_TDB)

   Converts from a state vectors into orbital elements
   using the universal variable formulation

   The input vector will determine the orientation
   of the positional angles (i, Omega, omega)


   Note that mu and the state vectors must have compatible units
   As an example, if x is in au and vx are in au/days, mu must
   be in (au^3)/days^2


   :param mu: Standard gravitational parameter GM (see note above about units)
   :type mu: float
   :param x: x coordinate
   :type x: float
   :param y: y coordinate
   :type y: float
   :param z: z coordinate
   :type z: float
   :param vx: x velocity
   :type vx: float
   :param vy: y velocity
   :type vy: float
   :param vz: z velocity
   :type vz: float
   :param epochMJD_TDB (float): Epoch (in TDB) when the elements are defined (see note above about units)

   :returns: * *float* -- Perihelion (see note above about units)
             * *float* -- Eccentricity
             * *float* -- Inclination (radians)
             * *float* -- Longitude of ascending node (radians)
             * *float* -- Argument of perihelion (radians)
             * *float* -- Time of perihelion passage in TDB scale (see note above about units)


