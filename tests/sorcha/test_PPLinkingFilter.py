import pandas as pd
import numpy as np

from sorcha.utilities.dataUtilitiesForTests import get_test_filepath


def test_PPLinkingFilter_window():
    from sorcha.modules.PPLinkingFilter import PPLinkingFilter

    min_observations = 2
    min_angular_separation = 0.5
    max_time_separation = 0.0625
    min_tracklets = 3
    min_tracklet_window = 15
    detection_efficiency = 1
    night_start_utc = 17.0

    # create object that should /not/ be linked not all tracklets are within
    # the window.
    obj_id = ["pretend_object"] * 6
    field_id = np.arange(1, 7)
    t0 = 60000.0
    times = np.asarray([0.03, 0.06, 5.03, 5.06, min_tracklet_window + 0.03, min_tracklet_window + 0.06]) + t0
    ra = [142, 142.1, 143, 143.1, 144, 144.1]
    dec = [8, 8.1, 9, 9.1, 10, 10.1]

    observations = pd.DataFrame(
        {"ObjID": obj_id, "FieldID": field_id, "fieldMJD_TAI": times, "RA_deg": ra, "Dec_deg": dec}
    )

    linked_observations = PPLinkingFilter(
        observations,
        detection_efficiency,
        min_observations,
        min_tracklets,
        min_tracklet_window,
        min_angular_separation,
        max_time_separation,
        night_start_utc,
    )
    assert len(linked_observations) == 0

    # now bring it into the linking window by changing the
    # time of the last tracklet, and verify it's successfully linked
    observations = pd.DataFrame(
        {"ObjID": obj_id, "FieldID": field_id, "fieldMJD_TAI": times, "RA_deg": ra, "Dec_deg": dec}
    )
    observations.loc[observations["fieldMJD_TAI"] > min_tracklet_window + t0, "fieldMJD_TAI"] -= 1.0

    linked_observations = PPLinkingFilter(
        observations,
        detection_efficiency,
        min_observations,
        min_tracklets,
        min_tracklet_window,
        min_angular_separation,
        max_time_separation,
        night_start_utc,
    )
    observations["date_linked_MJD"] = int(observations["fieldMJD_TAI"].max()) - 1.0

    pd.testing.assert_frame_equal(observations, linked_observations)


def test_PPLinkingFilter_discoveryChances():
    from sorcha.modules.PPMiniDifi import linkObservations

    # verify that the discoveryChances are computed correctly in case
    # such as this:
    #
    # Say our discovery window is 10, and the object has tracklets
    # at nights:
    #
    #    2 4 6 8
    #
    # This should generate the following discovery opportunities:
    #
    #    2 4 6
    #    2 4 6 8
    #      4 6 8
    #
    # (the last one appears because night=2 slides out of the discovery
    # window)

    min_observations = 2
    min_angular_separation = 0.5
    max_time_separation = 0.0625
    min_tracklets = 3
    min_tracklet_window = 10
    detection_efficiency = 1

    obj_id = ["pretend_object"] * 8
    field_id = np.arange(1, 9)
    t0 = 60000.0
    times = np.asarray([2.03, 2.06, 4.03, 4.06, 6.03, 6.06, 8.03, 8.06]) + t0
    ra = [142, 142.1, 143, 143.1, 144, 144.1, 144, 144.1]
    dec = [8, 8.1, 9, 9.1, 10, 10.1, 10, 10.1]
    obsv = pd.DataFrame(
        {"ssObjectId": obj_id, "diaSourceId": field_id, "midPointTai": times, "ra": ra, "decl": dec}
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
        maxdt_minutes=max_time_separation * 24 * 60,
        minlen_arcsec=min_angular_separation,
        window=min_tracklet_window,
        nlink=min_tracklets,
        p=detection_efficiency,
    )
    assert len(obj) == 1

    ssObjectId, discoveryObservationId, discoverySubmissionDate, discoveryChances = obj[0]
    assert discoveryChances == 3


