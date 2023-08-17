import spiceypy as spice
from assist import Ephem

from sorcha.ephemeris.simulation_data_files import make_retriever, DE440S, JPL_PLANETS, JPL_SMALL_BODIES


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
