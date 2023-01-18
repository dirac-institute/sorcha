from surveySimPP.tests.data import get_test_filepath


class args:
    def __init__(self, m, dw, dr, dl):
        self.p = get_test_filepath('testcolour.txt')
        self.o = get_test_filepath('testorb.des')
        self.e = get_test_filepath('oiftestoutput.txt')
        self.c = get_test_filepath('test_PPConfig.ini')
        self.u = './'
        self.m = m
        self.s = 'lsst'
        self.t = 'testout'
        self.v = True
        self.dw = dw
        self.dr = dr
        self.dl = dl


def test_PPCommandLineParser():

    from surveySimPP.modules.PPCommandLineParser import PPCommandLineParser

    cmd_dict_1 = PPCommandLineParser(args(False, False, None, False))
    expected_1 = {'paramsinput': '/Users/stephaniemerritt/Projects/survey_simulator_post_processing/surveySimPP/tests/data/testcolour.txt',
                  'orbinfile': '/Users/stephaniemerritt/Projects/survey_simulator_post_processing/surveySimPP/tests/data/testorb.des',
                  'oifoutput': '/Users/stephaniemerritt/Projects/survey_simulator_post_processing/surveySimPP/tests/data/oiftestoutput.txt',
                  'configfile': '/Users/stephaniemerritt/Projects/survey_simulator_post_processing/surveySimPP/tests/data/test_PPConfig.ini',
                  'outpath': './',
                  'makeTemporaryEphemerisDatabase': False,
                  'readTemporaryEphemerisDatabase': None,
                  'deleteTemporaryEphemerisDatabase': False,
                  'surveyname': 'lsst',
                  'outfilestem': 'testout',
                  'verbose': True}

    cmd_dict_2 = PPCommandLineParser(args(get_test_filepath('testcomet.txt'), False, get_test_filepath('test_data_mag.csv'), True))
    expected_2 = {'paramsinput': '/Users/stephaniemerritt/Projects/survey_simulator_post_processing/surveySimPP/tests/data/testcolour.txt',
                  'orbinfile': '/Users/stephaniemerritt/Projects/survey_simulator_post_processing/surveySimPP/tests/data/testorb.des',
                  'oifoutput': '/Users/stephaniemerritt/Projects/survey_simulator_post_processing/surveySimPP/tests/data/oiftestoutput.txt',
                  'configfile': '/Users/stephaniemerritt/Projects/survey_simulator_post_processing/surveySimPP/tests/data/test_PPConfig.ini',
                  'outpath': './',
                  'cometinput': '/Users/stephaniemerritt/Projects/survey_simulator_post_processing/surveySimPP/tests/data/testcomet.txt',
                  'makeTemporaryEphemerisDatabase': False,
                  'readTemporaryEphemerisDatabase': '/Users/stephaniemerritt/Projects/survey_simulator_post_processing/surveySimPP/tests/data/test_data_mag.csv',
                  'deleteTemporaryEphemerisDatabase': True,
                  'surveyname': 'lsst',
                  'outfilestem': 'testout',
                  'verbose': True}

    cmd_dict_3 = PPCommandLineParser(args(False, True, None, True))
    expected_3 = {'paramsinput': '/Users/stephaniemerritt/Projects/survey_simulator_post_processing/surveySimPP/tests/data/testcolour.txt',
                  'orbinfile': '/Users/stephaniemerritt/Projects/survey_simulator_post_processing/surveySimPP/tests/data/testorb.des',
                  'oifoutput': '/Users/stephaniemerritt/Projects/survey_simulator_post_processing/surveySimPP/tests/data/oiftestoutput.txt',
                  'configfile': '/Users/stephaniemerritt/Projects/survey_simulator_post_processing/surveySimPP/tests/data/test_PPConfig.ini',
                  'outpath': './',
                  'makeTemporaryEphemerisDatabase': True,
                  'readTemporaryEphemerisDatabase': None,
                  'deleteTemporaryEphemerisDatabase': True,
                  'surveyname': 'lsst',
                  'outfilestem': 'testout',
                  'verbose': True}

    assert cmd_dict_1 == expected_1
    assert cmd_dict_2 == expected_2
    assert cmd_dict_3 == expected_3

    return
