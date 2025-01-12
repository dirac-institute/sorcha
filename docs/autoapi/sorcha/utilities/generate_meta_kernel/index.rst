sorcha.utilities.generate_meta_kernel
=====================================

.. py:module:: sorcha.utilities.generate_meta_kernel


Functions
---------

.. autoapisummary::

   sorcha.utilities.generate_meta_kernel.build_meta_kernel_file
   sorcha.utilities.generate_meta_kernel._build_file_name


Module Contents
---------------

.. py:function:: build_meta_kernel_file(auxconfigs, retriever: pooch.Pooch) -> None

   Builds a specific text file that will be fed into `spiceypy` that defines
   the list of spice kernel to load, as well as the order to load them.

   :param retriever: Pooch object that maintains the registry of files to download
   :type retriever: pooch
   :param auxconfigs: Dataclass of auxiliary configuration file arguments.
   :type auxconfigs: dataclass

   :rtype: None


.. py:function:: _build_file_name(cache_dir: str, file_path: str) -> str

   Given a string defining the cache directory, and a string defining the full
   path to a given file. This function will strip out the cache directory from
   the file path and replace it with the required meta_kernel directory
   substitution character.

   :param cache_dir: The full path to the cache directory used when retrieving files for Assist
                     and Rebound.
   :type cache_dir: string
   :param file_path: The full file path for a given file that will have the cache directory
                     segment replace.
   :type file_path: string

   :returns: Shortened file path, appropriate for use in kernel_meta files.
   :rtype: string


