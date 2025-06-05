import numpy as np
import astropy.units as u
import numba
import pandas as pd
from numba.typed import List

## filter for the DES object discovery requirements.
#    An ARCCUT limit (has to be at least 2 objects not in a triplet discovery season)
#    the observation of the discovery triplets have to be within 60/90 days (depending on distance) of eachother
#    compute_arccut and compute_triplet are from DESTNOSIM: https://github.com/bernardinelli/DESTNOSIM

bound = ((50 * u.au).to(u.km).value) ** 2  # square of the boundary 50au


def DESDiscoveryFilter(
    observations,
    objectId="ObjID",
    mjdTime="fieldMJD_TAI",
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
    observations : Pandas dataframe
        Modified 'observations' dataframe without observations that could not be observed.

    """
    # creating a numpy array of the obervations
    obsv = observations[[objectId, mjdTime, x_km, y_km, z_km]]  # new dataframe of reduced columns
    nameLen = obsv[objectId].str.len().max()  # allows strings in objectid to be fixed length for numby array
    obsv = obsv.to_records(
        index=False,
        column_dtypes=dict(objectId=f"S{nameLen}", midPointTai="f8", x_km="f8", y_km="f8", z_km="f8"),
    )  # converts pd.dataframe to numpy array

    i = np.argsort(obsv[objectId])  # index of objects sorted
    _, idx = np.unique(obsv[objectId][i], return_index=True)  # making an idx for each unique object

    splits = np.split(i, idx[1:])  # splitting the objects into their detections

    # creating a mask for dropping observations that dont meet requirments
    mask = np.zeros(len(obsv), dtype=bool)
    for obsv_indices in splits:  # loop for each object
        thisObsv = obsv[obsv_indices]
        # boundary condition for triplet detection (depends on minimum distance)
        distance_sq = np.min(thisObsv[x_km] ** 2 + thisObsv[y_km] ** 2 + thisObsv[z_km] ** 2)
        window = 90 if distance_sq >= bound else 60

        # sort the object's observations by time mjd
        i_times = np.argsort(thisObsv[mjdTime])
        thisObsv = thisObsv[i_times]

        # check cinditions are meet for detection.
        if compute_arccut(thisObsv[mjdTime]) and compute_triplet(thisObsv[mjdTime], window):
            mask[obsv_indices] = True

    observations = observations[mask]

    return observations.sort_values(mjdTime).reset_index(drop=True)


@numba.jit(
    "b1(f8[:])",
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

    return arccut > 0.5 * 365.25


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
