import configparser
import os

from sorcha.utilities.makeMultiConfigOIF import makeConfig
from sorcha.utilities.dataUtilitiesForTests import get_test_filepath


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


def test_makeMultiConfigOIF():
    # NB: the lack of teardown deleting the files created by this test is
    # deliberate: the files are used by another test.

    outpath = os.path.dirname(get_test_filepath("testorb.des"))
    argv = args(outpath, get_test_filepath("baseline_10klines_2.0.db"), -1, outpath)

    makeConfig(argv)

    config_ex1 = configparser.ConfigParser()
    config_ex1.read(get_test_filepath("makeMultiConfigOIF_test1.ini"))

    config_ex2 = configparser.ConfigParser()
    config_ex2.read(get_test_filepath("makeMultiConfigOIF_test2.ini"))

    config_1 = configparser.ConfigParser()
    config_1.read(get_test_filepath("config_test1.ini"))

    config_2 = configparser.ConfigParser()
    config_2.read(get_test_filepath("config_test2.ini"))

    # have to change the paths - makeConfig gives absolute paths, machine-dependent
    config_1.set("ASTEROID", "population model", "../tests/data/orbits_test1.txt")
    config_1.set("SURVEY", "survey database", "../tests/data/baseline_10klines_2.0.db")

    config_2.set("ASTEROID", "population model", "../tests/data/orbits_test2.txt")
    config_2.set("SURVEY", "survey database", "../tests/data/baseline_10klines_2.0.db")

    assert config_1 == config_ex1
    assert config_2 == config_ex2

    return
