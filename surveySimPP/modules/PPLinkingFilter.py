#!/usr/bin/python

import pandas as pd
import numpy as np
from astropy import units as u
from astropy.coordinates import SkyCoord

from .PPDetectionEfficiency import PPDetectionEfficiency

# Author: Steph Merritt


def PPLinkingFilter(observations,
                       detection_efficiency,
                       min_observations,
                       min_tracklets,
                       tracklet_interval,
                       minimum_separation,
                       rng):
    """
    A function which mimics the effects of the SSP linking process by looking
    for valid tracklets within valid tracks and only outputting observations
    which would be thus successfully "linked" by SSP.

    Parameters:
    -----------
    detection_efficiency (float): the fractional percentage of successfully linked
                                  detections
    min_observations (int):       the minimum number of observations in a night required
                                  to form a tracklet
    min_tracklets (int):          the minimum number of tracklets required to
                                  form a valid track
    tracklet_interval (int):      the time window (in days) in which the minimum number of
                                  tracklets must occur to form a valid track
    minimum_separation (float):   the minimum separation inside a tracklet for it
                                  to be recognised as motion between images (in arcseconds)
    rng (numpy RNG object):       random number generator object


    Returns:
    -----------
    observations_out (pandas dataframe): a pandas dataframe containing observations
                                         of linked objects

    """

    # remove set percentage of entries at random based on linking efficiency
    observations_deteff = PPDetectionEfficiency(observations, detection_efficiency, rng)
    observations_deteff.reset_index(inplace=True, drop=True)

    # store original integer row indices as a column
    # could just use drop=False above but I wanted an unambiguous column name
    observations_deteff["original_index"] = np.arange(len(observations_deteff))

    # store copy of this original dataframe to select all valid observations from later
    # this is quicker than making a dataframe as we go, pd.concat() is slow
    orig_observations = observations_deteff.copy()
    final_idx = []

    objid_list = observations_deteff['ObjID'].unique().tolist()

    # calculate night number from FieldMJD (makes calculations easier)
    observations_deteff["night"] = np.round(observations_deteff["FieldMJD"].values - 60218.001806).astype(int)

    # this for-loop could possibly be avoided by using groupby().apply() but I suspect the
    # time saving would be negligible, .apply() is slow.
    for objID in objid_list:

        obs_object = observations_deteff.loc[observations_deteff['ObjID'] == objID]

        # get dataframe of night and number of observations per night
        obs_per_night_df = pd.DataFrame({"frequency": obs_object.value_counts("night", sort=False)})

        # merge, then drop observations where object was observed less than min_observations a night
        obs_freq = pd.merge(obs_object, obs_per_night_df, on="night")
        obs_above_min = obs_freq.loc[obs_freq["frequency"] >= min_observations]
        obs_above_min.reset_index(inplace=True, drop=True)

        # group this dataframe by night
        grouped_by_night = obs_above_min.groupby(['night'])

        # calculate separation between first and last observation of the night
        first_ra = grouped_by_night.head(1)["AstRA(deg)"].reset_index(drop=True).values
        last_ra = grouped_by_night.tail(1)["AstRA(deg)"].reset_index(drop=True).values
        first_dec = grouped_by_night.head(1)["AstDec(deg)"].reset_index(drop=True).values
        last_dec = grouped_by_night.tail(1)["AstDec(deg)"].reset_index(drop=True).values

        first_coord = SkyCoord(first_ra * u.degree, first_dec * u.degree)
        last_coord = SkyCoord(last_ra * u.degree, last_dec * u.degree)
        separation = first_coord.separation(last_coord).arcsecond

        separation_df = pd.DataFrame({'night': obs_above_min["night"].unique(), "separation": separation})

        # merge on and drop all observations where separation < minimum separation
        obs_sep = pd.merge(obs_above_min, separation_df, on="night")
        obs_above_min_sep = obs_sep.loc[obs_sep["separation"] >= minimum_separation]
        obs_above_min_sep.reset_index(inplace=True, drop=True)

        # quick check: if number of nights left is less than min_tracklets, skip this object
        # as there aren't enough tracklets to count as a full track
        if len(obs_above_min_sep["night"].unique()) < min_tracklets:
            continue

        unique_nights = obs_above_min_sep["night"].unique()
        valid = np.zeros(len(unique_nights), dtype=bool)

        # checks to see if a track containing a number of tracklets >= min_tracklets
        # exists in a window of days <= tracklet_interval.
        # assumes all observations in a night are part of a valid tracklet
        # which should be true at this point
        
        # once a linking is made, the night on which the linking was made is stored
        for i, night in enumerate(unique_nights):

            if i + min_tracklets - 1 >= len(unique_nights):
                break

            diff = unique_nights[i + min_tracklets - 1] - night

            if diff < tracklet_interval:
                linked_night = night
                break
        
        # get all observations of this object made on or after the night it was linked
        obs_final_night = obs_object[obs_object["night"]>=linked_night]

        # get the original index numbers of the observations that made it through
        # append them to the final index
        final_index = obs_final_night["original_index"].values
        final_idx.append(final_index.tolist())

    # flatten the final index
    flat_idx = [x for xs in final_idx for x in xs]

    # get the rows that survived the filter from the original observations dataframe
    final_observations = orig_observations[orig_observations.index.isin(flat_idx)]

    return final_observations
