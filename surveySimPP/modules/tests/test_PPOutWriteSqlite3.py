#!/bin/python

import pytest
import pandas as pd
import os
import sys
import sqlite3


def test_PPOutWriteSqlite3():

    from surveySimPP.modules.PPJoinColourPointing import PPJoinColourPointing
    from surveySimPP.modules.PPReadOif import PPReadOif
    from surveySimPP.modules.PPReadColours import PPReadColours
    from surveySimPP.modules.PPMatchPointing import PPMatchPointing
    from surveySimPP.modules.PPMatchPointingsAndColours import PPMatchPointingsAndColours
    from surveySimPP.modules.PPOutWriteSqlite3 import PPOutWriteSqlite3

    padafr = PPReadOif('./data/test/oiftestoutput.txt', "whitespace")
    padacl = PPReadColours('./data/test/testcolour.txt', 0, 5, "whitespace")

    resdf = PPJoinColourPointing(padafr, padacl)

    dbq = 'SELECT observationId, observationStartMJD, filter, seeingFwhmGeom, seeingFwhmEff, fiveSigmaDepth, fieldRA, fieldDec, rotSkyPos FROM SummaryAllProps order by observationId'

    pada5 = PPMatchPointing('./data/test/baseline_10yrs_10klines.db', ['g', 'r', 'i'], dbq)
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
