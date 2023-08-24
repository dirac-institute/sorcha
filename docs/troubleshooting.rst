.. _troubleshooting:


Troubleshooting
=================

Have You Checked the Error Log File?
---------------------------------------------------------------
If sorcha runs successfully the .err log file created will be empty. If the software exited gracefully with an error it will print error statements to the error log file. If sorcha looks like it completed but you're not getting the expected output, the .err log file is the first place to check. 

Using Relative File Paths
---------------------------------------------------------------

We recommend using explicit file paths so ../this_directory will cause errors. It is best to give the full 
output and input paths for directories and input file/ouput file locations.


Running Multiple Instances With the Same Output Directories
---------------------------------------------------------------
If your output looks mixed up or garbled, double check that you are not running more than one Sorcha process with 
the same output path. You can **only run one** instance of Sorcha  at the same time for a given output directory. 
Otherwise, you run the risk of the output files being mixed up. If you want to run multiple versions of Sorcha on 
the same computer/compute node, make sure to update the output path in the config file or commandline arguments, 
as appropriate. We have developed tools and example slurm scripts to help you run multiple instances safely. 

Pointing Database 
---------------------

If you are having issues with reading the LSST pointing database such asgetting an error like::
  
   pandas.io.sql.DatabaseError: Execution failed on sql 'SELECT observationStartMJD, observationId FROM observations ORDER BY observationStartMJD': no such table: observations

Then it is likely that you are using the older or newer version of the (simulated) LSST pointing database. See  :ref:`database_query`

Mismatch in Inputs 
---------------------
There are several files associated with the synthetic small bodies  which are passed into Sorcha. These are
the orbit file, the physical parameter file and an optional complexy parameters file and optional ephemeris 
file (if not using the ephemeris generator within sorcha. Each provide specific information about the 
synthetic population that is being analysed. Within these files, it is necessary to specify an entry for every 
object. The Sorcha code will run a check to ensure that all entries have an associated orbit and 
physical/complex physical  parameter value, so if you get an error like::

   ERROR: PPCheckOrbitAndColourMatching: input colour/cometary parameter and orbit files do not match.

then make sure that for each file (orbit, ephemerides and phs) contains information 
for each object you wish to simulate.








