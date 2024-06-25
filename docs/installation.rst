.. _installation:

Installation
=================

.. note::
   Sorcha is both conda/mamba and pip installable. We recommend installing via conda/mamba. 

Requirements
-----------------------------

Sorcha has the following requirements that will be automatically installed  using pip or conda when you install the sorcha package:

* python 3.10 or later
* assist
* astropy
* healpy
* importlib_resources
* matplotlib
* numba
* numpy
* pandas
* pooch
* pytables
* rebound
* sbpy
* scipy
* spiceypy
* tqdm

.. tip::
   We also recommend installing h5py in your conda/mamba environment to ensure that the proper HD5 libraries are installed. 



Setup Your Conda Environment 
------------------------------

**Step 1** Create a conda or mamba environment.

If using conda::

   conda create -n sorcha -c conda-forge assist numpy numba pandas scipy astropy matplotlib sbpy pytables spiceypy healpy rebound pooch tqdm h5py importlib_resources python=3.10 

If using mamba::

   mamba create -n sorcha -c conda-forge assist numpy numba pandas scipy astropy matplotlib sbpy pytables spiceypy healpy rebound pooch tqdm h5py importlib_resources python=3.10

.. tip::
   We recommend using python version 3.10 or higher with Sorcha. The conda command uses python 3.10.

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

   pip install sorcha

.. _installation_aux:

Downloading Required Supplemental Files
----------------------------------------

To run Sorcha's built in :ref:`ephemeris generator<ephemeris_gen>`, you will need to download the auxiliary files required by  assist and rebound for performing the N-body integrations. 
  
To install the necessary `SPICE (Spacecraft, Planet, Instrument, C-matrix, Events) <https://naif.jpl.nasa.gov/naif/spiceconcept.html>`_ auxiliary files and other required data files for ephemeris generation (774 MB total in size)::

    sorcha bootstrap

.. note::
   This script will download and store the auxiliary files in your computer's local cache directory by default. 

.. note::
   The optional --cache flag allows you to specify a specific location to download the auxillary files. If the files have  already downloaded and want a fresh download, you need to use the -f flag. 

.. warning:: These files can change/be updated with the revised positions of the planets every once in a while. So if you're running simulations for population statistics, we recommend downloading these files to a directory and having all Sorcha runs these files for consistency. 
 
Testing Your Sorcha Installation
----------------------------------

You can check that the Sorcha installation was successful, by obtaining the demo input files and running the demo command. 

The demo input files and configuration file are installed with the socha package. You can run the following command on the command line to copy the files to the current directory (or a different location)::

    sorcha demo prepare

.. note::
   The optional -p flag allows you to specify a specific location to copy the demo input files. If the files already exist, the  -f flag can be used to force a fresh copy of the files to be generated. .

You can find the command to run the sorcha demo on the command line in two ways. First on the command line::

   sorcha demo howto

Or you can in an interactive python session or jupyter notebook. You can run the following

.. exec::

   from sorcha.utilities.sorcha_demo_command import get_demo_command
   print(get_demo_command())

.. note::
   The demo command assumes that the demo input files are in the local directory.

.. tip::
   If the auxillary files are installed in a different location you will need to specify their location using the --ar flag
   
The output will appear in a csv file (testrun_e2e.csv) in your current directory. The first 51 lines of the csv file should look like this (because of the random number generation the values will not be exactly the same):

.. literalinclude:: ../docs/example_files/testrun_e2e.csv
    :language: text
    :lines: 1-51

.. tip::
   Two log files will be created in the current directory. One \*.log and one \*.err. The \*.err log file should be empty if all run successfully. 

.. _dev_mode:

Installing Sorcha in Development Mode
---------------------------------------------------------------------

**This is the installation method for adding/edit Sorcha's codebase or for working on/updating Sorcha's documentation.**

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


