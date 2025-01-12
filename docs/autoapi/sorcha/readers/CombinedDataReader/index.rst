sorcha.readers.CombinedDataReader
=================================

.. py:module:: sorcha.readers.CombinedDataReader

.. autoapi-nested-parse::

   The CombinedDataReader class supports loading the entire input data
   for the simulator post processing by using individuals reader classes
   to read individual input files and combining the data into a single table.

   The CombinedDataReader object reads the data in blocks to limit memory usage.
   For each blocks, it uses two stages:
   1) It reads a range of individual rows from the ``primary_reader``. By default this
      reader is the first auxiliary data reader, but can be set to the ephemeris reader.
      This reader is used to extract a list of object IDs for this block.
   2) For each of the readers (ephemeris and auxiliary data) load in all the rows
      corresponding to the object IDs extracted in stage 1.

   For example, if the ephemeris file is used as the primary reader, the algorithm
   will load data in blocks of the ephemeris rows and join in the auxiliary data
   for just the object IDs on those rows. It is not guaranteed to include all
   rows for the current objects.



Classes
-------

.. autoapisummary::

   sorcha.readers.CombinedDataReader.CombinedDataReader


Module Contents
---------------

.. py:class:: CombinedDataReader(ephem_primary=False, **kwargs)

   .. py:attribute:: ephem_reader
      :value: None



   .. py:attribute:: aux_data_readers
      :value: []



   .. py:attribute:: block_start
      :value: 0



   .. py:attribute:: ephem_primary
      :value: False



   .. py:method:: add_ephem_reader(new_reader)

      Add a new reader for ephemeris data.

      :param new_reader: The reader for a specific input file.
      :type new_reader: ObjectDataReader



   .. py:method:: add_aux_data_reader(new_reader)

      Add a new object reader that corresponds to an auxiliary input data type..

      :param new_reader: The reader for a specific input file.
      :type new_reader: ObjectDataReader



   .. py:method:: check_aux_object_ids()

      Checks the ObjIDs in all of the auxiliary data readers to make sure
      both files contain exactly the same ObjIDs.



   .. py:method:: read_block(block_size=None, verbose=False, **kwargs)

      Reads in a set number of rows from the input, performs
      post-processing and validation, and returns a data frame.

      :param block_size: the number of rows to read in.
                         Use block_size=None to read in all available data.
                         Default = None
      :type block_size: integer, optional
      :param verbose: Use verbose logging.
                      Default = False
      :type verbose: boolean, optional
      :param \*\*kwargs: Extra arguments
      :type \*\*kwargs: dictionary, optional

      :returns: **res_df** -- dataframe of the combined object data.
      :rtype: pandas dataframe



   .. py:method:: read_aux_block(block_size=None, verbose=False, **kwargs)

      Reads in a set number of rows from the input, performs
      post-processing and validation, and returns a data frame.

      This function DOES NOT include the ephemeris data in the returned data frame.
      It is to be used when generating the ephemeris during the execution of Sorcha.

      :param block_size: the number of rows to read in.
                         Use block_size=None to read in all available data.
                         Default = None
      :type block_size: integer, optional
      :param verbose: use verbose logging.
                      Default = False
      :type verbose: boolean, optional
      :param \*\*kwargs: Extra arguments
      :type \*\*kwargs: dictionary, optional

      :returns: **res_df** -- dataframe of the combined object data, excluding any ephemeris data.
      :rtype: pandas dataframe



