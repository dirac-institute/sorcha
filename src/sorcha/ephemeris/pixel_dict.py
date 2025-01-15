from collections import defaultdict

import healpy as hp
import numba
import numpy as np

from sorcha.ephemeris.simulation_constants import *
from sorcha.ephemeris.simulation_geometry import *


@numba.njit(fastmath=True)
def lagrange3(t0, t1, t2, t):
    """Calculate the coefficients for
    second-order Lagrange interpolation
    for measured points at times t0, t1,
    and t2 and for an array of times t.

    These coefficients can be reused for
    any number of input vectors.

    Parameters
    ----------
    t0 : float
        Time t0
    t1 : float
        Time t1
    t2 : float
        Time t2
    t : 1D array
        Times for the interpolation

    Returns
    -------
    L0 : 1D array
        interpolation coefficient at t0
    L1 : 1D array
        interpolation coefficient at t1
    L2 : 1D array
        interpolation coefficient at t2

    """
    L0 = (t - t1) * (t - t2) / ((t0 - t1) * (t0 - t2))
    L1 = (t - t0) * (t - t2) / ((t1 - t0) * (t1 - t2))
    L2 = (t - t0) * (t - t1) / ((t2 - t0) * (t2 - t1))
    return L0, L1, L2


class PixelDict:
    """
    Class with methods needed during the ephemerides generation
    Interfaces directly with the ASSIST+Rebound simulation objects as well as healpix
    """

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
        use_integrate=False,
    ):
        """
        Initialization function for the class. Computes the initial positions required for the ephemerides interpolation
        Parameters
        ----------
        jd_tdb: float
            Reference time for the initialization
        sim_dict: dictionary
            dictionary of ASSIST simulation objects
        ephem: Ephem
            ASSIST Ephem object
        obsCode: str
            MPC Observatory code
        observatories: Observatory
            Observatory object
        picket_interval : float
            The interval (days) between picket calculations.  This is 1 day
            by default
        nside : integer
            The nside value used for the HEALPIx calculations.  Must be a
            power of 2 (1, 2, 4, ...)  nside=128 is current default.
        nested: boolean
            Defines the ordering scheme for the healpix ordering. True (default) means a NESTED ordering
        n_sub_intervals: int
            Number of sub-intervals for the Lagrange interpolation (default: 101)
        use_integrate: boolean
            Whether to use the integrator to compute the ephemerides (default: False)
        """
        self.nside = nside
        self.picket_interval = picket_interval
        self.n_sub_intervals = n_sub_intervals
        self.obsCode = obsCode
        self.nested = nested
        self.sim_dict = sim_dict
        self.ephem = ephem
        self.observatory = observatory
        self.use_integrate = use_integrate
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

        self.rho_hat_m_dict = self.get_all_object_unit_vectors(self.r_obs_m, self.tm, use_integrate=self.use_integrate)
        self.rho_hat_0_dict = self.get_all_object_unit_vectors(self.r_obs_0, self.t0, use_integrate=self.use_integrate)
        self.rho_hat_p_dict = self.get_all_object_unit_vectors(self.r_obs_p, self.tp, use_integrate=self.use_integrate)

        self.compute_pixel_traversed()

    def get_observatory_position(self, t):
        """
        Computes the barycentric position of the observatory (in au)

        Parameters
        ----------
            t : float
                Epoch for the position vector
        Returns
        -------
            : array (3,)
                Barycentric position of the observatory (x,y,z)
        """
        et = (t - spice.j2000()) * 24 * 60 * 60
        r_obs = self.observatory.barycentricObservatory(et, self.obsCode) / AU_KM
        return r_obs

    def get_object_unit_vectors(self, desigs, r_obs, t, lt0=0.01, use_integrate=False):
        """
        Computes the unit vector (in the equatorial sphere) that point towards the object - observatory vector
        for a list of objects, at a given time

        Parameters
        ----------
        desigs: list
            List of designations (consistent with the simulation dictionary)
        r_obs: array (3 entries)
            Observatory location
        t: float
            Time of the observation
        lt0: float
            Initial guess (in days) for light-time correction (default: 0.01 days)
        Returns
        -------
        rho_hat_dict: dict
            Dictionary of unit vectors
        """
        rho_hat_dict = {}
        for k in desigs:
            v = self.sim_dict[k]
            sim, ex = v["sim"], v["ex"]

            # Get the topocentric unit vectors
            rho, rho_mag, lt, r_ast, v_ast = integrate_light_time(
                sim, ex, t - self.ephem.jd_ref, r_obs, lt0=lt0, use_integrate=use_integrate
            )
            rho_hat = rho / rho_mag
            rho_hat_dict[k] = rho_hat
        return rho_hat_dict

    def get_all_object_unit_vectors(self, r_obs, t, lt0=0.01, use_integrate=False):
        """
        Computes the unit vector (in the equatorial sphere) that point towards the object - observatory vector
        for *all* objects, at a given time

        Parameters
        ----------
        r_obs: array (3 entries)
            Observatory location
        t: float
            Time of the observation
        lt0: float
            Initial guess (in days) for light-time correction (default: 0.01 days)
        Returns
        -------
        rho_hat_dict: dict
            Dictionary of unit vectors
        """

        desigs = self.sim_dict.keys()
        return self.get_object_unit_vectors(desigs, r_obs, t, lt0=lt0, use_integrate=use_integrate)

    def get_interp_factors(self, tm, t0, tp, n_sub_intervals):
        """
        Computes the Lagrange interpolation factors at a set of 3 times for an
        equally spaced grid of points with a chosen number of sub-intervals
        Parameters
        ----------
        tm: float
            First reference time
        t0: float
            Second reference time
        tp: float
            Third reference time
        n_sub_intervals: int
            Number of sub-intervals for the Lagrange interpolation (default: 101)
        Returns
        -------
        Lm: 2D array
            Lagrange coefficients at tm
        L0: 2D array
            Lagrange coefficients at t0
        Lp: 2D array
            Lagrange coefficient at tp
        """
        times = np.linspace(tm, tp, n_sub_intervals)
        Lm, L0, Lp = lagrange3(tm, t0, tp, times)
        Lm = Lm[:, np.newaxis]
        L0 = L0[:, np.newaxis]
        Lp = Lp[:, np.newaxis]
        return Lm, L0, Lp

    def interpolate_unit_vectors(self, desigs, jd_tdb):
        """
        Interpolates the unit vectors for a list of designations towards the new target time

        Parameters
        ----------
        desigs: list
            List of designations (consistent with the simulation dictionary)
        jd_tdb: float
            Target time
        Returns
        -------
        unit_vector_dict: dict
            Dictionary of unit vectors
        """
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
        """
        Computes the healpix pixels traversed by all the objects during between times tm and tp
        """
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
        """
        Updates the picket interpolation vectors for the new reference time

        Parameters
        ----------
        jd_tdb: float
            Target time
        """
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
                    self.rho_hat_m_dict = self.get_all_object_unit_vectors(self.r_obs_m, self.tm, use_integrate=self.use_integrate)

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
                    self.rho_hat_p_dict = self.get_all_object_unit_vectors(self.r_obs_p, self.tp, use_integrate=self.use_integrate)

            else:
                # Need to compute three new sets
                n = round((jd_tdb - self.t0) / self.picket_interval)

                # This is repeated code
                self.t0 += n * self.picket_interval
                self.r_obs_0 = self.get_observatory_position(self.t0)
                self.rho_hat_0_dict = self.get_all_object_unit_vectors(self.r_obs_0, self.t0, use_integrate=self.use_integrate)

                self.tp = self.t0 + self.picket_interval
                self.r_obs_p = self.get_observatory_position(self.tp)
                self.rho_hat_p_dict = self.get_all_object_unit_vectors(self.r_obs_p, self.tp, use_integrate=self.use_integrate)

                self.tm = self.t0 - self.picket_interval
                self.r_obs_m = self.get_observatory_position(self.tm)
                self.rho_hat_m_dict = self.get_all_object_unit_vectors(self.r_obs_m, self.tm, use_integrate=self.use_integrate)

            self.compute_pixel_traversed()
        else:
            pass

    def get_designations(self, jd_tdb, ra, dec, ang_fov):
        """
        Get the object designations that are within an angular radius of a topocentric unit vector at a
        given time.

        Parameters
        ----------
        jd_tdb: float
            Target time
        ra: float
            right ascension (degrees)
        dec: float
            declination (degrees)
        ang_fov: float
            Field of view radius
        Returns
        -------
        desigs : list
            List of designations
        """
        # Update the table of unit vectors if needed.
        self.update_pickets(jd_tdb)

        pixels = get_hp_neighbors(ra, dec, ang_fov, nside=self.nside, nested=self.nested)

        desigs = set()
        for pix in pixels:
            desigs.update(self.pixel_dict[pix])

        return desigs
