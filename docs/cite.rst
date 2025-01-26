.. _citethecode:

.. image:: images/sorcha_logo.png
  :width: 410
  :alt: Sorcha logo
  :align: center

Citing the Software
==========================

``Sorcha`` is described provided in joint Astromical Journal/JOSS software papers:  `Merritt et al. (submitted) <https://www.dropbox.com/scl/fi/secetw7n0a936iynzxmau/sorcha_paper_2025_Jan_submission_version.pdf?rlkey=pbhchiattrw5bna8sfo6ljvto&dl=0>`_  and `Holman et al. (submitted) <https://www.dropbox.com/scl/fi/lz1lmua2s0yf9t9a2gpmm/sorcha_ephemeris_generation_paper.pdf?rlkey=blm9u4zbk0ci1i4lc5yqz8dbs&dl=0>`_. We also ask that you reference in your software citations and acknowledgements the other packages that ``Sorcha`` is built upon (see below). 

.. tip::
   Beyond citing the relevant papers, make sure to include details about your configuration for ``Sorcha`` (e.g. which footprint filter you're using), details about your input population (e.g. orbital, H, color, and phase curve distribution), and information about the pointing database used. 


.. hint::
   You find out what version of ``Sorcha`` you're running by typing **sorcha --version** on the command line. 

.. _citefunc:

Built-In Citation Function
----------------------------

If you use ``Sorcha`` in your research, please do include a citation in your published papers for ``Sorcha`` and the software packages and resources that ``Sorcha`` is based on.  The user can create a text file of the citation information (or output the information to the standard output on the terminal) by running the following command on the command line:: 
   
   sorcha cite
   

Additional Citation Details
----------------------------

Please also cite the software and ancillary data files that helps power ``Sorcha``. Our :ref:`citation function<citefunc>` described above will give the full details or you can manually find the acknowledgement information for each package:

* assist https://assist.readthedocs.io/en/latest/
* astropy https://www.astropy.org/acknowledging.html
* healpy https://healpy.readthedocs.io/en/latest/
* importlib_resources https://github.com/python/importlib_resources 
* matplotlib https://matplotlib.org/stable/users/project/citing.html
* Minor Planet Center https://www.minorplanetcenter.net/data
* numba https://numba.pydata.org/ 
* numpy https://numpy.org/citing-numpy/
* pandas https://pandas.pydata.org/about/citing.html
* pooch https://www.fatiando.org/pooch/latest/#
* pyTables https://www.pytables.org/
* rebound https://rebound.readthedocs.io/en/latest/
* sbpy https://joss.theoj.org/papers/10.21105/joss.01426
* scipy https://scipy.org/citing-scipy/
* SPICE kernels and ancillary data files https://naif.jpl.nasa.gov/naif/credit.html
* spiceypy https://spiceypy.readthedocs.io/en/main/citation.html
* tqdm https://tqdm.github.io/

.. note::
   The same information is available from our :ref:`built-on citation function<citefunc>`.

