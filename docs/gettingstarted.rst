Getting Started
=====================

In this tutorial, we will show you how to setup and run a basic simulation using Sorcha. 

.. tip::
   In this tutorial,  we demonstrate how to run a single instance of Sorcha. Sorcha is designed to allow multiple instances to be run in parallel in order to accommodate simulations with very large numbers of synthetic planetesimals by breaking up the job across multiple live processes. We recommend first starting with the examples below, before moving on to parallel processing.


.. important::
  You can copy all the files used in this tutorial to your local directory  via the **sorcha demo prepare** command. 

.. note::
  All input data files in this example are white-space separated format solely for the ease of reading.   

Creating the Orbit and Physical Parameter Files For the Synthetic Solar System Populations
--------------------------------------------------------------------------------------------
The first step in the process is to generate a set of files which describe the orbital and physical parameters
of our synthetic Solar System population that we wish to input into the simulator. 

Making the Orbit File
~~~~~~~~~~~~~~~~~~~~~~~~

First, we will start with creating an :ref:`orbits`, and generate a file called 'sspp_testset_orbits.des', which contains the orbits of five synthetic objects The contents of the file is below:

.. literalinclude:: ../demo/sspp_testset_orbits.des
    :language: text

Make the Physical Parameters File
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Next, we need to produce the :ref:`physical`, which we call 'sspp_testset_colours.txt'. This file assigns colors, phase curve properties, and absolute magnitudes to each of the simulated small bodies whose orbits are defined in our input orbit file. The contents of the file is below:

.. literalinclude:: ../demo/sspp_testset_colours.txt
    :language: text

.. note::
  For this tutorial, we have defined chosen the main filter to be r-band. In the following configuration file, we will list the r filter first when we have to input our list of filters to use. 

Getting the Pointing Database 
------------------------------------------
For this tutorial, we're using the first year of the baseline v2.0 LSST cadence simulation as the :ref:`pointing`.

Setting Up Sorcha's Configuration File 
------------------------------------------

The key information about the simulation parameters are held in the configuration file. For further details check out our :ref:`configs` page. We'll be using the configuration file we have set up to get you started. The contents of the file is below: 

.. literalinclude:: ../demo/sorcha_config_demo.ini
    :language: text

.. note::
  For this tutorial, we have set up Sorcha to only find detections on g,r,i,z,u, or y filter observations, by what we have set the **observing_filters** parameter to. Since we specified the absolute magnitude and colors for our synthetic objects to r-band, the r filter starts the list of filters for  **observing_filters**.

.. note::
   This config file sets the  output to be in CSV format.   


Running Sorcha
----------------------

We now have all the required input files. If you downloaded the Sorcha repository, start by moving into the sorcha directory or make a demo directory called **demo** and move/copy all the input files into there. For this example run, we assume that you have downloaded the required ephemeris generator's auxiliary files to ./ar_files. Check the :ref:`installation` instructions for further details. 

Next, let's take a look at the command line arguments for sorcha. On the command line, typing::

   sorcha --help 

will produce

.. literalinclude:: ./example_files/help_output.txt 
    :language: text

Now that you know how to provide the input files, let's go run a simulation: You can find the command to run the sorcha demo on the command line in two ways. First on the command line::

   sorcha demo howto

Or you can in an interactive python session or jupyter notebook. You can run the following

.. exec::

   from sorcha.utilities.sorcha_demo_command import get_demo_command
   print(get_demo_command())


.. tip::
   Sorcha outputs a log file (*.sorcha.log) and error file (*.sorcha.err) in the output directory. If all has gone well, the error file will be empty. The log file has the configuration parameters outputted to it as a record of the run setup.

The output will appear in a csv file (testrun_e2e.csv) in your current directory. The first 51 lines of the csv file should look something like this:

.. literalinclude:: ../docs/example_files/testrun_e2e.csv
    :language: text
    :lines: 1-51

.. note:: The values will not be exactly the same because of the different random number generator seed applied each time Sorcha runs. We use the random generator to adjust the calculated values to be within the measurement precision/uncertainty both in position (RA/Dec) and apparent magnitude.  

.. tip::
   If you want to run this command a second time you'll need to add a **-f** flag to the command line to force overwriting output files that already were exist in the output directory. Do note that the previous run's log and error log files will not be removed. New log files are generated at each run.  

.. warning::
   Only one instance of Sorcha should be run per output directory to ensure that distinct log and error files are created for each Sorcha run. Make sure to have different output pathways if you are running multiple instances on the same compute node.
