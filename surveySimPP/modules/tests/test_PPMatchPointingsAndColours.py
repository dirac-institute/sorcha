#!/bin/python

from surveySimPP.tests.data import get_test_filepath


def test_PPMatchPointingsAndColours():

    from surveySimPP.modules.PPJoinPhysicalParametersPointing import PPJoinPhysicalParametersPointing
    from surveySimPP.modules.PPReadOif import PPReadOif
    from surveySimPP.modules.PPReadPhysicalParameters import PPReadPhysicalParameters
    from surveySimPP.modules.PPMatchPointing import PPMatchPointing
    # from surveySimPP.modules.PPMatchPointingsAndColours import PPMatchPointingsAndColours

    padafr = PPReadOif(get_test_filepath('oiftestoutput.txt'), 'whitespace')
    padacl = PPReadPhysicalParameters(get_test_filepath('testcolour.txt'), ['g-r', 'i-r', 'z-r'], 0, 5, 'whitespace')

    resdf = PPJoinPhysicalParametersPointing(padafr, padacl)

    # DRY COMMENT OUT BELOW - PPhookBrightnessWithColour NO LONGER EXISTS
    # resdf1=PPhookBrightnessWithColour(resdf, 'r', 'i-r', 'i')
    # resdf3=PPhookBrightnessWithColour(resdf1, 'r', 'g-r', 'g')

    dbq = 'SELECT observationId, observationStartMJD, filter, seeingFwhmGeom, seeingFwhmEff, fiveSigmaDepth, fieldRA, fieldDec, rotSkyPos FROM SummaryAllProps order by observationId'

    pada5 = PPMatchPointing(get_test_filepath('baseline_10yrs_10klines.db'), ['g', 'r', 'i'], dbq)
    # pada6=PPMatchPointingsAndColours(resdf3,pada5)

    # ncols=38
    # ncolsre=len(pada6.columns)

    # assert ncols==ncolsre
    return
