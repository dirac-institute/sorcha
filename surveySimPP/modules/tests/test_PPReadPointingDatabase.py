#!/bin/python

from surveySimPP.tests.data import get_test_filepath


def test_PPReadPointingDatabase():

    from surveySimPP.modules.PPReadPointingDatabase import PPReadPointingDatabase

    padapo = PPReadPointingDatabase(
        get_test_filepath('baseline_10yrs_10klines.db'),
        ['u', 'g', 'r', 'i', 'z', 'y'],
        'SELECT observationId, observationStartMJD, filter, seeingFwhmGeom, seeingFwhmEff, fiveSigmaDepth, fieldRA, fieldDec, rotSkyPos FROM SummaryAllProps order by observationId'
    )

    nlines = 10007

    nlinesdb = len(padapo.index)

    assert nlines == nlinesdb
    return
