#!/bin/python
import os
import shutil
import configparser
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
                    'position_decimals': 7,
                    'magnitude_decimals': 3,
                    'sizeSerialChunk': 10,
                    'rng_seed': None}

    assert configs == test_configs

    return


def test_PPGetOrExit():

    from surveySimPP.modules.PPConfigParser import PPGetOrExit

    config = configparser.ConfigParser()
    config.read(get_test_filepath('test_PPconfig.ini'))

    test_value = PPGetOrExit(config, 'INPUTFILES', 'ephFormat', 'none')

    with pytest.raises(SystemExit) as e:
        PPGetOrExit(config, 'INPUTFILES', 'veryFakeKey', 'this key does not exist!')

    assert test_value == 'whitespace'
    assert e.type == SystemExit
    assert e.value.code == 'this key does not exist!'

    return


def test_PPGetFloatOrExit():

    from surveySimPP.modules.PPConfigParser import PPGetFloatOrExit

    config = configparser.ConfigParser()
    config.read(get_test_filepath('test_PPconfig.ini'))

    test_value = PPGetFloatOrExit(config, 'FILTERINGPARAMETERS', 'fadingFunctionWidth', 'none')

    with pytest.raises(SystemExit) as e:
        PPGetFloatOrExit(config, 'FILTERINGPARAMETERS', 'fadingFunctionOn', 'none')

    assert test_value == 0.1
    assert isinstance(test_value, float)
    assert e.type == SystemExit
    assert e.value.code == 'ERROR: expected a float for config parameter fadingFunctionOn. Check value in config file.'

    return


def test_PPGetIntOrExit():

    from surveySimPP.modules.PPConfigParser import PPGetIntOrExit

    config = configparser.ConfigParser()
    config.read(get_test_filepath('test_PPconfig.ini'))

    test_value = PPGetIntOrExit(config, 'OUTPUTFORMAT', 'position_decimals', 'none')

    with pytest.raises(SystemExit) as e:
        PPGetIntOrExit(config, 'FILTERINGPARAMETERS', 'fadingFunctionOn', 'none')

    assert test_value == 7
    assert isinstance(test_value, int)
    assert e.type == SystemExit
    assert e.value.code == 'ERROR: expected an int for config parameter fadingFunctionOn. Check value in config file.'

    return


def test_PPGetBoolOrExit():

    from surveySimPP.modules.PPConfigParser import PPGetBoolOrExit

    config = configparser.ConfigParser()
    config.read(get_test_filepath('test_PPconfig.ini'))

    test_value = PPGetBoolOrExit(config, 'FILTERINGPARAMETERS', 'fadingFunctionOn', 'none')

    with pytest.raises(SystemExit) as e:
        PPGetBoolOrExit(config, 'OUTPUTFORMAT', 'position_decimals', 'none')

    assert test_value is True
    assert isinstance(test_value, bool)
    assert e.type == SystemExit
    assert e.value.code == 'ERROR: position_decimals could not be converted to a Boolean.'

    return


def test_PPGetValueAndFlag():

    from surveySimPP.modules.PPConfigParser import PPGetValueAndFlag

    config = configparser.ConfigParser()
    config.read(get_test_filepath('test_PPconfig.ini'))

    test_value_1, test_flag_1 = PPGetValueAndFlag(config, 'FILTERINGPARAMETERS', 'fillfactor', 'float')
    test_value_2, test_flag_2 = PPGetValueAndFlag(config, 'FILTERINGPARAMETERS', 'brightLimit', 'float')

    with pytest.raises(SystemExit) as e:
        PPGetValueAndFlag(config, 'FILTERINGPARAMETERS', 'brightLimit', 'int')

    assert test_value_1 is None
    assert test_flag_1 is False
    assert test_value_2 == 16.
    assert test_flag_2 is True
    assert e.type == SystemExit
    assert e.value.code == 'ERROR: expected an int for config parameter brightLimit. Check value in config file.'

    return


def test_PPFindFileOrExit():

    from surveySimPP.modules.PPConfigParser import PPFindFileOrExit

    test_file = PPFindFileOrExit(get_test_filepath('test_PPConfig.ini'), 'config file')

    with pytest.raises(SystemExit) as e:
        PPFindFileOrExit('totally_fake_file.txt', 'test')

    assert test_file == get_test_filepath('test_PPConfig.ini')
    assert e.type == SystemExit
    assert e.value.code == 'ERROR: filename totally_fake_file.txt supplied for test argument does not exist.'

    return


def test_PPFindDirectoryOrExit():

    from surveySimPP.modules.PPConfigParser import PPFindDirectoryOrExit

    test_dir = PPFindDirectoryOrExit('./', 'test')

    with pytest.raises(SystemExit) as e:
        PPFindDirectoryOrExit('./fake_dir/', 'test')

    assert test_dir == './'
    assert e.type == SystemExit
    assert e.value.code == 'ERROR: filename ./fake_dir/ supplied for test argument does not exist.'

    return


def test_PPCheckFiltersForSurvey():

    from surveySimPP.modules.PPConfigParser import PPCheckFiltersForSurvey

    PPCheckFiltersForSurvey('lsst', ['u', 'g', 'r', 'i', 'z', 'y'])

    with pytest.raises(SystemExit) as e:
        PPCheckFiltersForSurvey('lsst', ['j'])

    assert e.type == SystemExit
