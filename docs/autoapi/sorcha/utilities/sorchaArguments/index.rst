sorcha.utilities.sorchaArguments
================================

.. py:module:: sorcha.utilities.sorchaArguments


Classes
-------

.. autoapisummary::

   sorcha.utilities.sorchaArguments.sorchaArguments


Module Contents
---------------

.. py:class:: sorchaArguments(cmd_args_dict=None)

   Data class for holding runtime arguments


   .. py:attribute:: paramsinput
      :type:  str
      :value: ''


      path to file with input objects


   .. py:attribute:: orbinfile
      :type:  str
      :value: ''


      path to file with input object orbits


   .. py:attribute:: input_ephemeris_file
      :type:  str
      :value: ''


      path the ephemeris input file


   .. py:attribute:: configfile
      :type:  str
      :value: ''


      path to the config.ini file


   .. py:attribute:: outpath
      :type:  str
      :value: ''


      path where data should be output


   .. py:attribute:: outfilestem
      :type:  str
      :value: ''


      file system for output


   .. py:attribute:: loglevel
      :type:  bool
      :value: False


      logger verbosity


   .. py:attribute:: surveyname
      :type:  str
      :value: ''


      name of the survey (`rubin_sim` is only one implemented currently)


   .. py:attribute:: complex_parameters
      :type:  str
      :value: ''


      optional, extra complex physical parameter input files


   .. py:attribute:: linking
      :type:  bool
      :value: True


      Turns on or off the rejection of unlinked sources


   .. py:attribute:: _rngs
      :value: None


      A collection of per-module random number generators


   .. py:attribute:: pplogger
      :value: None


      The Python logger instance


   .. py:method:: read_from_dict(args)

      set the parameters from a cmd_args dict.

      :param aguments: dictionary of configuration parameters
      :type aguments: dictionary

      :rtype: None



   .. py:method:: validate_arguments()


