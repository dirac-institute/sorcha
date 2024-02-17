.. _configs:

Configuration File
=====================

Sorcha uses a configuration files to set the majority of the various parameters required for running these software packages. The configuration file for Sorcha allows turning on and off various filters for biasing the simulated small body population to what the survey should have found. An overview of the possible options for the configuration file are described below with recommendations on what you should set these config parameters to depending on your use case.

.. tip::
  We have developed  a set of utilities that are installed alongside Sorcha that can generate some default config files for Sorcha (See :ref:`copy_configs`). 

.. _copy_configs:

Copy Example Configuration Files
------------------------------------

.. _example_configs:

Example Configuration Files
------------------------------------

The following sections show reasonable configuration files for various settings.

Rubin Full Footprint
~~~~~~~~~~~~~~~~~~~~~~

This configuration file is appropriate for running ``sorcha`` using the Rubin
full detector footprint.

The source code is available `here <https://github.com/dirac-institute/sorcha/blob/main/survey_setups/Rubin_full_footprint.ini>`__.

.. literalinclude:: ../survey_setups/Rubin_full_footprint.ini
   :language: text
   :linenos:

Rubin Circular Approximation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This configuration file is appropriate for running ``sorcha`` using a circular 
approximation of the Rubin detector.

The source code is available `here <https://github.com/dirac-institute/sorcha/blob/main/survey_setups/Rubin_circular_approximation.ini>`__.

.. literalinclude:: ../survey_setups/Rubin_circular_approximation.ini
    :language: text
    :linenos:


.. _database_query:

Setting Up the Correct LSST Pointing Database Query
---------------------------------------------------

Sorcha's **ppsqldbquery** config file parameter contain the sql query for obtaining this information from the pointing database.

From rubin_sim v2.0 simulations onward use the query::

  SELECT observationId, observationStartMJD as observationStartMJD_TAI, visitTime, filter, seeingFwhmGeom, seeingFwhmEff, fiveSigmaDepth, fieldRA, fieldDec, rotSkyPos FROM observations order by observationId

For past rubin_sim/OpSim simulations pre-v2.0 use the query::

  SELECT observationId, observationStartMJD as observationStartMJD_TAI, visitTime, filter, seeingFwhmGeom, seeingFwhmEff, fiveSigmaDepth, fieldRA, fieldDec, rotSkyPos FROM SummaryAllProps order by observationId


