import pandas as pd
import numpy as np


def PPLinkingFilter(
    observations,
    detection_efficiency,
    min_observations,
    min_tracklets,
    tracklet_interval,
    minimum_separation,
    maximum_time,
    night_start_utc,
    survey_name="rubin_sim",
    drop_unlinked=True,
):
    """
    A function which mimics the effects of the SSP linking process by looking
    for valid tracklets within valid tracks and only outputting observations
    which would be thus successfully "linked" by SSP.

    Parameters:
    -----------
    detection_efficiency (float): the fractional percentage of successfully linked
    detections.

    min_observations (int): the minimum number of observations in a night required
    to form a tracklet.

    min_tracklets (int): the minimum number of tracklets required to form a valid track.

    tracklet_interval (int): the time window (in days) in which the minimum number of
    tracklets must occur to form a valid track.

    minimum_separation (float): the minimum separation inside a tracklet for it
    to be recognised as motion between images (in arcseconds).

    maximum_time (float): # Maximum time separation (in days) between subsequent observations in a tracklet.

    rng (numpy Generator object): numpy random number generator object.

    survey_name (str): a string with the survey name. used for time-zone purposes.
    Currently only accepts "rubin_sim", "RUBIN_SIM", "lsst", "LSST".

    drop_unlinked (boolean): rejects all observations that are considered to not be linked. Default is True

    Returns:
    -----------
    observations_out (pandas dataframe): a pandas dataframe containing observations
    of linked objects only.

    """

    # create the ndarray that the linker expects
    from sorcha.modules.PPMiniDifi import linkObservations

    obsv = pd.DataFrame(
        {
            "ssObjectId": observations["ObjID"],
            "diaSourceId": observations["FieldID"],
            "midPointTai": observations["fieldMJD_TAI"],
            "ra": observations["RA_deg"],
            "decl": observations["Dec_deg"],
        }
    )
    nameLen = obsv["ssObjectId"].str.len().max()
    obsv = obsv.to_records(
        index=False,
        column_dtypes=dict(ssObjectId=f"S{nameLen}", diaSourceId="u8", midPointTai="f8", ra="f8", decl="f8"),
    )

    # link
    obj = linkObservations(
        obsv,
        seed=0,
        objectId="ssObjectId",
        maxdt_minutes=maximum_time * 24 * 60,
        minlen_arcsec=minimum_separation,
        window=tracklet_interval,
        nlink=min_tracklets,
        p=detection_efficiency,
        night_start_utc_days=night_start_utc / 24.0,
    )

    # unpack the results and filter the observations
    objs_found = obj["ssObjectId"][~np.isnan(obj["discoverySubmissionDate"])]
    obsv_found = np.isin(obsv["ssObjectId"], objs_found)
    observations["object_linked"] = obsv_found

    if drop_unlinked:
        linked_object_observations = observations.iloc[obsv_found]
    else:
        linked_object_observations = observations

    # adding discovery submission date
    obj_discovery = pd.DataFrame(
        {"ObjID": obj["ssObjectId"], "date_linked_MJD": obj["discoverySubmissionDate"]}
    )
    obj_discovery["ObjID"] = obj_discovery["ObjID"].str.decode("utf-8")
    linked_object_observations = pd.merge(linked_object_observations, obj_discovery, on="ObjID")
    linked_object_observations = linked_object_observations.sort_values("fieldMJD_TAI").reset_index(drop=True)

    return linked_object_observations
