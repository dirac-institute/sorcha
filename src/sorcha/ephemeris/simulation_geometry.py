import healpy as hp
import numpy as np
from sorcha.ephemeris.simulation_constants import speed_of_light

ecl = (84381.4118*(1./3600)*np.pi/180.) # Obliquity of ecliptic at J2000

# This rotates from equatorial to ecliptic
def rotate_matrix(ecl):
    ce = np.cos(ecl)
    se = np.sin(-ecl)
    rotmat = np.array([[1.0, 0.0, 0.0],
                       [0.0,  ce,  se],
                       [0.0, -se,  ce]])
    return rotmat

rot_mat = rotate_matrix(-ecl)
def ecliptic_to_equatorial(v, rot_mat=rot_mat.T):
    return np.dot(v, rot_mat.T)

def integrate_light_time(sim, ex, t, r_obs, lt0=0, iter=3, speed_of_light=speed_of_light):
    lt=lt0
    for i in range(iter):
        ex.integrate_or_interpolate(t-lt)
        target = np.array(sim.particles[0].xyz)
        rho = target-r_obs
        rho_mag = np.linalg.norm(rho)
        lt = rho_mag/speed_of_light
        
    return rho, rho_mag, lt

def get_hp_neighbors(ra_c, dec_c, search_radius, nside=32, nested=True):
    
    sr = search_radius * np.pi/180.0
    phi_c   = ra_c * np.pi / 180.
    theta_c = np.pi / 2.0 - dec_c * np.pi / 180.

    vec = hp.ang2vec(theta_c, phi_c)
    res = hp.query_disc(nside, vec, sr, nest=nested, inclusive=True)
    
    return res

# TODO: Can this be replaced with healpy's `ang2vec`?
def ra_dec2vec(ra, dec):
    radeg=180./np.pi
    x = np.cos(ra/radeg)*np.cos(dec/radeg)
    y = np.sin(ra/radeg)*np.cos(dec/radeg)
    z = np.sin(dec/radeg)
    return np.array((x,y,z)).T