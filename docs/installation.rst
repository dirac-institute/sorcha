.. _installation:

Installation
=================

.. note::
   The Sorcha python package is currently pip installable. 

Requirements
-----------------------------

Sorcha has the following requirements that will be automatically installed  using pip or conda when you install the sorcha package:

* python 3.9 or later
* numpy
* pandas
* scipy
* astropy
* matplotlib
* sbpy
* pytables
* difi == 1.2rc3
* sqlite3
* spiceypy
* healpy
* assist
* rebound
* pooch
* tqdm

Setup Your Conda Environment 
------------------------------
**Step 1** Create a directory to contain the OIF and Sorcha repos::

   mkdir sorcha
   cd sorcha

.. tip::
   We recommend using python version 3.9 or higher with Sorcha. 

**Step 2** Create a conda environment::

   conda create -n sorcha -c conda-forge -c moeyensj numpy pandas scipy astropy matplotlib sbpy pytables difi==1.2rc3 sqlite3 spiceypy healpy rebound pooch tqdm python=3.10
   conda activate sorcha

Installing Sorcha
----------------------

Unless you're editing the source code, you can use the version of Sorcha published on pypy using pip::
   pip install sorcha --upgrade

Installing Sorcha in Development Mode
----------------------------------------
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
   
The output will appear in a csv file (testrun_e2e.csv) in .data/out (this pathway can be changed via the -u command line argument). The first 51 lines of the csv file should look like this:

.. literalinclude:: ../docs/example_files/testrun_e2e.csv
    :language: text
    :lines: 1-51

.. note::
   This test run is using pre-made ephemeris generasted by OIF already stored in the demo directory of the github Sorcha repository. 
