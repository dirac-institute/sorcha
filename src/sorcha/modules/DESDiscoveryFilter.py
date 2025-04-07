
import numpy as np


## filter for the DES object discovery requirements. 
#  the reqiurments are:
#       a distance and motion limit 
#       An ARCCUT limit (has to be at least 2 objects not in a triplet discovery season)
#       SSP_number_tracklets >= 7 (this is a config file parameter and already decided by the user, the default config file will ) 
#       the observation of the discovery triplets have to be within 60/90 days (depending on distance) of eachother



# this is a rough example of a discovery filter for DES that can be used after PPLinkingFilter

def discoveryfilter(sconfigs,observations):
    discoveried_index = []
    if sconfigs.linkingfilter.ssp_distance_cut_on:
        observations = observations[sconfigs.linkingfilter.ssp_distance_cut_lower < observations["Obj_Sun_LTC_km"]>sconfigs.linkingfilter.ssp_distance_cut_upper]

    if sconfigs.linkingfilter.ssp_motion_cut_on:
        observations = observations[sconfigs.linkingfilter.ssp_motion_cut_lower < observations["Obj_Sun_LTC_km"]>sconfigs.linkingfilter.ssp_motion_cut_upper]


    for object in observations["ObjID"].unique():
        obj = observations[observations["ObjID"] == object]

        if obj["Obj_Sun_LTC_km"]> 50 :
            window = 90
        if  obj["Obj_Sun_LTC_km"]< 50 :
            window = 60
        if arccut(obj) and triplet(obj,window):
            discoveried_index = 
    
    return discoveried_index

def arccut(obj):
    if abs(obj["mjd"][-2] - obj["mjd"][0]) > 6 and abs(obj["mjd"][-1] - obj["mjd"][1]) > 6:
        return True
    else: 
        return False
    

def triplet(obj,window):
    for n in np.arange(1, len(obj)):
        if abs(obj["mjd"][n]- obj["mjd"][n+1]) < window and abs(obj["mjd"][n+2]- obj["mjd"][n+1]) < window :
            continue
        else:
            return False
    return True