def test_PPLinkingFilter_nlink1():
    from sorcha.modules.PPMiniDifi import linkObservations

    # verify that the special case of nlink=1 just returns the number
    # of nights with tracklets, irrespective of the window. We set up
    # a test case with four tracklets in a time-span slightly larger
    # than the linking window.
    min_observations = 2
    min_angular_separation = 0.5
    max_time_separation = 0.0625
    min_tracklets = 1
    min_tracklet_window = 15
    detection_efficiency = 1

    obj_id = ["pretend_object"] * 8
    field_id = np.arange(1, 9)
    t0 = 60000.0
    times = np.asarray([0.03, 0.06, 5.03, 5.06, 7.03, 7.06, 16.03, 16.06]) + t0
    ra = [142, 142.1, 143, 143.1, 144, 144.1, 144, 144.1]
    dec = [8, 8.1, 9, 9.1, 10, 10.1, 10, 10.1]
    obsv = pd.DataFrame(
        {"ssObjectId": obj_id, "diaSourceId": field_id, "midPointTai": times, "ra": ra, "decl": dec}
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
        maxdt_minutes=max_time_separation * 24 * 60,
        minlen_arcsec=min_angular_separation,
        window=min_tracklet_window,
        nlink=min_tracklets,
        p=detection_efficiency,
    )
    assert len(obj) == 1

    ssObjectId, discoveryObservationId, discoverySubmissionDate, discoveryChances = obj[0]
    assert discoveryChances == 4


def test_PPLinkingFilter():
    from sorcha.modules.PPLinkingFilter import PPLinkingFilter

    min_observations = 2
    min_angular_separation = 0.5
    max_time_separation = 0.0625
    min_tracklets = 3
    min_tracklet_window = 15
    detection_efficiency = 1
    night_start_utc = 17.0

    # create object that should definitely be linked
    obj_id = ["pretend_object"] * 6
    field_id = np.arange(1, 7)
    times = [60000.03, 60000.06, 60005.03, 60005.06, 60008.03, 60008.06]
    ra = [142, 142.1, 143, 143.1, 144, 144.1]
    dec = [8, 8.1, 9, 9.1, 10, 10.1]
    date = [60007.0] * 6

    observations = pd.DataFrame(
        {"ObjID": obj_id, "FieldID": field_id, "fieldMJD_TAI": times, "RA_deg": ra, "Dec_deg": dec}
    )

    linked_observations = PPLinkingFilter(
        observations,
        detection_efficiency,
        min_observations,
        min_tracklets,
        min_tracklet_window,
        min_angular_separation,
        max_time_separation,
        night_start_utc,
    )

    observations["date_linked_MJD"] = date

    pd.testing.assert_frame_equal(observations, linked_observations)

    # remove a tracklet
    observations_two_tracklets = observations.iloc[1:].copy()
    unlinked_observations_1 = PPLinkingFilter(
        observations_two_tracklets,
        detection_efficiency,
        min_observations,
        min_tracklets,
        min_tracklet_window,
        min_angular_separation,
        max_time_separation,
        night_start_utc,
    )
    assert len(unlinked_observations_1) == 0

    # put one tracklet outside of the track time window
    observations_large_window = observations.copy()
    observations_large_window["fieldMJD_TAI"] = [60000.03, 60000.06, 60005.03, 60005.06, 60016.03, 60016.06]
    unlinked_observations_2 = PPLinkingFilter(
        observations_large_window,
        detection_efficiency,
        min_observations,
        min_tracklets,
        min_tracklet_window,
        min_angular_separation,
        max_time_separation,
        night_start_utc,
    )
    assert len(unlinked_observations_2) == 0

    # move two observations too close together for a tracklet
    observations_small_sep = observations.copy()
    observations_small_sep["RA_deg"] = [142, 142.00001, 143, 143.1, 144, 144.1]
    observations_small_sep["Dec_deg"] = [8, 8.00001, 9, 9.1, 10, 10.1]
    unlinked_observations_3 = PPLinkingFilter(
        observations_small_sep,
        detection_efficiency,
        min_observations,
        min_tracklets,
        min_tracklet_window,
        min_angular_separation,
        max_time_separation,
        night_start_utc,
    )
    assert len(unlinked_observations_3) == 0

    # move two observations too far away in time for a tracklet
    observations_large_time = observations.copy()
    observations_large_time["fieldMJD_TAI"] = [60000.03, 60000.10, 60005.03, 60005.06, 60008.03, 60008.06]
    unlinked_observations_4 = PPLinkingFilter(
        observations_large_time,
        detection_efficiency,
        min_observations,
        min_tracklets,
        min_tracklet_window,
        min_angular_separation,
        max_time_separation,
        night_start_utc,
    )
    assert len(unlinked_observations_4) == 0

    # check detection efficiency
    detection_efficiency = 0.75

    # I'm only creating 1000 objects so the unit tests don't take a prohibitively long time
    nobjects = 5000
    objs = [["pretend_object_" + str(a)] * 6 for a in range(0, nobjects)]
    obj_id_long = [item for sublist in objs for item in sublist]
    field_id_long = list(np.arange(1, 7)) * nobjects
    times_long = [60000.03, 60000.06, 60005.03, 60005.06, 60008.03, 60008.06] * nobjects
    ra_long = np.asarray([142, 142.1, 143, 143.1, 144, 144.1] * nobjects)
    dec_long = np.asarray([8, 8.1, 9, 9.1, 10, 10.1] * nobjects)

    # mix in smallr random errors. This is needed as the mock linker
    # uses the randomness in the R.A. coordinate to deterministically
    # decide which observations to drop and which to keep to meet
    # the detection_efficiency target.
    np.random.seed(42)
    ra_long += np.random.uniform(size=len(ra_long)) / 3600.0 / 10.0
    dec_long += np.random.uniform(size=len(dec_long)) / 3600.0 / 10.0

    observations_long = pd.DataFrame(
        {
            "ObjID": obj_id_long,
            "FieldID": field_id_long,
            "fieldMJD_TAI": times_long,
            "RA_deg": ra_long,
            "Dec_deg": dec_long,
        }
    )

    long_linked_observations = PPLinkingFilter(
        observations_long,
        detection_efficiency,
        min_observations,
        min_tracklets,
        min_tracklet_window,
        min_angular_separation,
        max_time_separation,
        night_start_utc,
    )

    fraction_linked = len(long_linked_observations["ObjID"].unique()) / nobjects

    # check that the number of discoveries is in a 3-sigma confidence interval
    sigma = np.sqrt(nobjects) / nobjects
    resid_sigma = (fraction_linked - detection_efficiency) / sigma
    print(f"{sigma=} {fraction_linked=} {detection_efficiency=} {resid_sigma=}")

    assert -3 < resid_sigma < 3

    return


