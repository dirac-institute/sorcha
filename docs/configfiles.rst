.. _configs:

Configuration File
=====================

``Sorcha`` uses a configuration file to set the majority of the various required and optional parameters as well as providing the ability to turn on and off various calculations and filters applied to the input small body population. Details about the main settings and options available in the configuration files are described in the  :ref:`inputs`, :ref:`ephemeris_gen`, :ref:`post_processing` and :ref:`output` pages. 


The configuration file is using the Windowst INI file format. The configuration file is formatted into distinct sections with headers. The headers are enclosed in square brackets ([]). Below each header are the associated configuration variable key pair (e.g. configvariablename = value). Any lines started with '#' are considered comments and ignored when parsing the cofiguration file. 

The presence or absence of various variables in the configuration file will turn on/off or initialize different functions and features within ``Sorcha``. 


.. attention::
   Use the **-c (--config)** flag when using the **sorcha run** command on the terminal to specify the configuration file  that ``Sorcha`` should use.
 
.. _example_configs:

Example Configuration Files
------------------------------------

We provide below example configuration files  appropriate for setting up ``Sorcha`` to simulate what the LSST would discover. These example config files come installed with ``Sorcha`` and can be copied over to your working directory by typing on the command line::

    sorcha init 

Rubin Full Footprint
~~~~~~~~~~~~~~~~~~~~~~

This configuration file is appropriate for running ``Sorcha`` using the Rubin LSSTCam (LSST Camera) full detector footprint.

.. literalinclude:: ../src/sorcha/data/survey_setups/Rubin_full_footprint.ini
   :language: text
   :linenos:

Rubin Circular Approximation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This configuration file is appropriate for running ``Sorcha`` using a circular 
approximation of the Rubin LSSTCam (LSST Camera) field-of-view (FOV).

.. literalinclude:: ../src/sorcha/data/survey_setups/Rubin_circular_approximation.ini
    :language: text
    :linenos:

.. _known_config:

Rubin Known Object Prediction
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This configuration file is appropriate for running ``Sorcha`` using the full camera footprint but with randomization,
applying the fading function, accounting for vignetting, applying the linking filter, using the  saturation limit filter, and accounting for trailing losses all turned off. This will output all potential detections of the input population 
which lie on the LSSTCam (LSST Camera) CCDs (Charged Couple Devices) with unadulterated apparent magnitudes. This could thus be used to predict when 
and where known objects will land in LSST  observations.

.. warning::
   As this configuration file turns off most of Sorcha's features, we strongly recommend you **do not** use this example  configuration file unless you are certain that this is what you need out of ``Sorcha``.  

.. literalinclude:: ../src/sorcha/data/survey_setups/Rubin_known_object_prediction.ini
    :language: text
    :linenos:
