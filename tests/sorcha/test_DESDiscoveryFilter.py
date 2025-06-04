import pytest
from sorcha.modules.DESDiscoveryFilter import compute_arccut, compute_triplet, DESDiscoveryFilter
import pandas as pd
import numpy as np
import astropy.units as u


def test_arccut():
    """
    testing the arccut function where when removing any observtaion will always result in a arccut > 6 months (182 days)

    """

    times = np.array([0,100,200,300], dtype=np.float64) # arccuts will be 200
    test = compute_arccut(times)
    assert test >= 0.5*365.25

    times = np.array([0,10,20,30], dtype=np.float64) # arccuts will be 20 
    test = compute_arccut(times)
    assert test <= 0.5*365.25


def test_triplet():
    """
    testing triplet criteria checks. triplet pairs t1,t2 and t2,t3 will have difference less than window. 
    """
    window = 60
    # has at least one triplet fitting critera
    times = np.array([10,30,50,80,100,500], dtype=np.float64)
    test = compute_triplet(times,window)
    assert test == True
    #moving triplet to differnt place in array
    times = np.array([1000,3000,5000,6080,6100,6120], dtype=np.float64)
    test = compute_triplet(times,window)
    assert test == True
    # has no triplets fitting criteria 
    times = np.array([10,30,150,180,500,5000], dtype=np.float64)
    test = compute_triplet(times,window)
    assert test == False

def test_DESDiscoveryFilter():
    # testing when object not dropped
    obs = {
        "ObjID":["unique","unique","unique","unique","unique","unique","unique"],
        "Obj_Sun_x_LTC_km":[1,1,1,1,1,1,1],
        "Obj_Sun_y_LTC_km":[0,0,0,0,0,0,0],
        "Obj_Sun_z_LTC_km":[0,0,0,0,0,0,0],
        'fieldMJD_TAI':[10.0,30.0,50.0,80.0,100.0,400.0,500.0],
    }
    
    obs = pd.DataFrame(obs)
    test = DESDiscoveryFilter(obs)
    assert len(test) == len(obs)
    # testing when object is dropped
    obs = {
        "ObjID":["unique","unique","unique","unique","unique","unique","unique"],
        "Obj_Sun_x_LTC_km":[1,1,1,1,1,1,1],
        "Obj_Sun_y_LTC_km":[0,0,0,0,0,0,0],
        "Obj_Sun_z_LTC_km":[0,0,0,0,0,0,0],
        'fieldMJD_TAI':[10.0,30.0,50.0,80.0,100.0,110.0,120.0],
    }
    obs = pd.DataFrame(obs)
    test = DESDiscoveryFilter(obs)
    assert len(test) == 0