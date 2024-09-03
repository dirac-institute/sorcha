# TEST FILES/DATA README

The data within this folder is used by the unit tests, located in .../tests/\*/'*\
In some cases the location of the given file is used in the test, rather than its contents.

## Files:

**baseline_10klines_2.0.db**  
Small (10k lines) version of pointing database located at /demo/baseline_v2.0_1yr.db.  
Used by:  
- test_combined_data_reading.py
- test_createResultsSQLDatabase.py  
- test_PPCommandLineParser.py
- test_PPConfigParser.py
- test_PPMatchPointingToObservations.py
- test_PPReadAllInput.py  
- test_PPReadPointingDatabase.py

**config_for_ephemeris_init_test.ini**  
Config file for ephemeris end-to-end unit test.  
Used by:  
- test_demo_end2end.py

**detectors_corners.csv**  
Corners of the LSST camera footprint.  
Used by:  
- test_PPApplyFOVFilter.py
- test_PPConfigParser.py
- test_PPFootprintFilter.py

**goldens/out_end2end.csv**  
Golden or "ideal" output used to check end-to-end test results.  
Used by:  
- test_demo_end2end.py  

**goldens/sorcha_ephemeris.csv**  
Golden or "ideal" ephemeris output used to check end-to-end test results.  
Used by:  
- test_demo_end2end.py  

**goldens/verification_truth.csv**  
Golden or "ideal" output used to validate end-to-end test results.  
Used by:  
- test_demo_end2end.py  

**ObsCodes_test.json**  
Example MPC-style observatory codes files.  
Used by:  
- test_simulation_parsing.py

**oiftestoutput_comment.csv**  
Example ephemeris output in .csv format when the columns are not the start of row 0 but later in the file after a header.  
Used by:  
- tests/readers/test_CSVReader.py

**oiftestoutput.csv**  
Example ephemeris output in .csv format.  
Used by:  
- test_CSVReader.py  
- test_OIFReader.py

**oiftestoutput.h5**  
Example ephemeris output, in HDF5 format.  
Used by:  
- test_OIFReader.py  
- tests/readers/test_HDF5Reader.py

**oiftestoutput.txt**  
Example ephemeris output, whitespace-separated.  
Used by:  
- test_CombinedDataReader.py  
- test_OIFReader.py  
- test_PPCommandLineParser.py  
- test_PPCheckInputObjectIDs.py  
- test_PPJoinEphemeridesAndOrbits.py  
- test_PPJoinEphemeridesAndParameters.py  

**orbit_test_files/orbit_bcart.csv**  
Barycentric cartesian orbit format test input file.  
Used by:  
- test_OrbitAuxReader.py

**orbit_test_files/orbit_bcom.csv**  
Barycentric cometary orbit format test input file.  
Used by:  
- test_OrbitAuxReader.py

**orbit_test_files/orbit_bkep.csv**  
Barycentric Keplarian orbit format test input file.  
Used by:  
- test_OrbitAuxReader.py

**orbit_test_files/orbit_cart.csv**  
Heliocentric cartesian orbit format test input file.  
Used by:  
- test_OrbitAuxReader.py

**orbit_cart_wrong_cols.csv**  
Heliocentric cartesian orbit format test input file with incorrect headers.  
Used by:  
- test_OrbitAuxReader.py

**orbit_test_files/orbit_com.csv**  
Heliocentric cometary orbit format test input file.  
Used by:  
- test_OrbitAuxReader.py

**orbit_test_files.orbit_com_wrong_cols.csv**  
Heliocentric cometary orbit format test input file with incorrect columns.  
Used by:  
- test_OrbitAuxReader.py

**orbit_test_files/orbit_extra_cols.csv**  
Heliocentric cartiesian orbit format test input file with extra columns.  
Used by:  
- test_OrbitAuxReader.py

**orbit_test_files/orbit_kep.csv**  
Heliocentric Keplarian orbit format test input file.  
Used by:  
- test_OrbitAuxReader.py

**orbit_test_files/orbit_kep_wrong_cols.csv**  
Heliocentric Keplerian orbit format test input file with incorrect columns.  
Used by:  
- test_OrbitAuxReader.py

**orbit_test_files/orbit_unknown_format.csv**  
Orbit input file with unallowed orbit format.  
Used by:  
- test_OrbitAuxReader.py

**orbits_small_random_mpcorb.csv**  
Random set of MPCORB orbits used in ephemeris end-to-end test.  
Used by:  
- test_demo_end2end.py

**params_small_random_mpcorb.csv**  
Random set of MPCORB orbits used in ephemeris end-to-end test.  
Used by:  
- test_demo_end2end.py

**PPConfig_goldens_test.ini**  
Configuration file used in generation of goldens and end-to-end tests.  
Used by:  
- test_demo_end2end.py

**PPConfig_test_chunked.ini**  
Configuration file used to check chunked vs. unchunked Sorcha output.  
Used by:  
- test_demo_chunking.py

