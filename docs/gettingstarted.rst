Getting Started
=====================

In this section we provide an overview of how to use the survey simulator. We start by generating a set of 
files containing information on the synethic planetoids that we wish to study. We take you through the process of generating
ephemerides for these synthetic bodiess using OIF (Objects in Field), and show you how to use Sorcha. 

.. tip::
   In this quick start guide, we demonstrate how to run a single instance of OIF and Sorcha. Both packages are designed to allow multiple instances to be run in parallel in order to accomodate simulations with very large numbers of synthetic planetesimals by breaking up the job across multiple live proccesses. We recommend first starting with the examples below, before moving on to parallel processing.


.. important::
  All the input files and configuration files used in this demonstation are available in the demo directory within the Sorcha github repository (sorcha/sorcha/demo). Below includes instructions on how to generate these, but you can skip those setps and go straight to the run commands if you need to.

.. note::
  All input data files in this example are white-space separated format solely for the ease of reading.   

Creating Object Files
-------------------------
The first step in the process is to generate a set of files which describe the orbital and physical parameters
of the objects that we wish to study. Here we will generate a file called 'testorb.des', which contains
the orbits of five objects::

   ObjID t_0 t_p argperi node i e q FORMAT
   6 54800.0 6340.99721 16.4209 45.79141 21.20084 0.67411 5.65043 COM
   632 54800.0 23466.22367 284.5519 217.91073 5.37133 0.4966 6.88417 COM
   6624 54800.0 26018.29348 107.05559 285.0348 22.55248 0.31532 8.0147 COM
   12733 54800.0 -35166.67218 204.92643 193.27826 31.25325 0.68699 7.76983 COM
   28311 54466.0 39984.71835 260.982851 122.344837 2.801063 0.25719962 40.02995082 COM
   39262 54466.0 54670.08858857185 80.463152617168 132.486568373398 18.303864557524 0.6625177539 1.286218727856 COM
   39265 54466.0 54075.567351641024 73.11929900858 314.32320360528 22.761089277031 0.772124864464 0.569263692349 COM
   307764 54466.0 54641.54032677078 102.019078535164 278.124566551661 10.994324503586 0.567173981581 0.504552654462 COM
   356450 54466.0 90480.35745 7.89 144.25849 8.98718 0.09654 33.01305 COM
   387449 54800.0 54026.65733 349.45493 115.41492 11.28725 0.19587 2.48289 COM

We will also generate a file called 'sspp_testset_colours.txt' which contains information about the colour and brightness of the objects::

   ObjID H u-r g-r i-r z-r y-r GS
   6 15.88 1.72 0.48 -0.11 -0.12 -0.12 0.15
   632 14.23 1.72 0.48 -0.11 -0.12 -0.12 0.15
   6624 14.23 1.72 0.48 -0.11 -0.12 -0.12 0.15
   12733 15.75 1.72 0.48 -0.11 -0.12 -0.12 0.15
   28311 7.76 2.55 0.92 -0.38 -0.59 -0.7 0.15
   39262 10.818 1.72 0.48 -0.11 -0.12 -0.12 0.15
   39265 11.678 2.13 0.65 -0.19 -0.14 -0.14 0.15
   307764 25.0 2.13 0.65 -0.19 -0.14 -0.14 0.15
   356450 7.99 2.55 0.92 -0.38 -0.59 -0.7 0.15
   387449 18.92 1.72 0.48 -0.11 -0.12 -0.12 0.15


Sorcha
-----------------------------------------

Now that we have the information about the ephemerides, we can begin to run the survey simulator to 
check if these objects are observable by the LSST.

Generate a Sorcha Config File 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The key information about the simulation paramteres are held in the post processing configuration file.
There is a configuration file generator build into the survey simulator, which can be run using::
   
  makeConfigPP ./demo/PPConfig_test.ini --ephformat csv --trailinglosseson True
 
which will generate a default config file, named config.ini. There are several optional parameters that
can be added (see inputs). 

Running Sorcha
~~~~~~~~~~~~~~~~~~~~~~~

Finally, we have all the information required to run the survey simulator. This can be done by typing::

   sorcha -c ./demo/PPConfig_test.ini -p ./demo/sspp_testset_colours.txt -o ./demo/sspp_testset_orbits.des -e ./demo/example_oif_output.txt -u ./data/out/ -t testrun_e2e 

