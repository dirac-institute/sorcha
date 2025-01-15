import logging
import os
import sys
from collections import defaultdict
from functools import partial

import assist
import numpy as np
import rebound
import spiceypy as spice
from assist import Ephem

from sorcha.ephemeris.simulation_constants import *
from sorcha.ephemeris.simulation_data_files import make_retriever
from sorcha.ephemeris.simulation_geometry import (barycentricObservatoryRates,
                                                  get_hp_neighbors, ra_dec2vec)
from sorcha.ephemeris.simulation_parsing import Observatory, mjd_tai_to_epoch
from sorcha.utilities.generate_meta_kernel import build_meta_kernel_file

from . import simulation_parsing as sp


def create_assist_ephemeris(args, auxconfigs) -> tuple:
    """Build the ASSIST ephemeris object
    Parameter
    ---------
    auxconfigs: dataclass
        Dataclass of auxiliary configuration file arguments.
    Returns
    ---------
    Ephem : ASSIST ephemeris obejct
        The ASSIST ephemeris object
    gm_sun : float
        value for the GM_SUN value
    gm_total : float
        value for gm_total
    """
    pplogger = logging.getLogger(__name__)

    retriever = make_retriever(auxconfigs, args.ar_data_file_path)
    planets_file_path = retriever.fetch(auxconfigs.jpl_planets)
    small_bodies_file_path = retriever.fetch(auxconfigs.jpl_small_bodies)
    ephem = Ephem(planets_path=planets_file_path, asteroids_path=small_bodies_file_path)
    gm_sun = ephem.get_particle("Sun", 0).m
    gm_total = sum(sorted([ephem.get_particle(i, 0).m for i in range(27)]))

    pplogger.info(f"Calculated GM_SUN value from ASSIST ephemeris: {gm_sun}")
    pplogger.info(f"Calculated GM_TOTAL value from ASSIST ephemeris: {gm_total}")

    return ephem, gm_sun, gm_total


def furnish_spiceypy(args, auxconfigs):
    """
    Builds the SPICE kernel, downloading the required files if needed
    Parameters
    -----------
    auxconfigs: dataclass
        Dataclass of auxiliary configuration file arguments.
    """
    # The goal here would be to download the spice kernel files (if needed)
    # Then call spice.furnish(<filename>) on each of those files.

    pplogger = logging.getLogger(__name__)

    retriever = make_retriever(auxconfigs, args.ar_data_file_path)

    for kernel_file in auxconfigs.ordered_kernel_files:
        retriever.fetch(kernel_file)

    # check if the META_KERNEL file exists. If it doesn't exist, create it.
    if not os.path.exists(os.path.join(retriever.abspath, auxconfigs.meta_kernel)):
        build_meta_kernel_file(auxconfigs, retriever)

    # try to get the META_KERNEL file. If it's not there, error out.
    try:
        meta_kernel = retriever.fetch(auxconfigs.meta_kernel)
    except ValueError:
        pplogger.error(
            "ERROR: furnish_spiceypy: Must create meta_kernel.txt by running `bootstrap_sorcha_data_files` on the command line."
        )
        sys.exit(
            "ERROR: furnish_spiceypy: Must create meta_kernel.txt by running `bootstrap_sorcha_data_files` on the command line."
        )

    spice.furnsh(meta_kernel)


def generate_simulations(ephem, gm_sun, gm_total, orbits_df, args):
    """
    Creates the dictionary of ASSIST simulations for the ephemeris generation

    Parameters
    ------------
    ephem : Ephem
        The ASSIST ephemeris object
    gm_sun : float
        Standard gravitational parameter GM for the Sun
    gm_total : float
        Standard gravitational parameter GM for the Solar System barycenter
    orbits_df : dataframe
        Pandas dataframe with the input orbits
    args : dictionary or `sorchaArguments` object
        dictionary of command-line arguments.

    Returns
    ---------
    sim_dict : dict
        Dictionary of ASSIST simulations

    """
    sim_dict = defaultdict(dict)  # return

    sun_dict = dict()  # This could be passed in and reused
    for i, row in orbits_df.iterrows():
        epoch = row["epochMJD_TDB"]
        # convert from MJD to JD, if not done already.
        if epoch < 2400000.5:
            epoch += 2400000.5

        try:
            x, y, z, vx, vy, vz = sp.parse_orbit_row(row, epoch, ephem, sun_dict, gm_sun, gm_total)
            if np.isnan(x):
                args.pplogger.error(
                    f"Input elements for orbit {i} failed - see documentation for suggested solutions"
                )
                sys.exit(f"Input elements for orbit {i} failed - see documentation for suggested solutions")
        except ValueError as val_err:
            args.pplogger.error(val_err)
            sys.exit(val_err)

        # Instantiate a rebound particle
        ic = rebound.Particle(x=x, y=y, z=z, vx=vx, vy=vy, vz=vz)

        # Instantiate a rebound simulation and set initial time and time step
        # The time step is just a guess to start with.
        sim = rebound.Simulation()
        sim.t = epoch - ephem.jd_ref
        sim.dt = 10
        # This turns off the iterative timestep introduced in arXiv:2401.02849 and default since rebound 4.0.3
        sim.ri_ias15.adaptive_mode = 1
        # Add the particle to the simulation
        sim.add(ic)

        # Attach assist extras to the simulation
        ex = assist.Extras(sim, ephem)

        # Change the GR model for speed
        forces = ex.forces
        forces.remove("GR_EIH")
        forces.append("GR_SIMPLE")
        ex.forces = forces

        # Save the simulation in the dictionary
        sim_dict[row["ObjID"]]["sim"] = sim
        sim_dict[row["ObjID"]]["ex"] = ex

    return sim_dict


