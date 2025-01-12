sorcha.readers.HDF5Reader
=========================

.. py:module:: sorcha.readers.HDF5Reader


Classes
-------

.. autoapisummary::

   sorcha.readers.HDF5Reader.HDF5DataReader


Module Contents
---------------

.. py:class:: HDF5DataReader(filename, **kwargs)

   Bases: :py:obj:`sorcha.readers.ObjectDataReader.ObjectDataReader`


   A class to read in object data files stored as HDF5 files.


   .. py:attribute:: filename


   .. py:attribute:: obj_id_table
      :value: None



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
                         Default = None
      :type block_size: integer, optional
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
      :rtype: Pandas dataframe



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



