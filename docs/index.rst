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

Sorcha (pronounced "surk-ha") is an open-source Solar System survey simulator written in Python. 
Sorcha means light or brightness in Irish and Scots Gaelic. Sorcha estimates the brightness of
simulated Solar System small bodies and determines which ones the survey could detect in
each of the survey's observations  based on user set criteria. Sorcha has been designed 
with the `Vera C. Rubin Observatory Legacy Survey of Space and Time (LSST) <https://www.lsst.org>`_ 
in mind. The software has a modular design, and our code  can be adapted to be 
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
   A summary paper (currently in prep) provides a more detailed account
   of the software and Sorcha’s design methodology.
   This documentation focuses on installation and examples of how to use Sorcha for LSST simulation.

.. toctree::
   :hidden:
   :maxdepth: 2
   :caption: Contents:

   overview
   installation
   inputs
   ephemerisgen
   apparentmag 
   filters
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
