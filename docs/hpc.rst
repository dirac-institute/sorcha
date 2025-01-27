.. _hpc:

Parallelization
===============================================

Embarrassingly Parallel Problem
------------------------------------

``Sorcha``’s design lends itself perfectly to parallelization – when it simulates a large number of solar system objects, each one is considered in turn independently of all other objects. If you have access to a large number of computing cores, you can run ``Sorcha`` much more quickly by dividing up the labor: giving a small part of your model population to each core. 

This involves two subtasks: breaking up your model population into an appropriate number of input files with unique names and organizing a large number of cores to simultaneously run ``Sorcha`` on their own individually-named input files. Both of these tasks are easy in theory, but tricky enough in practice that we provide some guidance below.


Slurm
---------

Slurm Workload Manager is a resource management utility commonly used by computing clusters. We provide starter code for running large parallel  batches using slurm, though general guidance we provide is applicable to any system. Documentation for slurm is available `here <https://slurm.schedmd.com/>`_. Please note that your HPC (High Performance Computing) facility’s slurm setup may differ from those on which ``Sorcha`` was tested, and it is always a good idea to read any facility-specific documentation or speak to the HPC maintainers before you begin to run jobs.

Quickstart
--------------

We provide as a starting point our example scripts for running  on HPC facilities using slurm. Some modifications will be required to make them work for your facility.

Below is a very simple slurm script example designed to run the :ref:`demo files <quickstart>` three times on three cores in parallel. Here, one core has been assigned to each ``Sorcha`` run, with each core assigned 1Gb of memory. 

.. literalinclude:: ./example_files/multi_sorcha.sh 
    :language: text

Please note that time taken to run and memory required will vary enormously based on the size of your input files, your input population, and the chunk size assigned in the ``Sorcha`` configuration file: we therefore recommend test runs before you commit to very large runs. The chunk size is an especially important parameter: too small and ``Sorcha`` will take a very long time to run, too large and the memory footprint may become prohibitive. We have found that chunk sizes of 1000 to 10,000 work best.

Below is a more complex example of a slurm script. Here, multi_sorcha.sh calls multi_sorcha.py, which splits up an input file into a number of ‘chunks’ and runs ``Sorcha`` in parallel on a user-specified number of cores. 

multi_sorcha.sh:

.. literalinclude:: ./example_files/multi_sorcha.sh
    :language: text

multi_sorcha.py:

.. literalinclude:: ./example_files/multi_sorcha.py
    :language: python

.. note::
  We provide these here for you to copy, paste, and edit as needed. You might have to some slight modifications to both the slurm script and multi_sorcha.py depending if you're using ``Sorcha`` without calling the stats file.   

multi_sorcha.sh requests many parallel Slurm jobs of multi_sorcha.py, feeding each a different --instance parameter. After changing ‘my_orbits.csv’, ‘my_colors.csv’, and ‘my_pointings.db’ to match the above, it could be run as sbatch --array=0-9 multi_sorcha.sh 25 4 to generate ten jobs, each with 4 cores running 25 orbits each. 


You can run multi_sorcha.py on the command line as well::

   python  multi_sorcha.py --config sorcha_config_demo.ini --input_orbits mba_sample_1000_orbit.csv --input_physical mba_sample_1000_physical.csv --pointings baseline_v2.0_1yr.db --path ./ --chunksize 1000 --norbits 250 --cores 4 --instance 0 --stats mbastats --cleanup --copy_inputs 

This will generate a single output file. It should work fine on a laptop, and be a bit, but not 4x, faster than the single-core equivalent due to overheads (time sorcha run -c sorcha_config_demo.ini -pd baseline_v2.0_1yr.db -o ./ -t 0_0 --st mbatats_0 -ob mba_sample_1000_orbit.csv -p mba_sample_1000_physical.csv).

.. note::
  This ratio improves as input file sizes grow. Make sure to experiment with different numbers of cores to find what’s fastest given your setup and file sizes.


Sorcha’s Helpful Utilities
---------------------------------

``Sorcha`` comes with a tool designed to combine the results of multiple runs and the input files used to create them into tables on a SQL database. This can make exploring your results easier. To see the usage of this tool, on the command line, run::

   sorcha outputs create-sqlite –help

``Sorcha`` also has a tool designed to search for and check the logs of a large number of runs. This tool can make sure all runs completed successfully, and output to either the terminal or a .csv file the names of the runs which have not completed and the relevant error message, if applicable. To see the usage of this tool, on the command line run::

   sorcha outputs check-logs –help


Best Practices/Tips and Tricks
-------------------------------------

1. We strongly recommend that HPC users download the auxiliary files needed to run the ASSIST+REBOUND into a known, named directory, and use the -ar command line flag in their **sorcha run** call to point ``Sorcha`` to those files. You can download the auxiliary files using::

    sorcha bootstrap --cache <directory>

 And then run ``Sorcha`` via::

    sorcha run … -ar /path/to/folder/ 

This is because ``Sorcha`` will otherwise attempt to download the files into the local cache, which may be on the HPC nodes rather than in your user directory, potentially triggering multiple slow downloads.

2. We recommend that each ``Sorcha`` run be given its own individual output directory. If multiple parallel ``Sorcha`` runs are attempting to save to the same file in the same directory, this will cause confusing and unexpected results.

3. ``Sorcha`` output files can be **very large**, and user directories on HPC facilities are usually space-limited. Please ensure that your ``Sorcha`` runs are directing the output to be saved in a location with sufficient space, like your HPC cluster’s scratch drive.

4. Think about having useful, helpful file names for your outputs. It is often tempting to call them something like “sorcha_output_<number>” or “sorcha_output_<taskid>”, but hard-won experience has led us to instead recommend more explanatory names for when you come back to your output later.
 

.. tip::
  You can use the **sorcha init** command to copy ``Sorcha``'s :ref:`example configuration files  <example_configs>` into a directory of your choice.
 
