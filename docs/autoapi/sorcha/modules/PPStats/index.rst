sorcha.modules.PPStats
======================

.. py:module:: sorcha.modules.PPStats


Functions
---------

.. autoapisummary::

   sorcha.modules.PPStats.stats


Module Contents
---------------

.. py:function:: stats(observations, statsfilename, outpath, sconfigs)

   Write a summary statistics file including whether each object was linked
   or not within miniDifi, their number of observations, min/max phase angles,
   min/max trailed source magnitudes, and median trailed source magnitudes
   per filter

   :param observations: Pandas dataframe of observations
   :type observations: Pandas dataframe
   :param statsfilename: Stem filename to write summary stats file to
   :type statsfilename: string
   :param sconfigs: Dataclass of configuration file arguments.
   :type sconfigs: dataclass

   :rtype: None.


