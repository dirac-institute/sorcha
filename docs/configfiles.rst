Configuration Files
=====================

Sorcha and Objects In Field both use configuration files to set the majority of the various parameters required for running these software packages. The configuration file for Sorcha allows turning on and off various filters for biasing the simulated small body population to what the survey should have found. An overview of the possible options for the config files are described below with recommendations on what you should set these config parameters to depending on your use case.

.. tip::
  We have developed  a set of utilities that are installed alongside Sorcha that can generate a config file for Objects in Field (See :ref:`makeConfigOIF`) and one for Sorcha (See :ref:`makeConfigPP`). 

Objects in Field Configuration File
------------------------------------

.. tip::
   We recommend that **nbody** should be always be set to **True**. You can break up the task across multiple proccesses if you need an increase in speed.

Sorcha Configuration File
------------------------------------

 .. _database_query:

Setting Up the Correct LSST Pointing Database Query
---------------------------------------------------

Object in Field's **Surveydbquery** config file parameter and Sorcha's **ppsqldbquery** config file parameter contain the sql query for obtaining this information from the pointing database.

From rubin_sim v2.0 simulations onward use the query::

  SELECT observationId, observationStartMJD, filter, seeingFwhmGeom, seeingFwhmEff, fiveSigmaDepth, fieldRA, fieldDec, rotSkyPos FROM observations order by observationId

For past rubin_sim/OpSim simulations pre-v2.0 use the query::

  SELECT observationId, observationStartMJD, filter, seeingFwhmGeom, seeingFwhmEff, fiveSigmaDepth, fieldRA, fieldDec, rotSkyPos FROM SummaryAllProps order by observationId

.. _makeConfigOIF:

Using makeConfigOIF
---------------------
The first config file generator works alongside OIF. By typing in the command::

   makeConfigOIF --help

It returns the following::

  usage: makeConfigOIF [-h] [-no NO] [-ndays NDAYS] [-day1 DAY1] [-prefix PREFIX] [-camerafov CAMERAFOV] [-inputformat INPUTFORMAT] [-cache CACHE] [-mpcfile MPCFILE][-spkstep SPKSTEP] [-telescope TELESCOPE] o pointing

This gives an overview of the arguments accepted by makeCConfigOIF. The two arguments that are required to generate an OIF config file are the name of a file containing 
the orbits and the name of the pointing database being used. Each of the other parameters are optional, 
but we will describe them here:



+--------------------------+----------------------------------------------------------------------------------------------------+
| Argument                 | Description                                                                                        |
+==========================+====================================================================================================+
| o                        | Orbits file                                                                                        |
+--------------------------+----------------------------------------------------------------------------------------------------+
| pointing                 | pointing database                                                                                  |
+--------------------------+----------------------------------------------------------------------------------------------------+
| -no NO                   | Number of orbits per config file, -1 runs all the orbits in one config file. Default value = 300   | 
+--------------------------+----------------------------------------------------------------------------------------------------+
| -ndays NDAYS             | Number of days in survey to run, -1 runs entire survey. Default value = -1                         | 
+--------------------------+----------------------------------------------------------------------------------------------------+
| -day1 DAY1               | First day in survey to run. Default value = 1                                                      | 
+--------------------------+----------------------------------------------------------------------------------------------------+
| -prefix PREFIX           | Config file name prefix, Default value is an empty string                                          | 
+--------------------------+----------------------------------------------------------------------------------------------------+
| -camerafov CAMERAFOV     | Path and file name of the camera fov. Default value = instrument_polygon.dat                       | 
+--------------------------+----------------------------------------------------------------------------------------------------+
| -inputformat INPUTFORMAT | Input format (CSV or whitespace). Default value = whitespace                                       | 
+--------------------------+----------------------------------------------------------------------------------------------------+
| -cache CACHE             | Base cache directory name. Default value = _cache                                                  | 
+--------------------------+----------------------------------------------------------------------------------------------------+
| -mpcfile MPCFILE         | Name of the file containing the MPC observatory codes. Default value = obslist.dat                 | 
+--------------------------+----------------------------------------------------------------------------------------------------+
| -spkstep SPKSTEP         | Integration step in days. Default value = 30                                                       | 
+--------------------------+----------------------------------------------------------------------------------------------------+
| -telescope TELESCOPE     | Observatory MPC Code. Default value = I11 (Gemini South to be changed to Rubin Observatory)        |
+--------------------------+----------------------------------------------------------------------------------------------------+


The most basic way to use the OIF config file generator is to run::

  makeConfigOIF ./data/test/testorb.des ./data/test/baseline_10yrs_10klines.db

Where testorb.des is the orbit file and baseline_10yrs_10klines.db is the pointing database. This will generate 
a basic config file, filled mostly with default values. These values can be tweaked by running something like::

  makeConfigOIF ./data/test/testorb.des ./data/test/baseline_10yrs_10klines.db -ndays 10
  
Which will generate a config file with the number of days in the survey set to 10.


.. note::
   makeConfigOIF is designed to help generate multiple configuration files if the user wants to divide the compute task across several nodes/processors.

.. _makeConfigPP:

Using makeConfigPP
-------------------------------------
Typing in the command::

   makeConfigPP --help

