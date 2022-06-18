#!/bin/python
import os
import shutil

import pytest

from surveySimPP.tests.data import get_test_filepath


@pytest.fixture
def setup_and_teardown_for_PPConfigFileParser(tmp_path):
    # Record initial working directory
    initial_wd = os.getcwd()

    # Copy files mentioned in config file into the temp directory
    shutil.copy(get_test_filepath("baseline_10yrs_10klines.db"), tmp_path)
    shutil.copy(get_test_filepath("detectors_corners.csv"), tmp_path)

    # Move to the temp directory
    os.chdir(tmp_path)

    # Yield to pytest to run the test
    yield

    # After running the test, move back to initial working directory
    os.chdir(initial_wd)


def test_PPConfigFileParser(setup_and_teardown_for_PPConfigFileParser):

    from surveySimPP.modules.PPConfigParser import PPConfigFileParser

    configs = PPConfigFileParser(get_test_filepath('test_PPConfig.ini'), 'lsst')

    test_configs = {'ephFormat': 'whitespace',
                    'filesep': 'whitespace',
                    'ephemerides_type': 'oif',
                    'pointingdatabase': './baseline_10yrs_10klines.db',
                    'ppdbquery': 'SELECT observationId, observationStartMJD, filter, seeingFwhmGeom, seeingFwhmEff, fiveSigmaDepth, fieldRA, fieldDec, rotSkyPos FROM SummaryAllProps order by observationId',
                    'cometactivity': 'none',
                    'observing_filters': ['r', 'g', 'i', 'z'],
                    'mainfilter': 'r',
                    'othercolours': ['g-r', 'i-r', 'z-r'],
                    'phasefunction': 'HG',
                    'trailingLossesOn': True,
                    'cameraModel': 'footprint',
                    'footprintPath': './detectors_corners.csv',
                    'fillfactor': 1.0,
                    'brightLimit': 16.0,
                    'brightLimitOn': True,
                    'SNRLimit': None,
                    'SNRLimitOn': False,
                    'magLimit': None,
                    'magLimitOn': False,
                    'fadingFunctionOn': True,
                    'fadingFunctionWidth': 0.1,
                    'inSepThreshold': 0.5,
                    'minTracklet': 2,
                    'noTracklets': 3,
                    'trackletInterval': 15.0,
                    'SSPDetectionEfficiency': 0.95,
                    'SSPLinkingOn': True,
                    'outputformat': 'csv',
                    'outputsize': 'default',
                    'sizeSerialChunk': 10,
                    'rng_seed': None}

    assert configs == test_configs
