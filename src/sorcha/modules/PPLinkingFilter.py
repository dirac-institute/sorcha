import pandas as pd
import numpy as np

# from difi.metrics import NightlyLinkagesMetric


def PPLinkingFilter_OLD(
    observations,
    detection_efficiency,
    min_observations,
    min_tracklets,
    tracklet_interval,
    minimum_separation,
    maximum_time,
    survey_name="lsst",
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
    Currently only accepts "lsst", "LSST".

    Returns:
    -----------
    observations_out (pandas dataframe): a pandas dataframe containing observations
    of linked objects only.

    """

    # we need to take into account timezones when we determine whether an observation
    # occurs on a specific night. this is implemented via survey_name
    # i.e. LSST is on Chile time.
    # we then calculate the boundary time between one night and the next in UTC MJD.

    if survey_name in ["lsst", "LSST"]:
        UTC_night_boundary = 17.0 / 24.0  # this corresponds to 5pm UTC, or 2pm Chile time.

    # calculate night number from FieldMJD_TAI
    first_day = np.min(observations["FieldMJD_TAI"].values)
    observations["night"] = (
        np.floor(observations["FieldMJD_TAI"].values - np.floor(first_day) + UTC_night_boundary).astype(int)
        + 1
    )

    # create a small dataframe for difi to work on with only the relevant columns

    difi_dataframe = pd.DataFrame(
        {
            "object_id": observations["ObjID"].astype(object),
            "obs_id": observations["FieldID"],
            "time": observations["FieldMJD_TAI"],
            "night": observations["night"],
            "ra": observations["AstRA(deg)"],
            "dec": observations["AstDec(deg)"],
        }
    )

    metric = NightlyLinkagesMetric(
        linkage_min_obs=min_observations,  # min observations per tracklet
        max_obs_separation=maximum_time,  # maximum time separation between subsequent observations in a tracklet [days]
        min_linkage_nights=min_tracklets,  # minimum number of nights on which a tracklet must be detected
        min_obs_angular_separation=minimum_separation,  # minimum angular separation between observations in a tracklet [arcseconds]
    )

    findable, _ = metric.run(
        difi_dataframe,
        detection_window=tracklet_interval,  # number of nights in a rolling detection window
        min_window_nights=min_tracklets,  # minimum size of a window as the rolling window is moved
        by_object=True,  # split observations by object instead of by window [set to True if you want ignore_after_discovery=True]
        discovery_probability=detection_efficiency,  # probability of discovery for any discovery chance
        num_jobs=1,  # number of parallel jobs
        ignore_after_discovery=True,  # ignore observations of an object after it has been discovered
    )

    linked_object_observations = observations[observations["ObjID"].isin(findable["object_id"])]

    return linked_object_observations


def PPLinkingFilter(
    observations,
    detection_efficiency,
    min_observations,
    min_tracklets,
    tracklet_interval,
    minimum_separation,
    maximum_time,
    survey_name="lsst",
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
    Currently only accepts "lsst", "LSST".

    Returns:
    -----------
    observations_out (pandas dataframe): a pandas dataframe containing observations
    of linked objects only.

    """

    # create the ndarray that the linker expects
    from sorcha.modules.miniDifi import linkObservations

    obsv = pd.DataFrame(
        {
            "ssObjectId": observations["ObjID"],
            "diaSourceId": observations["FieldID"],
            "midPointTai": observations["FieldMJD_TAI"],
            "ra": observations["AstRA(deg)"],
            "decl": observations["AstDec(deg)"],
        }
    )
    nameLen = obsv["ssObjectId"].str.len().max()
    obsv = obsv.to_records(
        index=False,
        column_dtypes=dict(ssObjectId=f"a{nameLen}", diaSourceId="u8", midPointTai="f8", ra="f8", decl="f8"),
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
    )

    # unpack the results and filter the observations
    objs_found = obj["ssObjectId"][~np.isnan(obj["discoverySubmissionDate"])]
    obsv_found = np.isin(obsv["ssObjectId"], objs_found)
    linked_object_observations = observations.iloc[obsv_found]

    return linked_object_observations
