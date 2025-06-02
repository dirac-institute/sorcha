.. Sorcha documentation master file, created by
   sphinx-quickstart on Fri Jan  1 13:51:32 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. image:: images/sorcha_logo.png
  :width: 410
  :alt: Sorcha logo
  :align: center

=========================================================================

.. tip::
    We strongly recommend all new users read the ``Sorcha`` documentation before beginning any science-quality simulations.

Welcome to Sorcha's documentation!
------------------------------------------

This documentation site contains an installation guide, an overview of how ``Sorcha``
works, tutorials, and demonstration notebooks that show how each of the various components within ``Sorcha`` work and can be customized.

.. seealso::
   For a more detailed description of ``Sorcha`` and how it works, please see  `Merritt et al. (in press) <https://www.dropbox.com/scl/fi/ku3s6aqpo6p8cambfclqi/Merritt_et_al_sorcha_paper.pdf?rlkey=07daa4q51nvr1tf7b818s3fy4&dl=0>`_  and `Holman et al. (in press) <https://www.dropbox.com/scl/fi/uofk7nz64a9xzf0aszmtx/sorcha_ephemeris_generation_paper.pdf?rlkey=2xmzwxar7qj2tj48qpqq3xcae&dl=0>`_.

.. warning::
   The code is still under going JOSS (Journal of Open Source Software) review, but we expect minimal changes as that finalizes. The code in the repository has been validated (see the :ref:`various validation notebooks we provide <demonotebooks>`).
   We will release ``Sorcha`` v1.0 on PyPI and conda-forge soon - do double check the version from conda-forge/pypi. If your version is less than v1.0 uninstall and install via the development instructions using the source code directly from the Github repo. 


What is Sorcha?
------------------------------------------

``Sorcha`` (pronounced "sur-kha"; derived from the Old Irish word for 'light' or 'brightness') is an open-source Solar System survey simulator written in Python. 
``Sorcha`` estimates the brightness of simulated Solar System small bodies and determines which ones the survey could detect in
each of the survey's observations  based on user set criteria. ``Sorcha`` has been designed with the `Vera C. Rubin Observatory Legacy Survey of Space and Time (LSST) <https://rubinobservatory.org>`_ 
in mind. The software has a modular design, and our code can be adapted to be used with any survey.   

.. toctree::
   :hidden:
   :maxdepth: 2
   :caption: Contents:

   overview
   installation
   configfiles
   inputs
   ephemerisgen
   postprocessing 
   outputs
   gettingstarted
   hpc
   whatsorchadoesnotdo
   cite
   troubleshooting
   support
   uninstall 
   advanced
   notebooks   
   release
   contributors   
   acknowledgements
