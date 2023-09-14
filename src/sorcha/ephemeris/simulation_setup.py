from functools import partial
import spiceypy as spice
from assist import Ephem
from . import simulation_parsing as sp
import rebound
from collections import defaultdict
import assist
import logging
import sys

from sorcha.ephemeris.simulation_constants import *
from sorcha.ephemeris.simulation_data_files import (
    make_retriever,
    JPL_PLANETS,
    JPL_SMALL_BODIES,
    META_KERNEL,
    ORDERED_KERNEL_FILES,
)

from sorcha.ephemeris.simulation_geometry import (
    barycentricObservatoryRates,
    get_hp_neighbors,
    ra_dec2vec,
)
from sorcha.ephemeris.simulation_parsing import (
    Observatory,
    mjd_tai_to_epoch,
)


def create_assist_ephemeris(args) -> tuple:
    """Build the ASSIST ephemeris object

    Returns
    -------
    Ephem, gm_sun
        The ASSIST ephemeris object
    """
    pplogger = logging.getLogger(__name__)

    retriever = make_retriever(args.ar_data_file_path)
    planets_file_path = retriever.fetch(JPL_PLANETS)
    small_bodies_file_path = retriever.fetch(JPL_SMALL_BODIES)
    ephem = Ephem(planets_path=planets_file_path, asteroids_path=small_bodies_file_path)
    gm_sun = ephem.get_particle("Sun", 0).m

    pplogger.info(f"Calculated GM_SUN value from ASSIST ephemeris: {gm_sun}")

    return ephem, gm_sun


def furnish_spiceypy(args):
    # The goal here would be to download the spice kernel files (if needed)
    # Then call spice.furnish(<filename>) on each of those files.

    pplogger = logging.getLogger(__name__)

    retriever = make_retriever(args.ar_data_file_path)

    for kernel_file in ORDERED_KERNEL_FILES:
        retriever.fetch(kernel_file)

    # TODO: The previous line will fetch all the remote kernel files if they are
    # not present on the local machine, however, it does not create the META_KERNEL
    # file needed in the next line. We should abstract the creation of the META_KERNEL
    # to a separate utility function that can be called here as needed.

    try:
        meta_kernel = retriever.fetch(META_KERNEL)
    except ValueError:
        pplogger.error(
            "ERROR: furnish_spiceypy: Must create meta_kernel.txt by running `bootstrap_sorcha_data_files` on the command line."
        )
        sys.exit(
            "ERROR: furnish_spiceypy: Must create meta_kernel.txt by running `bootstrap_sorcha_data_files` on the command line."
        )

    spice.furnsh(meta_kernel)


def generate_simulations(ephem, gm_sun, orbits_df):
    sim_dict = defaultdict(dict)  # return

    sun_dict = dict()  # This could be passed in and reused
    for _, row in orbits_df.iterrows():
        epoch = row["epoch"]
        # convert from MJD to JD, if not done already.
        if epoch < 2400000.5:
            epoch += 2400000.5

        x, y, z, vx, vy, vz = sp.parse_orbit_row(row, epoch, ephem, sun_dict, gm_sun)

        # Instantiate a rebound particle
        ic = rebound.Particle(x=x, y=y, z=z, vx=vx, vy=vy, vz=vz)

        # Instantiate a rebound simulation and set initial time and time step
        # The time step is just a guess to start with.
        sim = rebound.Simulation()
        sim.t = epoch - ephem.jd_ref
        sim.dt = 10

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


def precompute_pointing_information(pointings_df, args, configs):
    """This function is meant to be run once to prime the pointings dataframe
    with additional information that Assist & Rebound needs for it's work.

    Parameters
    ----------
    pointings_df : pd.dataframe
        Contains the telescope pointing database.
    args : dict
        Command line arguments needed for initialization.
    configs : dict
        Configuration settings.

    Returns
    -------
    pointings_df : pd.dataframe
        The original dataframe with several additional columns of precomputed values.
    """
    ephem, _ = create_assist_ephemeris(args)

    furnish_spiceypy(args)
    obsCode = configs["ar_obs_code"]
    observatories = Observatory(args)

    # vectorize the calculation to get x,y,z vector from ra/dec
    vectors = ra_dec2vec(pointings_df["fieldRA"].astype("float"), pointings_df["fieldDec"].astype("float"))
    pointings_df["visit_vector"] = vectors.tolist()

    # use pandas `apply` (even though it's slow) instead of looping over the df in a for loop
    pointings_df["jd_tdb"] = pointings_df.apply(
        lambda row: mjd_tai_to_epoch(row["observationStartMJD"]), axis=1
    )
    et = (pointings_df["jd_tdb"] - spice.j2000()) * 24 * 60 * 60

    # create a partial function since most params don't change, and it makes the lambda easier to read
    partial_get_hp_neighbors = partial(
        get_hp_neighbors,
        search_radius=configs["ar_ang_fov"] + configs["ar_fov_buffer"],
        nside=2 ** configs["ar_healpix_order"],
        nested=True,
    )

    # use pandas `apply` again because healpy.query_disc is not easily vectorizable
    pointings_df["pixels"] = pointings_df.apply(
        lambda row: partial_get_hp_neighbors(ra_c=float(row["fieldRA"]), dec_c=float(row["fieldDec"])),
        axis=1,
    )

    # create empty arrays for observatory position and velocity to be filled in
    r_obs = np.empty((len(pointings_df), 3))
    v_obs = np.empty((len(pointings_df), 3))

    for idx, et_i in enumerate(et):
        r_obs[idx], v_obs[idx] = barycentricObservatoryRates(et_i, obsCode, observatories=observatories)

    r_obs /= AU_KM  # convert to au
    v_obs *= (24 * 60 * 60) / AU_KM  # convert to au/day

    pointings_df["r_obs"] = r_obs.tolist()
    pointings_df["v_obs"] = v_obs.tolist()

    # create empty arrays for sun position and velocity to be filled in
    r_sun = np.empty((len(pointings_df), 3))
    v_sun = np.empty((len(pointings_df), 3))
    time_offsets = pointings_df["jd_tdb"] - ephem.jd_ref
    for idx, time_offset_i in enumerate(time_offsets):
        sun = ephem.get_particle("Sun", time_offset_i)
        r_sun[idx] = np.array((sun.x, sun.y, sun.z))
        v_sun[idx] = np.array((sun.vx, sun.vy, sun.vz))

    pointings_df["r_sun"] = r_sun.tolist()
    pointings_df["v_sun"] = v_sun.tolist()

    spice.kclear()
    return pointings_df
