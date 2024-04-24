import healpy as hp
import numpy as np
from sorcha.ephemeris.simulation_constants import (
    RADIUS_EARTH_KM,
    SPEED_OF_LIGHT,
    ECL_TO_EQ_ROTATION_MATRIX,
)
import spiceypy as spice


def ecliptic_to_equatorial(v, rot_mat=ECL_TO_EQ_ROTATION_MATRIX):
    return np.dot(v, rot_mat)


def integrate_light_time(sim, ex, t, r_obs, lt0=0, iter=3, speed_of_light=SPEED_OF_LIGHT):
    lt = lt0
    for i in range(iter):
        ex.integrate_or_interpolate(t - lt)
        target = np.array(sim.particles[0].xyz)
        vtarget = np.array(sim.particles[0].vxyz)
        rho = target - r_obs
        rho_mag = np.linalg.norm(rho)
        lt = rho_mag / speed_of_light
    # Compute a second value to get rates (need v_obs)
    return rho, rho_mag, lt, target, vtarget


def get_hp_neighbors(ra_c, dec_c, search_radius, nside=32, nested=True):
    sr = search_radius * np.pi / 180.0
    phi_c = ra_c * np.pi / 180.0
    theta_c = np.pi / 2.0 - dec_c * np.pi / 180.0

    vec = hp.ang2vec(theta_c, phi_c)
    res = hp.query_disc(nside, vec, sr, nest=nested, inclusive=True)

    return res


def ra_dec2vec(ra, dec):
    radeg = np.pi / 180.0
    x = np.cos(ra * radeg) * np.cos(dec * radeg)
    y = np.sin(ra * radeg) * np.cos(dec * radeg)
    z = np.sin(dec * radeg)
    return np.array((x, y, z)).T


def vec2ra_dec(vec):
    radeg = 180.0 / np.pi
    x = vec[0]
    y = vec[1]
    z = vec[2]
    ra = radeg * np.arctan2(y, x) % 360
    dec = radeg * np.arcsin(z)
    return ra, dec


def barycentricObservatoryRates(
    et, obsCode, observatories, Rearth=RADIUS_EARTH_KM, delta_et=10
):  # This JPL's quoted Earth radius (km)
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
