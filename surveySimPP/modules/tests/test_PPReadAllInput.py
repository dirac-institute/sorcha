import numpy as np
from numpy.testing import assert_equal

from surveySimPP.tests.data import get_test_filepath


def test_PPReadAllInput():

    from surveySimPP.modules.PPReadAllInput import PPReadAllInput
    from surveySimPP.modules.PPReadPointingDatabase import PPReadPointingDatabase

    cmd_args = {'paramsinput': get_test_filepath('testcolour.txt'),
                'orbinfile': get_test_filepath('testorb.des'),
                'oifoutput': get_test_filepath('oiftestoutput.txt'),
                'configfile': get_test_filepath('test_PPConfig.ini'),
                'outpath': './',
                'makeTemporaryEphemerisDatabase': False,
                'readTemporaryEphemerisDatabase': None,
                'verbose': False}

    configs = {'cometactivity': 'none',
               'filesep': 'whitespace',
               'ephemerides_type': 'oif',
               'ephFormat': 'whitespace',
               'pointingdatabase': get_test_filepath('baseline_10yrs_10klines.db'),
               'observing_filters': ['u', 'g', 'r', 'i', 'z', 'y'],
               'ppdbquery': 'SELECT observationId, observationStartMJD, filter, seeingFwhmGeom, seeingFwhmEff, fiveSigmaDepth, fieldRA, fieldDec, rotSkyPos FROM SummaryAllProps order by observationId'}

    filterpointing = PPReadPointingDatabase(configs['pointingdatabase'], configs['observing_filters'], configs['ppdbquery'])

    observations = PPReadAllInput(cmd_args, configs, filterpointing, 0, 10)

    expected_first_line = np.array(['S00000t', 379, 59853.205174, 283890475.515, -1.12, 11.969664,
                                    -0.280799, -0.19939, -0.132793, 426166274.581, 77286024.759,
                                    6987943.309, -2.356, 11.386, 4.087, 148449956.422, 18409281.409,
                                    7975891.432, -4.574, 27.377, 11.699, 2.030016, 17.615, 0.3, 0.0,
                                    0.1, 0.15, 0.952105479028, 0.504888475701, 4.899098347472,
                                    148.881068605772, 39.949789586436, 54486.32292808, 54466.0, 'y',
                                    0.8335900735376087, 0.9508395055202052, 21.90666355001711,
                                    12.51891, -1.720966, 284.16549987479397], dtype=object)

    expected_columns = np.array(['ObjID', 'FieldID', 'FieldMJD', 'AstRange(km)',
                                 'AstRangeRate(km/s)', 'AstRA(deg)', 'AstRARate(deg/day)',
                                 'AstDec(deg)', 'AstDecRate(deg/day)', 'Ast-Sun(J2000x)(km)',
                                 'Ast-Sun(J2000y)(km)', 'Ast-Sun(J2000z)(km)',
                                 'Ast-Sun(J2000vx)(km/s)', 'Ast-Sun(J2000vy)(km/s)',
                                 'Ast-Sun(J2000vz)(km/s)', 'Obs-Sun(J2000x)(km)',
                                 'Obs-Sun(J2000y)(km)', 'Obs-Sun(J2000z)(km)',
                                 'Obs-Sun(J2000vx)(km/s)', 'Obs-Sun(J2000vy)(km/s)',
                                 'Obs-Sun(J2000vz)(km/s)', 'Sun-Ast-Obs(deg)', 'H_r', 'g-r', 'i-r',
                                 'z-r', 'GS', 'q', 'e', 'incl', 'node', 'argperi', 't_p', 't_0',
                                 'optFilter', 'seeingFwhmGeom', 'seeingFwhmEff', 'fiveSigmaDepth',
                                 'fieldRA', 'fieldDec', 'rotSkyPos'], dtype=object)

    assert_equal(observations.columns.values, expected_columns)
    assert_equal(expected_first_line, observations.iloc[0].values)

    assert len(observations) == 9

    return
