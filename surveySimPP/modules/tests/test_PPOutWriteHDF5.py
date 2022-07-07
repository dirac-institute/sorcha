#!/bin/python

from surveySimPP.tests.data import get_test_filepath


def test_PPOutWriteHDF5():

    from surveySimPP.modules.PPJoinPhysicalParametersPointing import PPJoinPhysicalParametersPointing
    from surveySimPP.modules.PPReadOif import PPReadOif
    from surveySimPP.modules.PPReadPhysicalParameters import PPReadPhysicalParameters
    from surveySimPP.modules.PPMatchPointing import PPMatchPointing
    # from surveySimPP.modules.PPMatchPointingsAndColours import PPMatchPointingsAndColours
    # from surveySimPP.modules.PPOutput import PPOutWriteHDF5

    padafr = PPReadOif(get_test_filepath('oiftestoutput.txt'), "whitespace")
    padacl = PPReadPhysicalParameters(get_test_filepath('testcolour.txt'), ['g-r', 'i-r', 'z-r'], 0, 20, "whitespace")

    resdf = PPJoinPhysicalParametersPointing(padafr, padacl)

    dbq = 'SELECT observationId, observationStartMJD, filter, seeingFwhmGeom, seeingFwhmEff, fiveSigmaDepth, fieldRA, fieldDec, rotSkyPos FROM SummaryAllProps order by observationId'

    pada5 = PPMatchPointing(get_test_filepath('baseline_10yrs_10klines.db'), ['r', 'g', 'i'], dbq)

    # DRY COMMENT OUT BELOW - resdf3 NOT CREATED
    # pada6 = PPMatchPointingsAndColours(resdf3, pada5)

    # pada7 = PPOutWriteHDF5(pada6, 'outtest.h5', str(1))

    # pd.read_hdf('outtest.h5', str(1)).dtypes

    # ncols = 5

    # print(pada6)

    # rer = pd.read_hdf('outtest.h5')

    # nrs = len(rer.index)

    # os.system("rm outtest.h5")

    # # ncolsre=len(pada6.columns)

    # assert ncols == nrs
    return
