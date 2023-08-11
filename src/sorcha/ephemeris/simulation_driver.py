import spiceypy as spice
from sorcha.ephemeris.simulation_setup import create_assist_ephemeris, furnish_spiceypy


def create_ephemeris():
    create_assist_ephemeris()
    furnish_spiceypy()

    

    spice.kclear()