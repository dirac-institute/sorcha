import pooch

from assist import Ephem

JPL_PLANETS = "planets/Linux/de440/linux_p1550p2650.440"
JPL_SMALL_BODIES = "small_bodies/asteroids_de441/sb441-n16.bsp"

RETRIEVER = pooch.create(
        path=pooch.os_cache("sorcha"),
        base_url="https://ssd.jpl.nasa.gov/ftp/eph/",
        registry={
            JPL_PLANETS: "sha256:29915576d0a6555766b99485ac3056ee415e86df4fce282611c31afb329ad062",
            JPL_SMALL_BODIES: "sha256:919d612ce3c72a78fc7158f9120156542d0f21e6b8b052e4c1339c759747fd90",
            },
        retry_if_failed=1
    )

def retrieve_file(file_name:str = None) -> str:
    return RETRIEVER.fetch(file_name)

def create_assist_ephemeris() -> Ephem:
    """Build the ASSIST ephemeris object

    Returns
    -------
    Ephem
        The ASSIST ephemeris object
    """
    planets_file_path = retrieve_file(JPL_PLANETS)
    small_bodies_file_path = retrieve_file(JPL_SMALL_BODIES)

    return Ephem(planets_path=planets_file_path, asteroids_path=small_bodies_file_path)
