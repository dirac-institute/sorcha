import pytest
from sorcha.configs.sorchaConfigs import sorchaConfigs
from sorcha.utilities.sorchaArguments import sorchaArguments

from sorcha.configs.configUtilities import *


def test_check_key_exists():
    key_name = "None"
    with pytest.raises(SystemExit) as error_text:
        check_key_exists(None, key_name)

    assert (
        error_text.value.code
        == f"ERROR: No value found for required key {key_name} in config file. Please check the file and try again."
    )


def test_check_key_doesnt_exist():
    key_name = "None"
    reason = "test reason statement"
    with pytest.raises(SystemExit) as error_text:
        check_key_doesnt_exist(1, key_name, reason)

    assert error_text.value.code == f"ERROR: {key_name} supplied in config file {reason}"


def test_cast_as_int():
    key_name = "None"
    with pytest.raises(SystemExit) as error_text:
        cast_as_int("ten", key_name)

    assert (
        error_text.value.code
        == f"ERROR: expected an int for config parameter {key_name}. Check value in config file."
    )
    str_int = "1"
    cast_int = cast_as_int(str_int, key_name)

    assert type(cast_int) == type(int(1))


def test_cast_as_float():
    key_name = "None"
    with pytest.raises(SystemExit) as error_text:
        cast_as_float("ten", key_name)

    assert (
        error_text.value.code
        == f"ERROR: expected a float for config parameter {key_name}. Check value in config file."
    )
    str_float = "1.5"
    cast_float = cast_as_float(str_float, key_name)

    assert type(cast_float) == type(float(1.5))


def test_cast_as_bool():
    key_name = "None"
    with pytest.raises(SystemExit) as error_text:
        cast_as_bool("ten", key_name)

    assert (
        error_text.value.code
        == f"ERROR: expected a bool for config parameter {key_name}. Check value in config file."
    )
    str_bool = "True"
    cast_bool = cast_as_bool(str_bool, key_name)

    assert type(cast_bool) == type(bool(True))


def test_cast_as_bool_or_set_default():
    key_name = "None"
    with pytest.raises(SystemExit) as error_text:
        cast_as_bool_or_set_default("ten", key_name, True)

    assert (
        error_text.value.code
        == f"ERROR: expected a bool for config parameter {key_name}. Check value in config file."
    )
    str_bool = "True"
    cast_bool = cast_as_bool_or_set_default(str_bool, key_name, True)

    assert type(cast_bool) == type(bool(True))

    cast_bool = cast_as_bool_or_set_default(None, key_name, False)

    assert cast_bool == False


def test_check_value_in_list():
    key_name = "None"
    value = "ten"
    value_list = ["five", "six"]
    with pytest.raises(SystemExit) as error_text:
        check_value_in_list(value, value_list, key_name)

    assert (
        error_text.value.code
        == f"ERROR: value {value} for config parameter {key_name} not recognised. Expecting one of: {value_list}."
    )
    value = "five"
    check_value_in_list(value, value_list, key_name)


def test_PrintConfigsToLog(tmp_path):
    from sorcha.utilities.sorchaGetLogger import sorchaGetLogger
    from sorcha.configs.configUtilities import PrintConfigsToLog
    from sorcha.utilities.dataUtilitiesForTests import get_test_filepath
    import os
    import glob

    test_path = os.path.dirname(get_test_filepath("test_input_fullobs.csv"))
    config_file_location = get_test_filepath("test_PPConfig.ini")
    pplogger = sorchaGetLogger(tmp_path, "test_log", log_format="%(name)-12s %(levelname)-8s %(message)s ")

    cmd_args = {
        "paramsinput": "testcolour.txt",
        "orbinfile": "testorb.des",
        "input_ephemeris_file": "ephemtestoutput.txt",
        "configfile": "test_PPConfig.ini",
        "pointing_database": "./baseline_10klines_2.0.db",
        "outpath": "./",
        "surveyname": "rubin_sim",
        "outfilestem": "testout",
        "loglevel": True,
        "seed": 24601,
        "stats": None,
        "visits_database": None,
    }
    test_configs = sorchaConfigs(config_file_location, "rubin_sim")
    test_configs.filters.mainfilter = "r"
    test_configs.filters.othercolours = ["g-r", "i-r", "z-r"]
    args = sorchaArguments(cmd_args)

    PrintConfigsToLog(test_configs, args)

    datalog = glob.glob(os.path.join(tmp_path, "*-sorcha.log"))
    # when updating PrintConfigsToLog text file test_PPPrintConfigsToLog.txt needs to be updated too.
    testfile = open(os.path.join(test_path, "test_PrintConfigsToLog.txt"), mode="r")
    newfile = open(datalog[0], mode="r")
    alltest = testfile.readlines()
    allnew = newfile.readlines()
    allnew_ = allnew[1:]  # skipping first line as that line specifies user file location
    assert alltest == allnew_

    testfile.close()
    newfile.close()

    return
