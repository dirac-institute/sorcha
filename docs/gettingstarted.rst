.. _quickstart:

Getting Started
=====================

In this demonstration, we will show you how to setup and run a basic simulation using ``Sorcha``. 

.. seealso::
    ``Sorcha`` is designed to allow multiple instances to be run in parallel in order to accommodate simulations with very large numbers of synthetic planetesimals by breaking up the job across multiple live processes. We recommend first starting with the examples below, before moving on to our :ref:`parallel processing/high-performance computing (HPC) guide <hpc>`.

Grab All The Demo Files
-------------------------

Use the following command to copy all the demo :ref:`inputs <inputs>` and :ref:`configuration file <configs>` to your local directory::

   sorcha demo prepare

.. note::
  All input data files in this example are white-space separated format solely for the ease of reading.


.. note::
   The optional -p (--path) flag allows you to specify a specific location to copy the demo input files. The demo command you will be using expects these files will be in your current workingn directory.

.. tip::
    If the files already exist and you want a fresh copy, the -f (--force)  flag can be used to force a fresh copy of the files to be generated.

Orbit and Physical Parameters Files For the Input Solar System Small Body Population
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Orbit File
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The :ref:`orbits` in the demo set is labeled **sspp_testset_orbits.des**, which contains the orbits of five synthetic objects:

.. literalinclude:: ../src/sorcha/data/demo/sspp_testset_orbits.des
    :language: text

Physical Parameters File
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The :ref:`physical` is named **sspp_testset_colours.txt**. This file assigns colors, phase curve properties, and absolute magnitudes to each of the simulated small bodies whose orbits are defined in our input orbit file. The contents of the file are below:

.. literalinclude:: ../src/sorcha/data/demo/sspp_testset_colours.txt
    :language: text

.. note::
  For this demo, we have defined chosen the main filter to be r-band.

Survey Pointing Database 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We'll be using the first year of the baseline v2.0 ``rubin_sim`` LSST cadence simulation as the :ref:`pointing` (**baseline_v2.0_1yr.db**).

Configuration File 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The **sorcha_config_demo.ini** :ref:`configs` will initalize ``Sorcha``. The contents of the file are below: 

.. literalinclude:: ../demo/sorcha_config_demo.ini
    :language: text

.. note::
   The demo configuration file sets the  output to be in CSV (comma-separated values) format.   


Downloading Auxiliary Files For the Ephemeris Generator
-----------------------------------------------------------

To run ``Sorcha``'s built in :ref:`ephemeris generator<ephemeris_gen>`, you will need to download the auxiliary files required by  assist and rebound for performing the N-body integrations.
   
To install the necessary `SPICE (Spacecraft, Planet, Instrument, C-matrix, Events) <https://naif.jpl.nasa.gov/naif/spiceconcept.html>`_ auxiliary files and other required data files for ephemeris generation (774 MB total in size) run the following command on the command line::

    sorcha bootstrap

.. note::
   This script will download and store the auxiliary files in your computer's local cache directory by default which is where the demo command will expect the files are installed. The optional --cache flag allows you to specify a specific location to download the auxiliary files. If the files have  already downloaded and want a fresh download, you need to use the -f flag. 

.. warning:: These files can change/be updated with the revised positions of the planets every once in a while. So if you're running simulations for population statistics, we recommend downloading these files to a directory and having all Sorcha runs these files for consistency.


.. tip::
   If the auxiliary files are installed in a different location you will need to specify their location using the --ar flag when running ``Sorcha``

Running Sorcha
----------------------

We now have all the required input files. If you downloaded the ``Sorcha`` repository, start by moving into the ``Sorcha`` directory or make a demo directory called **demo** and move/copy all the input files into there. For this example run, we assume that you have downloaded the required ephemeris generator's auxiliary files to ./ar_files. Check the :ref:`installation` instructions for further details. 

Next, let's take a look at the command line arguments for the ``sorcha run``. On the command line, typing::

   sorcha run --help 

will produce

.. literalinclude:: ./example_files/help_output.txt 
    :language: text

Now that you know how to provide the input files, let's go run a simulation: You can find the command to run the ``Sorcha`` demo on the command line in two ways. First on the command line::

   sorcha demo howto

Or you can in an interactive python session or jupyter notebook. You can run the following

.. exec::

   from sorcha.utilities.sorcha_demo_command import get_demo_command
   print(get_demo_command())

Four files will be created in the current directory after you run the **sorcha run** command. Two will be log files (.log and .err). The other two files will be CSV (comma-separated values; .csv) files.

.. tip::
   The log files have One \*.log with information about the run  and one \*.err that is used to save error messages from the run. The \*.err log file should be empty if ``Sorcha`` ran successfully.

One of the files will be the  :ref:`detections file <detections>` (information about each observation of the input small body population in the simulated astronomical survey) will appear in a CSV file (**testrun_e2e.csv**) in your current directory. The first 21 lines of this CSV file should look like this (because of the random number generation the values will not be exactly the same):

.. literalinclude:: ../docs/example_files/testrun_e2e.csv
    :language: text
    :lines: 1-21

The last file outputted will be the :ref:`statistics or tally file <statsf>` (**testrun_stats.csv**) in CSV format that has summary statistics about each of the input objects detected by the simulated survey. The first 15  lines of this CSV file should look like this (because of the random number generation the values will not be exactly the same):

.. literalinclude:: ../docs/example_files/testrun_stats.csv
    :language: text
    :lines: 1-15

.. tip::
   If you want to run this command a second time you'll need to add a **-f** flag to the command line to force overwriting output files that already were exist in the output directory. Do note that the previous run's log and error log files will not be removed. New log files are generated at each run.  

Available Commands Within Sorcha
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To see all the commands/utilities available within ``Sorcha``, run::

   sorcha --help

.. literalinclude:: ./example_files/sorcha_help.txt
    :language: text
