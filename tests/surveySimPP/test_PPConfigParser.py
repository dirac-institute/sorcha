#!/bin/python
import os
import shutil
import configparser
import pytest
import glob

from sorcha.utilities.dataUtilitiesForTests import get_test_filepath


@pytest.fixture
def setup_and_teardown_for_PPConfigFileParser(tmp_path):
    # Record initial working directory
    initial_wd = os.getcwd()

    # Copy files mentioned in config file into the temp directory
    shutil.copy(get_test_filepath("baseline_10klines_2.0.db"), tmp_path)
    shutil.copy(get_test_filepath("detectors_corners.csv"), tmp_path)

    # Move to the temp directory
    os.chdir(tmp_path)

    # Yield to pytest to run the test
    yield

    # After running the test, move back to initial working directory
    os.chdir(initial_wd)


def test_PPConfigFileParser(setup_and_teardown_for_PPConfigFileParser):
    from sorcha.modules.PPConfigParser import PPConfigFileParser

    configs = PPConfigFileParser(get_test_filepath("test_PPConfig.ini"), "lsst")

    test_configs = {
        "eph_format": "csv",
        "aux_format": "whitespace",
        "ephemerides_type": "oif",
        "pointing_database": "./baseline_10klines_2.0.db",
        "pointing_sql_query": "SELECT observationId, observationStartMJD, filter, seeingFwhmGeom, seeingFwhmEff, fiveSigmaDepth, fieldRA, fieldDec, rotSkyPos FROM observations order by observationId",
        "comet_activity": "none",
        "observing_filters": ["r", "g", "i", "z"],
        "phase_function": "HG",
        "trailing_losses_on": True,
        "camera_model": "footprint",
        "footprint_path": "./detectors_corners.csv",
        "bright_limit": 16.0,
        "bright_limit_on": True,
        "SNR_limit": None,
        "SNR_limit_on": False,
        "default_SNR_cut": True,
        "mag_limit": None,
        "mag_limit_on": False,
        "fading_function_on": True,
        "fading_function_width": 0.1,
        "fading_function_peak_efficiency": 1.0,
        "SSP_separation_threshold": 0.5,
        "SSP_number_observations": 2,
        "SSP_number_tracklets": 3,
        "SSP_track_window": 15.0,
        "SSP_detection_efficiency": 0.95,
        "SSP_linking_on": True,
        "output_format": "csv",
        "output_size": "default",
        "position_decimals": 7,
        "magnitude_decimals": 3,
        "size_serial_chunk": 10,
        "rng_seed": None,
    }

    assert configs == test_configs

    return


def test_PPGetOrExit():
    from sorcha.modules.PPConfigParser import PPGetOrExit

    config = configparser.ConfigParser()
    config.read(get_test_filepath("test_PPConfig.ini"))

    test_value = PPGetOrExit(config, "INPUT", "eph_format", "none")

    with pytest.raises(SystemExit) as e:
        PPGetOrExit(config, "INPUT", "veryFakeKey", "this key does not exist!")

    assert test_value == "csv"
    assert e.type == SystemExit
    assert e.value.code == "this key does not exist!"

    return


def test_PPGetFloatOrExit():
    from sorcha.modules.PPConfigParser import PPGetFloatOrExit

    config = configparser.ConfigParser()
    config.read(get_test_filepath("test_PPConfig.ini"))

    test_value = PPGetFloatOrExit(config, "FADINGFUNCTION", "fading_function_width", "none")

    with pytest.raises(SystemExit) as e:
        PPGetFloatOrExit(config, "FADINGFUNCTION", "fading_function_on", "none")

    assert test_value == 0.1
    assert isinstance(test_value, float)
    assert e.type == SystemExit
    assert (
        e.value.code
        == "ERROR: expected a float for config parameter fading_function_on. Check value in config file."
    )

    return


def test_PPGetIntOrExit():
    from sorcha.modules.PPConfigParser import PPGetIntOrExit

    config = configparser.ConfigParser()
    config.read(get_test_filepath("test_PPConfig.ini"))

    test_value = PPGetIntOrExit(config, "OUTPUT", "position_decimals", "none")

    with pytest.raises(SystemExit) as e:
        PPGetIntOrExit(config, "FADINGFUNCTION", "fading_function_on", "none")

    assert test_value == 7
    assert isinstance(test_value, int)
    assert e.type == SystemExit
    assert (
        e.value.code
        == "ERROR: expected an int for config parameter fading_function_on. Check value in config file."
    )

    return


def test_PPGetBoolOrExit():
    from sorcha.modules.PPConfigParser import PPGetBoolOrExit

    config = configparser.ConfigParser()
    config.read(get_test_filepath("test_PPConfig.ini"))

    test_value = PPGetBoolOrExit(config, "FADINGFUNCTION", "fading_function_on", "none")

    with pytest.raises(SystemExit) as e:
        PPGetBoolOrExit(config, "OUTPUT", "position_decimals", "none")

    assert test_value is True
    assert isinstance(test_value, bool)
    assert e.type == SystemExit
    assert e.value.code == "ERROR: position_decimals could not be converted to a Boolean."

    return


