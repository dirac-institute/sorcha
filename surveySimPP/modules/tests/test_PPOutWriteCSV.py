#!/bin/python

from surveySimPP.tests.data import get_test_filepath


def test_PPOutWriteCSV():

    from surveySimPP.modules.PPJoinEphemeridesAndParameters import PPJoinEphemeridesAndParameters
    from surveySimPP.modules.PPReadOif import PPReadOif
    from surveySimPP.modules.PPReadPhysicalParameters import PPReadPhysicalParameters
    from surveySimPP.modules.PPReadPointingDatabase import PPReadPointingDatabase
    # from surveySimPP.modules.PPMatchPointingsAndColours import PPMatchPointingsAndColours
    # from surveySimPP.modules.PPOutput import PPOutWriteCSV

    padafr = PPReadOif(get_test_filepath('oiftestoutput.txt'), "whitespace")
    padacl = PPReadPhysicalParameters(get_test_filepath('testcolour.txt'), ['g-r', 'i-r', 'z-r'], 0, 5, "whitespace")

    resdf = PPJoinEphemeridesAndParameters(padafr, padacl)

    dbq = 'SELECT observationId, observationStartMJD, filter, seeingFwhmGeom, seeingFwhmEff, fiveSigmaDepth, fieldRA, fieldDec, rotSkyPos FROM SummaryAllProps order by observationId'

    pada5 = PPReadPointingDatabase(get_test_filepath('baseline_10yrs_10klines.db'), ['g', 'r', 'i'], dbq)

    # DRY COMMENT OUT BELOW - resdf3 NOT CREATED
    # pada6 = PPMatchPointingsAndColours(resdf3, pada5)

    # pada7 = PPOutWriteCSV(pada6, './outtest.csv')
    # ncols = 6

    # tpt = os.popen("wc -l ./outtest.csv | awk '{print $1}'")
    # cmp = tpt.read()
    # cmp.strip()
    # cmp1 = int(cmp)
    # os.system("rm ./outtest.csv")

    # # ncolsre=len(pada6.columns)

    # assert ncols == cmp1
    return
