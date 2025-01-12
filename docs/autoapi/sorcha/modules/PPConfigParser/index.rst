sorcha.modules.PPConfigParser
=============================

.. py:module:: sorcha.modules.PPConfigParser


Functions
---------

.. autoapisummary::

   sorcha.modules.PPConfigParser.log_error_and_exit
   sorcha.modules.PPConfigParser.PPGetOrExit
   sorcha.modules.PPConfigParser.PPGetFloatOrExit
   sorcha.modules.PPConfigParser.PPGetIntOrExit
   sorcha.modules.PPConfigParser.PPGetBoolOrExit
   sorcha.modules.PPConfigParser.PPGetValueAndFlag
   sorcha.modules.PPConfigParser.PPFindFileOrExit
   sorcha.modules.PPConfigParser.PPFindDirectoryOrExit
   sorcha.modules.PPConfigParser.PPCheckFiltersForSurvey
   sorcha.modules.PPConfigParser.PPConfigFileParser
   sorcha.modules.PPConfigParser.PPPrintConfigsToLog


Module Contents
---------------

.. py:function:: log_error_and_exit(message: str) -> None

   Log a message to the error output file and terminal, then exit.

   :param message: The error message to be logged to the error output file.
   :type message: string

   :rtype: None


.. py:function:: PPGetOrExit(config, section, key, message)

   Checks to see if the config file parser has a key. If it does not, this
   function errors out and the code stops.

   :param config: ConfigParser object containing configs.
   :type config: ConfigParser
   :param section: Section of the key being checked.
   :type section: string
   :param key: The key being checked.
   :type key: string)
   :param message: The message to log and display if the key is not found.
   :type message: string

   :rtype: None.


.. py:function:: PPGetFloatOrExit(config, section, key, message)

   Checks to see if a key in the config parser is present and can be read as a
   float. If it cannot, this function errors out and the code stops.

   :param config: ConfigParser object containing configs.
   :type config: ConfigParser
   :param section: section of the key being checked.
   :type section: string
   :param key: The key being checked.
   :type key: string
   :param message: The message to log and display if the key is not found.
   :type message: string

   :rtype: None.


.. py:function:: PPGetIntOrExit(config, section, key, message)

   Checks to see if a key in the config parser is present and can be read as an
   int. If it cannot, this function errors out and the code stops.

   :param config: ConfigParser object containing configs.
   :type config: ConfigParser
   :param section: Section of the key being checked.
   :type section: string
   :param key: The key being checked.
   :type key: string
   :param message: The message to log and display if the key is not found.
   :type message: string

   :rtype: None.


.. py:function:: PPGetBoolOrExit(config, section, key, message)

   Checks to see if a key in the config parser is present and can be read as a
   Boolean. If it cannot, this function errors out and the code stops.

   :param config: ConfigParser object containing configs.
   :type config: ConfigParser object
   :param section: Section of the key being checked.
   :type section: string
   :param key: The key being checked.
   :type key: string
   :param message: The message to log and display if the key is not found.
   :type message: string

   :rtype: None.


.. py:function:: PPGetValueAndFlag(config, section, key, type_wanted)

   Obtains a value from the config flag, forcing it to be the specified
   type and error-handling if it can't be forced. If the value is not present
   in the config fie, the flag is set to False; if it is, the flag is True.

   :param config: ConfigParser object containing configs.
   :type config: ConfigParser
   :param section: Section of the key being checked.
   :type section: string
   :param key: The key being checked.
   :type key: string
   :param type_wanted: The type the value should be forced to.
                       Accepts int, float, none (for no type-forcing).
   :type type_wanted: string

   :returns: * **value** (*any type*) -- The value of the key, with type dependent on type_wanted.
               Will be None if the key is not present.
             * **flag** (*boolean*) -- Will be False if the key is not present in the config file
               and True if it is.


.. py:function:: PPFindFileOrExit(arg_fn, argname)

   Checks to see if a file given by a filename exists. If it doesn't,
   this fails gracefully and exits to the command line.

   :param arg_fn: The filepath/name of the file to be checked.
   :type arg_fn: string
   :param argname: The name of the argument being checked. Used for error message.
   :type argname: string

   :returns: **arg_fn** -- The filepath/name of the file to be checked.
   :rtype: string


.. py:function:: PPFindDirectoryOrExit(arg_fn, argname)

   Checks to see if a directory given by a filepath exists. If it doesn't,
   this fails gracefully and exits to the command line.

   :param arg_fn: The filepath of the directory to be checked.
   :type arg_fn: string
   :param argname: The name of the argument being checked. Used for error message.
   :type argname: string

   :returns: **arg_fn** -- The filepath of the directory to be checked.
   :rtype: string


.. py:function:: PPCheckFiltersForSurvey(survey_name, observing_filters)

   When given a list of filters, this function checks to make sure they exist in the
   user-selected survey, and if the filters given in the config file do not match the
   survey filters, the function exits the program with an error.

   :param survey_name: Survey name. Currently only "LSST", "lsst" accepted.
   :type survey_name: string
   :param observing_filters: Observation filters of interest.
   :type observing_filters: list of strings

   :rtype: None.

   .. rubric:: Notes

   Currently only has options for LSST, but can be expanded upon later.


.. py:function:: PPConfigFileParser(configfile, survey_name)

   Parses the config file, error-handles, then assigns the values into a single
   dictionary, which is passed out.

   :param configfile: Filepath/name of config file.
   :type configfile: string
   :param survey_name: Survey name. Currently only "LSST", "lsst" accepted.
   :type survey_name: string

   :returns: **config_dict** -- Dictionary of config file variables.
   :rtype: dictionary

   .. rubric:: Notes

   We chose not to use the original ConfigParser object for readability: it's a dict of
   dicts, so calling the various values can become quite unwieldy.


.. py:function:: PPPrintConfigsToLog(configs, cmd_args)

   Prints all the values from the config file and command line to the log.

   :param configs: Dictionary of config file variables.
   :type configs: dictionary
   :param cmd_args: Dictionary of command line arguments.
   :type cmd_args: dictionary

   :rtype: None.


