.. _configs:

Configuration File
=====================

Sorcha uses a configuration files to set the majority of the various parameters required for running these software packages. The configuration file for Sorcha allows turning on and off various filters for biasing the simulated small body population to what the survey should have found. An overview of the possible options for the configuration file are described below with recommendations on what you should set these config parameters to depending on your use case.

.. _example_configs:

Example Configuration Files
------------------------------------

The following sections show reasonable configuration files for various settings.

Rubin Full Footprint
~~~~~~~~~~~~~~~~~~~~~~

This configuration file is appropriate for running ``sorcha`` using the Rubin
full detector footprint.

.. literalinclude:: ../survey_setups/Rubin_full_footprint.ini
   :language: text
   :linenos:

Rubin Circular Approximation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This configuration file is appropriate for running ``sorcha`` using a circular 
approximation of the Rubin detector.

.. literalinclude:: ../survey_setups/Rubin_circular_approximation.ini
    :language: text
    :linenos:


