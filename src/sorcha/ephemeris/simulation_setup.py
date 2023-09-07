import spiceypy as spice
from assist import Ephem
from . import simulation_parsing as sp
import random
import rebound
from collections import defaultdict
import assist
import logging
import sys
from sorcha.readers.OrbitAuxReader import OrbitAuxReader

from sorcha.ephemeris.simulation_data_files import (
    make_retriever,
    JPL_PLANETS,
    JPL_SMALL_BODIES,
    META_KERNEL,
    ORDERED_KERNEL_FILES,
)


def create_assist_ephemeris() -> Ephem:
    """Build the ASSIST ephemeris object

    Returns
    -------
    Ephem
        The ASSIST ephemeris object
    """
    retriever = make_retriever()
    planets_file_path = retriever.fetch(JPL_PLANETS)
    small_bodies_file_path = retriever.fetch(JPL_SMALL_BODIES)
    ephem = Ephem(planets_path=planets_file_path, asteroids_path=small_bodies_file_path)
    gm_sun = ephem.get_particle("Sun", 0).m
    return ephem, gm_sun


def furnish_spiceypy():
    # The goal here would be to download the spice kernel files (if needed)
    # Then call spice.furnish(<filename>) on each of those files.
    # The hope is that automagically that will make properly furnished in
    # this namespace, and when we access it via `import spiceypy as spice`, that
    # we'll be able to work with it correctly.

    pplogger = logging.getLogger(__name__)

    retriever = make_retriever()

    for kernel_file in ORDERED_KERNEL_FILES:
        retriever.fetch(kernel_file)

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


def generate_simulations(ephem, gm_sun, args, configs):
    sim_dict = defaultdict(dict)  # return

    orbits_df = OrbitAuxReader(args.orbinfile, configs["aux_format"]).read_rows()
    orbit_format = orbits_df["FORMAT"].iloc[0]
    sun_dict = dict()  # This could be passed in and reused
    for index, row in orbits_df.iterrows():
        # desig, H, G, epoch, pos, vel = sp.convert_mpc_orbit(row, ephem, sun_dict)
        epoch = row["epoch"]
        # convert from MJD to JD, if not done already.
        if epoch < 2400000.5:
            epoch += 2400000.5

        x, y, z, vx, vy, vz = sp.parse_orbit_row(row, epoch, ephem, sun_dict, gm_sun)

        # Instantiate a rebound particle
        ic = rebound.Particle(x=x, y=y, z=z, vx=vx, vy=vy, vz=vz)

        # Instantiate a rebound simulation and set inital time and time step
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
        # sim_dict[row["ObjID"]]['H'] = H
        # sim_dict[row["ObjID"]]['G'] = G

        # count += 1
        # except:
        #     # TODO: better error handling
        #     # (do we want to fail gracefully here?)
        #     print("Error", index)
    return sim_dict
