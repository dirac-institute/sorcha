Using Objects In Field
======================


A basic configuration file::


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

   