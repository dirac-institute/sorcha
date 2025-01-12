sorcha.modules.PPCalculateApparentMagnitude
===========================================

.. py:module:: sorcha.modules.PPCalculateApparentMagnitude


Functions
---------

.. autoapisummary::

   sorcha.modules.PPCalculateApparentMagnitude.PPCalculateApparentMagnitude


Module Contents
---------------

.. py:function:: PPCalculateApparentMagnitude(observations, phasefunction, mainfilter, othercolours, observing_filters, cometary_activity_choice=None, lightcurve_choice=None, verbose=False)

   This function applies the correct colour offset to H for the relevant filter, checks to make sure
   the correct columns are included (with additional functionality for colour-specific phase curves),
   then calculates the trailed source apparent magnitude including optional adjustments for
   cometary activity and rotational light curves.

   Adds the following columns to the observations dataframe:

   - H_filter
   - trailedSourceMagTrue
   - any columns created by the optional light curve and cometary activity models

   Removes the following columns from the observations dataframe:

   - Colour offset columns (i.e. u-r)
   - Colour-specific phase curve variables (if extant): the correct filter-specific value
   for each observation is located and stored instead. i.e. GS_r and GS_g columns will be deleted
   and replaced with a GS column containing either GS_r or GS_g depending on observation filter.

   :param observations: dataframe of observations.
   :type observations: Pandas dataframe
   :param phasefunction: Desired phase function model. Options are HG, HG12, HG1G2, linear, none
   :type phasefunction: string
   :param mainfilter: The main filter in which H is given and all colour offsets are calculated against.
   :type mainfilter: string
   :param othercolours: List of colour offsets present in input files.
   :type othercolours: list of strings
   :param observing_filters: List of observation filters of interest.
   :type observing_filters: list of strings
   :param cometary_activity_choice: Choice of cometary activity model.
                                    Default = None
   :type cometary_activity_choice: string
   :param lc_choice: Choice of lightcurve model. Default =  None
   :type lc_choice: string
   :param verbose: Flag for turning on verbose logging. Default = False
   :type verbose: boolean

   :returns: **observations** -- Modified observations pandas dataframe with calculated trailed source
             apparent magnitude column, H calculated in relevant filter (H_filter),
             renames the column for H in the main filter as H_original and
             adds a column for the light curve contribution to the trailed source
             apparent magnitude (if included)
   :rtype: Pandas dataframe


