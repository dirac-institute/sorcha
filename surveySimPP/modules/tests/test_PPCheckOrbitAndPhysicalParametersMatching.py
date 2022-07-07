#!/bin/python

from surveySimPP.tests.data import get_test_filepath


def test_PPCheckOrbitAndPhysicalParametersMatching():

    from surveySimPP.modules.PPReadOrbitFile import PPReadOrbitFile
    from surveySimPP.modules.PPReadPhysicalParameters import PPReadPhysicalParameters
    from surveySimPP.modules.PPCheckOrbitAndPhysicalParametersMatching import PPCheckOrbitAndPhysicalParametersMatching
    from surveySimPP.modules.PPReadOif import PPReadOif

    compval = 1

    padaor = PPReadOrbitFile(get_test_filepath('testorb.des'), 0, 10, 'whitespace')
    padacl = PPReadPhysicalParameters(get_test_filepath('testcolour.txt'), ['g-r', 'i-r', 'z-r'], 0, 10, 'whitespace')
    padapo = PPReadOif(get_test_filepath('oiftestoutput.txt'), 'whitespace')

    print(padaor)
    print(padacl)
    print(padapo)

    try:
        PPCheckOrbitAndPhysicalParametersMatching(padaor, padacl, padapo)
        ret = 1
    except:
        ret = 0

    assert ret == compval

    return
