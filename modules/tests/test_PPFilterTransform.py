import pytest
import numpy as np
import pandas as pd

from ..PPFilterTransform import addFilterMag

def test_addFilterMag():
    # Test the fucntion addFilterMag
    ephemsdf = pd.DataFrame({
        "ObjID"  : ["test_object"],
        "FieldID": [1],
        "V"      : [19.0],
    })
    obsdf = pd.DataFrame({
        "filter" : ['g'],
        "observationId": [1]
    })
    popdf = pd.DataFrame({
        "!!OID" : ["test_object"],
        "color" : ["C"]
    })

    result_nominal = pd.DataFrame({
        "ObjID"     : ["test_object"],
        "FieldID"   : [1],
        "V"         : [19.0],
        "Filtermag" : [19.302]
    })

    result = addFilterMag(ephemsdf, obsdf, popdf)

    assert  result == result_nominal

    return