The first several lines of  output will look something like::

   ObjID,FieldMJD,fieldRA,fieldDec,AstRA(deg),AstDec(deg),AstrometricSigma(deg),optFilter,observedPSFMag,observedTrailedSourceMag,PhotometricSigmaPSF(mag),PhotometricSigmaTrailedSource(mag),fiveSigmaDepth,fiveSigmaDepthAtSource
   632,60315.2441,141.4554595,8.1858813,142.5089358,8.434994,1.36e-05,r,22.607,22.722,0.084,0.084,23.783,23.771
   632,60315.26793,141.4554595,8.1858813,142.5075236,8.4352135,1.17e-05,i,22.587,22.509,0.09,0.09,23.595,23.583
   632,60322.248,141.0466609,9.4406351,142.0713696,8.5214621,7.9e-06,g,23.138,23.16,0.06,0.06,24.591,24.558
   632,60322.2717,141.0466609,9.4406351,142.0697072,8.5218264,5.9e-06,r,22.762,22.64,0.051,0.051,24.315,24.282
   632,60328.19755,141.6678165,7.1548011,141.64208,8.6235416,1.79e-05,z,22.517,22.556,0.139,0.139,22.962,22.918
   632,60328.25587,140.9158928,9.8725584,141.6375209,8.6246736,1.03e-05,i,22.423,22.368,0.08,0.079,23.619,23.579
   632,60328.27875,140.9158928,9.8725584,141.6357097,8.6251096,1.76e-05,z,22.729,22.423,0.136,0.136,22.982,22.943
   632,60328.30071,141.6678165,7.1548011,141.634002,8.6255457,1.71e-05,z,22.506,22.552,0.134,0.133,23.006,22.962
   632,60329.25405,142.8361496,7.6203923,141.5610457,8.6442007,9.4e-06,g,23.129,23.081,0.065,0.065,24.462,24.39
   632,60340.20215,140.7268621,9.0201761,140.6614046,8.8967256,1.04e-05,i,22.395,22.27,0.089,0.089,23.291,23.291
   632,60340.22599,140.7268621,9.0201761,140.6593039,8.8973371,1.37e-05,z,22.461,22.368,0.119,0.119,22.942,22.942
   632,60344.1987,140.326146,7.7906532,140.314112,9.0038707,3.22e-05,g,23.158,23.076,0.111,0.111,23.583,23.563
   632,60344.22335,140.326146,7.7906532,140.3118898,9.0045278,9.6e-06,r,22.345,22.586,0.061,0.061,23.802,23.782
   632,60344.27754,140.326146,7.7906532,140.307012,9.0060477,2.74e-05,i,22.111,22.477,0.121,0.121,22.894,22.875
   632,60344.30119,140.326146,7.7906532,140.3048883,9.0066966,2.52e-05,z,22.157,22.296,0.152,0.152,22.616,22.596
   632,60345.18907,140.2280447,8.5837329,140.2272922,9.0314101,1.23e-05,r,22.345,22.448,0.067,0.067,23.668,23.668
   632,60346.16835,141.2076529,9.0398667,140.1413377,9.0589925,1.68e-05,r,22.27,22.395,0.079,0.079,23.477,23.466
   632,60348.25973,140.0293005,8.965671,139.9570249,9.1190653,6.9e-06,r,22.447,22.326,0.049,0.049,24.011,24.011
   632,60351.19357,139.8492054,8.6320566,139.6992239,9.2054883,7.3e-06,g,22.816,22.853,0.05,0.05,24.472,24.472
   632,60351.21734,139.8492054,8.6320566,139.6970959,9.2061844,5.7e-06,r,22.414,22.32,0.043,0.043,24.163,24.163
   632,60356.23982,139.7624114,10.611928,139.2607587,9.3586028,3.09e-05,z,22.276,22.303,0.167,0.167,22.542,22.511
   632,60366.0856,137.8508484,9.4076278,138.4526989,9.6644812,3.53e-05,z,22.248,22.441,0.234,0.233,22.242,22.242
   632,60377.14141,135.9939995,10.2602506,137.6736389,9.9991782,8.7e-06,i,22.612,22.701,0.076,0.076,23.784,23.703
   632,60384.12561,137.578367,10.4153852,137.2810625,10.1951391,9e-06,r,22.692,22.733,0.067,0.067,24.041,24.041
   632,60397.0945,137.6294414,10.4654572,136.8071117,10.5053467,2.82e-05,i,22.715,22.781,0.18,0.18,22.89,22.887
   632,60397.11835,137.6294414,10.4654572,136.8065221,10.5058448,2.86e-05,z,22.447,22.321,0.21,0.209,22.697,22.694
   632,60399.0693,137.5007909,9.6835542,136.7666383,10.5451375,2.45e-05,r,22.901,22.642,0.138,0.138,23.341,23.327
   632,60399.09351,137.5007909,9.6835542,136.7661228,10.5456264,1.57e-05,i,22.846,22.781,0.124,0.124,23.356,23.343
   632,60404.02967,136.6652419,10.7150041,136.703629,10.635411,1.48e-05,r,23.031,22.856,0.093,0.093,23.834,23.834
   632,60407.01166,137.9003026,10.4601787,136.6928919,10.6825895,1.01e-05,r,23.012,22.954,0.078,0.078,24.083,24.064
   632,60407.03549,137.9003026,10.4601787,136.6928541,10.6829441,1.08e-05,i,22.884,22.873,0.094,0.094,23.755,23.735
   632,60419.97412,138.2254847,11.0456903,136.8872669,10.8206369,4.34e-05,i,22.218,22.964,0.272,0.272,22.592,22.563
   632,60426.97045,137.6919103,9.2401203,137.1521501,10.84754,2.4e-05,r,23.096,23.018,0.136,0.136,23.638,23.552
   632,60426.98127,137.6919103,9.2401203,137.1526965,10.8474947,2.59e-05,i,22.967,22.818,0.158,0.158,23.348,23.263
   632,60432.96527,138.1759203,10.3996733,137.4653145,10.8432948,1.47e-05,r,23.093,23.366,0.108,0.108,23.861,23.858
   632,60432.97609,138.1759203,10.3996733,137.4659096,10.8432426,1.12e-05,i,23.105,23.082,0.104,0.104,23.8,23.797
   632,60435.95804,136.7133685,10.5177289,137.6504775,10.8316439,1.94e-05,r,23.373,23.434,0.137,0.137,23.608,23.6
   39265,60370.38399,192.6418095,-32.5378881,193.6750982,-32.7017699,2.8e-06,i,18.027,18.016,0.004,0.004,23.121,23.116
   
.. warning::
   Only one instance of Sorcha can be run per output directory. Make sure to have different output pathways if you are running multiple instances on the same compute node. 

.. note::
   Sorcha outputs a log file and error file. If all has gone well, the error file will be empty. The log file has the configuration parameters outputted to it as a record of the run setup. 
