sorcha.readers.ObjectDataReader
===============================

.. py:module:: sorcha.readers.ObjectDataReader

.. autoapi-nested-parse::

   Base class for reading object-related data from a variety of sources
   and returning a pandas data frame.

   Each subclass of ObjectDataReader must implement at least the functions
   _read_rows_internal and _read_objects_internal, both of which return a
   pandas data frame. Each data source needs to have a column ObjID that
   identifies the object and can be used for joining and filtering.

   Caching is implemented in the base class. This will lazy load the full
   table into memory from the chosen data source, so it should only be
   used with smaller data sets. Both ``read_rows`` and ``read_objects``
   will check for a cached table before reading the files, allowing them
   to perform direct pandas operations if the data is already in memory.



Classes
-------

.. autoapisummary::

   sorcha.readers.ObjectDataReader.ObjectDataReader


Module Contents
---------------

.. py:class:: ObjectDataReader(cache_table=False, **kwargs)

   Bases: :py:obj:`abc.ABC`


   The base class for reading in the object data.


   .. py:attribute:: _cache_table
      :value: False



   .. py:attribute:: _table
      :value: None



   .. py:method:: get_reader_info()
      :abstractmethod:


      Return a string identifying the current reader name
      and input information (for logging and output).

      :returns: **name** -- The reader information.
      :rtype: str



   .. py:method:: read_rows(block_start=0, block_size=None, **kwargs)

      Reads in a set number of rows from the input, performs
      post-processing and validation, and returns a data frame.

      :param block_start: The 0-indexed row number from which
                          to start reading the data. For example in a CSV file
                          block_start=2 would skip the first two lines after the header
                          and return data starting on row=2. Default=0
      :type block_start: int (optional)
      :param block_size: the number of rows to read in.
                         Use block_size=None to read in all available data.
                         Default = None
      :type block_size: int (optional)
      :param \*\*kwargs: Extra arguments
      :type \*\*kwargs: dictionary, optional

      :returns: **res_df** -- dataframe of the object data.
      :rtype: Pandas dataframe



   .. py:method:: _read_rows_internal(block_start=0, block_size=None, **kwargs)
      :abstractmethod:


      Function to do the actual source-specific reading.



   .. py:method:: read_objects(obj_ids, **kwargs)

      Read in a chunk of data corresponding to all rows for
      a given set of object IDs.

      :param obj_ids: A list of object IDs to use.
      :type obj_ids: list
      :param \*\*kwargs: Extra arguments
      :type \*\*kwargs: dictionary, optional

      :returns: **res_df** -- The dataframe for the object data.
      :rtype: Pandas dataframe



   .. py:method:: _read_objects_internal(obj_ids, **kwargs)
      :abstractmethod:


      Function to do the actual source-specific reading.



   .. py:method:: _validate_object_id_column(input_table)

      Checks that the object ID column exists and converts it to a string.
      This is the common validity check for all object data tables.

      :param input_table: A loaded table.
      :type input_table: Pandas dataframe

      :returns: **input_table** -- Returns the input dataframe modified in-place.
      :rtype: Pandas dataframe



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

      Additional arguments to use:

      disallow_nan : boolean
          if True then checks the data for  NaNs or nulls.



