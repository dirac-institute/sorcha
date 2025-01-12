sorcha.modules.PPGetLogger
==========================

.. py:module:: sorcha.modules.PPGetLogger


Functions
---------

.. autoapisummary::

   sorcha.modules.PPGetLogger.PPGetLogger


Module Contents
---------------

.. py:function:: PPGetLogger(log_location, log_stem, log_format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s ', log_name='', log_file_info='sorcha.log', log_file_error='sorcha.err')

   Initialises log and error files.

   :param log_location: Filepath to directory in which to save logs.
   :type log_location: string
   :param log_stem: String output stem used to prefix all Sorcha outputs.
   :type log_stem: string
   :param log_format: Format for log filename.
                      Default = "%(asctime)s %(name)-12s %(levelname)-8s %(message)s "
   :type log_format: string, optional
   :param log_name: Name of log. Default = ""
   :type log_name: string, optional
   :param log_file_info: Suffix and extension with which to save info log. Default = "sorcha.log"
   :type log_file_info: string, optional
   :param log_file_error: Suffix and extension with which to save error log. Default = "sorcha.err"
   :type log_file_error: string, optional

   :returns: **log** -- Log object.
   :rtype: logging object


