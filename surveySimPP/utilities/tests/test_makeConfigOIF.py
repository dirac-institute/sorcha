from ..makeConfigOIF import makeConfig
from surveySimPP.tests.data import get_test_filepath
import configparser
import os


class args:
    def __init__(self, o, pointing, no, prefix):
        self.o = o
        self.pointing = pointing
        self.no = no
        self.ndays = -1
        self.day1 = 1
        self.prefix = prefix
        self.camerafov = 'instrument_polygon.dat'
        self.cache = '_cache'
        self.mpcfile = 'obslist.dat'
        self.inputformat = 'whitespace'
        self.query = 'SELECT observationId,observationStartMJD,fieldRA,fieldDEC,rotSkyPos FROM SummaryAllProps order by observationStartMJD'
        self.spkstep = 30
        self.telescope = 'I11'


def test_makeConfigOIF():

    outpath = os.path.dirname(get_test_filepath('testorb.des'))
    argv = args(get_test_filepath('testorb.des'), get_test_filepath('baseline_10yrs_10klines.db'), -1, outpath)

    makeConfig(argv)

    config = configparser.ConfigParser()
    config.read(get_test_filepath('testorb-1-5.ini'))

    config.set('ASTEROID', 'population model', '../tests/data/testorb.des')
    config.set('SURVEY', 'survey database', '../tests/data/baseline_10yrs_10klines.db')

    config2 = configparser.ConfigParser()
    config2.read(get_test_filepath('test_oif_1.ini'))

    assert (config == config2)

    argv = args(get_test_filepath('testorb.des'), get_test_filepath('baseline_10yrs_10klines.db'), 3, outpath)

    makeConfig(argv)

    config = configparser.ConfigParser()
    config.read(get_test_filepath('testorb-1-3.ini'))

    config.set('ASTEROID', 'population model', '../tests/data/testorb.des')
    config.set('SURVEY', 'survey database', '../tests/data/baseline_10yrs_10klines.db')

    config1 = configparser.ConfigParser()
    config1.read(get_test_filepath('testorb-4-5.ini'))

    config1.set('ASTEROID', 'population model', '../tests/data/testorb.des')
    config1.set('SURVEY', 'survey database', '../tests/data/baseline_10yrs_10klines.db')

    config2 = configparser.ConfigParser()
    config2.read(get_test_filepath('test_oif_2.ini'))

    config3 = configparser.ConfigParser()
    config3.read(get_test_filepath('test_oif_3.ini'))

    assert (config == config2)
    assert (config1 == config3)

    return
