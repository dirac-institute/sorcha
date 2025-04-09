import numpy as np
import astropy.units as u


## filter for the DES object discovery requirements.
#    An ARCCUT limit (has to be at least 2 objects not in a triplet discovery season)
#    the observation of the discovery triplets have to be within 60/90 days (depending on distance) of eachother


def DESDiscoveryFilter(observations):
    discovered_indices = []

    for object in observations["ObjID"].unique():
        obj = observations[observations["ObjID"] == object]
        bound = (50 * u.au).to(u.km).value
        distance = np.sqrt(
            observations["Obj_Sun_x_LTC_km"].values ** 2
            + observations["Obj_Sun_y_LTC_km"].values ** 2
            + observations["Obj_Sun_z_LTC_km"].values ** 2
        )
        if all(distance >= bound):
            window = 90
        else:
            window = 60

        if not arccut(np.array(obj["fieldMJD_TAI"])):
            continue

        if not triplet(np.array(obj["fieldMJD_TAI"]), window):
            continue

        discovered_indices.extend(obj.index.tolist())
    observations = observations.iloc[discovered_indices].copy()

    observations = observations.sort_index()

    return observations


def arccut(obj):
    if abs(obj[-2] - obj[0]) > 0.5 * 365.25 and abs(obj[-1] - obj[1]) > 0.5 * 365.25:
        return True
    else:
        return False


def triplet(obj, window):
    flag = 0
    for n in np.arange(len(obj) - 2):
        if abs(obj[n] - obj[n + 1]) < window and abs(obj[n + 2] - obj[n + 1]) < window:
            flag = 1
            break
    if flag == 1:

        return True
    else:
        return False
