import pooch

JPL_PLANETS = "linux_p1550p2650.440"
JPL_SMALL_BODIES = "sb441-n16.bsp"
DE440S = "de440s.bsp"
# TODO - Add the rest of the files

URLS = {
    JPL_PLANETS: "https://ssd.jpl.nasa.gov/ftp/eph/planets/Linux/de440/linux_p1550p2650.440",
    JPL_SMALL_BODIES: "https://ssd.jpl.nasa.gov/ftp/eph/small_bodies/asteroids_de441/sb441-n16.bsp",
    DE440S: "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/de440s.bsp",
    # TODO - Add the rest of the URLs
}

DATA_FILE_LIST = [
    JPL_PLANETS,
    JPL_SMALL_BODIES,
    DE440S,
    # TODO - Add the rest of the file name variables
]

REGISTRY = {data_file: None for data_file in DATA_FILE_LIST}


def make_retriever(directory_path: str = None) -> pooch.Pooch:
    dir_path = pooch.os_cache("sorcha")
    if directory_path:
        dir_path = directory_path

    return pooch.create(
        path=dir_path,
        base_url="https://example.com",
        urls=URLS,
        registry=REGISTRY,
        retry_if_failed=1,
    )
