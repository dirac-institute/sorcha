# survey_simulator_post_processing

<!-- [![Build Status](https://travis-ci.org/dirac-institute/survey_simulator_post_processing.svg?branch=master)](https://travis-ci.org/dirac-institute/survey_simulator_post_processing) -->

[![ci](https://github.com/dirac-institute/survey_simulator_post_processing/actions/workflows/ci.yml/badge.svg)](https://github.com/dirac-institute/survey_simulator_post_processing/actions/workflows/ci.yml)
[![pytest](https://github.com/dirac-institute/survey_simulator_post_processing/actions/workflows/pytest.yml/badge.svg)](https://github.com/dirac-institute/survey_simulator_post_processing/actions/workflows/pytest.yml) [![Documentation Status](https://readthedocs.org/projects/survey-simulator-post-processing/badge/?version=latest)](https://survey-simulator-post-processing.readthedocs.io/en/latest/?badge=latest)

LSST stack based post-processing modules in python for the JPL survey simulator: https://github.com/AsteroidSurveySimulator/objectsInField

Currently tested with the following fork: https://github.com/eggls6/objectsInField

Documentation: https://survey-simulator-post-processing.readthedocs.io/en/latest/

## developer best practices
* Data sets should be moved to the `data` folder, have a readme.txt or readme.md to explain where the data came from as well as a time stamp in the readme.txt.
* Data sets that are used for unit testing should live in `data/test`.  
* All required input files for the main software or unit tests should have extensions that clearly describe the file format (e.g. .csv, .txt, .db, .fits)
* Function/methods names should follow Rubin / LSST developer guide conventions: https://developer.lsst.io/
* If you are working on addressing a specific issue ticket, assign yourself the ticket and set the status to "in progress"
* When making a pull request that closes an issue, cite the issue ticket in the pull request summary


## Making pip work
When making edits to the code, its likely that the only thing you need to worry about is making sure the imports are consistent. There are two places where this is important, the sorcha/sorcha.py file and the sorcha/modules/__init__.py file. If you want to add, remove or change the name of a module, then these files need to be updated to reflect that. 

Within the sorcha/modules/__init__.py file it will look something like this:
```
from . import PPAddUncertainties
```
And in the sorcha.py file it will look something like this:
```
from sorcha.modules import PPAddUncertainties
```
When adding, removing or changing the name of any module, just make sure that you've updated both of these files to reflect the changes.


If you want to make some more major changes, e.g. adding another utility to the command line, then there are two things to keep in mind. Firstly, the python file containing the utility has to be formatted in a specific way and secondly, the setup.py file has to be changed.

Examples of the file formatting can be seen in sorcha.py, makeConfigOIF and makeConfigPP, so you can try to follow that. In short, you need to define the main containing the parser arguments, e.g. 

```
def main():
    parser=argparse.ArgumentParser(description='creating config file(s) for Objects in Field')
    parser.add_argument("o", help="orbits file", type=str)
    etc....
```

and then after, include:
```
if __name__=='__main__':
    main()
```

setup.py is the file which contains the information for the install. This contains some general information on things like the version (which needs to be changed when the code is updated to a new version) and the author. Generally this file won't have to be changed unless you want to:

- Update the version number, author info etc. : this can just be manually changed.

- Add a prerequisite package e.g. pandas: this can be added in the install_requires section just by adding the name of the prerequisite package to the list. This means that the package will be installed alongside the survey simulator. Specific versions can be added e.g. 'pandas==1.3.5'

- Add a new command line argument: In the case of adding new utilities (e.g. the config file generators). This is a bit more complicated and relies on the file being in the format given above. If this is the case then a new function can be added to the entry_points

```          
 entry_points={
        'console_scripts': ['makeConfigPP = utilities.makeConfigOIF:main'],
    },
```
where makeConfigPP is the name of the command line argument, and utilities.makeConfigOIF is the pathway of the file.

## Collaboration
This effort is a collaboration between the University of Washington's DIRAC Institute, Queen's University Belfast, and the University of Illinois at Urbana-Champaign

