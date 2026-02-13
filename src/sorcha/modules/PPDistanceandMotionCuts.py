import numpy as np
import astropy.units as u


def distance_cut(observations, distance_upper, distance_lower):
    """
    removes objects outside of distance range from Sun given

    Parameters
    -----------
    observations: pandas dataframe
      a pandas dataframe containing observations
    distance_upper: float
        upper distance limit to keep (au)
    distance_lower: float
        lower distance limit to keep (au)

    Returns
    -----------
    observations: pandas dataframe
      a pandas dataframe containing observations with distance cuts

    """

    distance_sq = (
        observations["Obj_Sun_x_LTC_km"].values ** 2
        + observations["Obj_Sun_y_LTC_km"].values ** 2
        + observations["Obj_Sun_z_LTC_km"].values ** 2
    )
    distance_upper = ((distance_upper * u.au).to(u.km).value) ** 2
    distance_lower = ((distance_lower * u.au).to(u.km).value) ** 2

    within_bounds = (distance_sq < distance_upper) & (distance_sq > distance_lower)

    objects_within_bounds = observations.loc[within_bounds, "ObjID"].unique()

    # Keep all detections for objects that have at least one detection within bounds
    observations = observations[observations["ObjID"].isin(objects_within_bounds)]

    return observations


def motion_cut(observations, motion_upper, motion_lower):
    """
    removes objects outside of motion range given

    Parameters
    -----------
    observations: pandas dataframe
      a pandas dataframe containing observations
    motion_upper: float
        upper motion limit to keep (deg/day)
    motion_lower: float
        lower motion limit to keep (deg/day)

    Returns
    -----------
    observations: pandas dataframe
      a pandas dataframe containing observations with motion cuts

    """

    motion_sq = observations["RARateCosDec_deg_day"] ** 2 + observations["DecRate_deg_day"] ** 2
    motion_upper = motion_upper**2
    motion_lower = motion_lower**2
    observations = observations.drop(
        observations[~((motion_sq < motion_upper) & (motion_sq > motion_lower))].index
    )
    return observations
