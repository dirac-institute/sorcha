sorcha.readers.EphemerisReader
==============================

.. py:module:: sorcha.readers.EphemerisReader


Classes
-------

.. autoapisummary::

   sorcha.readers.EphemerisReader.EphemerisDataReader


Functions
---------

.. autoapisummary::

   sorcha.readers.EphemerisReader.read_full_ephemeris_table


Module Contents
---------------

.. py:class:: EphemerisDataReader(filename, inputformat, **kwargs)

   Bases: :py:obj:`sorcha.readers.ObjectDataReader.ObjectDataReader`


   A class to read in ephemeris from an external ephemeris file.

   Instead of subclassing the various readers (CSV, HDF5, etc.) individually, this class instantiates
   one of those classes in an internal ``reader`` attribute. As such all reading, validation, etc. is
   passed off to the ``reader`` object this object owns. While this adds a level of indirection, it
   allows us to support a cross product of N file types from M ephemeris generators with M + N readers
   instead of M * N.


   .. py:attribute:: reader
      :value: None



   .. py:method:: get_reader_info()

      Return a string identifying the current reader name
      and input information (for logging and output).

      :returns: The reader information.
      :rtype: string



   .. py:method:: _read_rows_internal(block_start=0, block_size=None, **kwargs)

      Reads in a set number of rows from the input.

      :param block_start: The 0-indexed row number from which
                          to start reading the data. For example in a CSV file
                          block_start=2 would skip the first two lines after the header
                          and return data starting on row=2. Default =0
      :type block_start: int, optional
      :param block_size: the number of rows to read in.
                         Use block_size=None to read in all available data.
                         Default = None
      :type block_size: int, optional
      :param \*\*kwargs: Extra arguments
      :type \*\*kwargs: dictionary, optional

      :returns: **res_df** -- dataframe of the object data.
      :rtype: Pandas dataframe



   .. py:method:: _read_objects_internal(obj_ids, **kwargs)

      Read in a chunk of data corresponding to all rows for
      a given set of object IDs.

      :param obj_ids: A list of object IDs to use.
      :type obj_ids: list
      :param \*\*kwargs: Extra arguments
      :type \*\*kwargs: dictionary, optional

      :returns: **res_df** -- The dataframe for the object data.
      :rtype: pandas dataframe



   .. py:method:: _process_and_validate_input_table(input_table, **kwargs)

      Perform any input-specific processing and validation on the input table.
      Modifies the input dataframe in place.

      :param input_table: A loaded table.
      :type input_table: Pandas dataframe
      :param \*\*kwargs: Extra arguments
      :type \*\*kwargs: dictionary, optional

      :returns: **input_table** -- Returns the input dataframe modified in-place.
      :rtype: Pandas dataframe

      .. rubric:: Notes

      The base implementation includes filtering that is common to most
      input types. Subclasses should call super.process_and_validate()
      to ensure that the ancestor’s validation is also applied.



.. py:function:: read_full_ephemeris_table(filename, inputformat)

   A helper function for testing that reads and returns an entire ephemeris table.

   :param filename: location/name of the data file.
   :type filename: string
   :param inputformat: format of input file ("whitespace"/"comma"/"csv"/"h5"/"hdf5").
   :type inputformat: string

   :returns: **res_df** -- dataframe of the object data.
   :rtype: pandas dataframe


