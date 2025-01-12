sorcha.modules.PPApplyColourOffsets
===================================

.. py:module:: sorcha.modules.PPApplyColourOffsets


Functions
---------

.. autoapisummary::

   sorcha.modules.PPApplyColourOffsets.PPApplyColourOffsets


Module Contents
---------------

.. py:function:: PPApplyColourOffsets(observations, function, othercolours, observing_filters, mainfilter)

   Adds the correct colour offset to H based on the filter of each observation,
   then checks to make sure the appropriate columns exist for each phase function model.
   If phase model variables exist for each colour, this function also selects the
   correct variables for each observation based on filter.

   Adds the following columns to the observations dataframe:

   - H_filter

   Removes the following columns from the observations dataframe:

   - Colour offset columns (i.e. u-r, g-r)
   - Colour-specific phase curve variables (if extant): the correct filter-specific value
   for each observation is located and stored instead. i.e. GS_r and GS_g columns will be deleted
   and replaced with a GS column containing either GS_r or GS_g depending on observation filter.

   :param observations: dataframe of observations.
   :type observations: Pandas dataframe
   :param function: string of desired phase function model. Options are HG, HG12, HG1G2, linear, H.
   :type function: string
   :param othercolours: list of colour offsets present in input files.
   :type othercolours: list of strings
   :param observing_filters: list of observation filters of interest.
   :type observing_filters: list of strings
   :param mainfilter: the main filter in which H is given and all colour offsets are calculated against.
   :type mainfilter: string

   :returns: **observations** -- observations dataframe modified with H calculated in relevant filter (H_filter)
             The dataframe has also been modified to have the appropriate phase curve filter specific values/columns.
   :rtype: Pandas dataframe


