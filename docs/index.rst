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
   For a more detailed description of ``Sorcha`` and how it works, please see Merritt et al. (submiited) and Holman et al. (submitted).

.. warning::
   This documentation site and the software package it describes are under
   review.. DO NOT USE this for science purposes just yet. Please wait until we release version 1.0.



What is Sorcha?
------------------------------------------

``Sorcha`` (pronounced "surk-ha") is an open-source Solar System survey simulator written in Python. 
``Sorcha`` means light or brightness in Irish and Scots Gaelic. Sorcha estimates the brightness of
simulated Solar System small bodies and determines which ones the survey could detect in
each of the survey's observations  based on user set criteria. ``Sorcha`` has been designed 
with the `Vera C. Rubin Observatory Legacy Survey of Space and Time (LSST) <https://www.lsst.org>`_ 
in mind. The software has a modular design, and our code  can be adapted to be 
used with any survey.   

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
