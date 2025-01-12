sorcha.utilities.check_output_logs
==================================

.. py:module:: sorcha.utilities.check_output_logs


Functions
---------

.. autoapisummary::

   sorcha.utilities.check_output_logs.find_all_log_files
   sorcha.utilities.check_output_logs.check_all_logs
   sorcha.utilities.check_output_logs.check_output_logs


Module Contents
---------------

.. py:function:: find_all_log_files(filepath)

   Looks for all Sorcha log files in the given filepath and subdirectories
   recursively. Specifically searches for files ending *sorcha.log.

   :param filepath: Filepath of top-level directory within which to search for Sorcha log files.
   :type filepath: str

   :returns: **log_files** -- A list of the discovered log files (absolute paths)
   :rtype: list


.. py:function:: check_all_logs(log_files)

   Checks the last line of all the log files supplied and checks to see
   if the Sorcha run completed successfully, saving the last line of the log
   in question if it did not.

   :param log_files: A list of filepaths pointing to Sorcha log files.
   :type log_files: list

   :returns: * **good_log** (*list of Booleans*) -- A list of whether each log file was deemed to be successful or not
             * **last_lines** (*list of str*) -- A list of the last lines of unsuccessful Sorcha runs.


.. py:function:: check_output_logs(filepath, output=False)

   Searches directories recursively for Sorcha log files, classifies them as
   belonging to successful or unsuccessful Sorcha runs, and provides this information
   to the user. This is helpful in cases where several runs of Sorcha are being
   performed simultaneously (i.e. on a supercomputer). Can output either a .csv
   file or straight to the terminal.

   :param filepath: Filepath of top-level directory within which to search for Sorcha log files.
   :type filepath: str
   :param output: Either the filepath/name in which to save output, or False to print output to terminal. Default=False.
   :type output: str or bool


