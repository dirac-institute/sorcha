Getting Started
=====================

In this section we provide an overview of how to use Sorcha. We start by generating a set of files containing information 
on the synethic planetoids that we wish to study. We take you through the process of generating
ephemerides for these synthetic bodiess using OIF (Objects in Field), and show you how to use Sorcha. 

.. tip::
   In this quick start guide, we demonstrate how to run a single instance of Sorcha. Sorcha is designed to allow multiple instances to be run in parallel in order to accomodate simulations with very large numbers of synthetic planetesimals by breaking up the job across multiple live proccesses. We recommend first starting with the examples below, before moving on to parallel processing.


.. important::
  All the input files and configuration files used in this demonstation are available in the demo directory within the Sorcha github repository (sorcha/sorcha/demo). Below includes instructions on how to generate these, but you can skip those setps and go straight to the run commands if you need to.

.. note::
  All input data files in this example are white-space separated format solely for the ease of reading.   

Creating the Orbit and Physical Parameter Files For the Synthetic Small Bodies
----------------------------------------------------------------------------------------
The first step in the process is to generate a set of files which describe the orbital and physical parameters
of the objects that we wish to study. Here we will generate a file called 'sspp_testset_orbits.des', which contains
the orbits of five objects

.. literalinclude:: ../demo/sspp_testset_orbits.des
    :language: text

We will also generate a file called 'sspp_testset_colours.txt' which contains information about the colour and brightness of the objects

.. literalinclude:: ../demo/sspp_testset_colours.txt
    :language: text


Setting Up Sorcha's Configuration File 
------------------------------------------

The key information about the simulation paramteres are held in the configuration file. For further details check out our :ref:`configs` page. 

Running Sorcha
----------------------

Let's take a look at the command line arguments for sorcha. On the command line, typing::

   sorcha --help 

will produce

.. literalinclude:: ../demo/sspp_testset_colours.txt
    :language: text


Finally, we have all the information required to run the survey simulator. This can be done by typing::

   sorcha -c ./demo/PPConfig_test.ini -p ./demo/sspp_testset_colours.txt -o ./demo/sspp_testset_orbits.des -e ./demo/example_oif_output.txt -u ./data/out/ -t testrun_e2e 

.. tip::
   Sorcha outputs a log file and error file. If all has gone well, the error file will be empty. The log file has the configuration parameters outputted to it as a record of the run setup.

.. warning::
   Only one instance of Sorcha can be run per output directory. Make sure to have different output pathways if you are running multiple instances on the same compute node.

The first 51 lines of  output will look something like

.. literalinclude:: ../docs/example_files/testrun_e2e.csv
    :language: text
    :lines: 1-51

   
