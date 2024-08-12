.. _configs:

Configuration File
=====================

Sorcha uses a configuration file to set the majority of the various required and optional parameters and well as providing the ability to turn on and off various filters applied to the simulated small body population. Details about the various settings and options available in the configuration files are described in the  :ref:`inputs`, :ref:`filters`, :ref:`ephemeris_gen`, and :ref:`output` pages. 

.. _example_configs:

Example Configuration Files
------------------------------------

The example configuration files are appropriate for setting up Sorcha to simulate what the LSST would discover. These examples come pre-installed with Sorcha. You use the **sorcha init** command on the terminal to copy these files to your working directory. 

Rubin Full Footprint
~~~~~~~~~~~~~~~~~~~~~~

This configuration file is appropriate for running ``sorcha`` using the Rubin
full detector footprint.

.. literalinclude:: ../src/sorcha/data/survey_setups/Rubin_full_footprint.ini
   :language: text
   :linenos:

Rubin Circular Approximation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This configuration file is appropriate for running ``sorcha`` using a circular 
approximation of the Rubin detector.

.. literalinclude:: ../src/sorcha/data/survey_setups/Rubin_circular_approximation.ini
    :language: text
    :linenos:

Rubin Known Object Prediction
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This configuration file is appropriate for running ``sorcha`` using the full camera footprint but with randomization,
fading function, vignetting, SSP linking, saturation limit and trailing losses off. This will output all detections
which lie on the CCD with unadulterated apparent magnitudes. This could thus be used to predict when 
and where known objects will appear in Rubin observations.

.. warning::
   As this configuration file turns off most of Sorcha's features, we strongly recommend you do not use it unless you are certain you know what you are doing.

.. literalinclude:: ../src/sorcha/data/survey_setups/Rubin_known_object_prediction.ini
    :language: text
    :linenos:
