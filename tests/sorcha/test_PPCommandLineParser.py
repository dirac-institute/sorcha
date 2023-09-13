import os
import pytest

from sorcha.utilities.dataUtilitiesForTests import get_test_filepath


class args:
    def __init__(self, cp, dw, dr, dl, t="testout", o="./", f=False):
        self.p = get_test_filepath("testcolour.txt")
        self.ob = get_test_filepath("testorb.des")
        self.er = get_test_filepath("oiftestoutput.txt")
        self.ew = None
        self.c = get_test_filepath("test_PPConfig.ini")
        self.pd = get_test_filepath("baseline_10klines_2.0.db")
        self.o = o
        self.cp = cp
        self.s = "lsst"
        self.t = t
        self.v = True
        self.dw = dw
        self.dr = dr
        self.dl = dl
        self.f = f
        self.ar = None


def test_PPCommandLineParser():
    from sorcha.modules.PPCommandLineParser import PPCommandLineParser

    tmp_path = os.path.dirname(get_test_filepath("test_input_fullobs.csv"))

    cmd_dict_1 = PPCommandLineParser(args(False, False, None, False))
    expected_1 = {
        "paramsinput": get_test_filepath("testcolour.txt"),
        "orbinfile": get_test_filepath("testorb.des"),
        "oifoutput": get_test_filepath("oiftestoutput.txt"),
        "configfile": get_test_filepath("test_PPConfig.ini"),
        "pointing_database": get_test_filepath("baseline_10klines_2.0.db"),
        "outpath": "./",
        "makeTemporaryEphemerisDatabase": False,
        "readTemporaryEphemerisDatabase": None,
        "deleteTemporaryEphemerisDatabase": False,
        "surveyname": "lsst",
        "outfilestem": "testout",
        "verbose": True,
        "ar_data_path": None,
        "output_ephemeris_file": None,
    }

    cmd_dict_2 = PPCommandLineParser(
        args(get_test_filepath("testcomet.txt"), False, get_test_filepath("sqlresults.db"), True)
    )
    expected_2 = {
        "paramsinput": get_test_filepath("testcolour.txt"),
        "orbinfile": get_test_filepath("testorb.des"),
        "oifoutput": get_test_filepath("oiftestoutput.txt"),
        "configfile": get_test_filepath("test_PPConfig.ini"),
        "pointing_database": get_test_filepath("baseline_10klines_2.0.db"),
        "outpath": "./",
        "makeTemporaryEphemerisDatabase": False,
        "complex_physical_parameters": get_test_filepath("testcomet.txt"),
        "readTemporaryEphemerisDatabase": get_test_filepath("sqlresults.db"),
        "deleteTemporaryEphemerisDatabase": True,
        "surveyname": "lsst",
        "outfilestem": "testout",
        "verbose": True,
        "ar_data_path": None,
        "output_ephemeris_file": None,
    }

    cmd_dict_3 = PPCommandLineParser(args(False, os.path.join(tmp_path, "test.db"), None, True))
    expected_3 = {
        "paramsinput": get_test_filepath("testcolour.txt"),
        "orbinfile": get_test_filepath("testorb.des"),
        "oifoutput": get_test_filepath("oiftestoutput.txt"),
        "configfile": get_test_filepath("test_PPConfig.ini"),
        "pointing_database": get_test_filepath("baseline_10klines_2.0.db"),
        "outpath": "./",
        "makeTemporaryEphemerisDatabase": os.path.join(tmp_path, "test.db"),
        "readTemporaryEphemerisDatabase": None,
        "deleteTemporaryEphemerisDatabase": True,
        "surveyname": "lsst",
        "outfilestem": "testout",
        "verbose": True,
        "ar_data_path": None,
        "output_ephemeris_file": None,
    }

    cmd_dict_4 = PPCommandLineParser(args(False, "default", None, True))
    expected_4 = {
        "paramsinput": get_test_filepath("testcolour.txt"),
        "orbinfile": get_test_filepath("testorb.des"),
        "oifoutput": get_test_filepath("oiftestoutput.txt"),
        "configfile": get_test_filepath("test_PPConfig.ini"),
        "pointing_database": get_test_filepath("baseline_10klines_2.0.db"),
        "outpath": "./",
        "makeTemporaryEphemerisDatabase": os.path.join(tmp_path, "temp_oiftestoutput.db"),
        "readTemporaryEphemerisDatabase": None,
        "deleteTemporaryEphemerisDatabase": True,
        "surveyname": "lsst",
        "outfilestem": "testout",
        "verbose": True,
        "ar_data_path": None,
        "output_ephemeris_file": None,
    }

    with open(os.path.join(tmp_path, "dummy_file.txt"), "w") as _:
        pass

    with pytest.raises(SystemExit) as e:
        _ = PPCommandLineParser(args(False, False, None, False, o=tmp_path, t="dummy_file"))

    _ = PPCommandLineParser(args(False, False, None, False, o=tmp_path, t="dummy_file", f=True))

    assert cmd_dict_1 == expected_1
    assert cmd_dict_2 == expected_2
    assert cmd_dict_3 == expected_3
    assert cmd_dict_4 == expected_4
    assert e.type == SystemExit
    assert not os.path.isfile(os.path.join(tmp_path, "dummy_file.txt"))

    return
