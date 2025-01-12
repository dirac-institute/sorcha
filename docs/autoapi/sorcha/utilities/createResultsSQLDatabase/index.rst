sorcha.utilities.createResultsSQLDatabase
=========================================

.. py:module:: sorcha.utilities.createResultsSQLDatabase


Functions
---------

.. autoapisummary::

   sorcha.utilities.createResultsSQLDatabase.create_results_table
   sorcha.utilities.createResultsSQLDatabase.create_inputs_table
   sorcha.utilities.createResultsSQLDatabase.create_results_database
   sorcha.utilities.createResultsSQLDatabase.get_column_names


Module Contents
---------------

.. py:function:: create_results_table(cnx_out, filename, output_path, output_stem, table_name='sorcha_results')

   Creates a table in a SQLite database from SSPP results.

   :param cnx_out: Connection to sqlite3 database.
   :type cnx_out: sqlite3 connection
   :param filename: filepath/name of sqlite3 database.
   :type filename: string
   :param output_path: filepath of directory containing SSPP output folders.
   :type output_path: string
   :param output_stem: stem filename for SSPP outputs.
   :type output_stem: string
   :param table_name: name of table of for storing sorcha results. Default ="sorcha_results"
   :type table_name: string, optional

   :rtype: None


.. py:function:: create_inputs_table(cnx_out, input_path, table_type)

   Creates a table in a SQLite database from the input files (i.e. orbits,
   physical parameters, etc).

   :param cnx_out: Connection to sqlite3 database.
   :type cnx_out: sqlite3 connection
   :param input_path: Filepath of directory containing input files.
   :type input_path: string
   :param table_type: Type of file. Should be "orbits"/"params"/"complex".
   :type table_type: string

   :rtype: None


.. py:function:: create_results_database(args)

   Creates a SQLite database with tables of SSPP results and all orbit/physical
   parameters/comet files.

   :param args: argparse ArgumentParser object; command line arguments.
   :type args: ArgumentParser

   :rtype: None


.. py:function:: get_column_names(filename, table_name='sorcha_results')

   Obtains column names from a table in a SQLite database.

   :param filename: Filepath/name of sqlite3 database.
   :type filename: string
   :param table_name: Name of table. Default = "sorcha_results"
   :type table_name: string, optional

   :returns: **col_names (list)**
   :rtype: list of column names.


