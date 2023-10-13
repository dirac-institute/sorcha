Running on HPCs & Parallel Processing 
===============================================
Testing Your Sorcha Installation

**Step 6** Install the necessary SPICE auxiliary files for ephemeris generation (774 MB total in size)::

    bootstrap_sorcha_data_files --cache <directory>

.. tip::
   For the getting started tutorial we recommend installing these auxiliary files in ./ar_files

.. note::
   These files are stored in your system's cache by default if the --cache flag is not provided. If the files already downloaded and want a fresh download, you need to use the -f flag.

.. warning:: These files can change/be updated with the revised positions of the planets every once in a while. So if you're running simulations for population statistics, we recommend downloading these files to a directory and having all Sorcha runs these files for consistency.

