.. _installation:

Installation
=================

.. note::
   ``Sorcha`` is both conda/mamba and pip installable. We recommend installing via conda/mamba. 

Requirements
-----------------------------

``Sorcha`` has the following requirements that will be automatically installed  using pip or conda when you install the sorcha package:

* python 3.11 or later
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
   We also recommend installing h5py in your conda/mamba environment to ensure that the proper HDF5 libraries are installed. 



Setup Your Conda Environment 
------------------------------

**Step 1** Create a conda or mamba environment.

If using conda::

   conda create -n sorcha -c conda-forge assist numpy numba pandas scipy astropy matplotlib sbpy pytables spiceypy healpy rebound pooch tqdm h5py importlib_resources python=3.11 

If using mamba::

   mamba create -n sorcha -c conda-forge assist numpy numba pandas scipy astropy matplotlib sbpy pytables spiceypy healpy rebound pooch tqdm h5py importlib_resources python=3.11

.. tip::
   We recommend using python version 3.11 or higher with  ``Sorcha``. The conda/mamba install command uses python 3.11.

**Step 2** Activate your conda/mamba environment

On conda::

   conda activate sorcha

On mamba::

   mamba activate sorcha

Installing Sorcha
----------------------

Unless you're editing the source code, you can use the version of  ``Sorcha`` published on conda-forge. 

If using conda::

   conda install -c conda-forge sorcha

If using mamba::

   mamba install -c conda-forge sorcha

You can install ``Sorcha`` via from PyPi using pip, but installation via  conda/mamba is recommended. 

If using pip::

   pip install sorcha

Testing Your Sorcha Installation
----------------------------------

You can check that the  ``Sorcha`` installation was successful, by obtaining the demo input files and running the demo command. The demo input files and configuration file are installed with the ``Sorcha`` package. Further details are provided on the :ref:`quickstart` page.

.. _dev_mode:

Installing Sorcha in Development Mode
---------------------------------------------------------------------

**This is the installation method for adding/edit sorcha's codebase or for working on/updating sorcha's documentation.**

**Step 1** Create a directory to contain the ``Sorcha`` repos::

   mkdir sorcha

**Step 2** Navigate to the directory you want to store the ``Sorcha`` source code in::

   cd sorcha
  
**Step 3** Download the ``Sorcha`` source code via::

   git clone https://github.com/dirac-institute/sorcha.git

**Step 4** Navigate to the  ``Sorcha`` repository directory::

   cd sorcha
  
**Step 5** Install an editable (in-place) development version of ``Sorcha``. This will allow you to run the code from the source directory.

If you just want the source code installed so edits in the source code are automatically installed::

   pip install -e .

If you are going to be editing documentation or significantly modifying unit tests, it is best to install the full development version::

   pip install -e '.[dev]'

**Step 6 (Optional unless working on documentation):** You will need to install the pandoc package (either via conda/pip or `direct download <https://pandoc.org/installing.html>`_ and a version of the `sorcha-addons package <https://github.com/dirac-institute/sorcha-addons>`_. 


