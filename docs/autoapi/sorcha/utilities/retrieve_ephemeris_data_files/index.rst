sorcha.utilities.retrieve_ephemeris_data_files
==============================================

.. py:module:: sorcha.utilities.retrieve_ephemeris_data_files


Functions
---------

.. autoapisummary::

   sorcha.utilities.retrieve_ephemeris_data_files._decompress
   sorcha.utilities.retrieve_ephemeris_data_files._remove_files
   sorcha.utilities.retrieve_ephemeris_data_files._check_for_existing_files


Module Contents
---------------

.. py:function:: _decompress(fname, action, pup)

   Override the functionality of Pooch's `Decompress` class so that the resulting
   decompressed file uses the original file name without the compression extension.
   For instance `filename.json.bz` will be decompressed and saved as `filename.json`.

   :param fname: Original filename
   :type fname: string
   :param action: One of []"download", "update", "fetch"]
   :type action: string
   :param pup: The Pooch object that defines the location of the file.
   :type pup: pooch

   :rtype: None


.. py:function:: _remove_files(auxconfigs, retriever: pooch.Pooch) -> None

   Utility to remove all the files tracked by the pooch retriever. This includes
   the decompressed ObservatoryCodes.json file as well as the META_KERNEL file
   that are created after downloading the files in the DATA_FILES_TO_DOWNLOAD
   list.

   :param retriever: Pooch object that maintains the registry of files to download.
   :type retriever: pooch
   :param auxconfigs: Dataclass of auxiliary configuration file arguments.
   :type auxconfigs: dataclass


.. py:function:: _check_for_existing_files(retriever: pooch.Pooch, file_list: list[str]) -> bool

   Will check for existing local files, any file not found will be printed
   to the terminal.

   :param retriever: Pooch object that maintains the registry of files to download.
   :type retriever: pooch
   :param file_list: A list of file names look for in the local cache.
   :type file_list: list of strings

   :returns: Returns True if all files are found in the local cache, False otherwise.
   :rtype: bool


