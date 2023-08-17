import pooch

# Define variables for the file names

DE440S = "de440s.bsp"
EARTH_PREDICT = "earth_200101_990825_predict.bpc"
EARTH_HISTORICAL = "earth_720101_230601.bpc"
EARTH_HIGH_PRECISION = "earth_latest_high_prec.bpc"
JPL_PLANETS = "linux_p1550p2650.440"
JPL_SMALL_BODIES = "sb441-n16.bsp"
LEAP_SECONDS = "naif0012.tls"
OBSERVATORY_CODES = "ObsCodes.json.gz"
ORIENTATION_CONSTANTS = "pck00010.pck"

# Dictionary of filename: url
URLS = {
    DE440S: "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/de440s.bsp",
    EARTH_PREDICT: "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/earth_200101_990825_predict.bpc",
    EARTH_HISTORICAL: "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/earth_720101_230601.bpc",
    EARTH_HIGH_PRECISION: "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/earth_latest_high_prec.bpc",
    JPL_PLANETS: "https://ssd.jpl.nasa.gov/ftp/eph/planets/Linux/de440/linux_p1550p2650.440",
    JPL_SMALL_BODIES: "https://ssd.jpl.nasa.gov/ftp/eph/small_bodies/asteroids_de441/sb441-n16.bsp",
    LEAP_SECONDS: "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/lsk/naif0012.tls",
    OBSERVATORY_CODES: "https://minorplanetcenter.net/Extended_Files/obscodes_extended.json.gz",
    ORIENTATION_CONSTANTS: "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/pck00010.tpc",
}

# Convenience list of all the file names
DATA_FILE_LIST = [
    DE440S,
    EARTH_PREDICT,
    EARTH_HISTORICAL,
    EARTH_HIGH_PRECISION,
    JPL_PLANETS,
    JPL_SMALL_BODIES,
    LEAP_SECONDS,
    OBSERVATORY_CODES,
    ORIENTATION_CONSTANTS,
]

# Used by Pooch to define which files will be tracked and retrievable
REGISTRY = {data_file: None for data_file in DATA_FILE_LIST}


def make_retriever(directory_path: str = None) -> pooch.Pooch:
    dir_path = pooch.os_cache("sorcha")
    if directory_path:
        dir_path = directory_path

    return pooch.create(
        path=dir_path,
        base_url="",
        urls=URLS,
        registry=REGISTRY,
        retry_if_failed=1,
    )