Returns the following::

  usage: makeConfigPP [-h] [--objecttype OBJECTTYPE] [-pointingdatabase POINTINGDATABASE] [--footprintpath FOOTPRINTPATH] [--pointingformat POINTINGFORMAT]
  [--auxformat AUXFORMAT] [--mainfilter MAINFILTER] [--othercolours OTHERCOLOURS] [--resfilter RESFILTER] [--phasefunction PHASEFUNCTION]
  [--trailinglosseson] [--cameramodel CAMERAMODEL] [--detectionefficiency DETECTIONEFFICIENCY] [--fillfactor FILLFACTOR] [--mintracklet MINTRACKLET]
  [--notracklets NOTRACKLETS] [--trackletinterval TRACKLETINTERVAL] [--brightlimit BRIGHTLIMIT] [--insepthreshold INSEPTHRESHOLD] [--outpath OUTPATH]
  [--outfilestem OUTFILESTEM] [--outputformat OUTPUTFORMAT] [--separatelycsv] [--sizeserialchunk SIZESERIALCHUNK]
  filename

The only required argument is the filename, which is the location in which you want to store the config file. Each other argument is optional.
They are described as follows:

+------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Argument                                                                     | Description                                                                                                                                                                                                                                                          |
+==============================================================================+======================================================================================================================================================================================================================================================================+
| filename                                                                     | The pathway where you want to store the configuration file                                                                                                                                                                                                           |
+------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| --objecttype OBJECTTYPE, -obj OBJECTTYPE                                     | Type of object: asteroid or comet. Default is "asteroid".                                                                                                                                                                                                            |
+------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| --pointingdatabase POINTINGDATABASE, -inpt POINTINGDATABASE                  | Path to pointing database. Default is "./data/test/baseline_10yrs_10klines.db".                                                                                                                                                                                      |
+------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| --footprintpath FOOTPRINTPATH, -infoot FOOTPRINTPATH                         | Path to camera footprint file. Default is "./data/detectors_corners.csv".                                                                                                                                                                                            | 
+------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| --pointingformat POINTINGFORMAT, -inptf POINTINGFORMAT                       |  Separator in pointing database: csv, whitespace, hdf5. Default is "whitespace".                                                                                                                                                                                     | 
+------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| --auxformat AUXFORMAT, -inauxf AUXFORMAT                                     | Separator in orbit/colour/brightness/cometary data files: comma or whitespace. Default is "whitespace".                                                                                                                                                              | 
+------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| --mainfilter MAINFILTER, -mfilt MAINFILTER                                   | The main filter in the colour file to which all other colours are compared. Default is "r".                                                                                                                                                                          | 
+------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| --othercolours OTHERCOLOURS, -ofilt OTHERCOLOURS                             | Other colours with respect to the main filter, e.g g-r. Should be given separated by comma. Default is "g-r,i-r,z-r".                                                                                                                                                | 
+------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| --resfilter RESFILTER, -rfilt RESFILTER                                      | resulting filters; main filter, followed by resolved colours, such as, e.g. 'r'+'g-r'='g'. Should be given in the following order: main filter, resolved filters in the same order as respective other colours. Should be separated by comma. Default is "r,g,i,z"   | 
+------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| --phasefunction PHASEFUNCTION, -phfunc PHASEFUNCTION                         | Define the used input phase function. Options: HG, HG1G2, HG12, linear, none. Default is "HG".                                                                                                                                                                       | 
+------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| --trailinglosseson, -tloss                                                   |Switch on trailing losses. Revelant for close-approaching NEOs. Default False.                                                                                                                                                                                        | 
+------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| --cameramodel CAMERAMODEL, -cammod CAMERAMODEL                               | Choose between surface area equivalent or actual camera footprint, including chip gaps. Options: circle, footprint. Default is "footprint".                                                                                                                          | 
+------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| --detectionefficiency DETECTIONEFFICIENCY, -deteff DETECTIONEFFICIENCY       | Which fraction of the detections will the automated Solar System processing pipeline recognise? Expects a float. Default is 0.95.                                                                                                                                    |
+------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| --fillfactor FILLFACTOR, -ff FILLFACTOR                                      |  Fraction of detector surface area which contains CCD -- simulates chip gaps. Expects a float. Default is 0.9.                                                                                                                                                       | 
+------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| --mintracklet MINTRACKLET, -mintrk MINTRACKLET                               | How many observations during one night are required to produce a valid tracklet? Expects an int. Default 2.                                                                                                                                                          | 
+------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| --notracklets NOTRACKLETS, -ntrk NOTRACKLETS                                 | How many tracklets are required to classify as a detection? Expects an int. Default 3.                                                                                                                                                                               | 
+------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|  --trackletinterval TRACKLETINTERVAL, -inttrk TRACKLETINTERVAL               | In what amount of time does the aforementioned number of tracklets needs to be discovered to constitute a complete detection? In days. Expects a float. Default 15.0.                                                                                                | 
+------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| --brightlimit BRIGHTLIMIT, -brtlim BRIGHTLIMIT                               | Limit of brightness: detections brighter than this are omitted assuming saturation. Expects a float. Default is 16.0.                                                                                                                                                | 
+------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| --outpath OUTPATH, -out OUTPATH                                              |  Path to output. Default is "./data/out".                                                                                                                                                                                                                            |                                                                                                                                            
+------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| --outfilestem OUTFILESTEM, -outstem OUTFILESTEM                              |  Output file name stem. Default is "hundredcomets"                                                                                                                                                                                                                   | 
+------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| --outputformat OUTPUTFORMAT, -outf OUTPUTFORMAT                              | Output format. Options: csv, sqlite3, hdf5. Default is csv.                                                                                                                                                                                                          |
+------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| --separatelycsv, -sepcsv                                                     | Toggle to write out the CSV file for each object separately. Default is False.                                                                                                                                                                                       | 
+------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| --sizeserialchunk SIZESERIALCHUNK, -chunk SIZESERIALCHUNK                    |  Size of chunk of objects to be processed serially. Default is 10.                                                                                                                                                                                                   | 
+------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+



