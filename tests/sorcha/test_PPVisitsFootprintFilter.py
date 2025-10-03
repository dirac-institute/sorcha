from sorcha.modules.PPVisitsFootprintFilter import PPVisitsFootprint
import pandas as pd
import os
from sorcha.utilities.dataUtilitiesForTests import get_test_filepath
import numpy as np
 
visits_filename = get_test_filepath("test_visits_footprint.db")

# camera footprint 05 is not wrapped in 0-360, simialr to how the DECam footprints are given when at this boundary.
# camera footprint 06 is a normal footprint not near this boundary

# testing the PPVisitsFootprint using simulated visits ccds
def test_is_on():
    "testing if points are on ccd using simulated visits file.  points are on detectorId= '6' and '0' "
    fieldid = ["05","06"]
    fieldra = [0.11,10]
    # using the ra and dec of the centre of detector '0' for both visits 
    ra = [2,10] # both points lie on the footprint, (ra =2 wont be wrapped)
    dec = [0,0]
    observations= {
        "FieldID":fieldid,
        "fieldRA_deg":fieldra,
        "RA_deg":ra,
        "Dec_deg":dec,
    }
    field_df = pd.DataFrame(observations)
    query  = "SELECT llcra, llcdec, lrcra, lrcdec, urcra, urcdec, ulcra, ulcdec, ra as ra_centre, dec as dec_centre, detector as detectorID, magLim as limMag_perChip FROM observations WHERE visitId = ?"


    onsensor, detectorId,_ = PPVisitsFootprint(
        field_df=field_df,
        query=query,
        visits_filename= visits_filename,
        k_num=1,
        plot = False
    )
    assert len(onsensor) == 2
    print(detectorId)
    assert detectorId == ['6', '0']

def test_is_off():
    "testing if points are off ccd using simulated visits file. Both points are far away from the footprint "
    fieldid = ["05","06"]
    fieldra = [0.11,10]

    ra = [50,50]
    dec = [-28,-28]
    observations= {
        "FieldID":fieldid,
        "fieldRA_deg":fieldra,
        "RA_deg":ra,
        "Dec_deg":dec,
    }
    field_df = pd.DataFrame(observations)
    query  = "SELECT llcra, llcdec, lrcra, lrcdec, urcra, urcdec, ulcra, ulcdec, ra as ra_centre, dec as dec_centre, detector as detectorID, magLim as limMag_perChip FROM observations WHERE visitId = ?"
 

    onsensor, _, _ = PPVisitsFootprint(
        field_df=field_df,
        query=query,
        visits_filename= visits_filename,
        k_num=1,
        plot = False
    )
    assert len(onsensor) == 0


def test_wrap_around_is_working():
    """
    testing if two points are in the camera footprint. in this case the two points are at 359.xx and the camera footprint is 
    at 0.11. This tests that the points are properky unwrapped and fall into the camera footprint
    """
    fieldid = ["05","05"]
    fieldra = [0.11,0.11]
    # this points should land on detectorID "0" which is centred around coords [0,0], i.e unwrapped onto this ccd 
    ra = [359.8,359.95]
    dec = [0,0.5]

    observations= {
        "FieldID":fieldid,
        "fieldRA_deg":fieldra,
        "RA_deg":ra,
        "Dec_deg":dec,
    }

    field_df = pd.DataFrame(observations)
    query  = "SELECT llcra, llcdec, lrcra, lrcdec, urcra, urcdec, ulcra, ulcdec, ra as ra_centre, dec as dec_centre, detector as detectorID, magLim as limMag_perChip FROM observations WHERE visitId = ?"


    onsensor, detectorId,_ = PPVisitsFootprint(
        field_df=field_df,
        query=query,
        visits_filename= visits_filename,
        k_num=1,
        plot = False
    )
    assert len(onsensor) == 2
    assert all(detector == '0' for detector in detectorId)







# testing des camera footprint 

# testing the PPVisitsFootprint using simulated visits ccds
def test_is_DES_on():
    "testing if points are on ccd using DES visits file.  "
    visits_DES_filename = get_test_filepath("test_DES_visits_footprint.db")

    # using the ra and dec of the centre of detector '0' for both visits 
    ra =    [305.683,   # top wall, centre left of ccd 
            307.379,    # middle of ccd 
            306.140,    # at a ccd corner
            305.483,    # at a ccd corner 
            306.701,    # at a ccd corner
            306.704,    # at a ccd corner
            305.709,    # middle of a ccd
            305.136,    # at a ccd corner 
            304.5,      # left most ccd left edge
            306.704,    # middle of a ccd 
            306.91,     # not on footprint
            ]
    
    dec =   [-50.795088,    # top wall, centre left of ccd 
             -50.712309,    # middle of ccd 
             -51.301,       # at a ccd corner
             -50.308,       # at a ccd corner 
             -50.259,       # at a ccd corner
             -51.409,       # at a ccd corner
             -51.744,       # middle of a ccd
             -51.289,       # at a ccd corner 
             -50.833,       # left most ccd left edge
             -51.848,       # middle of a ccd 
             -51.017,       # not on footprint
            ]
    

    fieldid = np.full(len(dec),"226650")
    fieldra = np.full(len(dec),306.4814)
    observations= {
        "FieldID":fieldid,
        "fieldRA_deg":fieldra,
        "RA_deg":ra,
        "Dec_deg":dec,
    }
    field_df = pd.DataFrame(observations)
    query  = "SELECT llcra, llcdec, lrcra, lrcdec, urcra, urcdec, ulcra, ulcdec, ra_centre, dec_centre, detectorID, limMag_perChip FROM observations WHERE visitId = ?"


    onsensor, detectorId,_ = PPVisitsFootprint(
        field_df=field_df,
        query=query,
        visits_filename= visits_DES_filename,
        k_num= 2,
        plot= True, # set this to true to manuelly see the camera footprint
    )
    assert len(onsensor) == 10
    print(detectorId)
    assert detectorId == [34, 24, 47, 9, 7, 49, 57, 45, 25, 62]



def test_des_k_num():
    """
    This unit test is for testing the number of ccds needed to generate for each point. 
    From testing 3 ccds avoids the edge cases for DES.
    this unit test shows this edge case failing for 1 and 2 ccds and passing for 3.

    LSST might be differnt as its in a sqare grid. this parameter might be camera footprint specific 
    more testing with LSST data would be needed 
    """