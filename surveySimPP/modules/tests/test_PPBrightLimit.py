#!/bin/python

import pytest
import pandas as pd


def test_PPBrightLimit():

    from surveySimPP.modules.PPJoinPhysicalParametersPointing import PPJoinPhysicalParametersPointing
    from surveySimPP.modules.PPReadOif import PPReadOif
    from surveySimPP.modules.PPReadPhysicalParameters import PPReadPhysicalParameters
    from surveySimPP.modules.PPMatchPointing import PPMatchPointing
    from surveySimPP.modules.PPMatchPointingsAndColours import PPMatchPointingsAndColours
    from surveySimPP.modules.PPBrightLimit import PPBrightLimit

    padafr = PPReadOif('./data/test/oiftestoutput.txt', 'whitespace')
    padacl = PPReadPhysicalParameters('./data/test/testcolour.txt', 0, 5, 'whitespace')

    resdf = PPJoinPhysicalParametersPointing(padafr, padacl)

    dbq = 'SELECT observationId, observationStartMJD, filter, seeingFwhmGeom, seeingFwhmEff, fiveSigmaDepth, fieldRA, fieldDec, rotSkyPos FROM SummaryAllProps order by observationId'

    pada5 = PPMatchPointing('./data/test/baseline_10yrs_10klines.db', ['r', 'g', 'i'], dbq)

    # DRY COMMENT OUT BELOW - resdf3 NOT CREATED
    # pada6=PPMatchPointingsAndColours(resdf3,pada5)

    # print(pada6)

    # pada7=PPBrightLimit(pada6,18.2)

    # nros=5
    # nrosre=len(pada7.index)

    # assert nros==nrosre

    return
