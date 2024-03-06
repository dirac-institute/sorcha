import numpy as np
import healpy as hp
import numba

from collections import defaultdict

from sorcha.ephemeris.simulation_geometry import *
from sorcha.ephemeris.simulation_constants import *


@numba.njit(fastmath=True)
def lagrange3(t0, t1, t2, t):
    """Calculate the coefficients for
    second-order Lagrange interpolation
    for measured points at times t0, t1,
    and t2 and for an array of times t.

    These coefficients can be reused for
    any number of input vectors.
    """
    L0 = (t - t1) * (t - t2) / ((t0 - t1) * (t0 - t2))
    L1 = (t - t0) * (t - t2) / ((t1 - t0) * (t1 - t2))
    L2 = (t - t0) * (t - t1) / ((t2 - t0) * (t2 - t1))
    return L0, L1, L2


def get_hp_neighbors(ra_c, dec_c, search_radius, nside=32, nested=True):
    sr = search_radius * np.pi / 180.0
    phi_c = ra_c * np.pi / 180.0
    theta_c = np.pi / 2.0 - dec_c * np.pi / 180.0

    vec = hp.ang2vec(theta_c, phi_c)
    res = hp.query_disc(nside, vec, sr, nest=nested, inclusive=True)

    return res


class PixelDict:
    def __init__(
        self,
        jd_tdb,
        sim_dict,
        ephem,
        obsCode,
        observatory,
        picket_interval=1.0,
        nside=128,
        nested=True,
        n_sub_intervals=101,
    ):
        self.nside = nside
        self.picket_interval = picket_interval
        self.n_sub_intervals = n_sub_intervals
        self.obsCode = obsCode
        self.nested = nested
        self.sim_dict = sim_dict
        self.ephem = ephem
        self.observatory = observatory

        # Set the three times and compute the observatory position
        # at those times
        # Using a quadratic isn't very general, but that can be
        # improved later

        self.t0 = jd_tdb
        self.r_obs_0 = self.get_observatory_position(self.t0)

        self.tp = self.t0 + picket_interval
        self.r_obs_p = self.get_observatory_position(self.tp)

        self.tm = self.t0 - picket_interval
        self.r_obs_m = self.get_observatory_position(self.tm)

        # Initialize the dictionary of positions

        self.pixel_dict = defaultdict(list)

        self.rho_hat_m_dict = self.get_all_object_unit_vectors(self.r_obs_m, self.tm)
        self.rho_hat_0_dict = self.get_all_object_unit_vectors(self.r_obs_0, self.t0)
        self.rho_hat_p_dict = self.get_all_object_unit_vectors(self.r_obs_p, self.tp)

        self.compute_pixel_traversed()

    def get_observatory_position(self, t):
        et = (t - spice.j2000()) * 24 * 60 * 60
        r_obs = self.observatory.barycentricObservatory(et, self.obsCode) / AU_KM
        return r_obs

    def get_object_unit_vectors(self, desigs, r_obs, t, lt0=0.01):
        rho_hat_dict = {}
        for k in desigs:
            v = self.sim_dict[k]
            sim, ex = v["sim"], v["ex"]

            # Get the topocentric unit vectors
            rho, rho_mag, lt, r_ast, v_ast = integrate_light_time(
                sim, ex, t - self.ephem.jd_ref, r_obs, lt0=lt0
            )
            rho_hat = rho / rho_mag
            rho_hat_dict[k] = rho_hat
        return rho_hat_dict

    def get_all_object_unit_vectors(self, r_obs, t, lt0=0.01):
        desigs = self.sim_dict.keys()
        return self.get_object_unit_vectors(desigs, r_obs, t, lt0=lt0)

    def get_interp_factors(self, tm, t0, tp, n_sub_intervals):
        times = np.linspace(tm, tp, n_sub_intervals)
        Lm, L0, Lp = lagrange3(tm, t0, tp, times)
        Lm = Lm[:, np.newaxis]
        L0 = L0[:, np.newaxis]
        Lp = Lp[:, np.newaxis]
        return Lm, L0, Lp

    def interpolate_unit_vectors(self, desigs, jd_tdb):
        # Update the table of unit vectors if needed.
        # Should not normally need to, if this routine is being
        # called properly
        self.update_pickets(jd_tdb)

        Lm, L0, Lp = lagrange3(self.tm, self.t0, self.tp, jd_tdb)

        unit_vector_dict = {}

        for k in desigs:
            rho_hat_m = self.rho_hat_m_dict[k]
            rho_hat_0 = self.rho_hat_0_dict[k]
            rho_hat_p = self.rho_hat_p_dict[k]

            # Interpolate the unit vectors over a finer sampled set of times
            vec = rho_hat_m * Lm + rho_hat_0 * L0 + rho_hat_p * Lp

            unit_vector_dict[k] = vec

        return unit_vector_dict

    def compute_pixel_traversed(self):
        # These don't need to be recomputed, if the interval stays the same
        Lm, L0, Lp = self.get_interp_factors(self.tm, self.t0, self.tp, self.n_sub_intervals)

        self.pixel_dict = defaultdict(list)

        for k, v in self.sim_dict.items():
            rho_hat_m = self.rho_hat_m_dict[k]
            rho_hat_0 = self.rho_hat_0_dict[k]
            rho_hat_p = self.rho_hat_p_dict[k]

            # Interpolate the unit vectors over a finer sampled set of times
            vec = rho_hat_m * Lm + rho_hat_0 * L0 + rho_hat_p * Lp

            # Find the healpix locations
            pixels = hp.vec2pix(self.nside, vec[:, 0], vec[:, 1], vec[:, 2], nest=self.nested)
            pixels = list(set(pixels))

            # Add the neighboring pixels
            pixels = set(hp.get_all_neighbours(self.nside, pixels, nest=self.nested).flatten())

            # Add the pixels that the object traverse, and the neighbors, to the pixel_dict
            for pix in pixels:
                self.pixel_dict[pix].append(k)

    def update_pickets(self, jd_tdb):
        if abs(jd_tdb - self.t0) > 0.5 * self.picket_interval:
            # Need to update
            if abs(jd_tdb - self.t0) <= 1.5 * self.picket_interval:
                # Can compute just one new set and shift the others

                if jd_tdb <= self.tm:
                    # shift earlier
                    self.tp = self.t0
                    self.r_obs_p = self.r_obs_0
                    self.rho_hat_p_dict = self.rho_hat_0_dict

                    self.t0 = self.tm
                    self.r_obs_0 = self.r_obs_m
                    self.rho_hat_0_dict = self.rho_hat_m_dict

                    self.tm = self.t0 - self.picket_interval
                    self.r_obs_m = self.get_observatory_position(self.tm)
                    self.rho_hat_m_dict = self.get_all_object_unit_vectors(self.r_obs_m, self.tm)

                else:
                    # shift later
                    self.tm = self.t0
                    self.r_obs_m = self.r_obs_0
                    self.rho_hat_m_dict = self.rho_hat_0_dict

                    self.t0 = self.tp
                    self.r_obs_0 = self.r_obs_p
                    self.rho_hat_0_dict = self.rho_hat_p_dict

                    self.tp = self.t0 + self.picket_interval
                    self.r_obs_p = self.get_observatory_position(self.tp)
                    self.rho_hat_p_dict = self.get_all_object_unit_vectors(self.r_obs_p, self.tp)

            else:
                # Need to compute three new sets
                n = round((jd_tdb - self.t0) / self.picket_interval)

                # This is repeated code
                self.t0 += n * self.picket_interval
                self.r_obs_0 = self.get_observatory_position(self.t0)
                self.rho_hat_0_dict = self.get_all_object_unit_vectors(self.r_obs_0, self.t0)

                self.tp = self.t0 + self.picket_interval
                self.r_obs_p = self.get_observatory_position(self.tp)
                self.rho_hat_p_dict = self.get_all_object_unit_vectors(self.r_obs_p, self.tp)

                self.tm = self.t0 - self.picket_interval
                self.r_obs_m = self.get_observatory_position(self.tm)
                self.rho_hat_m_dict = self.get_all_object_unit_vectors(self.r_obs_m, self.tm)

            self.compute_pixel_traversed()
        else:
            pass

    # Get the designations that are within an angular radius of a topocentric unit vector at a
    # given time.
    def get_designations(self, jd_tdb, ra, dec, ang_fov):
        # Update the table of unit vectors if needed.
        self.update_pickets(jd_tdb)

        pixels = get_hp_neighbors(ra, dec, ang_fov, nside=self.nside, nested=self.nested)

        desigs = set()
        for pix in pixels:
            desigs.update(self.pixel_dict[pix])

        return desigs
