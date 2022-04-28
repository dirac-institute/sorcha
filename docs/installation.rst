Installation
============

In order to use the Solar System survey simulator, we must first install 
`Objects in Field <https://github.com/eggls6/objectsInField>`_. 
This is used to generate candidate detections for an input population of 
moving objects in a specified list of field pointings.

OIF Requirements
-----------------------
* python 3
* spiceypy python library
* pyoorb python library
* numpy
* pandas
* matplotlib
* NAIF SPICE Utilities

Initial Steps
----------------------------------
Create a directory to contain the OIF and Survey Simulator repos::

   mkdir survey_sim_pp
   cd survey_sim_pp
   
Create a conda environment::

   conda create -n survey_sim_pp -c conda-forge -c mjuric python spiceypy openorb numpy pandas matplotlib spice-utils pip
   conda activate survey_sim_pp
   

Installing Objects in Field
----------------------------------
Make sure you are in the directory you want to contain the Survey Simulator repo in::

   cd survey_sim_pp
   
Download the OIF repo via::
    
   git clone https://github.com/eggls6/objectsInField.git
   
And cd into the repo::

   cd objectsInField
   
There are various large binary files (mostly SPICE kernels) that aren't kept in git, so these
can be installed by running::

   ./bootstrap.sh
   
. note::
   The bash script downloads and stores the SPICE files to oif/data/  

Next, set up an editable (in-place) development environment::

   pip install -e .

This will allow you to run the code from the source directory.

Finally, run a test to make sure everything worked::

   cd test
   oif input.config

If everything has installed correctly, the first few lines from this output will be::
   
   ObjID, FieldID, FieldMJD, AstRange(km), AstRangeRate(km/s), AstRA(deg), AstRARate(deg/day), AstDec(deg), AstDecRate(deg/day), Ast-Sun(J2000x)(km), Ast-Sun(J2000y)(km), Ast-Sun(J2000z)(km), Ast-Sun(J2000vx)(km/s), Ast-Sun(J2000vy)(km/s), Ast-Sun(J2000vz)(km/s), Obs-Sun(J2000x)(km), Obs-Sun(J2000y)(km), Obs-Sun(J2000z)(km), Obs-Sun(J2000vx)(km/s), Obs-Sun(J2000vy)(km/s), Obs-Sun(J2000vz)(km/s), Sun-Ast-Obs(deg), V, V(H=0)
   S100003Ua,992,59855.012720,232764749.248562,19.381,313.391309,0.093855,-14.189297,-0.001147,302701424.872,-141376977.611,-47258199.518,10.938,16.381,6.838,147675817.300,22607836.793,9798564.669,-5.071,27.085,11.641,22.025168,12.229,3.789
   S100005xa,40,59854.002209,311895722.264139,18.108,312.493375,0.024745,-10.868628,-0.020284,355032405.197,-205593003.122,-50029660.233,8.437,15.234,7.005,148124584.428,20259701.559,8780700.962,-4.542,27.134,11.674,17.656392,14.416,4.726


To uninstall::

   python setup.py develop -u

Survey Simulator Requirements
-----------------------------
* python 3
* numpy
* pandas
* pytest
* pytest-cov<2.6.0
* coveralls
* setuptools>=42
* wheel
* setuptools_scm>=3.4
* astropy
* scipy
* sbpy

Installing the Survey Simulator Post Processing
------------------------------------------------
Make sure you are in the directory you want to contain the Survey Simulator repo in::

   cd survey_sim_pp
   
In order to install the Solar System survey simulator, either clone the repo 
directly from the `projects github <https://github.com/dirac-institute/survey_simulator_post_processing>`_ or
via::

   git clone https://github.com/dirac-institute/survey_simulator_post_processing.git
   
Next, ensure you are in the main Survey Simulator directory and set up an editable (in-place) development environment::

   cd ~/survey_simulator_post_processing
   pip install -e .


Testing the Installation
------------------------------------------------

To test that the installation was done correctly, run::

   surveySimPP -c ./PPConfig.ini -l ./data/test/testcolour.txt -o ./data/test/testorb.des -p ./data/test/oiftestoutput.txt
   
The output will appear in a csv file in .data/out (this pathway can be changed in the config file).
The output should look like::

   This
