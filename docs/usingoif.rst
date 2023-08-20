Using Objects in Field (OIF) for Ephemeris Generation
=====================================================

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
   The first part of the OIF output is a header that describes how the software was configured. The next part is the ephemeris for the synthetic planetesimals that land within the field-of-view (FOV) of a specific survey observation based on the test input simulated LSST observation database. 

IF
-----------
The survey simulator post processing code relies on using an orbital calculator to generate ephemerides,
we recommend using Objects in Field, but you can use any orbital calculator as long as the outputs are 
consistent. Here we give an overview of how to use Objects in Field. If you are using another orbit calculator
then you can skip to the section on using the survey simulator.


Generate an OIF Config File 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The survey simulator post processing code comes with several command line utilities. One of these is 
a config file generator for Objects in Field. makeConfigOIF takes two required parameters, the name of 
the orbit file and the pointing database. There are several optional arguments which can be used to further 
customise your OIF usage. Details of these optional arguments can be seen in inputs.


The most basic OIF config file can be generated by typing::

   makeConfigOIF ./demo/sspp_testset_orbits.des ./demo/baseline_v2.0_1yr.db -no -1 -ndays -1 -camerafov instrument_circle.dat -spkstep 1

This will return the following::

   [CONF]
   cache dir = _cache/sspp_testset_orbits/1-10
   
   [ASTEROID]
   population model = ./demo/sspp_testset_orbits.des
   spk t0 = 60188
   ndays = 395
   object1 = 1
   nobjects = 10
   spk step = 1
   nbody = T
   input format = whitespace
   
   [SURVEY]
   survey database = ./demo/baseline_v2.0_1yr.db
   field1 = 1
   nfields = 216011
   mpcobscode file = obslist.dat
   telescope = I11
   surveydbquery = SELECT observationId,observationStartMJD,fieldRA,fieldDEC,rotSkyPos FROM observations order by observationStartMJD
   
   [CAMERA]
   threshold = 5
   camera = instrument_circle.dat

   output file = stdout
   output format = csv
 
This file will be saved as OIFconfig_test.ini in the directory it has been run within. 

Running OIF
~~~~~~~~~~~~
Now that we have an OIF config file, we can easily run OIF by typing::

   oif -f ./demo/OIFconfig_test.ini > ./demo/test_oif_output.txt
  mv sspp_testset_orbits-01-10.ini OIFconfig_test.ini
   
The first few lines returned will look something like this::

   START HEADER
   [CONF]
   cache dir = _cache/sspp_testset_orbits/1-10
   [ASTEROID]
   population model = ./demo/sspp_testset_orbits.des
   spk t0 = 60188
   ndays = 395
   object1 = 1
   nobjects = 10
   spk step = 1
   nbody = T
   input format = whitespace
   [SURVEY]
   survey database = ./demo/baseline_v2.0_1yr.db
   field1 = 1
   nfields = 216011
   mpcobscode file = obslist.dat
   telescope = I11
   surveydbquery = SELECT observationId,observationStartMJD,fieldRA,fieldDEC,rotSkyPos FROM observations order by observationStartMJD
   [CAMERA]
   threshold = 5
   camera = instrument_circle.dat
   [OUTPUT]
   output file = stdout
   output format = csv
   Survey length:
   Field 1 : 60218.001805555556
   Field n : 60582.99947369435
   Days : 365.0
   END HEADER
   ObjID,FieldID,FieldMJD,AstRange(km),AstRangeRate(km/s),AstRA(deg),AstRARate(deg/day),AstDec(deg),AstDecRate(deg/day),Ast-Sun(J2000x)(km),Ast-Sun(J2000y)(km),Ast-Sun(J2000z)(km),Ast-Sun(J2000vx)(km/s),Ast-Sun(J2000vy)(km/s),Ast-Sun(J2000vz)(km/s),Obs-Sun(J2000x)(km),Obs-Sun(J2000y)(km),Obs-Sun(J2000z)(km),Obs-Sun(J2000vx)(km/s),Obs-Sun(J2000vy)(km/s),Obs-Sun(J2000vz)(km/s),Sun-Ast-Obs(deg),V,V(H=0)
   632,38059,60277.351867,983057302.988296,-27.914,143.141481,0.024483,8.677660,-0.022025,-718755527.053,707115399.940,202146766.832,-9.461,-9.435,-3.858,58803455.841,124187416.914,53827633.096,-28.129,10.565,4.677,8.010336,28.838,8.838
   632,46306,60289.319749,955259166.375772,-25.916,143.290960,-0.003491,8.469810,-0.012344,-728491905.519,697311952.040,198144183.848,-9.369,-9.524,-3.883,28969257.489,132531884.873,57445740.529,-30.037,5.053,2.290,7.422641,28.748,8.748
   632,46328,60289.330920,955234165.662179,-25.887,143.290920,-0.003562,8.469672,-0.012355,-728500949.842,697302758.025,198140435.373,-9.369,-9.524,-3.883,28940272.325,132536748.654,57447949.381,-30.022,5.025,2.287,7.421909,28.748,8.748
   632,48406,60292.334497,948632591.573514,-25.159,143.275797,-0.010595,8.436174,-0.009812,-730929572.603,694827991.907,197131809.209,-9.346,-9.547,-3.889,21194286.022,133717766.728,57960238.222,-30.274,3.559,1.661,7.219795,28.724,8.724
   632,48432,60292.346208,948607150.833510,-25.127,143.275672,-0.010647,8.436059,-0.009824,-730939030.057,694818331.543,197127873.378,-9.346,-9.547,-3.890,21163663.520,133721354.533,57961917.731,-30.254,3.533,1.659,7.218942,28.724,8.724
   632,49105,60293.342276,946459498.864074,-24.881,143.266024,-0.012946,8.426666,-0.008965,-731743091.175,693996357.947,196793023.849,-9.338,-9.554,-3.892,18580786.934,134029746.520,58095614.789,-30.327,3.053,1.450,7.147094,28.715,8.715
   632,50469,60295.348632,942200588.209358,-24.322,143.239649,-0.017554,8.410343,-0.007257,-733360678.321,692338765.443,196118002.537,-9.323,-9.569,-3.896,13361661.832,134524609.291,58310240.323,-30.416,2.061,1.028,6.995151,28.698,8.698


This generates the ephemerides for the objects we are looking for. This information will be used when running the SSPP.
Save this information as a file called 'test_oif_output.txt'.

.. warning::
   Only one instance of OIF can be run per output directory. Make sure to have different output pathways if you are running multiple instances on the same compute node. 


Using Relative File Paths
---------------------------------------------------------------

OIF assumes explicit file paths so ../this_directory will cause errors. It is best to give the full output and input paths for directories and input file/ouput file locations.


Objects in Field Configuration File
------------------------------------

.. tip::
   We recommend that **nbody** should be always be set to **True**. You can break up the task across multiple proccesses if you need an increase in speed.

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

