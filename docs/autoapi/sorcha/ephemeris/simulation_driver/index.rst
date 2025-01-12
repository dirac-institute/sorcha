sorcha.ephemeris.simulation_driver
==================================

.. py:module:: sorcha.ephemeris.simulation_driver


Classes
-------

.. autoapisummary::

   sorcha.ephemeris.simulation_driver.EphemerisGeometryParameters


Functions
---------

.. autoapisummary::

   sorcha.ephemeris.simulation_driver.get_vec
   sorcha.ephemeris.simulation_driver.create_ephemeris
   sorcha.ephemeris.simulation_driver.get_residual_vectors
   sorcha.ephemeris.simulation_driver.calculate_rates_and_geometry
   sorcha.ephemeris.simulation_driver.write_out_ephemeris_file


Module Contents
---------------

.. py:class:: EphemerisGeometryParameters

   Data class for holding parameters related to ephemeris geometry


   .. py:attribute:: obj_id
      :type:  str
      :value: None



   .. py:attribute:: mjd_tai
      :type:  float
      :value: None



   .. py:attribute:: rho
      :type:  float
      :value: None



   .. py:attribute:: rho_hat
      :type:  float
      :value: None



   .. py:attribute:: rho_mag
      :type:  float
      :value: None



   .. py:attribute:: r_ast
      :type:  float
      :value: None



   .. py:attribute:: v_ast
      :type:  float
      :value: None



.. py:function:: get_vec(row, vecname)

   Extracts a vector from a Pandas dataframe row
   :param row:
   :type row: row from the dataframe
   :param vecname:
   :type vecname: name of the vector

   :rtype: 3D numpy array


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


.. py:function:: get_residual_vectors(v1)

   Decomposes the vector into two unit vectors to facilitate computation of on-sky angles
   The decomposition is such that A  = (-sin (RA), cos(RA), 0) is in the direction of increasing RA,
   and D = (-sin(dec)cos (RA), -sin(dec) sin(RA), cos(dec)) is in the direction of increasing Dec
   The triplet (A,D,v1) forms an orthonormal basis of the 3D vector space
   :param v1: The vector to be decomposed
   :type v1: array, shape = (3,))

   :returns: * **A** (*array, shape = (3,))*) -- A  vector
             * **D** (*array, shape = (3,))*) -- D vector


.. py:function:: calculate_rates_and_geometry(pointing: pandas.DataFrame, ephem_geom_params: EphemerisGeometryParameters)

   Calculate rates and geometry for objects within the field of view

   :param pointing: The dataframe containing the pointing database.
   :type pointing: pandas dataframe
   :param ephem_geom_params: Various parameters necessary to calculate the ephemeris
   :type ephem_geom_params: EphemerisGeometryParameters

   :returns: Tuple containing the ephemeris parameters needed for Sorcha post processing.
   :rtype: tuple


.. py:function:: write_out_ephemeris_file(ephemeris_df, ephemeris_csv_filename, args, sconfigs)

   Writes the ephemeris out to an external file.

   :param ephemeris_df: The data frame of ephemeris information to be written out.
   :type ephemeris_df: Pandas DataFrame
   :param ephemeris_csv_filename: The filepath (without extension) to write the ephemeris file to.
   :type ephemeris_csv_filename: string
   :param args: Command-line arguments from Sorcha.
   :type args: sorchaArguments object or similar
   :param sconfigs: Dataclass of configuration file arguments.
   :type sconfigs: dataclass

   :rtype: None.


