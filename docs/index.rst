.. Sorcha documentation master file, created by
   sphinx-quickstart on Fri Jan  1 13:51:32 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Sorcha's documentation!
=========================================================================
Welcome to the Sorcha documentation. Sorcha is a survey simulator Python package
for studying Solar System object population statistics. It has been designed 
with the `Vera C. Rubin Observatory Legacy Survey of Space and Time (LSST) <https://www.lsst.org>`_ 
in mind but can be adapted to be used with any survey.


This documentation webpage contains an installation guide and an overview of how the survey simulator 
works. Tutorials are provided which give examples on how to determine if an object is on a field of view, 
if it is observable with LSST, and specific guides for near earth objects, Jupiter trojans, cometary objects etc.

.. warning::
   This documentation site and the software packages it describes are under
   active development. Validation is still on-going. DO NOT USE this for science
   purposes just yet.
 
.. seealso::
   We have a summary paper (currently in prep) that provides and a broad summary
   of the software and with significant detail in the methodology behind in it.
   This documentation covers some of the same material but dives deeper into how
   to install and how to run simulations of what LSST would discover given a
   model population of synthetic Solar System bodies and a given pointing history
   for the survey.



.. toctree::
   :hidden:
   :maxdepth: 2
   :caption: Contents:

   overview
   installation
   inputs
   filters
   configfiles
   exampleconfig
   outputs
   gettingstarted
   whatsspdoesnotdo
   troubleshooting
   support
   release
   contributors   
   acknowledgements
   cite
   uninstall 
   notebooks
