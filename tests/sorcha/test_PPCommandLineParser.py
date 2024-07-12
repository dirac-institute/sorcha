import os
import pytest
import pprint

from sorcha.utilities.dataUtilitiesForTests import get_test_filepath


class args:
    def __init__(self, cp, t="testout", o="./", f=False):
        self.colors = get_test_filepath("testcolour.txt")
        self.orbits = get_test_filepath("testorb.des")
        self.ephem_input = get_test_filepath("oiftestoutput.txt")
        self.ephem_output = None
        self.config = get_test_filepath("test_PPConfig.ini")
        self.pointings = get_test_filepath("baseline_10klines_2.0.db")
        self.output_dir = o
        self.extra_object_data = cp
        self.survey = "rubin_sim"
        self.prefix = t
        self.verbose = True
        self.force = f
        self.integrator_data = None
        self.stats = True
        self.log_file = f"{self.output_dir}/{self.prefix}.log"


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
        "stats": "testout-stats",
    }

    cmd_dict_2 = PPCommandLineParser(args(get_test_filepath("testcomet.txt")))
    expected_2 = {
        "paramsinput": get_test_filepath("testcolour.txt"),
        "orbinfile": get_test_filepath("testorb.des"),
        "oifoutput": get_test_filepath("oiftestoutput.txt"),
        "configfile": get_test_filepath("test_PPConfig.ini"),
        "pointing_database": get_test_filepath("baseline_10klines_2.0.db"),
        "outpath": "./",
        "extra_object_data": get_test_filepath("testcomet.txt"),
        "surveyname": "rubin_sim",
        "outfilestem": "testout",
        "verbose": True,
        "ar_data_path": None,
        "output_ephemeris_file": None,
        "stats": "testout-stats",
    }

    with open(os.path.join(tmp_path, "dummy_file.txt"), "w") as _:
        pass

    with pytest.raises(SystemExit) as e:
        _ = PPCommandLineParser(args(False, o=tmp_path, t="dummy_file"))

    _ = PPCommandLineParser(args(False, o=tmp_path, t="dummy_file", f=True))

    # Helpful debugging info for if things go south..
    print("======= cmd_dict_1 vs expected_1 ========")
    import json, sys

    json.dump(cmd_dict_1, sys.stdout, sort_keys=True, indent=4)
    json.dump(expected_1, sys.stdout, sort_keys=True, indent=4)
    print("======= cmd_dict_2 vs expected_2 ========")
    json.dump(cmd_dict_2, sys.stdout, sort_keys=True, indent=4)
    json.dump(expected_2, sys.stdout, sort_keys=True, indent=4)
    print("=========================================")

    assert cmd_dict_1 == expected_1, "cmd_dict_1 != expected_1"
    assert cmd_dict_2 == expected_2, "cmd_dict_2 != expected_2"
    assert e.type == SystemExit
    assert not os.path.isfile(os.path.join(tmp_path, "dummy_file.txt"))

    return
