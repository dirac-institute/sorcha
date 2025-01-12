sorcha.ephemeris
================

.. py:module:: sorcha.ephemeris


Submodules
----------

.. toctree::
   :maxdepth: 1

   /autoapi/sorcha/ephemeris/orbit_conversion_utilities/index
   /autoapi/sorcha/ephemeris/pixel_dict/index
   /autoapi/sorcha/ephemeris/simulation_constants/index
   /autoapi/sorcha/ephemeris/simulation_data_files/index
   /autoapi/sorcha/ephemeris/simulation_driver/index
   /autoapi/sorcha/ephemeris/simulation_geometry/index
   /autoapi/sorcha/ephemeris/simulation_parsing/index
   /autoapi/sorcha/ephemeris/simulation_setup/index


Attributes
----------

.. autoapisummary::

   sorcha.ephemeris.AU_KM
   sorcha.ephemeris.AU_M
   sorcha.ephemeris.RADIUS_EARTH_KM
   sorcha.ephemeris.SPEED_OF_LIGHT
   sorcha.ephemeris.OBLIQUITY_ECLIPTIC


Classes
-------

.. autoapisummary::

   sorcha.ephemeris.Observatory


Functions
---------

.. autoapisummary::

   sorcha.ephemeris.create_ecl_to_eq_rotation_matrix
   sorcha.ephemeris.make_retriever
   sorcha.ephemeris.barycentricObservatoryRates
   sorcha.ephemeris.ecliptic_to_equatorial
   sorcha.ephemeris.integrate_light_time
   sorcha.ephemeris.ra_dec2vec
   sorcha.ephemeris.mjd_tai_to_epoch
   sorcha.ephemeris.parse_orbit_row
   sorcha.ephemeris.create_assist_ephemeris
   sorcha.ephemeris.furnish_spiceypy
   sorcha.ephemeris.precompute_pointing_information
   sorcha.ephemeris.create_ephemeris
   sorcha.ephemeris.universal_cartesian
   sorcha.ephemeris.universal_keplerian


Package Contents
----------------

.. py:data:: AU_KM
   :value: 149597870.7


.. py:data:: AU_M
   :value: 149597870700


.. py:data:: RADIUS_EARTH_KM
   :value: 6378.137


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


.. py:function:: make_retriever(auxconfigs, directory_path: str = None) -> pooch.Pooch

   Helper function that will create a Pooch object to track and retrieve files.

   :param directory_path: The base directory to place all downloaded files. Default = None
   :type directory_path: string, optional
   :param registry: A dictionary of file names to SHA hashes. Generally we'll not use SHA=None
                    because the files we're tracking change frequently. Default = REGISTRY
   :type registry: dictionary, optional
   :param auxconfigs: Dataclass of auxiliary configuration file arguments.
   :type auxconfigs: dataclass

   :returns: The instance of a Pooch object used to track and retrieve files.
   :rtype: pooch


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


.. py:function:: ra_dec2vec(ra, dec)

   Converts a RA/Dec pair to a unit vector on the sphere
   :param ra: Target RA
   :type ra: float
   :param dec: Target dec
   :type dec: float

   :returns: Unit vector
   :rtype: array


.. py:function:: mjd_tai_to_epoch(mjd_tai)

   Converts a MJD value in TAI to SPICE ephemeris time

   :param mjd_tai: Input mjd
   :type mjd_tai: float

   :rtype: Ephemeris time


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


.. py:function:: create_assist_ephemeris(args, auxconfigs) -> tuple

   Build the ASSIST ephemeris object
   Parameter
   ---------
   auxconfigs: dataclass
       Dataclass of auxiliary configuration file arguments.
   :returns: * **Ephem** (*ASSIST ephemeris obejct*) -- The ASSIST ephemeris object
             * **gm_sun** (*float*) -- value for the GM_SUN value
             * **gm_total** (*float*) -- value for gm_total


.. py:function:: furnish_spiceypy(args, auxconfigs)

   Builds the SPICE kernel, downloading the required files if needed
   :param auxconfigs: Dataclass of auxiliary configuration file arguments.
   :type auxconfigs: dataclass


.. py:function:: precompute_pointing_information(pointings_df, args, sconfigs)

   This function is meant to be run once to prime the pointings dataframe
   with additional information that Assist & Rebound needs for it's work.

   :param pointings_df: Contains the telescope pointing database.
   :type pointings_df: pandas dataframe
   :param args: Command line arguments needed for initialization.
   :type args: dictionary
   :param sconfigs: Dataclass of configuration file arguments.
   :type sconfigs: dataclass

   :returns: **pointings_df** -- The original dataframe with several additional columns of precomputed values.
   :rtype: pandas dataframe


.. py:function:: create_ephemeris(orbits_df, pointings_df, args, sconfigs)

   Generate a set of observations given a collection of orbits
   and set of pointings.

   :param orbits_df: The dataframe containing the collection of orbits.
   :type orbits_df: pandas dataframe
   :param pointings_df: The dataframe containing the collection of telescope/camera pointings.
   :type pointings_df: pandas dataframe
   :param args: Various arguments necessary for the calculation
   :param sconfigs: Dataclass of configuration file arguments.
                    Various configuration parameters necessary for the calculation
                    ang_fov : float
                        The angular size (deg) of the field of view
                    buffer : float
                        The angular size (deg) of the buffer around the field of view.
                        A buffer is required to allow for some motion between the time
                        of the observation and the time of the picket (t_picket)
                    picket_interval : float
                        The interval (days) between picket calculations.  This is 1 day
                        by default.  Current there is only one such interval, used for
                        all objects.  It is currently possible for extremely fast-moving
                        objects to be missed.  This will be remedied in future releases.
                    obsCode : string
                        The MPC code for the observatory.  (This is current a configuration
                        parameter, but these should be included in the visit information,
                        to allow for multiple observatories.
                    nside : integer
                        The nside value used for the HEALPIx calculations.  Must be a
                        power of 2 (1, 2, 4, ...)  nside=64 is current default.

   :returns: **observations** -- The dataframe of observations needed for Sorcha to continue
   :rtype: pandas dataframe

   .. rubric:: Notes

   This works by calculating and regularly updating the sky-plane
   locations (unit vectors) of all the objects in the collection
   of orbits.  The HEALPix index for each of the locations is calculated.
   A dictionary with pixel indices as keys and lists of ObjIDs for
   those objects in each HEALPix tile as values is generated.  An individual
   one of these calculations is called a 'picket', as one element of a long
   picket fence.  Typically, the interval between pickets is one day.

   Given a specific pointing, the set of HEALPix tiles that are overlapped
   by the pointing (and a buffer region) is computed.  Then the precise
   locations of just those objects within that set of HEALPix tiles are
   computed.  Details for those that actually do land within the field
   of view are passed along.


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


