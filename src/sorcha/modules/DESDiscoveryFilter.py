import numpy as np
import astropy.units as u
import numba

from numba.typed import List

## filter for the DES object discovery requirements.
#    An ARCCUT limit (has to be at least 2 objects not in a triplet discovery season)
#    the observation of the discovery triplets have to be within 60/90 days (depending on distance) of eachother
#    compute_arccut and compute_triplet are from DESTNOSIM: https://github.com/bernardinelli/DESTNOSIM

bound = ((50 * u.au).to(u.km).value) ** 2  # square of the boundary 50au


def DESDiscoveryFilter(
    observations,
    objectId="ObjID",
    mjdTime="midPointTai",
    x_km="Obj_Sun_x_LTC_km",
    y_km="Obj_Sun_y_LTC_km",
    z_km="Obj_Sun_z_LTC_km",
):
    """
    Filter for the DES object discovery requirements. This filter checks for an ARCCUT limit (has to be at least 2 objects not in a triplet discovery season) and 
    that the observation of the discovery triplets have to be within 60/90 days (depending on distance) of eachother.
    Parameters
    -----------

    observations : Pandas dataframe
        Dataframe of observations containing midPointTai and distance from Sun in cartesian co-ordinates.

    Returns
    ----------
    observations : Pandas dataframe)
        Modified 'observations' dataframe without observations that could not be observed.

    """

    discovered_indices = []
    i = np.argsort(observations[objectId]) # index of objects sorted  
    _ , idx = np.unique(observations[objectId][i], return_index=True) # making an idx for each unique object

    splits = np.split(i, idx[1:]) # splitting the objects into their detections 

    for _ , obsv_indices in enumerate(splits): # loop for each object
        thisObsv = observations[[objectId, mjdTime, x_km, y_km, z_km]][obsv_indices]
        thisObsv.dtype.names = [objectId, mjdTime, x_km, y_km, z_km]

        distance_sq = thisObsv[x_km] ** 2 + thisObsv[y_km] ** 2 + thisObsv[z_km] ** 2 # should i just calculate for one detection 
        if any(distance_sq >= bound):  # boundary condition for triplet detection (depends on distance)
            window = 90
        else:
            window = 60
        # sort the objects observations by time mjd
        i_times = np.argsort(thisObsv[mjdTime]) 
        thisObsv = thisObsv[i_times] 

        # check cinditions are meet for detection. 
        if not compute_arccut(thisObsv[mjdTime]) > 0.5 * 365.25 or not compute_triplet(
            thisObsv[mjdTime], window
        ):
            continue # if conditions are not met skip object

        discovered_indices.extend(obsv_indices)
    # return pandas dataframe of only the discovered objects
    observations = observations.iloc[discovered_indices].copy()

    observations = observations.sort_index()

    return observations


@numba.jit(
    "f8(f8[:])",
    nopython=True,
)
def compute_arccut(times):
    """
    Computes ARCCUT, the time between the first and last detection dropping one night of detection
    Arguments:
    - times: list of times, must be in DAYS
    """
    arccut = 0.0
    t1 = np.min(times)
    t2 = np.max(times)
    t1a = t2
    t2a = t1

    n = len(times)

    for i in range(n):
        if times[i] - t1 > 0.7 and times[i] < t1a:
            t1a = times[i]
        if t2 - times[i] > 0.7 and times[i] > t2a:
            t2a = times[i]

    arccut = min(t2 - t1a, t2a - t1)

    return arccut


@numba.jit(
    "b1(f8[:], f8)",
    nopython=True,
)
def compute_triplet(times, thresh):
    """
    Computes the time difference between triplets, returns if a triplet is formed

    Arguments:
    - times: list of times, must be in DAYS
    - thresh: threshold time for pairs
    """
    first_pair = 999.0
    second_pair = 999.0
    det = List()

    det.append(times[0])

    n = len(times)

    for i in range(n - 1):
        if times[i + 1] - times[i] > 0.4:
            det.append(times[i + 1])

    n = len(det)
    for i in range(1, n - 1):
        if det[i + 1] - det[i] < first_pair and det[i] - det[i - 1] < second_pair:
            first_pair = det[i + 1] - det[i]
            second_pair = det[i] - det[i - 1]

    if first_pair < thresh and second_pair < thresh:
        return True
    else:
        return False