**PPConfig_test_unchunked.ini**  
Configuration file used to check chunked vs. unchunked Sorcha output.  
Used by:  
- test_demo_chunking.py

**PPReadAllInput_oif.txt**  
Example OIF output, compatible with pointing database.  
Used by:  
- test_combined_data_reading.py
- test_CombinedDataReader.py

**PPReadAllInput_orbits.des**  
Example orbits file, compatible with pointing database.  
Used by:  
- test_combined_data_reading.py  
- test_CombinedDataReader.py  
- test_ephemeris_generation.py  
- test_pixdict.py

**PPReadAllInput_params.txt**  
Example physical parameters file, compatible with pointing databse.  
Used by:  
- test_combined_data_reading.py  
- test_CombinedDataReader.py  
- test_ephemeris_generation.py  
- test_pixdict.py

**PPReadOrbitFile_bad_format.csv**  
Example orbits file with bad formatting.  
Used by:  
- test_OrbitAuxReader.py

**PPReadOrbitFile_bad.txt**  
Example orbits file with bad column headers.  
Used by:  
- test_OrbitAuxReader.py

**run_1/testrun_1-sorcha.log**  
Sorcha log file for a successful run.  
Used by:  
- test_check_output_logs.py

**run_2/testrun_2-sorcha.log**  
Sorcha log file for an unsuccessful run.  
Used by:  
- test_check_output_logs.py

**sorcha_logs_expected.csv**  
Test output for check_output_logs utility.  
Used by:  
- test_check_output_logs.py

**sql_results/orbits_test1.txt**  
Example orbits files with standardised names.  
Used by:  
- test_createResultsSQLDatabase.py

**sql_results/orbits_test2.txt**  
Example orbits files with standardised names.  
Used by:  
- test_createResultsSQLDatabase.py

**sql_results/params_test1.txt**  
Example physical parameters files with standardised names.  
Used by:  
- test_createResultsSQLDatabase.py

**sql_results/params_test2.txt**  
Example physical parameters files with standardised names.  
Used by:  
- test_createResultsSQLDatabase.py

**sql_results/sqlresults.db**  
Example sorcha output in SQL database form.  
Used by:  
- test_createResultsSQLDatabase.py

**test_ephem_config.ini**  
Configuration file used in testing ephemeris generation.  
Used by:  
- test_ephemeris_generation.py

**test_input_fullobs.csv**  
Example of full dataframe of observations created by sorcha.py.  
Used by:  
- test_PPApplyFOVFilter.py   
- test_PPCommandLineParser.py  
- test_PPConfigParser.py  
- test_PPDropObservations.py  
- test_PPFootprintFilter.py  
- test_PPOutput.py  
- test_PPRandomizeMeasurements.py

**test_PPConfig.ini**  
Test Sorcha config file.  
Used by:  
- test_combined_data_reading.py  
- test_PPCommandLineParser.py  
- test_PPConfigParser.py

**test_PPPrintConfigsToLog.txt**  
Example of an SSPP log file.  
Used by:  
- test_PPConfigParser.py

**testcolour.csv**  
Example physical parameters file, .csv format.  
Used by:  
- test_CSVReader.py

**testcolour.txt**  
Example physical parameters file, whitespace-separated.  
Used by:  
- test_createResultsSQLDatabase.py  
- test_CSVReader.py  
- test_HDF5Reader.py  
- test_OIFReader.py  
- test_PPCheckInputObjectIDs.py  
- test_PPCommandLineParser.py  
- test_PPConfigParser.py  
- test_PPGetMainFilterAndColourOffsets.py  
- test_PPJoinEphemeridesAndParameters.py  

**testcomet.txt**  
Example cometary parameters file.  
Used by:  
- test_CSVReader.py
- test_PPCommandLineParser.py

**test_ephem_config.ini**  
Example Sorcha config file with ephemeris keywords.  
Used by:  
 - test_ephemeris_generation.py

**testobs_clean.csv**  
Reduced version of test_input_fullobs.csv.  
Used by:  
- test_createResultsSQLDatabase.py

**testdb_PPIntermDB.db**  
SQL database of ephemeris output. Functionality no longer used but kept in for possible future software development.  
Used by:  
- test_DatabaseReader.py

**testorb.csv**  
Example orbits file, .csv format.  
Used by:  
- test_CSVReader.py
- test_OrbitAuxReader.py

**testorb.des**  
Example orbits file, whitespace-separated.  
Used by:  
- test_createResultsSQLDatabase.py
- test_CSVReader.py
- test_OrbitAuxReader.py 
- test_PPCheckInputObjectIDs.py
- test_PPCommandLineParser.py
- test_PPConfigParser.py
- test_PPJoinEphemeridesAndOrbits.py

**verification_colors.txt**
Test physical parameters file used in the validation end-to-end test.  
Used by:  
- test_demo_end2end.py

**verification_orbits.txt**
Test orbits file used in the validation end-to-end test.  
Used by:  
- test_demo_end2end.py

**verification.init**
Test configuration file used in the validation end-to-end test.  
Used by:  
- test_demo_end2end.py