def test_PPLinkingFilter_nodrop():
    from sorcha.modules.PPLinkingFilter import PPLinkingFilter

    # testing to make sure we get the expected results when we don't drop unlinked objects
    min_observations = 2
    min_angular_separation = 0.5
    max_time_separation = 0.0625
    min_tracklets = 3
    min_tracklet_window = 15
    detection_efficiency = 1
    night_start_utc = 17.0

    # create object that should not be linked (see above tests)
    obj_id = ["unlinked_object"] * 6
    field_id = np.arange(1, 7)
    t0 = 60000.0
    times = np.asarray([0.03, 0.06, 5.03, 5.06, min_tracklet_window + 0.03, min_tracklet_window + 0.06]) + t0
    ra = [142, 142.1, 143, 143.1, 144, 144.1]
    dec = [8, 8.1, 9, 9.1, 10, 10.1]

    obsv_1 = pd.DataFrame(
        {"ObjID": obj_id, "FieldID": field_id, "fieldMJD_TAI": times, "RA_deg": ra, "Dec_deg": dec}
    )

    # and an object that should definitely be linked (see above tests)
    obj_id = ["linked_object"] * 6
    field_id = np.arange(7, 13)
    times = [60000.03, 60000.06, 60005.03, 60005.06, 60008.03, 60008.06]
    ra = [142, 142.1, 143, 143.1, 144, 144.1]
    dec = [8, 8.1, 9, 9.1, 10, 10.1]

    obsv_2 = pd.DataFrame(
        {"ObjID": obj_id, "FieldID": field_id, "fieldMJD_TAI": times, "RA_deg": ra, "Dec_deg": dec}
    )

    obsv = pd.concat([obsv_1, obsv_2])

    linked_observations = PPLinkingFilter(
        obsv,
        detection_efficiency,
        min_observations,
        min_tracklets,
        min_tracklet_window,
        min_angular_separation,
        max_time_separation,
        night_start_utc,
        drop_unlinked=False,
    )

    assert all(linked_observations[linked_observations["ObjID"] == "linked_object"]["object_linked"])
    assert all(~linked_observations[linked_observations["ObjID"] == "unlinked_object"]["object_linked"])
    assert len(linked_observations[linked_observations["ObjID"] == "linked_object"]) == 6
    assert len(linked_observations[linked_observations["ObjID"] == "unlinked_object"]) == 6
