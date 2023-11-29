.. Sorcha documentation master file, created by
   sphinx-quickstart on Fri Jan  1 13:51:32 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. image:: images/sorcha_logo.png
  :width: 410
  :alt: Sorcha logo
  :align: center

=========================================================================

What is Sorcha?
=========================================================================

Sorcha (pronounced "surk-ha") is a python Solar System survey simulator. Sorcha means light 
or brightness in Irish and Scots Gaelic, and our software is estimating the brightness of
simulated Solar System small bodies and determines which ones the survey could detect in
each of the survey's observations or based on user set criteria. Sorcha has been designed 
with the `Vera C. Rubin Observatory Legacy Survey of Space and Time (LSST) <https://www.lsst.org>`_ 
in mind. The software has a modular design, and with some effort it can be adapted to be 
used with any survey.   

.. warning::
   This documentation site and the software package it describes are under
   active development. Validation is still on-going. DO NOT USE this for science
   purposes just yet. WE REALLY MEAN THIS. THE CODEBASE IS UNDER HEAVY DEVELOPMENT.
 

Welcome to Sorcha's documentation!
=========================================================================

This documentation site contains an installation guide, an overview of how Sorcha
works, tutorials, and demonstration notebooks that show how each of the various key filters within Sorcha work.

.. seealso::
   We have a summary paper (currently in prep) that provides a broad summary
   of the software with significant detail on the methodology behind Sorcha’s design.
   This documentation presented here covers some of the same material but dives 
   deeper into how to install and how to run simulations of what LSST would discover given a
   model population of synthetic Solar System bodies and a given pointing history
   for the survey.

.. toctree::
   :hidden:
   :maxdepth: 2
   :caption: Contents:

   overview
   installation
   inputs
   ephemerisgen
   filters
   complexparameters
   configfiles
   outputs
   gettingstarted
   hpc
   whatsorchadoesnotdo
   notebooks
   troubleshooting
   support
   release
   contributors   
   acknowledgements
   cite
   uninstall 


