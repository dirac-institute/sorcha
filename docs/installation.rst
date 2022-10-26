Installation
=================

.. note::
   The surveySimPP and OIF python packages are currently pip installable. We hope to have conda installable versions in the near future.

Initial Steps
-----------------------
**Step 1** Create a directory to contain the OIF and Survey Simulator repos::

   mkdir survey_sim_pp
   cd survey_sim_pp

.. tip::
   We recommend using python version 3.9 with surveySimPP and OIF. This is the version of python we currently use to test our unit tests. Also due to an udate to spiceypy, OIF requires the installation of spiceypy=4.0.1 (use the next step to create the correct conda environement).

**Step 2** Create a conda environment::

   conda create -n survey_sim_pp -c conda-forge -c mjuric python=3.9 spiceypy=4.0.1 openorb numpy pandas matplotlib spice-utils pip
   conda activate survey_sim_pp

   
OIF
-----------------------
In order to use the Solar System survey simulator, we must first install the specialized 
`clone of Objects in Field <https://github.com/eggls6/objectsInField>`_ set up for use with surveysimPP. 
This is used to generate candidate detections for an input population of 
moving objects in a specified list of field pointings.

OIF Requirements
~~~~~~~~~~~~~~~~~~~
*  python 3 
*  spiceypy 
*  openorb 
*  numpy 
*  pandas 
*  matplotlib 
*  spice-utils

Installing Objects in Field
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Step 1** Make sure you are in the directory you want to contain the Survey Simulator repo in::

   cd survey_sim_pp
   
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

SurveySimPP
-----------------------------

SurveySimPP Requirements
~~~~~~~~~~~~~~~~~~~~~~~~~~
*  python 3
*  numpy
*  pandas
*  pytest
*  pytest-cov<2.6.0
*  coveralls
*  setuptools>=42
*  wheel
*  setuptools_scm>=3.4
*  astropy
*  scipy
*  sbpy
*  matplotlib


Installing the Survey Simulator Post Processing 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Step 1** Navigate to the directory you want to storen the surveySimPP soure code in::

   cd survey_sim_pp
   
**Step 2** Download the Solar System survey simulator soure code via::

   git clone https://github.com/dirac-institute/survey_simulator_post_processing.git
   
**Step 3** Install an editable (in-place) development version of surveySimPP. This will allow you to run the code from the source directory.::

   cd survey_simulator_post_processing
   pip install -e .


Testing the surveySimPP Installation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**If you have not run and installed OIF from above**, you can check that the surveySimPP installation was done correctly, by running::

   surveySimPP -c ./demo/PPConfig_test.ini -l ./demo/sspp_testset_colours.txt -o ./demo/sspp_testset_orbits.des -p ./demo/example_oif_output.txt -u ./data/out/ -t testrun_e2e
   
The output will appear in a csv file (testrun_e2e.csv) in .data/out (this pathway can be changed via the -u command line argument)
The first several lines of the csv file should look like::

   ObjID,FieldMJD,fieldRA,fieldDec,AstRA(deg),AstDec(deg),AstrometricSigma(deg),optFilter,observedPSFMag,observedTrailedSourceMag,PhotometricSigmaPSF(mag),PhotometricSigmaTrailedSource(mag),fiveSigmaDepth,fiveSigmaDepthAtSource
   632,60315.2441,141.4554595,8.1858813,142.5089386,8.434987,1.36e-05,r,22.672,22.822,0.084,0.084,23.783,23.771
   632,60315.26793,141.4554595,8.1858813,142.5075126,8.4352226,1.17e-05,i,22.675,22.483,0.09,0.09,23.595,23.583
   632,60328.19755,141.6678165,7.1548011,141.6420647,8.6235514,1.79e-05,z,22.376,22.586,0.139,0.139,22.962,22.918
   632,60328.25587,140.9158928,9.8725584,141.6375299,8.6246771,1.03e-05,i,22.483,22.532,0.08,0.079,23.619,23.579
   632,60328.27875,140.9158928,9.8725584,141.6357117,8.6250849,1.76e-05,z,22.473,22.47,0.136,0.136,22.982,22.943
   632,60328.30071,141.6678165,7.1548011,141.6339921,8.6255543,1.71e-05,z,22.34,22.366,0.134,0.133,23.006,22.962
   632,60329.25405,142.8361496,7.6203923,141.5610427,8.6442104,9.4e-06,g,23.053,23.062,0.065,0.065,24.462,24.39
   632,60329.27614,140.7371655,9.7972372,141.5592804,8.644631,1.15e-05,r,22.562,22.662,0.072,0.072,23.83,23.794
   632,60426.96955,136.7340669,12.2432215,137.152149,10.8474825,2.27e-05,r,23.234,23.152,0.133,0.133,23.621,23.579
   632,60426.97045,137.6919103,9.2401203,137.1522171,10.8475022,2.4e-05,r,23.093,23.1,0.136,0.136,23.638,23.552
   632,60426.98127,137.6919103,9.2401203,137.1527036,10.8475279,2.59e-05,i,22.958,22.896,0.158,0.158,23.348,23.263
   632,60432.96527,138.1759203,10.3996733,137.4653232,10.8432814,1.47e-05,r,22.973,23.19,0.108,0.108,23.861,23.858
   632,60432.97609,138.1759203,10.3996733,137.4659291,10.8432429,1.12e-05,i,23.066,23.0,0.104,0.104,23.8,23.797
   632,60435.95804,136.7133685,10.5177289,137.6504883,10.831664,1.94e-05,r,23.036,23.067,0.137,0.137,23.608,23.6
   632,60435.96879,136.7133685,10.5177289,137.6511711,10.8316515,1.61e-05,i,23.071,23.01,0.127,0.127,23.584,23.576
   632,60437.02296,138.9314847,10.5647336,137.7208497,10.8260062,1.88e-05,r,23.218,23.304,0.12,0.12,23.777,23.757
   632,60437.04671,138.9314847,10.5647336,137.7223925,10.8257878,2.98e-05,i,23.188,22.828,0.177,0.177,23.207,23.187
   39265,60347.2776,196.15222,-30.2579928,196.9513634,-31.5022433,2.8e-06,r,18.416,18.412,0.003,0.003,24.037,24.0

