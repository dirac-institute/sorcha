Installation
=======

In order to use the Solar System survey simulator, we must first install 
`Objects in Field <https://github.com/eggls6/objectsInField>`_. 
This is used to generate candidate detections for an input population of 
moving objects in a specified list of field pointings.

Requirements
-----------------------
* python 3
* spiceypy python library
* pyoorb python library
* other standard python libraries like numpy, pandas, etc.
* NAIF SPICE Utilities


Installing Objects in Field
----------------------------------
The easiest way to get started is by using the Anaconda Python Distribution's 
conda package manager::


   conda create -n oif-dev -c conda-forge -c mjuric python spiceypy openorb numpy pandas matplotlib spice-utils
   conda activate oif-dev
   
Download the repo via::
    
   git clone https://github.com/eggls6/objectsInField.git

Then download the various large binary files (mostly SPICE kernels) that we don't keep in git by running::

   ./bootstrap.sh

Next, set up an editable (in-place) development environment::

   pip install -e .

This will allow you to run the code from the source directory.

Finally, run a test to make sure everything worked::

   cd test
   oif input.config

To uninstall::

   python setup.py develop -u



Installing the Survey Simulator Post Processing
------------------------------------------------
In order to install the Solar System survey simulator, either clone the repo 
directly from the `projects github <https://github.com/dirac-institute/survey_simulator_post_processing>`_ or
via::
   git clone https://github.com/dirac-institute/survey_simulator_post_processing.git