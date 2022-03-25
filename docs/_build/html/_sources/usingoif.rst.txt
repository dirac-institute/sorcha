Using Objects In Field
======================

The survey simulator post processing code can be used with any orbital parameter calculator, but we
recommend using Objects in Field. After installing Objects in Field, it can be run through the command 
line via::

   oif input.config
   
By providing OIF with a target population of moving objects, it will generate a list of detections for specified pointings. 
In our case, the pointing is given by the predicted LSST pointing database. This will be updated as observations are taken. 

The orbital parameters of an object are given in a separate file. Objects in field can take orbits in cometary, Keplarian and Cartesian
formats, but it is important not to mix and match within a single file. An example of an orbit file can be seen below::

   !!OID FORMAT q e i Omega argperi t_p H t_0 INDEX N_PAR MOID COMPCODE
   St500000a  COM   4.91636   0.05966   7.60840 313.71100 150.14863  47268.27529  5.63  54800.00000 1 6 -1 Python



A basic configuration file is provided with OIF, an it looks something like this::


   [ASTEROID]
   Population model    = asteroids.s3m
   SPK T0              = 59200
   nDays               = 800
   SPK step            = 30
   nbody               = T
   Input format       = whitespace

   [SURVEY]
   Survey database     = sample-lsst_baseline_v1p4_test.db
   Field1              = 1
   nFields             = 1000
   Telescope           = I11
   Surveydbquery       = SELECT observationId,observationStartMJD,fieldRA,fieldDEC,rotSkyPos FROM SummaryAllProps order by observationStartMJD

   [OUTPUT]
   Output file          = stdout
   Output format        = csv

   [CAMERA]
   Camera              = instrument_polygon.dat
   Threshold           = 5


There are four headers: [ASTEROID] [SURVEY] [OUTPUT] and [CAMERA] each with associated keywords and values. It is here that 
we can tweak the parameters for the simulation.


+----------+-------------------------+--------------------+-----------------------------------------------------------------------------------------------+
| Section  | Keyword                 | Default Value      | Description                                                                                   |
+==========+=========================+====================+===============================================================================================+
| ASTEROID | *Population Model       | NA                 | Name of the file containing the asteroid orbits. This file should be in the Data path folder. |
+----------+-------------------------+--------------------+-----------------------------------------------------------------------------------------------+
| ASTEROID | *Asteroid SPK path      | NA                 |                                                                                               |
+----------+-------------------------+--------------------+-----------------------------------------------------------------------------------------------+
| ASTEROID | *Asteroid SPKs          | NA                 |                                                                                               |
+----------+-------------------------+--------------------+-----------------------------------------------------------------------------------------------+
| ASTEROID | Object1                 | 1                  |                                                                                               |
+----------+-------------------------+--------------------+-----------------------------------------------------------------------------------------------+