sorcha.modules.PPReadPointingDatabase
=====================================

.. py:module:: sorcha.modules.PPReadPointingDatabase


Functions
---------

.. autoapisummary::

   sorcha.modules.PPReadPointingDatabase.PPReadPointingDatabase


Module Contents
---------------

.. py:function:: PPReadPointingDatabase(bsdbname, observing_filters, dbquery, surveyname)

   Reads in the pointing database as a Pandas dataframe.

   :param bsdbname: File location of pointing database.
   :type bsdbname: string
   :param observing_filters: List of observation filters of interest.
   :type observing_filters: list of strings
   :param dbquery: Databse query to perform on pointing database.
   :type dbquery: string

   :returns: **dfo** -- Dataframe of pointing database.
   :rtype: pandas dataframe


