<h1 align="center">
<img src="https://raw.githubusercontent.com/dirac-institute/sorcha/main/docs/images/sorcha_logo.png" width="500">
</h1><br>

# An open-source community LSST Solar System Simulator

[![ci](https://github.com/dirac-institute/sorcha/actions/workflows/smoke-test.yml/badge.svg)](https://github.com/dirac-institute/sorcha/actions/workflows/smoke-test.yml)
[![pytest](https://github.com/dirac-institute/sorcha/actions/workflows/testing-and-coverage.yml/badge.svg)](https://github.com/dirac-institute/sorcha/actions/workflows/testing-and-coverage.yml)
[![Documentation Status](https://readthedocs.org/projects/sorcha/badge/?version=latest)](https://sorcha.readthedocs.io/en/latest/?badge=latest)
[![astropy](http://img.shields.io/badge/powered%20by-AstroPy-orange.svg?style=flat)](http://www.astropy.org/) 
[![Anaconda-Server Badge](https://anaconda.org/conda-forge/sorcha/badges/version.svg)](https://anaconda.org/conda-forge/sorcha)
[![PyPI - Version](https://img.shields.io/pypi/v/sorcha)](https://pypi.python.org/pypi/sorcha)
[![Template](https://img.shields.io/badge/Template-LINCC%20Frameworks%20Python%20Project%20Template-brightgreen)](https://lincc-ppt.readthedocs.io/en/latest/)

Documentation: https://sorcha.readthedocs.io

Other software utilities can be found in this github repository: [https://github.com/dirac-institute/sorcha-addons](https://github.com/dirac-institute/sorcha-addons)
## developer best practices
* Data sets should be moved to the `data` folder, have a readme.txt or readme.md to explain where the data came from as well as a time stamp in the readme.txt.
* Data sets that are used for unit testing should live in `tests/data`.  
* All required input files for the main software or unit tests should have extensions that clearly describe the file format (e.g. .csv, .txt, .db, .fits)
* If you are working on addressing a specific issue ticket, assign yourself the ticket and set the status to "in progress"
* When making a pull request that closes an issue, cite the issue ticket in the pull request summary

## Collaboration
This effort is a collaboration between Queen's University Belfast, the University of Washington's DiRAC Institute, 
the University of Illinois at Urbana-Champaign, the Center for Astrophysics | Harvard & Smithsonian, and LINCC Frameworks (through the LINCC Frameworks Incubator Program).

This project is supported in part bythe generosity of Eric and Wendy Schmidt by recommendation of the Schmidt Futures program.


