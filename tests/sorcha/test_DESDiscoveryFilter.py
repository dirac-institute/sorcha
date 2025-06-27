import pytest
from sorcha.modules.DESDiscoveryFilter import compute_arccut, compute_triplet, DESDiscoveryFilter
import pandas as pd
import numpy as np
import astropy.units as u


def test_arccut():
    """
    testing the arccut function where when removing any observtaion will always result in a arccut > 6 months (182 days)

    """

    times = np.array([0, 100, 200, 300], dtype=np.float64)  # arccuts will be 200
    test = compute_arccut(times)
    assert test == True

    times = np.array([0, 10, 20, 30], dtype=np.float64)  # arccuts will be 20
    test = compute_arccut(times)
    assert test == False


def test_triplet():
    """
    testing triplet criteria checks. triplet pairs t1,t2 and t2,t3 will have difference less than window.
    """
    window = 60
    # has at least one triplet fitting critera
    times = np.array([10, 30, 50, 80, 100, 500], dtype=np.float64)
    test = compute_triplet(times, window)
    assert test == True
    # moving triplet to differnt place in array
    times = np.array([1000, 3000, 5000, 6080, 6100, 6120], dtype=np.float64)
    test = compute_triplet(times, window)
    assert test == True
    # has no triplets fitting criteria
    times = np.array([10, 30, 150, 180, 500, 5000], dtype=np.float64)
    test = compute_triplet(times, window)
    assert test == False


def test_DESDiscoveryFilter():
    # testing when object not dropped
    obs = {
        "ObjID": ["unique", "unique", "unique", "unique", "unique", "unique", "unique"],
        "Obj_Sun_x_LTC_km": [1, 1, 1, 1, 1, 1, 1],
        "Obj_Sun_y_LTC_km": [0, 0, 0, 0, 0, 0, 0],
        "Obj_Sun_z_LTC_km": [0, 0, 0, 0, 0, 0, 0],
        "fieldMJD_TAI": [10.0, 30.0, 50.0, 80.0, 100.0, 400.0, 500.0],
    }

    obs = pd.DataFrame(obs)
    test = DESDiscoveryFilter(obs)
    assert len(test) == len(obs)
    # testing when object is dropped
    obs = {
        "ObjID": ["unique", "unique", "unique", "unique", "unique", "unique", "unique"],
        "Obj_Sun_x_LTC_km": [1, 1, 1, 1, 1, 1, 1],
        "Obj_Sun_y_LTC_km": [0, 0, 0, 0, 0, 0, 0],
        "Obj_Sun_z_LTC_km": [0, 0, 0, 0, 0, 0, 0],
        "fieldMJD_TAI": [10.0, 30.0, 50.0, 80.0, 100.0, 110.0, 120.0],
    }
    obs = pd.DataFrame(obs)
    test = DESDiscoveryFilter(obs)
    assert len(test) == 0


def test_DESDiscoveryFilter_multiple_objects():
    """
    testing that when looking at mutiple indexes the expected results occur and that the order of values doesn't change
    """
    obs = {
        "ObjID": [
            *["obj1"] * 7,  # obj1 passes
            *["obj2"] * 7,  # obj2 fails
            *["obj3"] * 7,  # obj3 passes
            *["obj4"] * 7,  # obj4 fails
        ],
        "Obj_Sun_x_LTC_km": [
            *[1] * 7,
            *[2] * 7,
            *[3] * 7,
            *[4] * 7,
        ],
        "Obj_Sun_y_LTC_km": [
            *[0.1,0.4,0.91,1,4,5,10] ,
            *[0.2] * 7,
            *[0.3,0.45,0.99,2,4,6,6],
            *[0.4] * 7,
        ],
        "Obj_Sun_z_LTC_km": [
            *[0.1] * 7,
            *[0.2] * 7,
            *[0.3] * 7,
            *[0.4] * 7,
        ],
        "fieldMJD_TAI": [
            10.0,50.0,90.0,130.0,170.0,210.0,250.0,  # obj1: pass
            10.0,11.0,12.0,13.0,14.0,15.0,16.0,  # obj2:  fail arccut
            20.0,60.0,100.0,140.0,180.0,220.0,260.0,  # obj3: pass
            10,30,150,180,500,5000,6000,  # obj4: fail triplet
        ],
    }

    df = pd.DataFrame(obs).sort_values("fieldMJD_TAI").reset_index(drop=True) 
    df.reset_index(drop=True, inplace=True) # objects previously from linkingfilter will be sorted like this

    filtered = DESDiscoveryFilter(df)

    # checking correct objects kept
    remaining_ids = set(filtered["ObjID"].unique())
    expected_ids = {"obj1", "obj3"}
    assert remaining_ids == expected_ids

    # checking observations are sorted by mjd
    df_manuel_filter = df[(df["ObjID"] == "obj1") | (df["ObjID"] == "obj3")]
    df_manuel_filter = df_manuel_filter.sort_index().reset_index(drop=True)

    pd.testing.assert_frame_equal(df_manuel_filter, filtered)
