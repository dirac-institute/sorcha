import pytest
from sorcha.configs.sorchaConfigs import sorchaConfigs
from sorcha.utilities.sorchaArguments import sorchaArguments




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
