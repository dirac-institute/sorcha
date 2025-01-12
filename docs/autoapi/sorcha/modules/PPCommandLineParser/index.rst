sorcha.modules.PPCommandLineParser
==================================

.. py:module:: sorcha.modules.PPCommandLineParser


Functions
---------

.. autoapisummary::

   sorcha.modules.PPCommandLineParser.warn_or_remove_file
   sorcha.modules.PPCommandLineParser.PPCommandLineParser


Module Contents
---------------

.. py:function:: warn_or_remove_file(filepath, force_remove, pplogger)

   Given a path to a file(s), first determine if the file exists. If it does not
   exist, pass through.

   If the file does exist check if the user has set `--force` on the command line.
   If the user set --force, log that the existing file will be removed.
   Otherwise, warn the user that the file exists and exit the program.

   :param filepath: The full file path to a given file. i.e. /home/data/output.csv
   :type filepath: string
   :param force_remove: Whether to remove the file if it exists.
   :type force_remove: boolean
   :param pplogger: Used to log the output.
   :type pplogger: Logger


.. py:function:: PPCommandLineParser(args)

   Parses the command line arguments, error-handles them, then stores them in a single dict.

   Will only look for the comet parameters file if it's actually given at the command line.

   :param args: argparse object of command line arguments
   :type args: ArgumentParser object

   :returns: **cmd_args_dict** -- dictionary of variables taken from command line arguments
   :rtype: dictionary


