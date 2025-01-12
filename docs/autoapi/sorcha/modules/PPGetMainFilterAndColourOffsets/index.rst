sorcha.modules.PPGetMainFilterAndColourOffsets
==============================================

.. py:module:: sorcha.modules.PPGetMainFilterAndColourOffsets


Functions
---------

.. autoapisummary::

   sorcha.modules.PPGetMainFilterAndColourOffsets.PPGetMainFilterAndColourOffsets


Module Contents
---------------

.. py:function:: PPGetMainFilterAndColourOffsets(filename, observing_filters, filesep)

   Function to obtain the main filter (i.e. the filter in which H is
   defined) from the header of the physical parameters file and then generate
   the expected colour offsets. Also makes sure that columns exist for all
   the expected colour offsets in the physical parameters file.

   :param filename: The filename of the physical parameters file.
   :type filename: string
   :param observing_filters: The observation filters requested in the configuration file.
   :type observing_filters: list of strings
   :param filesep: The format of the physical parameters file. Should be "csv"/"comma"
                   or "whitespace".
   :type filesep: string

   :returns: * **mainfilter** (*string*) -- The main filter in which H is defined.
             * **colour_offsets** (*list of strings*) -- A list of the colour offsets present in the physical parameters file.

   .. rubric:: Notes

   The main filter should be found as a column heading of H_[mainfilter]. If
   this format isn NOT followed, this function will error out.


