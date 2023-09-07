import numpy as np

RADIUS_EARTH_KM = 6378.137
AU_M = 149597870700
AU_KM = AU_M / 1000.0
SPEED_OF_LIGHT = 2.99792458e5 * 86400.0 / AU_KM
OBLIQUITY_ECLIPTIC = 84381.4118 * (1.0 / 3600) * np.pi / 180.0


def create_ecl_to_eq_rotation_matrix(ecl):
    """
    Creates a rotation matrix for transforming ecliptical coordinates
    to equatorial coordinates. A rotation matrix based on the solar
    system's ecliptic obliquity is already provided as
    `ECL_TO_EQ_ROTATION_MATRIX`.

    Parameters:
    -----------
    ecl (float): The ecliptical obliquity.

    Returns:
    -----------
    `numpy` array with shape (3,3).

    """
    ce = np.cos(-ecl)
    se = np.sin(ecl)
    rotmat = np.array([[1.0, 0.0, 0.0], [0.0, ce, se], [0.0, -se, ce]])
    return rotmat


ECL_TO_EQ_ROTATION_MATRIX = create_ecl_to_eq_rotation_matrix(OBLIQUITY_ECLIPTIC)
