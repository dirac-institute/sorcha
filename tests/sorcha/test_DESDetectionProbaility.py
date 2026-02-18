import numpy as np
from sorcha.modules.DESDetectionProbability import DEScalcDetectionProbability, DESDetectionProbability
import math
import pandas as pd
def test_DEScalcDetectionProbability():
    mag, limmag, c, k = 20,23.1,0.90,4.55
    P = DEScalcDetectionProbability(mag,limmag,c,k)

    assert math.isclose(P, 0.8599493561841001,rel_tol=1e-10)

    mag, limmag, c, k = 24,23.1,0.90,3.99
    P = DEScalcDetectionProbability(mag,limmag,c,k)

    assert math.isclose(P, 0.0230733144369,rel_tol=1e-10)



def test_DESDectionProbability():

    obs = {
        "PSFMag": [20,24],
        "fiveSigmaDepth_mag": [23.1,23.1],
        "c":[0.90,0.90],
        "k":[4.55,3.99],
        }
    obs = pd.DataFrame(obs)
    P = DESDetectionProbability(obs)

    assert math.isclose(P[0], 0.8599493561841001,rel_tol=1e-10)

    assert math.isclose(P[1], 0.0230733144369,rel_tol=1e-10)