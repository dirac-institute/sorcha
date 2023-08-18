import spiceypy as spice
from assist import Ephem
from . import simulation_parsing as sp
import random
import rebound
from collections import defaultdict
import assist

from sorcha.ephemeris.simulation_data_files import make_retriever, DE440S, JPL_PLANETS, JPL_SMALL_BODIES

# TODO: this should be handled by the `simulation_data_files` module
dir_path = "/Users/maxwest/notebooks/assist_plus_rebound/input_for_mpchecker"


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

    return Ephem(planets_path=planets_file_path, asteroids_path=small_bodies_file_path)


def furnish_spiceypy():
    # The goal here would be to download the spice kernel files (if needed)
    # Then call spice.furnish(<filename>) on each of those files.
    # The hope is that automagically that will make properly furnished in
    # this namespace, and when we access it via `import spiceypy as spice`, that
    # we'll be able to work with it correctly.

    # ! The following is a place holder
    retriever = make_retriever()
    kernel_1 = retriever.fetch(DE440S)
    spice.furnsh(kernel_1)


def generate_simulations(ephem):
    sim_dict = defaultdict(dict)  # return

    count, nsamp = 0, 10000  # pass in
    prob = 0.1  # pass in

    sun_dict = dict()  # This could be passed in and reused
    with open(dir_path + "/MPCORB.DAT") as file:  # pass in file
        for line in file:
            if line.startswith("-----------"):
                break
        for line in file:
            try:
                draw = random.random()
                if draw < prob and count < nsamp:
                    desig, H, G, epoch, pos, vel = sp.convert_mpc_orbit(line, ephem, sun_dict)

                    # Instantiate a rebound particle
                    x, y, z = pos
                    vx, vy, vz = vel
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
                    sim_dict[desig]["sim"] = sim
                    sim_dict[desig]["ex"] = ex
                    count += 1
            except:
                print("Error", line)
            if count >= nsamp:
                break
    return sim_dict
