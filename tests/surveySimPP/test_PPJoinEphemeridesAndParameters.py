from sorcha.utilities.dataUtilitiesForTests import get_test_filepath
from numpy.testing import assert_equal


def test_PPJoinEphemeridesAndParameters():
    from sorcha.modules.PPJoinEphemeridesAndParameters import PPJoinEphemeridesAndParameters
    from sorcha.readers.OIFReader import read_full_oif_table
    from sorcha.readers.CSVReader import CSVDataReader

    oif_file = read_full_oif_table(get_test_filepath("oiftestoutput.txt"), "whitespace")
    param_reader = CSVDataReader(get_test_filepath("testcolour.txt"), "whitespace")
    params_file = param_reader.read_rows(0, 5)

    joined_df = PPJoinEphemeridesAndParameters(oif_file, params_file)

    first_row = [
        "S00000t",
        379,
        59853.205174,
        283890475.515,
        -1.12,
        11.969664,
        -0.280799,
        -0.19939,
        -0.132793,
        426166274.581,
        77286024.759,
        6987943.309,
        -2.356,
        11.386,
        4.087,
        148449956.422,
        18409281.409,
        7975891.432,
        -4.574,
        27.377,
        11.699,
        2.030016,
        17.615,
        0.3,
        0.0,
        0.1,
        0.15,
    ]

    assert_equal(joined_df.iloc[0].values[1:], first_row[1:])
    assert first_row[0] == "S00000t"
    assert len(joined_df.columns) == 27

    return