def precompute_pointing_information(pointings_df, args, sconfigs):
    """This function is meant to be run once to prime the pointings dataframe
    with additional information that Assist & Rebound needs for it's work.

    Parameters
    -----------
    pointings_df : pandas dataframe
        Contains the telescope pointing database.
    args : dictionary
        Command line arguments needed for initialization.
    sconfigs: dataclass
        Dataclass of configuration file arguments.

    Returns
    --------
    pointings_df : pandas dataframe
        The original dataframe with several additional columns of precomputed values.
    """
    ephem, _, _ = create_assist_ephemeris(args, sconfigs.auxiliary)

    furnish_spiceypy(args, sconfigs.auxiliary)
    obsCode = sconfigs.simulation.ar_obs_code
    observatories = Observatory(args, sconfigs.auxiliary)

    # vectorize the calculation to get x,y,z vector from ra/dec
    vectors = ra_dec2vec(
        pointings_df["fieldRA_deg"].astype("float"), pointings_df["fieldDec_deg"].astype("float")
    )
    pointings_df["visit_vector_x"] = vectors[:, 0]
    pointings_df["visit_vector_y"] = vectors[:, 1]
    pointings_df["visit_vector_z"] = vectors[:, 2]

    # use pandas `apply` (even though it's slow) instead of looping over the df in a for loop
    pointings_df["fieldJD_TDB"] = pointings_df["observationMidpointMJD_TAI"].apply(mjd_tai_to_epoch)

    et = (pointings_df["fieldJD_TDB"] - spice.j2000()) * 24 * 60 * 60

    # create a partial function since most params don't change, and it makes the lambda easier to read
    partial_get_hp_neighbors = partial(
        get_hp_neighbors,
        search_radius=sconfigs.simulation.ar_ang_fov + sconfigs.simulation.ar_fov_buffer,
        nside=2**sconfigs.simulation.ar_healpix_order,
        nested=True,
    )

    # create empty arrays for observatory position and velocity to be filled in
    r_obs = np.empty((len(pointings_df), 3))
    v_obs = np.empty((len(pointings_df), 3))

    for idx, et_i in enumerate(et):
        r_obs[idx], v_obs[idx] = barycentricObservatoryRates(et_i, obsCode, observatories=observatories)

    r_obs /= AU_KM  # convert to au
    v_obs *= (24 * 60 * 60) / AU_KM  # convert to au/day

    pointings_df["r_obs_x"] = r_obs[:, 0]
    pointings_df["r_obs_y"] = r_obs[:, 1]
    pointings_df["r_obs_z"] = r_obs[:, 2]
    pointings_df["v_obs_x"] = v_obs[:, 0]
    pointings_df["v_obs_y"] = v_obs[:, 1]
    pointings_df["v_obs_z"] = v_obs[:, 2]

    # create empty arrays for sun position and velocity to be filled in
    r_sun = np.empty((len(pointings_df), 3))
    v_sun = np.empty((len(pointings_df), 3))
    time_offsets = pointings_df["fieldJD_TDB"] - ephem.jd_ref
    for idx, time_offset_i in enumerate(time_offsets):
        sun = ephem.get_particle("Sun", time_offset_i)
        r_sun[idx] = np.array((sun.x, sun.y, sun.z))
        v_sun[idx] = np.array((sun.vx, sun.vy, sun.vz))

    pointings_df["r_sun_x"] = r_sun[:, 0]
    pointings_df["r_sun_y"] = r_sun[:, 1]
    pointings_df["r_sun_z"] = r_sun[:, 2]
    pointings_df["v_sun_x"] = v_sun[:, 0]
    pointings_df["v_sun_y"] = v_sun[:, 1]
    pointings_df["v_sun_z"] = v_sun[:, 2]

    spice.kclear()
    return pointings_df
