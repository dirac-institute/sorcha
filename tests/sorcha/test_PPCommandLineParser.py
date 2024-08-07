import os
import pytest

from sorcha.utilities.dataUtilitiesForTests import get_test_filepath


class args:
    def __init__(self, cp, t="testout", o="./", f=False, process_subset=("1/1")):
        self.p = get_test_filepath("testcolour.txt")
        self.ob = get_test_filepath("testorb.des")
        self.er = get_test_filepath("oiftestoutput.txt")
        self.ew = None
        self.c = get_test_filepath("test_PPConfig.ini")
        self.pd = get_test_filepath("baseline_10klines_2.0.db")
        self.o = o
        self.cp = cp
        self.s = "rubin_sim"
        self.t = t
        self.v = True
        self.f = f
        self.ar = None
        self.st = "test.csv"
        self.process_subset = process_subset


def test_PPCommandLineParser():
    from sorcha.modules.PPCommandLineParser import PPCommandLineParser

    tmp_path = os.path.dirname(get_test_filepath("test_input_fullobs.csv"))

    cmd_dict_1 = PPCommandLineParser(args(False))
    expected_1 = {
        "paramsinput": get_test_filepath("testcolour.txt"),
        "orbinfile": get_test_filepath("testorb.des"),
        "oifoutput": get_test_filepath("oiftestoutput.txt"),
        "configfile": get_test_filepath("test_PPConfig.ini"),
        "pointing_database": get_test_filepath("baseline_10klines_2.0.db"),
        "outpath": "./",
        "surveyname": "rubin_sim",
        "outfilestem": "testout",
        "verbose": True,
        "ar_data_path": None,
        "output_ephemeris_file": None,
        "stats": "test.csv",
        "process_subset": (1, 1),
    }

    cmd_dict_2 = PPCommandLineParser(args(get_test_filepath("testcomet.txt")))
    expected_2 = {
        "paramsinput": get_test_filepath("testcolour.txt"),
        "orbinfile": get_test_filepath("testorb.des"),
        "oifoutput": get_test_filepath("oiftestoutput.txt"),
        "configfile": get_test_filepath("test_PPConfig.ini"),
        "pointing_database": get_test_filepath("baseline_10klines_2.0.db"),
        "outpath": "./",
        "complex_physical_parameters": get_test_filepath("testcomet.txt"),
        "surveyname": "rubin_sim",
        "outfilestem": "testout",
        "verbose": True,
        "ar_data_path": None,
        "output_ephemeris_file": None,
        "stats": "test.csv",
        "process_subset": (1, 1),
    }

    with open(os.path.join(tmp_path, "dummy_file.txt"), "w") as _:
        pass

    with pytest.raises(SystemExit) as e:
        _ = PPCommandLineParser(args(False, o=tmp_path, t="dummy_file"))

    _ = PPCommandLineParser(args(False, o=tmp_path, t="dummy_file", f=True))

    assert cmd_dict_1 == expected_1
    assert cmd_dict_2 == expected_2
    assert e.type == SystemExit
    assert not os.path.isfile(os.path.join(tmp_path, "dummy_file.txt"))

    return


def test_PPCommandLineParser_subset():
    from sorcha.modules.PPCommandLineParser import PPCommandLineParser

    tmp_path = os.path.dirname(get_test_filepath("test_input_fullobs.csv"))

    with pytest.raises(SystemExit) as e:
        _ = PPCommandLineParser(args(False, process_subset="3/1"))

    assert e.value.code == "--process-subset: the chosen splits must be between 1 and <nsplits> (inclusive)."

    with pytest.raises(SystemExit) as e2:
        _ = PPCommandLineParser(args(False, process_subset="-1/1"))

    assert e2.value.code == "--process-subset: the argument must be in form of <split>/<nsplits>"

    with pytest.raises(SystemExit) as e3:
        _ = PPCommandLineParser(args(False, process_subset="1/0"))

    assert e3.value.code == "--process-subset: the number of splits must be >= 1"
