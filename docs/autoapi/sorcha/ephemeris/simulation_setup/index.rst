sorcha.ephemeris.simulation_setup
=================================

.. py:module:: sorcha.ephemeris.simulation_setup


Functions
---------

.. autoapisummary::

   sorcha.ephemeris.simulation_setup.create_assist_ephemeris
   sorcha.ephemeris.simulation_setup.furnish_spiceypy
   sorcha.ephemeris.simulation_setup.generate_simulations
   sorcha.ephemeris.simulation_setup.precompute_pointing_information


Module Contents
---------------

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


.. py:function:: generate_simulations(ephem, gm_sun, gm_total, orbits_df, args)

   Creates the dictionary of ASSIST simulations for the ephemeris generation

   :param ephem: The ASSIST ephemeris object
   :type ephem: Ephem
   :param gm_sun: Standard gravitational parameter GM for the Sun
   :type gm_sun: float
   :param gm_total: Standard gravitational parameter GM for the Solar System barycenter
   :type gm_total: float
   :param orbits_df: Pandas dataframe with the input orbits
   :type orbits_df: dataframe
   :param args: dictionary of command-line arguments.
   :type args: dictionary or `sorchaArguments` object

   :returns: **sim_dict** -- Dictionary of ASSIST simulations
   :rtype: dict


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


