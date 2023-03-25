# DEMO NOTEBOOKS README

## Files:

**OIFconfig_test.ini** - example OIF config file  
**PPConfig_test.ini** - example SSPP config file  


**baseline_v2.0_1yr.db** - example pointing database  
**sspp_testset_colours.txt** - example parameters input.  
**sspp_testset_orbits.des** - example orbits input   
**example_oif_output.txt** - example OIF input  
**test_ssp_output.csv** - example output  


**footprintFilterValidationObservations.csv** - needed for demo notebook  
**uncertaintiesDemo.csv** - needed for demo notebook  
**lsst-total-r.dat** - needed for demo notebook
**oneline_v2.0.db** - needed for demo notebook


## Notebooks:

demo_ApparentMagnitudeValidation
- **Validates:** PPCalculateApparentMagnitudeInFilter.
- **Files:** none

demo_CalculateSimpleCometaryMagnitude
- **Validates:** PPCalculateSimpleCometaryMagnitude
- **Files:** lsst-total-r.dat

demo_CircleFootprint
- **Validates:** PPCircleFootprint
- **Files:** footprintFilterValidationObservations.csv, oneline_v2.0.db

demo_DetectionEfficiencyValidation
- **Validates:** PPFadingFunctionFilter
- **Files:** oneline_v2.0.db

demo_footprintFilter
- **Validates:** PPFootprintFilter
- **Files:** footprintFilterValidationObservations.csv, oneline_v2.0.db

demo_MagnitudeAndSNRCuts
- **Validates:** PPBrightLimit, PPMagnitudeLimit, PPSNRLimit
- **Files:** none

demo_TrailingLossesValidation
- **Validates:** PPTrailingLoss
- **Files:** none

demo_UncertaintiesAndRandomization
- **Validates:** PPAddUncertainty, PPRandomizeMeasurements
- **Files:** uncertaintiesDemo.csv
