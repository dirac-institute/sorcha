sorcha.readers.OrbitAuxReader
=============================

.. py:module:: sorcha.readers.OrbitAuxReader


Classes
-------

.. autoapisummary::

   sorcha.readers.OrbitAuxReader.OrbitAuxReader


Module Contents
---------------

.. py:class:: OrbitAuxReader(filename, sep='csv', header=-1, **kwargs)

   Bases: :py:obj:`sorcha.readers.CSVReader.CSVDataReader`


   A class to read in the auxiliary orbit data files.


   .. py:method:: get_reader_info()

      Return a string identifying the current reader name
      and input information (for logging and output).

      :returns: The reader information.
      :rtype: string



   .. py:method:: _process_and_validate_input_table(input_table, **kwargs)

      Perform any input-specific processing and validation on the input table.
      Modifies the input dataframe in place.

      :param input_table: A loaded table.
      :type input_table: pandas dataframe
      :param \*\*kwargs:
      :type \*\*kwargs: dictionary, optional

      :returns: **res_df** -- Returns the input dataframe modified in-place.
      :rtype: pandas dataframe

      .. rubric:: Notes

      The base implementation includes filtering that is common to most
      input types. Subclasses should call super.process_and_validate()
      to ensure that the ancestor’s validation is also applied.



