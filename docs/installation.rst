Installation
=================

.. note::
   The Sorcha and OIF python packages are currently pip installable. We hope to have conda installable versions in the near future.

Initial Steps
-----------------------
**Step 1** Create a directory to contain the OIF and Sorcha repos::

   mkdir sorcha
   cd sorcha

.. tip::
   We recommend using python version 3.9 with Sorcha and OIF. This is the version of python we currently use to test our unit tests. Also due to an udate to spiceypy, OIF requires the installation of spiceypy=4.0.1 (use the next step to create the correct conda environement).

**Step 2** Create a conda environment::

   conda create -n sorcha -c conda-forge -c mjuric python=3.9 spiceypy=4.0.1 openorb numpy pandas matplotlib spice-utils pip setuptools=66.0.0
   conda activate sorcha

   
OIF
-----------------------
In order to use the Solar System survey simulator, we must first install the specialized 
`clone of Objects in Field <https://github.com/eggls6/objectsInField>`_ set up for use with surveysimPP. 
This is used to generate candidate detections for an input population of 
moving objects in a specified list of field pointings.

OIF Requirements
~~~~~~~~~~~~~~~~~~~
*  python 3 
*  spiceypy=4.0.1 
*  openorb 
*  numpy 
*  pandas 
*  matplotlib 
*  spice-utils
*  setuptools=66.0.0

Installing Objects in Field
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Step 1** Make sure you are in the directory you want to contain the Survey Simulator repo in::

   cd sorcha
   
**Step 2** Download the OIF repo via::
    
   git clone https://github.com/eggls6/objectsInField.git
   
**Step 3** And cd into the repo::

   cd objectsInField
   
**Step 4** Download the various large binary files (mostly SPICE kernels) that aren't kept in git, by running::

   ./bootstrap.sh
   
.. note::
   The bash script downloads and stores the SPICE files to oif/data/  

**Step 5** Install an editable (in-place) development version of OIF. This will allow you to run the code from the source directory.::

   pip install -e .

Testing the OIF Installation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
OIF has test data and a configuration file set up for checking your installation was successful. To  make sure everything worked::

   cd test
   oif input.config > test.output

If everything has installed correctly, test.output will include::
   
   ```
   START HEADER
   [ASTEROID]
   Population model    = asteroids.s3m
   SPK T0              = 59200
   nDays               = 800
   SPK step            = 30
   nbody               = T
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
   Survey length:
   Field 1 : 59853.98564382085
   Field n : 59855.015756339824
   Days : 2.0
   END HEADER
   ObjID,FieldID,FieldMJD,AstRange(km),AstRangeRate(km/s),AstRA(deg),AstRARate(deg/day),AstDec(deg),AstDecRate(deg/day),Ast-Sun(J2000x)(km),Ast-Sun(J2000y)(km),Ast-Sun(J2000z)(km),Ast-Sun(J2000vx)(km/s),Ast-Sun(J2000vy)(km/s),Ast-Sun(J2000vz)(km/s),Obs-Sun(J2000x)(km),Obs-Sun(J2000y)(km),Obs-Sun(J2000z)(km),Obs-Sun(J2000vx)(km/s),Obs-Sun(J2000vy)(km/s),Obs-Sun(J2000vz)(km/s),Sun-Ast-Obs(deg),V,V(H=0)
   S100003Ua,992,59855.012720,232764749.248534,19.381,313.391309,0.093855,-14.189297,-0.001147,302701424.873,-141376977.611,-47258199.518,10.938,16.381,6.838,147675817.300,22607836.793,9798564.669,-5.071,27.085,11.641,22.025168,12.229,3.789
   S100005xa,40,59854.002209,311895722.264189,18.108,312.493375,0.024745,-10.868628,-0.020284,355032405.197,-205593003.122,-50029660.233,8.437,15.234,7.005,148124584.428,20259701.559,8780700.962,-4.542,27.134,11.674,17.656392,14.416,4.726
   S100005Aa,993,59855.013142,293695449.878793,20.744,318.064945,0.007336,-15.326503,0.037457,358386286.782,-166683879.872,-67830362.667,10.529,13.637,8.301,147675632.576,22608823.379,9798988.673,-5.072,27.086,11.641,17.493547,24.184,4.524
   S100005Ma,992,59855.012720,254838551.295162,21.485,313.887934,0.073709,-12.318483,-0.032336,320275224.443,-156825113.314,-44570113.955,11.907,14.784,5.431,147675817.300,22607836.793,9798564.669,-5.071,27.085,11.641,20.397744,24.442,4.072
   S1000062a,30,59853.998050,270910872.953021,19.725,310.235405,0.055242,-11.054255,-0.052272,319868809.097,-182725429.454,-43167528.027,9.881,14.682,5.085,148126215.412,20249952.751,8776505.940,-4.535,27.125,11.674,20.257467,19.559,4.269
   S1000062a,41,59854.002624,270918670.134100,19.737,310.235658,0.055234,-11.054494,-0.052222,319872713.454,-182719627.936,-43165518.813,9.881,14.682,5.085,148124421.707,20260673.486,8781119.116,-4.543,27.135,11.674,20.258390,19.559,4.269
   S1000065a,27,59853.996810,347587844.429137,24.931,304.596386,0.078548,-11.561336,-0.039962,341479992.787,-260072351.727,-60887212.973,13.465,10.548,3.929,148126701.218,20247046.556,8775255.097,-4.533,27.122,11.674,18.177937,18.802,5.082
   S1000066a,995,59855.013982,361677977.928847,20.427,316.533583,-0.013516,-18.866810,0.037563,396069815.793,-212830311.061,-107155733.445,8.957,12.503,7.633,147675264.406,22610789.339,9799833.539,-5.073,27.088,11.640,15.593138,20.721,5.221
   ```

.. note::
   The first part of the OIF output is a header that describes how the software was configured. The next part is the ephemeris for the synthetic planetesimals that land within the field-of-view (FOV) of a specific survey observation based on the test input simulated LSST observation database. See :ref:`the outputs page<Outputs>` for further explanation.

Sorcha
-----------------------------

Sorcha Requirements
~~~~~~~~~~~~~~~~~~~~~~~~~~
*  python 3
*  numpy
*  pandas
*  pytest
*  pytest-cov<2.6.0
*  setuptools>=42
*  wheel
*  setuptools_scm>=3.4
*  astropy
*  scipy
*  sbpy
*  matplotlib


Installing Sorcha 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Step 1** Navigate to the directory you want to store the Sorcha soure code in::

   cd sorcha
   
**Step 2** Download the Sorcha soure code via::

   git clone https://github.com/dirac-institute/sorcha.git
   
**Step 3** Install an editable (in-place) development version of Sorcha. This will allow you to run the code from the source directory.::

   cd sorcha
   pip install -e .


Testing the Sorcha Installation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
You can check that the surveySimPP installation was done correctly, by running::

   sorcha -c ./demo/PPConfig_test.ini -p ./demo/sspp_testset_colours.txt -o ./demo/sspp_testset_orbits.des -e ./demo/example_oif_output.txt -u ./data/out/ -t testrun_e2e
   
The output will appear in a csv file (testrun_e2e.csv) in .data/out (this pathway can be changed via the -u command line argument). The first several lines of the csv file should look like::

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
.. note::
   This test run is using pre-made ephemeris generasted by OIF already stored in the demo directory of the github Sorcha repository. 
