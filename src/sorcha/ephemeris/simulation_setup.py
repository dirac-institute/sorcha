import spiceypy as spice
from assist import Ephem
from . import simulation_parsing as sp
import rebound
from collections import defaultdict
import assist
import logging
import sys

from sorcha.ephemeris.simulation_data_files import (
    make_retriever,
    JPL_PLANETS,
    JPL_SMALL_BODIES,
    META_KERNEL,
    ORDERED_KERNEL_FILES,
)


def create_assist_ephemeris(args) -> Ephem:
    """Build the ASSIST ephemeris object

    Returns
    -------
    Ephem
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
