#!/bin/python

# import sqlite3

from surveySimPP.tests.data import get_test_filepath


def test_PPOutWriteSqlite3():

    from surveySimPP.modules.PPJoinPhysicalParametersPointing import PPJoinPhysicalParametersPointing
    from surveySimPP.modules.PPReadOif import PPReadOif
    from surveySimPP.modules.PPReadPhysicalParameters import PPReadPhysicalParameters
    from surveySimPP.modules.PPMatchPointing import PPMatchPointing
    # from surveySimPP.modules.PPMatchPointingsAndColours import PPMatchPointingsAndColours
    from surveySimPP.modules.PPOutput import PPOutWriteSqlite3

    padafr = PPReadOif(get_test_filepath('oiftestoutput.txt'), "whitespace")
    padacl = PPReadPhysicalParameters(get_test_filepath('testcolour.txt'), ['g-r', 'i-r', 'z-r'], 0, 5, "whitespace")

    resdf = PPJoinPhysicalParametersPointing(padafr, padacl)

    dbq = 'SELECT observationId, observationStartMJD, filter, seeingFwhmGeom, seeingFwhmEff, fiveSigmaDepth, fieldRA, fieldDec, rotSkyPos FROM SummaryAllProps order by observationId'

    pada5 = PPMatchPointing(get_test_filepath('baseline_10yrs_10klines.db'), ['g', 'r', 'i'], dbq)
    # DRY COMMENT OUT BELOW - resdf3 NOT CREATED
    # pada6 = PPMatchPointingsAndColours(resdf3, pada5)

    # pada7 = PPOutWriteSqlite3(pada6, './outtest.db')
    # nrows = 5

    # con = sqlite3.connect('./outtest.db')
    # cur = con.cursor()
    # cur.execute("SELECT COUNT(*) FROM pp_results")
    # i = cur.fetchone()[0]
    # cmp = int(i)

    # os.system("rm ./outtest.db")

    # assert nrows == cmp
    return
