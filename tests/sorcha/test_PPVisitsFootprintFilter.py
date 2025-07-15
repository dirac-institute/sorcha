from sorcha.modules.PPVisitsFootprintFilter import PPVisitsFootprint
import pandas as pd
import os
from sorcha.utilities.dataUtilitiesForTests import get_test_filepath

 
visits_filename = get_test_filepath("test_visits_footprint.db")

# testing the PPVisitsFootprint using the LSST DP1 visits ccds
def test_is_on():
    "testing if points are on ccd using DP1 visits. Both points are on detectorId= '0' "
    fieldid = [2024110800245,2024110800246]
    # using the ra and dec of the centre of detector '0' for both visits 
    ra = [53.00453551947407,53.00490912491905]
    dec = [-28.190330812465483,-28.19118466571906]
    observations= {
        "FieldID":fieldid,
        "RA_deg":ra,
        "Dec_deg":dec,
    }
    field_df = pd.DataFrame(observations)
    query  = "SELECT llcra, llcdec, lrcra, lrcdec, urcra, urcdec, ulcra, ulcdec, ra as ra_centre, dec as dec_centre, detector as detectorID, magLim as fieldFiveSigmaDepth_mag FROM observations WHERE visitId = ?"


    onsensor, detectorId,_ = PPVisitsFootprint(
        field_df=field_df,
        query=query,
        visits_filename= visits_filename,
    )
    assert len(onsensor) == 2
    assert all(detector == '0' for detector in detectorId)

def test_is_off():
    "testing if points are off ccd using DP1 visits. Both points are far away from the footprint "
    fieldid = [2024110800245,2024110800246]
    ra = [10,10]
    dec = [-28,-28]
    observations= {
        "FieldID":fieldid,
        "RA_deg":ra,
        "Dec_deg":dec,
    }
    field_df = pd.DataFrame(observations)
    query  = "SELECT llcra, llcdec, lrcra, lrcdec, urcra, urcdec, ulcra, ulcdec, ra as ra_centre, dec as dec_centre, detector as detectorID, magLim as fieldFiveSigmaDepth_mag FROM observations WHERE visitId = ?"
 

    onsensor, _, _ = PPVisitsFootprint(
        field_df=field_df,
        query=query,
        visits_filename= visits_filename,
    )
    assert len(onsensor) == 0