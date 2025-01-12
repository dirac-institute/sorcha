sorcha.readers.DatabaseReader
=============================

.. py:module:: sorcha.readers.DatabaseReader


Classes
-------

.. autoapisummary::

   sorcha.readers.DatabaseReader.DatabaseReader


Module Contents
---------------

.. py:class:: DatabaseReader(intermdb, **kwargs)

   Bases: :py:obj:`sorcha.readers.ObjectDataReader.ObjectDataReader`


   A class to read in object data stored in a sqlite database.


   .. py:attribute:: intermdb


   .. py:method:: get_reader_info()

      Return a string identifying the current reader name
      and input information (for logging and output).

      :returns: **name** -- The reader information.
      :rtype: string



   .. py:method:: _read_rows_internal(block_start=0, block_size=None, **kwargs)

      Reads in a set number of rows from the input.

      :param block_start: The 0-indexed row number from which
                          to start reading the data. For example in a CSV file
                          block_start=2 would skip the first two lines after the header
                          and return data starting on row=2. Default=0
      :type block_start: integer, optional
      :param block_size: the number of rows to read in.
                         Use block_size=None to read in all available data.
                         A non-None block size must be provided if block_start > 0.
                         Default = None
      :type block_size: int, optional
      :param \*\*kwargs: Extra arguments
      :type \*\*kwargs: dictionary, optional

      :returns: **res_df** -- dataframe of the object data.
      :rtype: pandas dataframe

      .. rubric:: Notes

      A non-None block size must be provided if block_start > 0.



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
      :type input_table: pandas dataframe
      :param \*\*kwargs: Extra arguments
      :type \*\*kwargs: dictionary, optional

      :returns: **input_table** -- Returns the input dataframe modified in-place.
      :rtype: pandas dataframe



