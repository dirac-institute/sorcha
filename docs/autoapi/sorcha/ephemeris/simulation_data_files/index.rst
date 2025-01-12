sorcha.ephemeris.simulation_data_files
======================================

.. py:module:: sorcha.ephemeris.simulation_data_files


Functions
---------

.. autoapisummary::

   sorcha.ephemeris.simulation_data_files.make_retriever


Module Contents
---------------

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


