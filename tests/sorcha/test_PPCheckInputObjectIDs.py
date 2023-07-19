from sorcha.utilities.dataUtilitiesForTests import get_test_filepath


def test_PPCheckInputObjectIDs():
    from sorcha.modules.PPCheckInputObjectIDs import PPCheckInputObjectIDs
    from sorcha.readers.CSVReader import CSVDataReader
    from sorcha.readers.OIFReader import read_full_oif_table
    from sorcha.readers.OrbitAuxReader import OrbitAuxReader

    compval = 1

    orbit_reader = OrbitAuxReader(get_test_filepath("testorb.des"), "whitespace")
    padaor = orbit_reader.read_rows(0, 10)

    param_reader = CSVDataReader(get_test_filepath("testcolour.txt"), "whitespace")
    padacl = param_reader.read_rows(0, 10)

    padapo = read_full_oif_table(get_test_filepath("oiftestoutput.txt"), "whitespace")

    print(padaor)
    print(padacl)
    print(padapo)

    try:
        PPCheckInputObjectIDs(padaor, padacl, padapo)
        ret = 1
    except Exception:
        ret = 0

    assert ret == compval

    return
