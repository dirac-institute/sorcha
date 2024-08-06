## README file for survey_setups folder

This directory contains configuration files that simulate Solar System surveys.

The user are encouraged to familiarise themselves with the documentation for 
a deeper understanding of different parameters. 

Currently, the directory contains the following files:


**Rubin_full_footprint.ini** -- The configuration file for the Vera C. Rubin Observatory's
Legacy Survey of Space and Time (LSST) using the full camera footprint.

**Rubin_circular_approximation.ini** -- The configuration file for the Vera C. Rubin Observatory's
Legacy Survey of Space and Time (LSST) using the circular footprint approximation
where the circular footprint matches 90% of the detector surface area.

**Rubin_known_object_prediction.ini** -- The configuration file for the Vera C. Rubin Observatory's
Legacy Survey of Space and Time (LSST) using the full camera footprint but with randomization,
fading function, vignetting, SSP linking, saturation limit and trailing losses off. This will output all detections
which lie on the CCD with unadulterated apparent magnitudes. This could thus be used to predict when 
and where known objects will appear in Rubin observations.

