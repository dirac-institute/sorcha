import numpy as np
import astropy.units as u


def des_distance_cut(observations, distance_upper, distance_lower):
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
    distance = np.sqrt(
        observations["Obj_Sun_x_LTC_km"].values ** 2
        + observations["Obj_Sun_y_LTC_km"].values ** 2
        + observations["Obj_Sun_z_LTC_km"].values ** 2
    )
    distance_upper = (distance_upper * u.au).to(u.km).value
    distance_lower = (distance_lower * u.au).to(u.km).value
    observations = observations.drop(
        observations[~((distance < distance_upper) & (distance > distance_lower))].index
    )
    return observations


def des_motion_cut(observations, motion_upper, motion_lower):
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

    motion = np.sqrt(observations["RARateCosDec_deg_day"] ** 2 + observations["DecRate_deg_day"] ** 2)
    observations = observations.drop(observations[~((motion < motion_upper) & (motion > motion_lower))].index)
    return observations
