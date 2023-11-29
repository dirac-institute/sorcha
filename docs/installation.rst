.. _installation:

Installation
=================

.. note::
   Sorcha is both conda/mamba and pip installable. We recommend installing via conda/mamba. 

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
* spiceypy
* healpy
* assist
* rebound
* pooch
* tqdm

.. tip::
   We also recommend installing h5py in your conda/mamba environment to ensure that the proper HD5 libraries are installed. 



Setup Your Conda Environment 
------------------------------

**Step 1** Create a conda or mamba environment.

If using conda::

   conda create -n sorcha -c conda-forge assist numpy numba pandas scipy astropy matplotlib sbpy pytables spiceypy healpy rebound pooch tqdm h5py python=3.10 

If using mamba::

   mamba create -n sorcha -c conda-forge assist numpy numba pandas scipy astropy matplotlib sbpy pytables spiceypy healpy rebound pooch tqdm h5py python=3.10

.. tip::
   We recommend using python version 3.9 or higher with Sorcha. The conda command uses python 3.10.

**Step 2** Activate your conda/mamba environment

On conda::

   conda activate sorcha

On mamba::

   mamba activate sorcha

Installing Sorcha
----------------------

Unless you're editing the source code, you can use the version of Sorcha published on conda-forge. 

If using conda::

   conda install -c conda-forge sorcha

If using mamba::

   mamba install -c conda-forge sorcha

You can install sorcha via from pypi using pip, but installation via  conda/mamba is recommended. 

If using pip::

   pip install --upgrade sorcha

.. _dev_mode:

Installing Sorcha in Development Mode
---------------------------------------------------------------------

.. tip::
   This is in the installation method for adding/edit Sorcha's codebase or for working on/updating Sorcha's documentation. 

**Step 1** Create a directory to contain the Sorcha repos::

   mkdir sorcha

**Step 2** Navigate to the directory you want to store the Sorcha source code in::

   cd sorcha
   
**Step 3** Download the Sorcha source code via::

   git clone https://github.com/dirac-institute/sorcha.git

**Step 4** Navigate to the sorcha repository directory::

   cd sorcha
   
**Step 5** Install an editable (in-place) development version of Sorcha. This will allow you to run the code from the source directory.

If you just want the source code installed so edits in the source code are automatically installed::

   pip install -e .

If you are going to be editing documentation or significantly modifying unit tests, it is best to install the full development version::

   pip install -e '.[dev]'

**Step 6 (Optional unless working on documentation):** You will also install the pandoc package (either via conda/pip or `direct download <https://pandoc.org/installing.html>`_ .


.. _installation_aux:

Downloading Required Supplemental Files
----------------------------------------

To run the internal ephemeris generator, you will need to download the auxiliary files required by  assist and rebound for performing the N-body integrations. 
  
To install the necessary SPICE auxiliary files for ephemeris generation (774 MB total in size)::

    bootstrap_sorcha_data_files

.. note::
   This script will download and store the auxiliary files in your computer's local cache directory. 

.. note::
   These files are stored in your system's cache by default if the optional --cache flag is not provided. If the files already downloaded and want a fresh download, you need to use the -f flag. 

.. warning:: These files can change/be updated with the revised positions of the planets every once in a while. So if you're running simulations for population statistics, we recommend downloading these files to a directory and having all Sorcha runs these files for consistency. 
 
Testing Your Sorcha Installation
----------------------------------

You can check that the Sorcha installation was done correctly, by downloading the Sorcha source code repository (Steps 1-4 **only**  of :ref:`dev_mode`) and then running::

   sorcha -c ./demo/sorcha_config_demo.ini -p ./demo/sspp_testset_colours.txt -ob ./demo/sspp_testset_orbits.des -pd ./demo/baseline_v2.0_1yr.db -o ./ -t testrun_e2e
   
The output will appear in a csv file (testrun_e2e.csv) in your current directory. The first 51 lines of the csv file should look like this:

.. literalinclude:: ../docs/example_files/testrun_e2e.csv
    :language: text
    :lines: 1-51

.. note::
   This test run is using pre-generated ephemeris already stored in the demo directory of the Sorcha GitHub repository. 
