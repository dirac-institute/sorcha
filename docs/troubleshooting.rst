Troubleshooting
=================


Using Relative File Paths
---------------------------------------------------------------

OIF assumes explicit file paths so ../this_directory will cause errors. It is best to give the full output and input paths for directories and input file/ouput file locations.


Running Multiple Instances With the Same Output Directories
---------------------------------------------------------------
If your output looks mixed up or garbled, double check that you are not running more than one ObjectsInField or Sorcha process with the same output path. You can **only run one** instance of ObjectsInField or SurveySimPP at the same time for a given output directory. Otherwise, you run the risk of the output files being mixed up. If you want to run multiple versions of ObjectsInField/SurveySImPP on the same computer/compute node, make sure to update the output path in the config file or commandline arguments, as appropriate. We have developed tools and example slurm scripts to help you run multiple instances safely. 

Pointing Database 
---------------------

If you are having issues with reading the LSST pointing database such asgetting an error like::
  
   pandas.io.sql.DatabaseError: Execution failed on sql 'SELECT observationStartMJD, observationId FROM observations ORDER BY observationStartMJD': no such table: observations

Then it is likely that you are using the older or newer version of the (simulated) LSST pointing database. See  :ref:`database_query`

Mismatch in Inputs 
---------------------
There are several files which are passed into Sorcha. These are the 
orbit file, the physical parameter file and an optional cometary parameter file. Each provide
specific information about the synthetic population that is being analysed.

Within these files, it is necessary to specify an entry for every object. The Sorcha 
code will run a check to ensure that all entries have an associated 
orbit and physical/cometary parameter value, so if you get an error like::

   ERROR: PPCheckOrbitAndColourMatching: input colour/cometary parameter and orbit files do not match.

then make sure that for each file (orbit, ephemerides and physical/cometary parameters) contains information 
for each object you wish to simulate.








