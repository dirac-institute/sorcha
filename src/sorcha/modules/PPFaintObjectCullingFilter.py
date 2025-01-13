from sorcha.ephemeris.simulation_parsing import get_perihelion_row
from sorcha.lightcurves.lightcurve_registration import LC_METHODS
from sorcha.activity.activity_registration import CA_METHODS

from collections import namedtuple
import numpy as np
import pandas as pd


def PPFaintObjectCullingFilter(
    aux_df, filterpointing, mainfilter, observing_filters, lightcurve_choice, activity_choice
):
    """Performs a first pass over a dataframe of the orbits and physical parameters information
    to remove any objects that will definitely not be detected.

    It estimates the maximum apparent magnitude (at perihelion and max phase) of each object in each filter.
    If the object is never brighter in any filter than the limiting magnitude + 2 + any brightness added by sorcha-addons,
    then the object is dropped from the input dataframe.

    Parameters
    -----------
    aux_df : Pandas dataframe
        Dataframe of joined orbits and physical parameters from input files

    filterpointing : Pandas dataframe
        Dataframe of input pointing database.

    mainfilter : str
        String of filter in which H is supplied.

    observing_filters: list of str
        List of observation filters supplied by user.

    lightcurve_choice: None or str
        Name of lightcurve model, if using.

    activity_choice: None or str
        Name of activity model, if using.

    Returns
    --------
    Pandas dataframe
        aux_df with all objects deemed to be definitely unobservable removed.

    """

    # gets a dictionary of the maximum limiting magnitude in each filter
    max_five_sigma = (
        filterpointing.groupby("optFilter", observed=True)["fieldFiveSigmaDepth_mag"].max().to_dict()
    )

    if "q" not in aux_df.columns:
        aux_df["q"] = PPEstimatePerihelion(aux_df)

    # this only works if object perihelion
    aux_df_dropped = aux_df[aux_df["q"] >= 2]
    q = aux_df_dropped["q"]

    # rough estimation of object's distance from Earth
    estimated_geocentric = q - 1.0

    # there's a better way of doing this, I'm going to find it >:(
    # basically calculates apparent magnitude in every filter, then tracks
    # whether it's larger than the limiting magnitude in that filter
    drop_df = pd.DataFrame(aux_df_dropped["ObjID"])
    for filt in observing_filters:
        if filt == mainfilter:
            H = aux_df_dropped["H_" + mainfilter]
        else:
            H = (
                aux_df_dropped["H_" + mainfilter] + aux_df_dropped[f"{filt}-{mainfilter}"]
            )  # add the colour offset

        app_mag = H + (5.0 * np.log10(q)) + (5.0 * np.log10(estimated_geocentric))

        # we need to take into account that brightness may be added by
        # activity or light-curve subclasses
        if lightcurve_choice:
            lc_model = LC_METHODS.get(lightcurve_choice)()
            subclass_offset = lc_model.maxBrightness(aux_df_dropped)
            app_mag += subclass_offset

        if activity_choice:
            ca_model = CA_METHODS.get(activity_choice)()
            aux_df_dropped["trailedSourceMagTrue"] = (
                app_mag  # add some columns to comply with activity subclass functionality
            )
            aux_df_dropped["optFilter"] = filt
            app_mag = ca_model.maxBrightness(
                aux_df_dropped, [filt], q, q - 1.0, np.zeros(aux_df_dropped.shape[0])
            )

        # 2 is a fairly arbitrary value added to give a threshold
        drop_df[filt] = app_mag > max_five_sigma[filt] + 2

    # if the object's apparent magnitude fulfils the condition in the above loop for all filters, drop it
    objects_to_drop = drop_df.loc[drop_df[observing_filters].all(axis=1), "ObjID"].tolist()
    output = aux_df[~aux_df["ObjID"].isin(objects_to_drop)]

    return output


def PPEstimatePerihelion(aux_df):
    """Estimates perihelion for a dataframe of orbital data given in another format.

    Parameters
    -----------
    aux_df : Pandas dataframe
        Dataframe of joined orbits and physical parameters from input files

    Returns
    --------
    q : Pandas series
        Value of q for all rows in aux_df.

    """

    # values from the spice kernel - dec 13 2023
    # doesn't need to be precise, we're estimating
    gm_sun = 2.9591220828559115e-04
    gm_total = 2.9630927487993194e-04

    Sun = namedtuple("Sun", "x y z vx vy vz")

    # just assume heliocentric
    sun_epoch = Sun(x=0, y=0, z=0, vx=0, vy=0, vz=0)

    epochJD_TDB = aux_df["epochMJD_TDB"].iloc[0]  # what if the epoch is different for different objects?
    sun_dict = {epochJD_TDB: sun_epoch}

    q = aux_df.apply(
        lambda row: get_perihelion_row(row, epochJD_TDB, None, sun_dict, gm_sun, gm_total)[0], axis=1
    )

    return q
