.. _configs:

Configuration File
=====================

Sorcha uses a configuration files to set the majority of the various parameters required for running these software packages. The configuration file for Sorcha allows turning on and off various filters for biasing the simulated small body population to what the survey should have found. An overview of the possible options for the configuration file are described below with recommendations on what you should set these config parameters to depending on your use case.

.. tip::
  We have developed  a set of utilities that are installed alongside Sorcha that can generate a config file for Sorcha (See :ref:`makeConfigPP`). 

.. _example_configs:

Example Configuration Files
------------------------------------

The following sections show reasonable configuration files for various settings.

Rubin Full Footprint
~~~~~~~~~~~~~~~~~~~~~~

This configuration file is appropriate for running ``sorcha`` using the Rubin
full detector footprint.

The source code is available `here <https://github.com/dirac-institute/sorcha/blob/main/survey_setups/Rubin_full_footprint.ini>`__.

.. literalinclude:: ../survey_setups/Rubin_full_footprint.ini
   :language: text
   :linenos:

Rubin Circular Approximation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This configuration file is appropriate for running ``sorcha`` using a circular 
approximation of the Rubin detector.

The source code is available `here <https://github.com/dirac-institute/sorcha/blob/main/survey_setups/Rubin_circular_approximation.ini>`__.

.. literalinclude:: ../survey_setups/Rubin_circular_approximation.ini
    :language: text
    :linenos:


.. _database_query:

Setting Up the Correct LSST Pointing Database Query
---------------------------------------------------

Sorcha's **ppsqldbquery** config file parameter contain the sql query for obtaining this information from the pointing database.

From rubin_sim v2.0 simulations onward use the query::

  SELECT observationId, observationStartMJD as observationStartMJD_TAI, visitTime, filter, seeingFwhmGeom, seeingFwhmEff, fiveSigmaDepth, fieldRA, fieldDec, rotSkyPos FROM observations order by observationId

For past rubin_sim/OpSim simulations pre-v2.0 use the query::

  SELECT observationId, observationStartMJD as observationStartMJD_TAI, visitTime, filter, seeingFwhmGeom, seeingFwhmEff, fiveSigmaDepth, fieldRA, fieldDec, rotSkyPos FROM SummaryAllProps order by observationId

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



