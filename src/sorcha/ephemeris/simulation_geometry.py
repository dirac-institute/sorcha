import healpy as hp
import numpy as np
import spiceypy as spice

from sorcha.ephemeris.simulation_constants import (
    ECL_TO_EQ_ROTATION_MATRIX,
    EQ_TO_ECL_ROTATION_MATRIX,
    RADIUS_EARTH_KM,
    SPEED_OF_LIGHT,
)


def ecliptic_to_equatorial(v, rot_mat=ECL_TO_EQ_ROTATION_MATRIX):
    """
    Converts an ecliptic-aligned vector to an equatorially-aligned vector

    Parameters
    ----------
    v: array (3 entries)
        vector
    rot_mat: 2D array (3x3 matrix)
        Rotation matrix. Default is the matrix that computes the ecliptic to equatorial conversion
    Returns
    -------
    v: array (3 entries)
        Rotated vector
    """
    return np.dot(v, rot_mat)


def equatorial_to_ecliptic(v, rot_mat=EQ_TO_ECL_ROTATION_MATRIX):
    """
    Converts an equatorially-aligned vector to an ecliptic-aligned vector

    Parameters
    ----------
    v: array (3 entries)
        vector
    rot_mat: 2D array (3x3 matrix)
        Rotation matrix. Default is the matrix that computes the equatorial to ecliptic conversion
    Returns
    -------
    v: array (3 entries)
        Rotated vector
    """
    return np.dot(v, rot_mat)


def integrate_light_time(sim, ex, t, r_obs, lt0=0, iter=3, speed_of_light=SPEED_OF_LIGHT, use_integrate=False):
    """
    Performs the light travel time correction between object and observatory iteratively for the object at a given reference time

    Parameters
    ----------
    sim: simulation
        Rebound simulation object
    ex: simulation extras
        ASSIST simulation extras
    t: float
        Target time
    r_obs: array (3 entries)
        Observatory position at time t
    lt0: float
        First guess for light travel time
    iter: int
        Number of iterations
    speed_of_light: float
        Speed of light for the calculation (default is SPEED_OF_LIGHT constant)
    Returns
    -------
    rho: array
        Object-observatory vector
    rho_mag: float
        Magnitude of rho vector
    lt: float
        Light travel time
    target: array
        Object position vector at t-lt
    vtarget: array
        Object velocity at t-lt
    """
    lt = lt0

    for i in range(iter):
        if use_integrate:
            sim.integrate(t - lt)
        else:
            ex.integrate_or_interpolate(t - lt)
        target = np.array(sim.particles[0].xyz)
        vtarget = np.array(sim.particles[0].vxyz)
        rho = target - r_obs
        rho_mag = np.linalg.norm(rho)
        lt = rho_mag / speed_of_light
    # Compute a second value to get rates (need v_obs)
    return rho, rho_mag, lt, target, vtarget


def get_hp_neighbors(ra_c, dec_c, search_radius, nside=32, nested=True):
    """
    Queries the healpix grid for pixels near the given RA/Dec with a given search radius

    Parameters
    ----------
    ra_c: float
        Target RA
    dec_c: float
        Target dec
    search_radius: float
        Radius for the query
    nside: int
        healpix nside
    nested: boolean
        Defines the ordering scheme for the healpix ordering. True (default) means a NESTED ordering
    Returns
    -------
    res: list
        List of healpix pixels
    """
    sr = search_radius * np.pi / 180.0
    phi_c = ra_c * np.pi / 180.0
    theta_c = np.pi / 2.0 - dec_c * np.pi / 180.0

    vec = hp.ang2vec(theta_c, phi_c)
    res = hp.query_disc(nside, vec, sr, nest=nested, inclusive=True)

    return res


def ra_dec2vec(ra, dec):
    """
    Converts a RA/Dec pair to a unit vector on the sphere
    Parameters
    ----------
    ra: float
        Target RA
    dec: float
        Target dec
    Returns
    -------
    : array
        Unit vector
    """
    radeg = np.pi / 180.0
    x = np.cos(ra * radeg) * np.cos(dec * radeg)
    y = np.sin(ra * radeg) * np.cos(dec * radeg)
    z = np.sin(dec * radeg)
    return np.array((x, y, z)).T


def vec2ra_dec(vec):
    """
    Decomposes a unit vector on the sphere into a RA/Dec pair
    Parameters
    ----------
    vec : array
        Unit vector
    Returns
    -------
    ra: float
        Target RA
    dec: float
        Target dec
    """
    radeg = 180.0 / np.pi
    x = vec[0]
    y = vec[1]
    z = vec[2]
    ra = radeg * np.arctan2(y, x) % 360
    dec = radeg * np.arcsin(z)
    return ra, dec


def barycentricObservatoryRates(et, obsCode, observatories, Rearth=RADIUS_EARTH_KM, delta_et=10):
    """
    Computes the position and rate of motion for the observatory in barycentric coordinates

    Parameters
    ----------
    et: float
        JPL ephemeris time
    obsCode: str
        MPC observatory code
    observatories: Observatory
        Observatory object with spherical representations for the obsCode
    Rearth: float
        Radius of the Earth (default is RADIUS_EARTH_KM)
    delta_et: float
        Difference in ephemeris time (in days) to derive the rotation matrix from the fixed Earth equatorial frame to J2000 (default: 10)
    Returns
    -------
     : array
        Position of the observatory (baricentric)
     : array
        Velocity of the observatory (baricentric)
    """
    # This JPL's quoted Earth radius (km)
    # et is JPL's internal time
    # Get the barycentric position of Earth
    posvel, _ = spice.spkezr("EARTH", et, "J2000", "NONE", "SSB")
    pos = posvel[0:3]
    vel = posvel[3:6]
    # Get the matrix that rotates from the Earth's equatorial body fixed frame to the J2000 equatorial frame.
    m = spice.pxform("ITRF93", "J2000", et)
    mp = spice.pxform("ITRF93", "J2000", et + delta_et)
    mm = spice.pxform("ITRF93", "J2000", et - delta_et)
    # Get the MPC's unit vector from the geocenter to
    # the observatory
    obsVec = observatories.ObservatoryXYZ[obsCode]
    obsVec = np.array(obsVec)
    # Carry out the rotation and scale
    mVec = np.dot(m, obsVec) * Rearth
    mVecp = np.dot(mp, obsVec) * Rearth
    mVecm = np.dot(mm, obsVec) * Rearth
    return pos + mVec, vel + (mVecp - mVecm) / (2 * delta_et)
