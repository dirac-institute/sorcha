# TEST FILES/DATA README

The data within this folder is used by the unit tests, located in .../tests/*/*.

## Files:

**baseline_10klines_2.0.db**  
Small (10k lines) version of pointing database located at /demo/baseline_v2.0_1yr.db.  
Used by:  
- test_createResultsSQLDatabase.py
- test_makeConfigPP.py  
- test_makeConfigOIF.py  
- test_makeMultiConfigOif.py  
- test_makeSLURMscript.py  
- test_PPReadAllInput.py  
- test_PPReadPointingDatabase.py

**config_test\*.ini**  
Example OIF config files with standardised names.  
Used by:  
- test_makeMultiConfigOIF.py  
- test_makeSLURMscript.py

**detectors_corners.csv**  
Corners of the LSST camera footprint.  
Used by:  
- test_makeConfigPP.py  
- test_PPFootprintFilter.py

**lsst-total-r.dat**  
Throughput of LSST per wavelength.  
Used by:  
- /sorcha/lsstcomet/tests/test_model.py

**makeConfigOIF_*.ini**  
Example OIF config files.  
Used by:  
- test_makeConfigOIF.py

**makeConfigPP_ini**  
Example SSPP config file.  
Used by:  
- test_makeConfigPP.py

**makeMultiConfigOIF_test\*.ini**  
Example OIF config files.  
Used by:  
- test_makeMultiConfigOIF.py

**makeSLURMscript_*.sh**  
Example SLURM scripts.  
Used by:  
- test_makeSLURMscript.py

**oif_temptest.csv**  
Example OIF output with standardised name.  
Used by:  
- test_createTemporaryDatabases.py

**oiftestoutput_header.csv**
Example OIF output with extended header.  
Used by:  
- test_PPReadOif.py

**oiftestoutput.csv**  
Example OIF output in .csv format.  
Used by:  
- test_PPReadOif.py

**oiftestoutput.txt**  
Example OIF output, whitespace-separated.  
Used by:  
- test_createResultsSQLDatabase.py  
- test_makeConfigOIF.py  
- test_PPJoinEphemeridesAndOrbits.py  
- test_PPReadEphemerides.py  
- test_PPReadOif.py

**orbits_test\*.txt**  
Example orbits files with standardised names.  
Used by:  
- test_makeMultiConfigOIf.py  
- test_makeSLURMscript.py

**params_test\*.txt**  
Example physical parameters files with standardised names.
Used by:  
- test_makeMultiConfigOIf.py  
- test_makeSLURMscript.py

**PPReadAllInput_oif.txt**  
Example OIF output, compatible with pointing database.  
Used by:  
- test_PPReadAllInput.py

**PPReadAllInput_orbits.des**  
Example orbits file, compatible with pointing database.  
Used by:  
- test_PPReadAllInput.py

**PPReadAllInput_params.txt**  
Example physical parameters file, compatible with pointing databse.  
Used by:  
- test_PPReadAllInput.py

**PPReadOrbitFile_bad.txt**  
Example orbits file with bad column headers.  
Used by:  
- test_PPReadOrbitFile.py

**sqlresults.db**  
Example output in SQL database form.  
Used by:  
- test_createResultsSQLDatabase.py  
- test_PPCommandLineParser

**test_input_fullobs.csv**  
Example of full dataframe of observations created by sorcha.py.  
Used by: 
- test_PPApplyFOVFilter.py   
- test_PPCommandLineParser.py  
- test_PPConfigParser.py  
- test_PPDropObservations.py  
- test_PPFootprintFilter.py  
- test_PPLinkingFilter.py

**test_PPConfig.ini**  
Example SSPP config file.  
Used by:  
- test_makeSLURMscript.py  
- test_PPCommandLineParser.py  
- test_PPConfigParser.py  
- test_PPOutput.py  
- test_PPRandomizeMeasurements.py 
- test_PPReadAllInput.py

**test_PPPrintConfigsToLog.txt**  
Example of an SSPP log file.  
Used by:  
- PPPrintConfigsToLog.py

**testcolour.csv**  
Example physical parameters file, .csv format.  
Used by:  
- test_PPreadPhysicalParameters.py

**testcolour.txt**  
Example physical parameters file, whitespace-separated.  
Used by:  
- test_createResultsSQLDatabase.py  
- test_PPCheckInputObjectIDs.py  
- test_PPCommandLineParser.py  
- test_PPConfigParser.py  
- test_PPGetMainFilterAndColourOffsets.py  
- test_PPJoinEphemeridesAndParameters.py  
- test_PPReadOif.py  
- test_PPReadPhysicalParameters.py  
- test_PPReadTemporaryEphemerisDatabase.py

**testcomet.txt**  
Example cometary parameters file.  
Used by:  
- test_PPReadCometaryParameters.py

**testobs_clean.csv**  
Reduced version of test_input_fullobs.csv.  
Used by:  
- test_createResultsSQLDatabase.py

**testorb.csv**  
Example orbits file, .csv format.  
Used by:  
- test_PPReadOrbitFile.py

**testorb.des**  
Example orbits file, whitespace-separated.  
Used by:  
- test_createResultsSQLDatabase.py  
- test_makeConfigOIF.py  
- test_makeMultiConfigOIf.py  
- test_PPCheckInputObjectIDs.py  
- test_PPCommandLineParser.py  
- test_PPConfigParser.py  
- test_PPJoinEphemeridesAndOrbits.py
