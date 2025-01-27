.. _troubleshooting:


Troubleshooting
=================

Have You Checked the Error Log File?
---------------------------------------------------------------
If ``Sorcha`` runs successfully the .err log file created will be empty. If the software exited gracefully with an error it will print error statements to the error log file. If ``Sorcha'' looks like it completed but you're not getting the expected output, the .err log file is the first place to check. 

.. tip::
   You can also usee the **-l** flag to set get more detailed and informative messages in the log file produced by **sorcha run**. 

Using Relative File Paths
---------------------------------------------------------------

If you're using relative paths (e.g. '../this_directory') and those do not seem to be working, try using the full directory/file paths.

Running Multiple Instances With the Same Output Directories
---------------------------------------------------------------
If your output looks mixed up or garbled, double check that you are not running more than one ``Sorcha`` process with 
the same output path. You **should only run one** instance of ``Sorcha`` at the same time for a given output directory. 
Otherwise, you run the risk of the output files being mixed up. If you want to run multiple versions of ``Sorcha`` on 
the same computer/compute node, make sure to update the output path in the config file or commandline arguments, 
as appropriate. We have developed tools and example Slurm scripts to help you run multiple instances safely. 

sqlite3.OperationalError: index ObjID already exists/ sqlite3.OperationalError: index ObjID already exists
---------------------------------------------------------------------------------------------------------------------------------------------
This happens if you are outputting as sql databases and you have dueling ``Sorcha`` processes running in the same directory with the same output file names running on the same input files  using  the -f flag to force overwriting of output files. One way to check this is to only allow for one ``Sorcha`` run to be output to a directory and see if you've got two log files that are actively being written to/were created. Note if you're using CSV, text file, or pytables format you won't get this error when you hit this race condition.


Pointing Database Issues 
----------------------------

If you are having issues with reading the LSST pointing database such as getting an error like::
  
   pandas.io.sql.DatabaseError: Execution failed on sql 'SELECT observationStartMJD as observationStartMJD_TAI, observationId FROM observations ORDER BY observationStartMJD_TAI': no such table: observations

Then it is likely that you are using the older or newer version of the (simulated) LSST pointing database. See  :ref:`database_query`

If you see an error like::

   ERROR: PPReadPointingDatabase: SQL query on pointing database failed. Check that the query is correct in the config file.

it might be your computer setup. SQLite uses a temporary store to hold temporary files, and if it configured on your machine with a small quota you might get an error. You can fix this by setting the SQLITE_TEMPDIR environment variable to a folder in your working directory. Then if this variable is defined, SQLite will automatically default to using this pathway for its temporary store. 

Mismatch in Inputs 
---------------------
There are several files associated with the synthetic small bodies  which are passed into ``Sorcha``. These are
the orbit file, the physical parameter file and an optional complex parameters file and optional ephemeris 
file (if not using the :ref:`the internal ephemeris generator <ephemeris_gen>` buit within ``Sorcha``). Each provide specific information about the 
synthetic population that is being analysed. Within these files, it is necessary to specify an entry for every 
object. The ``Sorcha`` code will run a check to ensure that all entries have an associated orbit and 
physical/complex physical  parameter value, so if you get an error like::

   ERROR: PPCheckOrbitAndColourMatching: input colour/cometary parameter and orbit files do not match.

then make sure to check that you have entries in all the input files for each object you wish to simulate.


ERROR: Unable to find ObjID column headings (OrbitAuxReader:....)
--------------------------------------------------------------------
Check your :ref:`input files<inputs>` and ensure that they have ObjID column as the first column. 
