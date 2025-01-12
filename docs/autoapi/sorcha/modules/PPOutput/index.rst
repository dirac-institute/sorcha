sorcha.modules.PPOutput
=======================

.. py:module:: sorcha.modules.PPOutput


Functions
---------

.. autoapisummary::

   sorcha.modules.PPOutput.PPOutWriteCSV
   sorcha.modules.PPOutput.PPOutWriteHDF5
   sorcha.modules.PPOutput.PPOutWriteSqlite3
   sorcha.modules.PPOutput.PPIndexSQLDatabase
   sorcha.modules.PPOutput.PPWriteOutput


Module Contents
---------------

.. py:function:: PPOutWriteCSV(padain, outf, separator=',')

   Writes a pandas dataframe out to a CSV file at a location given by the user.

   :param padain: Dataframe of output.
   :type padain: pandas dataframe
   :param outf: Location to which file should be written.
   :type outf: string
   :param separator: String of CSV separator. Default is ','.
   :type separator: string of length 1

   :rtype: None.


.. py:function:: PPOutWriteHDF5(pp_results, outf, keyname='sorcha_results')

   Writes a pandas dataframe out to a HDF5 file at a location given by the user.

   :param padain: Dataframe of output.
   :type padain: pandas dataframe
   :param outf: Location to which file should be written.
   :type outf: string
   :param keyin: Key at which data will be located.
   :type keyin: string

   :rtype: None.


.. py:function:: PPOutWriteSqlite3(pp_results, outf, tablename='sorcha_results')

   Writes a pandas dataframe out to a CSV file at a location given by the user.

   :param pp_results: Dataframe of output.
   :type pp_results: pandas dataframe
   :param outf: Location to which file should be written.
   :type outf: string
   :param tablename: String of the table within the database to be indexed.
   :type tablename: string

   :rtype: None.


.. py:function:: PPIndexSQLDatabase(outf, tablename='sorcha_results')

   Indexes a SQLite database of Sorcha output.

   :param outf: Location of SQLite database to be indexed.
   :type outf: string
   :param tablename: String of the table within the database to be indexed.
   :type tablename: string

   :rtype: None.


.. py:function:: PPWriteOutput(cmd_args, sconfigs, observations_in, verbose=False)

   Writes the output in the format specified in the config file to a location
   specified by the user.

   :param cmd_args: Dictonary of command line arguments.
   :type cmd_args: dictionary
   :param sconfigs: Dataclass of configuration file arguments.
   :type sconfigs: dataclass
   :param observations_in: Dataframe of output.
   :type observations_in: Pandas dataframe
   :param endChunk: Integer of last object in chunk. Used only for HDF5 output key.
                    Default = 0
   :type endChunk: integer, optional
   :param verbose: Verbose logging mode on or off. Default = False
   :type verbose: boolean, optional

   :rtype: None.


