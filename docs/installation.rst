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
* numba
* scipy
* astropy
* matplotlib
* sbpy
* pytables
* difi == 1.2rc3
* spiceypy
* healpy
* assist
* rebound
* pooch
* tqdm

Setup Your Conda Environment 
------------------------------

**Step 1** Create a conda environment::

   conda create -n sorcha -c conda-forge -c moeyensj numpy numba pandas scipy astropy matplotlib sbpy pytables difi==1.2rc3 spiceypy healpy rebound pooch tqdm python=3.10
   conda activate sorcha

.. tip::
   We recommend using python version 3.9 or higher with Sorcha. The conda command uses python 3.10. 

Installing Sorcha
----------------------

Unless you're editing the source code, you can use the version of Sorcha published on pypy using pip::

   pip install --upgrade sorcha


.. _dev_mode:

Installing Sorcha in Development Mode
----------------------------------------
**Step 1** Create a directory to contain the Sorcha repos::

   mkdir sorcha

**Step 2** Navigate to the directory you want to store the Sorcha soure code in::

   cd sorcha
   
**Step 3** Download the Sorcha soure code via::

   git clone https://github.com/dirac-institute/sorcha.git

**Step 4** Navigate to the sorcha repository directory::

   cd sorcha
   
**Step 5** Install an editable (in-place) development version of Sorcha. This will allow you to run the code from the source directory.::

   pip install -e .


Testing Your Sorcha Installation
----------------------------------

You can check that the Sorcha installation was done correctly, by downloading the Sorcha source code repository (Steps 1-4 **only**  of :ref:`dev_mode`) and then running::

   sorcha -c ./demo/PPConfig_test.ini -p ./demo/sspp_testset_colours.txt -ob ./demo/sspp_testset_orbits.des -e ./demo/example_oif_output.txt -pd ./demo/baseline_v2.0_1yr.db -o ./ -t testrun_e2e
   
The output will appear in a csv file (testrun_e2e.csv) in your current directory. The first 51 lines of the csv file should look like this:

.. literalinclude:: ../docs/example_files/testrun_e2e.csv
    :language: text
    :lines: 1-51

.. note::
   This test run is using pre-generated ephemeris already stored in the demo directory of the Sorcha github repository. 
