#!/bin/python

from surveySimPP.tests.data import get_test_filepath


def test_PPReadIntermDatabase(tmp_path):

    from surveySimPP.modules.PPMakeIntermediatePointingDatabase import PPMakeIntermediatePointingDatabase
    from surveySimPP.modules.PPReadIntermDatabase import PPReadIntermDatabase
    from surveySimPP.modules.PPReadPhysicalParameters import PPReadPhysicalParameters
    
    padacl = PPReadPhysicalParameters(get_test_filepath('testcolour.txt'), ['g-r', 'i-r', 'z-r'], 0, 5, 'whitespace')
    print(padacl)
    objid_list = padacl['ObjID'].unique().tolist()

    testdb = str(tmp_path / "testdb_PPIntermDB.db")
    daba = PPMakeIntermediatePointingDatabase(get_test_filepath('oiftestoutput.txt'), testdb, 10)

    padafr = PPReadIntermDatabase(testdb, objid_list)

    nlines = 9

    nlinesdb = len(padafr.index)

    assert nlines == nlinesdb
    return