def test_PPGetValueAndFlag():
    from sorcha.modules.PPConfigParser import PPGetValueAndFlag

    config = configparser.ConfigParser()
    config.read(get_test_filepath("test_PPConfig.ini"))

    test_value_1, test_flag_1 = PPGetValueAndFlag(config, "FOV", "fill_factor", "float")
    test_value_2, test_flag_2 = PPGetValueAndFlag(config, "SATURATION", "bright_limit", "float")

    with pytest.raises(SystemExit) as e:
        PPGetValueAndFlag(config, "SATURATION", "bright_limit", "int")

    assert test_value_1 is None
    assert test_flag_1 is False
    assert test_value_2 == 16.0
    assert test_flag_2 is True
    assert e.type == SystemExit
    assert (
        e.value.code
        == "ERROR: expected an int for config parameter bright_limit. Check value in config file."
    )

    return


def test_PPFindFileOrExit():
    from sorcha.modules.PPConfigParser import PPFindFileOrExit

    test_file = PPFindFileOrExit(get_test_filepath("test_PPConfig.ini"), "config file")

    with pytest.raises(SystemExit) as e:
        PPFindFileOrExit("totally_fake_file.txt", "test")

    assert test_file == get_test_filepath("test_PPConfig.ini")
    assert e.type == SystemExit
    assert e.value.code == "ERROR: filename totally_fake_file.txt supplied for test argument does not exist."

    return


def test_PPFindDirectoryOrExit():
    from sorcha.modules.PPConfigParser import PPFindDirectoryOrExit

    test_dir = PPFindDirectoryOrExit("./", "test")

    with pytest.raises(SystemExit) as e:
        PPFindDirectoryOrExit("./fake_dir/", "test")

    assert test_dir == "./"
    assert e.type == SystemExit
    assert e.value.code == "ERROR: filepath ./fake_dir/ supplied for test argument does not exist."

    return


def test_PPCheckFiltersForSurvey():
    from sorcha.modules.PPConfigParser import PPCheckFiltersForSurvey

    PPCheckFiltersForSurvey("lsst", ["u", "g", "r", "i", "z", "y"])

    with pytest.raises(SystemExit) as e:
        PPCheckFiltersForSurvey("lsst", ["j"])

    assert e.type == SystemExit


def test_PPPrintConfigsToLog(tmp_path):
    from sorcha.modules.PPGetLogger import PPGetLogger
    from sorcha.modules.PPConfigParser import PPPrintConfigsToLog

    test_path = os.path.dirname(get_test_filepath("test_input_fullobs.csv"))

    PPGetLogger(tmp_path, log_format="%(name)-12s %(levelname)-8s %(message)s ")

    cmd_args = {
        "paramsinput": "testcolour.txt",
        "orbinfile": "testorb.des",
        "oifoutput": "oiftestoutput.txt",
        "configfile": "test_PPConfig.ini",
        "outpath": "./",
        "makeTemporaryEphemerisDatabase": False,
        "readTemporaryEphemerisDatabase": None,
        "deleteTemporaryEphemerisDatabase": False,
        "surveyname": "lsst",
        "outfilestem": "testout",
        "verbose": True,
    }

    configs = {
        "eph_format": "csv",
        "aux_format": "whitespace",
        "ephemerides_type": "oif",
        "pointing_database": "./baseline_10klines_2.0.db",
        "pointing_sql_query": "SELECT observationId, observationStartMJD, filter, seeingFwhmGeom, seeingFwhmEff, fiveSigmaDepth, fieldRA, fieldDec, rotSkyPos FROM observations order by observationId",
        "comet_activity": "none",
        "observing_filters": ["r", "g", "i", "z"],
        "phase_function": "HG",
        "trailing_losses_on": True,
        "camera_model": "footprint",
        "footprint_path": "./detectors_corners.csv",
        "bright_limit": 16.0,
        "bright_limit_on": True,
        "SNR_limit": None,
        "SNR_limit_on": False,
        "default_SNR_cut": True,
        "mag_limit": None,
        "mag_limit_on": False,
        "fading_function_on": True,
        "fading_function_width": 0.1,
        "fading_function_peak_efficiency": 1.0,
        "SSP_separation_threshold": 0.5,
        "SSP_number_observations": 2,
        "SSP_number_tracklets": 3,
        "SSP_track_window": 15.0,
        "SSP_detection_efficiency": 0.95,
        "SSP_linking_on": True,
        "output_format": "csv",
        "output_size": "default",
        "position_decimals": 7,
        "magnitude_decimals": 3,
        "size_serial_chunk": 10,
        "rng_seed": None,
        "mainfilter": "r",
        "othercolours": ["g-r", "i-r", "z-r"],
    }

    PPPrintConfigsToLog(configs, cmd_args)

    datalog = glob.glob(os.path.join(tmp_path, "*-postprocessing.log"))

    testfile = open(os.path.join(test_path, "test_PPPrintConfigsToLog.txt"), mode="r")
    newfile = open(datalog[0], mode="r")

    alltest = testfile.readlines()
    allnew = newfile.readlines()

    assert alltest == allnew

    testfile.close()
    newfile.close()

    return
