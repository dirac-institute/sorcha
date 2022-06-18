#!/bin/python

from surveySimPP.tests.data import get_test_filepath


def test_PPCalculateSimpleCometaryMagnitude():

    from surveySimPP.modules.PPReadOif import PPReadOif
    from surveySimPP.modules.PPReadPhysicalParameters import PPReadPhysicalParameters
    from surveySimPP.modules.PPReadCometaryInput import PPReadCometaryInput
    from surveySimPP.modules.PPJoinPhysicalParametersPointing import PPJoinPhysicalParametersPointing
    from surveySimPP.modules.PPJoinOrbitalData import PPJoinOrbitalData
    from surveySimPP.modules.PPReadOrbitFile import PPReadOrbitFile
    from surveySimPP.modules.PPCalculateSimpleCometaryMagnitude import PPCalculateSimpleCometaryMagnitude

    padafr = PPReadOif(get_test_filepath('67P.out'), 'whitespace')
    padacl = PPReadPhysicalParameters(get_test_filepath('testcometcolour.txt'), ['g-r', 'i-r', 'z-r'], 0, 3, 'whitespace')
    padaco = PPReadCometaryInput(get_test_filepath('testcomet.txt'), 0, 3, 'whitespace')
    padaor = PPReadOrbitFile(get_test_filepath('67P.orb.des'), 0, 3, 'whitespace')

    resdf1 = PPJoinPhysicalParametersPointing(padafr, padacl)
    resdf2 = PPJoinPhysicalParametersPointing(resdf1, padaco)
    resdf3 = PPJoinOrbitalData(resdf2, padaor)

    # resdf3['r'] = resdf3['V']

    ncols1 = len(resdf3.columns) + 4

    resdf = PPCalculateSimpleCometaryMagnitude(resdf3, 'r')

    ncols = len(resdf.columns)

    assert ncols == ncols1
    return
