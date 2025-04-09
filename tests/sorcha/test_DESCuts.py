import pytest
from sorcha.modules.DESCuts import des_distance_cut,des_motion_cut
import pandas as pd
import numpy as np
import astropy.units as u

def test_distancecut():
    """
    testing the distance cut function
    """
    #when in boundary nothing gets dropped
    observations = {
        "Obj_Sun_x_LTC_km":[1],
        "Obj_Sun_y_LTC_km":[0],
        "Obj_Sun_z_LTC_km":[0],
    }
    observations = pd.DataFrame(observations)
    distance_up = 2
    distance_low = 0

    test_cut = des_distance_cut(observations,distance_up,distance_low)
    assert len(observations) == len(test_cut)
    # when out of boundary value gets dropped
    observations = {
        "Obj_Sun_x_LTC_km":[3],
        "Obj_Sun_y_LTC_km":[0],
        "Obj_Sun_z_LTC_km":[0],
    }

    observations = pd.DataFrame(observations)
    distance_up = 2
    distance_low = 0
    distance_up = (distance_up * u.km).to(u.au).value
    

    test_cut = des_distance_cut(observations,distance_up,distance_low)
    assert 0 == len(test_cut)
    # one object dropped the other staying
    observations = {
        "Obj_Sun_x_LTC_km":[3,1],
        "Obj_Sun_y_LTC_km":[0,0],
        "Obj_Sun_z_LTC_km":[0,0],
    }

    observations = pd.DataFrame(observations)
    distance_up = 2
    distance_low = 0
    distance_up = (distance_up * u.km).to(u.au).value
    

    test_cut = des_distance_cut(observations,distance_up,distance_low)
    assert 1 == len(test_cut)


def test_motioncut():
    """
    testing the motion cut function
    """
    #when in boundary nothing gets dropped
    observations = {
        "RARateCosDec_deg_day":[1],
        "DecRate_deg_day":[0],
    }
    observations = pd.DataFrame(observations)
    motion_up = 2
    motion_low = 0

    test_cut = des_motion_cut(observations,motion_up,motion_low)
    assert len(observations) == len(test_cut)
    # when out of boundary value gets dropped
    observations = {
        "RARateCosDec_deg_day":[3],
        "DecRate_deg_day":[0],
    }
    observations = pd.DataFrame(observations)
    motion_up = 2
    motion_low = 0

    test_cut = des_motion_cut(observations,motion_up,motion_low)
    assert 0 == len(test_cut)
    # one object dropped the other staying
    observations = {
        "RARateCosDec_deg_day":[1,3],
        "DecRate_deg_day":[0,0],
    }
    observations = pd.DataFrame(observations)
    motion_up = 2
    motion_low = 0

    test_cut = des_motion_cut(observations,motion_up,motion_low)
    assert 1 == len(test_cut)

