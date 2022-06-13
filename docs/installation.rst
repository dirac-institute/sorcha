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
In order to use the Solar System survey simulator, we must first install 
`Objects in Field <https://github.com/eggls6/objectsInField>`_. 
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

Uninstalling OIF
~~~~~~~~~~~~~~~~~~~
To uninstall::

   python setup.py develop -u

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

   cd ~/survey_simulator_post_processing
   pip install -e .


Testing the surveySimPP Installation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
To test that the installation was done correctly, run::

   surveySimPP -c ./demo/PPConfig.ini -l ./demo/colours_10mbas.txt -o ./demo/orbits_10mbas.des -p ./demo/oif_10mbas.txt -u ./data/out/ -t demorun
   
The output will appear in a csv file in .data/out (this pathway can be changed in the config file).
The output should look like::

   This

Uninstalling surveySimPP
~~~~~~~~~~~~~~~~~~~~~~~~~~~
To uninstall::

   python setup.py develop -u


