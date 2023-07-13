from surveySimPP.utilities.test_data_utilities import get_test_filepath


def test_PPCheckInputObjectIDs():
    from surveySimPP.modules.PPReadOrbitFile import PPReadOrbitFile
    from surveySimPP.modules.PPReadPhysicalParameters import PPReadPhysicalParameters
    from surveySimPP.modules.PPCheckInputObjectIDs import PPCheckInputObjectIDs
    from surveySimPP.modules.PPReadOif import PPReadOif

    compval = 1

    padaor = PPReadOrbitFile(get_test_filepath("testorb.des"), 0, 10, "whitespace")
    padacl = PPReadPhysicalParameters(get_test_filepath("testcolour.txt"), 0, 10, "whitespace")
    padapo = PPReadOif(get_test_filepath("oiftestoutput.txt"), "whitespace")

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
