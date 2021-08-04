# survey_simulator_post_processing

<!-- [![Build Status](https://travis-ci.org/dirac-institute/survey_simulator_post_processing.svg?branch=master)](https://travis-ci.org/dirac-institute/survey_simulator_post_processing) -->

![pytest](https://github.com/dirac-institute/survey_simulator_post_processing/actions/workflows/pytest.yml/badge.svg)

LSST stack based post-processing modules in python for the JPL survey simulator: https://github.com/AsteroidSurveySimulator/objectsInField


## developer best practices
* Data sets should be moved to the `data` folder, have a readme.txt or readme.md to explain where the data came from as well as a time stamp in the readme.txt.
* Data sets that are used for unit testing should live in `data/test`.  
* All required input files for the main software or unit tests should have extensions that clearly describe the file format (e.g. .csv, .txt, .db, .fits)
