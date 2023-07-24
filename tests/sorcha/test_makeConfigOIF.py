import configparser
import os
import sys
import pytest

from sorcha.utilities.makeConfigOIF import makeConfig
from sorcha.utilities.dataUtilitiesForTests import get_test_filepath

# On Windows, the test is apparently not creating the files in the expected place.
# Not sure why, will troubleshoot later.
if sys.platform.startswith("win"):
    pytest.skip("These tests do not work on Windows.", allow_module_level=True)


class args:
    def __init__(self, o, pointing, no, prefix):
        self.o = o
        self.pointing = pointing
        self.no = no
        self.ndays = -1
        self.day1 = 1
        self.prefix = prefix
        self.camerafov = "instrument_polygon.dat"
        self.cache = "_cache"
        self.mpcfile = "obslist.dat"
        self.inputformat = "whitespace"
        self.query = "SELECT observationId,observationStartMJD,fieldRA,fieldDEC,rotSkyPos FROM observations order by observationStartMJD"
        self.spkstep = 30
        self.telescope = "I11"


@pytest.fixture
def teardown_for_makeConfigOIF():
    yield

    temp_path = os.path.dirname(get_test_filepath("oiftestoutput.txt"))
    file1 = "testorb-1-5.ini"
    file2 = "testorb-1-3.ini"
    file3 = "testorb-4-5.ini"

    os.remove(os.path.join(temp_path, file1))
    os.remove(os.path.join(temp_path, file2))
    os.remove(os.path.join(temp_path, file3))


def test_makeConfigOIF(teardown_for_makeConfigOIF):
    outpath = os.path.dirname(get_test_filepath("testorb.des"))
    argv = args(get_test_filepath("testorb.des"), get_test_filepath("baseline_10klines_2.0.db"), -1, outpath)

    makeConfig(argv)

    config = configparser.ConfigParser()
    config.read(get_test_filepath("testorb-1-5.ini"))

    # have to change the paths - makeConfig gives absolute paths, machine-dependent
    config.set("ASTEROID", "population model", "../tests/data/testorb.des")
    config.set("SURVEY", "survey database", "../tests/data/baseline_10klines_2.0.db")

    config2 = configparser.ConfigParser()
    config2.read(get_test_filepath("makeConfigOIF_1.ini"))

    assert config == config2

    argv = args(get_test_filepath("testorb.des"), get_test_filepath("baseline_10klines_2.0.db"), 3, outpath)

    makeConfig(argv)

    config = configparser.ConfigParser()
    config.read(get_test_filepath("testorb-1-3.ini"))

    config.set("ASTEROID", "population model", "../tests/data/testorb.des")
    config.set("SURVEY", "survey database", "../tests/data/baseline_10klines_2.0.db")

    config1 = configparser.ConfigParser()
    config1.read(get_test_filepath("testorb-4-5.ini"))

    config1.set("ASTEROID", "population model", "../tests/data/testorb.des")
    config1.set("SURVEY", "survey database", "../tests/data/baseline_10klines_2.0.db")

    config2 = configparser.ConfigParser()
    config2.read(get_test_filepath("makeConfigOIF_2.ini"))

    config3 = configparser.ConfigParser()
    config3.read(get_test_filepath("makeConfigOIF_3.ini"))

    assert config == config2
    assert config1 == config3

    return
