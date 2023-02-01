import numpy as np
import pytest
from numpy.testing import assert_equal
from pandas.testing import assert_frame_equal

from surveySimPP.tests.data import get_test_filepath


def test_PPReadOif():

    from surveySimPP.modules.PPReadOif import PPReadOif

    oif_file = PPReadOif(get_test_filepath('oiftestoutput.txt'), 'whitespace')
    oif_hdf5 = PPReadOif(get_test_filepath('oiftestoutput.h5'), 'hdf5')
    oif_csv = PPReadOif(get_test_filepath('oiftestoutput.csv'), 'csv')

    expected_first_row = np.array(['S00000t', 379, 59853.205174, 283890475.515, -1.12, 11.969664,
                                   -0.280799, -0.19939, -0.132793, 426166274.581, 77286024.759,
                                   6987943.309, -2.356, 11.386, 4.087, 148449956.422, 18409281.409,
                                   7975891.432, -4.574, 27.377, 11.699, 2.030016], dtype='object')

    column_headings = np.array(['ObjID', 'FieldID', 'FieldMJD', 'AstRange(km)',
                                'AstRangeRate(km/s)', 'AstRA(deg)', 'AstRARate(deg/day)',
                                'AstDec(deg)', 'AstDecRate(deg/day)', 'Ast-Sun(J2000x)(km)',
                                'Ast-Sun(J2000y)(km)', 'Ast-Sun(J2000z)(km)',
                                'Ast-Sun(J2000vx)(km/s)', 'Ast-Sun(J2000vy)(km/s)',
                                'Ast-Sun(J2000vz)(km/s)', 'Obs-Sun(J2000x)(km)',
                                'Obs-Sun(J2000y)(km)', 'Obs-Sun(J2000z)(km)',
                                'Obs-Sun(J2000vx)(km/s)', 'Obs-Sun(J2000vy)(km/s)',
                                'Obs-Sun(J2000vz)(km/s)', 'Sun-Ast-Obs(deg)'], dtype=object)

    assert_frame_equal(oif_file, oif_hdf5)
    assert_frame_equal(oif_file, oif_csv)

    assert_equal(expected_first_row, oif_file.iloc[0].values)
    assert_equal(column_headings, oif_file.columns.values)

    assert len(oif_file) == 9
    assert len(oif_file.columns) == 22

    with pytest.raises(SystemExit) as e:
        oif_file = PPReadOif(get_test_filepath('testcolour.txt'), 'whitespace')

    assert e.type == SystemExit
    assert e.value.code == 'ERROR: PPReadOif: column headings do not match expected OIF column headings.'

    return


def test_PPSkipOifHeader():

    from surveySimPP.modules.PPReadOif import PPSkipOifHeader

    oif_noheader = PPSkipOifHeader(get_test_filepath('oiftestoutput.txt'), 'ObjID', delim_whitespace=True)
    oif_header = PPSkipOifHeader(get_test_filepath('oiftestoutput_header.txt'), 'ObjID', delim_whitespace=True)

    expected_first_row = np.array(['S00000t', 379, 59853.205174, 283890475.515, -1.12, 11.969664,
                                   -0.280799, -0.19939, -0.132793, 426166274.581, 77286024.759,
                                   6987943.309, -2.356, 11.386, 4.087, 148449956.422, 18409281.409,
                                   7975891.432, -4.574, 27.377, 11.699, 2.030016, 17.615, 3.94],
                                  dtype='object')

    assert_frame_equal(oif_header, oif_noheader)
    assert_equal(expected_first_row, oif_header.iloc[0].values)

    assert len(oif_header) == 9
    assert len(oif_header.columns) == 24

    return
