sorcha.modules.PPCalculateApparentMagnitudeInFilter
===================================================

.. py:module:: sorcha.modules.PPCalculateApparentMagnitudeInFilter


Functions
---------

.. autoapisummary::

   sorcha.modules.PPCalculateApparentMagnitudeInFilter.PPCalculateApparentMagnitudeInFilter


Module Contents
---------------

.. py:function:: PPCalculateApparentMagnitudeInFilter(padain, function, observing_filters, colname='trailedSourceMagTrue', lightcurve_choice=None, cometary_activity_choice=None)

   The trailed source apparent magnitude is calculated in the filter for given H,
   phase function, light curve, and cometary activity parameters.

   Adds the following columns to the observations dataframe:

   - trailedSourceMagTrue
   - any columns created by the optional light curve and cometary activity models

   .. rubric:: Notes

   PPApplyColourOffsets should be run beforehand to apply any needed colour offset to H and ensure correct
   variables are present.

   The phase function model options utlized are the sbpy package's implementation:
       - HG:                Bowell et al. (1989) Asteroids II book.
       - HG1G2:             Muinonen et al. (2010) Icarus 209 542.
       - HG12:              Penttilä et al. (2016) PSS 123 117.
       - linear:             (as implemented in sbpy)
       - none :             No model is applied

   :param padain: Dataframe of observations.
   :type padain: Pandas dataframe
   :param function: Desired phase function model. Options are "HG", "HG12", "HG1G2", "linear", "none".
   :type function: string
   :param colname: Column name in which to store calculated magnitude to the padain dataframe.
                   Default = "TrailedSourceMag"
   :type colname: string
   :param lightcurve_choice: Choice of light curve model. Default = None
   :type lightcurve_choice: stringm optional
   :param cometary_activity_choice: Choice of cometary activity model. Default = None
   :type cometary_activity_choice: string, optional

   :returns: **padain** -- Dataframe of observations (padain) modified with calculated trailed
             source apparent magnitude column and any optional cometary actvity or
             light curve added columns based on the models used.
   :rtype: Pandas dataframe


