sorcha.readers.CSVReader
========================

.. py:module:: sorcha.readers.CSVReader


Classes
-------

.. autoapisummary::

   sorcha.readers.CSVReader.CSVDataReader


Module Contents
---------------

.. py:class:: CSVDataReader(filename, sep='csv', header=-1, **kwargs)

   Bases: :py:obj:`sorcha.readers.ObjectDataReader.ObjectDataReader`


   A class to read in object data files stored as CSV or whitespace
   separated values.

   Requires that the file's first column is ObjID.


   .. py:attribute:: filename


   .. py:attribute:: sep
      :value: 'csv'



   .. py:attribute:: header_row


   .. py:attribute:: obj_id_table
      :value: None



   .. py:method:: get_reader_info()

      Return a string identifying the current reader name
      and input information (for logging and output).

      :returns: **name** -- The reader information.
      :rtype: string



   .. py:method:: _find_and_validate_header_line(header=-1)

      Read and validate the header line. If no line number is provided, use
      a heuristic match to find the header line. This is used in cases
      where the header is not the first line and we want to skip down.

      :param header: The row number of the header. If not provided, does an automatic search.
                     Default = -1
      :type header: integer, optional

      :returns: The line index of the header.
      :rtype: integer



   .. py:method:: _check_header_line(header_line)

      Check that a given header line is valid and exit if it is invalid.

      :param header_line: The proposed header line.
      :type header_line: str



   .. py:method:: _read_rows_internal(block_start=0, block_size=None, **kwargs)

      Reads in a set number of rows from the input.

      :param block_start: The 0-indexed row number from which
                          to start reading the data. For example in a CSV file
                          block_start=2 would skip the first two lines after the header
                          and return data starting on row=2. Default =0
      :type block_start: integer, optional
      :param block_size: The number of rows to read in.
                         Use block_size=None to read in all available data.
                         default =None
      :type block_size: integer, optional, default=None
      :param \*\*kwargs: Extra arguments
      :type \*\*kwargs: dictionary, optional

      :returns: **res_df** -- Dataframe of the object data.
      :rtype: pandas dataframe



   .. py:method:: _build_id_map()

      Builds a table of just the object IDs



   .. py:method:: _read_objects_internal(obj_ids, **kwargs)

      Read in a chunk of data for given object IDs.

      :param obj_ids: A list of object IDs to use.
      :type obj_ids: list
      :param \*\*kwargs: Extra arguments
      :type \*\*kwargs: dictionary, optional

      :returns: **res_df** -- The dataframe for the object data.
      :rtype: pandas dataframe



   .. py:method:: _process_and_validate_input_table(input_table, **kwargs)

      Perform any input-specific processing and validation on the input table.
      Modifies the input dataframe in place.

      .. rubric:: Notes

      The base implementation includes filtering that is common to most
      input types. Subclasses should call super.process_and_validate()
      to ensure that the ancestor’s validation is also applied.

      :param input_table: A loaded table.
      :type input_table: Pandas dataframe
      :param \*\*kwargs: Extra arguments
      :type \*\*kwargs: dictionary, optional

      :returns: **input_table** -- Returns the input dataframe modified in-place.
      :rtype: pandas dataframe



