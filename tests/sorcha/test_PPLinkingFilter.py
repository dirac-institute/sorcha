import pandas as pd
import numpy as np

from sorcha.utilities.dataUtilitiesForTests import get_test_filepath


def test_PPLinkingFilter():
    from sorcha.modules.PPLinkingFilter import PPLinkingFilter

    min_observations = 2
    min_angular_separation = 0.5
    max_time_separation = 0.0625
    min_tracklets = 3
    min_tracklet_window = 15
    detection_efficiency = 1

    # create object that should definitely be linked
    obj_id = ["pretend_object"] * 6
    field_id = np.arange(1, 7)
    times = [60000.03, 60000.06, 60005.03, 60005.06, 60008.03, 60008.06]
    ra = [142, 142.1, 143, 143.1, 144, 144.1]
    dec = [8, 8.1, 9, 9.1, 10, 10.1]

    observations = pd.DataFrame(
        {"ObjID": obj_id, "FieldID": field_id, "FieldMJD": times, "AstRA(deg)": ra, "AstDec(deg)": dec}
    )

    linked_observations = PPLinkingFilter(
        observations,
        detection_efficiency,
        min_observations,
        min_tracklets,
        min_tracklet_window,
        min_angular_separation,
        max_time_separation,
    )

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
    )
    assert len(unlinked_observations_1) == 0

    # put one tracklet outside of the track time window
    observations_large_window = observations.copy()
    observations_large_window["FieldMJD"] = [60000.03, 60000.06, 60005.03, 60005.06, 60016.03, 60016.06]
    unlinked_observations_2 = PPLinkingFilter(
        observations_large_window,
        detection_efficiency,
        min_observations,
        min_tracklets,
        min_tracklet_window,
        min_angular_separation,
        max_time_separation,
    )
    assert len(unlinked_observations_2) == 0

    # move two observations too close together for a tracklet
    observations_small_sep = observations.copy()
    observations_small_sep["AstRA(deg)"] = [142, 142.00001, 143, 143.1, 144, 144.1]
    observations_small_sep["AstDec(deg)"] = [8, 8.00001, 9, 9.1, 10, 10.1]
    unlinked_observations_3 = PPLinkingFilter(
        observations_small_sep,
        detection_efficiency,
        min_observations,
        min_tracklets,
        min_tracklet_window,
        min_angular_separation,
        max_time_separation,
    )
    assert len(unlinked_observations_3) == 0

    # move two observations too far away in time for a tracklet
    observations_large_time = observations.copy()
    observations_large_time["FieldMJD"] = [60000.03, 60000.10, 60005.03, 60005.06, 60008.03, 60008.06]
    unlinked_observations_4 = PPLinkingFilter(
        observations_large_time,
        detection_efficiency,
        min_observations,
        min_tracklets,
        min_tracklet_window,
        min_angular_separation,
        max_time_separation,
    )
    assert len(unlinked_observations_4) == 0

    # check detection efficiency
    detection_efficiency = 0.95

    # I'm only creating 100 objects so the unit tests don't take a prohibitively long time
    objs = [["pretend_object_" + str(a)] * 6 for a in range(0, 100)]
    obj_id_long = [item for sublist in objs for item in sublist]
    field_id_long = list(np.arange(1, 7)) * 100
    times_long = [60000.03, 60000.06, 60005.03, 60005.06, 60008.03, 60008.06] * 100
    ra_long = [142, 142.1, 143, 143.1, 144, 144.1] * 100
    dec_long = [8, 8.1, 9, 9.1, 10, 10.1] * 100

    observations_long = pd.DataFrame(
        {
            "ObjID": obj_id_long,
            "FieldID": field_id_long,
            "FieldMJD": times_long,
            "AstRA(deg)": ra_long,
            "AstDec(deg)": dec_long,
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
    )

    fraction_linked = len(long_linked_observations["ObjID"].unique()) / 100

    assert 0.92 < fraction_linked < 0.98

    return
