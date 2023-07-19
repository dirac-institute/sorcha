from sorcha.utilities.dataUtilitiesForTests import get_test_filepath


def test_PPreadColoursUser():
    from sorcha.readers.OIFReader import read_full_oif_table
    from sorcha.utilities.PPreadColoursUser import PPreadColoursUser

    resval = 0.6

    padain = read_full_oif_table(get_test_filepath("oiftestoutput.txt"), "whitespace")
    padafr = PPreadColoursUser(padain, "r-X", 0.6, 0.0)

    val = padafr.at[0, "r-X"]

    assert resval == val

    return
