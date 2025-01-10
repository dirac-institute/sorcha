.. _configs:

Configuration File
=====================

``Sorcha`` uses a configuration file to set the majority of the various required and optional parameters as well as providing the ability to turn on and off various calculations and filters applied to the input small body population. Details about the various settings and options available in the configuration files are described in the  :ref:`inputs`,:ref:`ephemeris_gen`, :ref:`post_processing' and :ref:`output` pages. 


The configuration file is using the Windowst INI file format. The configuration file is formatted into distinct sections with headers. The headers are enclosed in squarebrackets ([]). Below each header are the asosciated configuration variable key pair (e.g. configvariablename = value). Any lines started with '#' are considered comments and ignored when parsing the cofiguration file. 

The presence or absence of various variables in the configuration file will turn on/off or inializie diifferent functions and features witin``Sorcha``. 


.. attention::
   Use the **-c** flag on the command line to specify the configuration file  that ``Sorcha`` should use.
 
.. _example_configs:

Example Configuration Files
------------------------------------

We provide below example configuration files  appropriate for setting up ``Sorcha`` to simulate what the LSST would discover. These example config files come installed with ``Sorcha`` and can be copied over to your working directory by typing on the command line::

    sorcha init 

Rubin Full Footprint
~~~~~~~~~~~~~~~~~~~~~~

This configuration file is appropriate for running ``Sorcha`` using the Rubin
full detector footprint.

.. literalinclude:: ../src/sorcha/data/survey_setups/Rubin_full_footprint.ini
   :language: text
   :linenos:

Rubin Circular Approximation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This configuration file is appropriate for running ``Sorcha`` using a circular 
approximation of the Rubin detector.

.. literalinclude:: ../src/sorcha/data/survey_setups/Rubin_circular_approximation.ini
    :language: text
    :linenos:

Rubin Known Object Prediction
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This configuration file is appropriate for running ``Sorcha`` using the full camera footprint but with randomization,
fading function, vignetting, SSP linking, saturation limit and trailing losses off. This will output all detections
which lie on the CCD with unadulterated apparent magnitudes. This could thus be used to predict when 
and where known objects will appear in Rubin observations.

.. warning::
   As this configuration file turns off most of Sorcha's features, we strongly recommend you do not use it unless you are certain you know what you are doing.

.. literalinclude:: ../src/sorcha/data/survey_setups/Rubin_known_object_prediction.ini
    :language: text
    :linenos:
