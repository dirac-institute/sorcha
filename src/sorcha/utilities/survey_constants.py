# dict of surveys for a given option, These are currently used in fov,  filters , expert  configs
# Where the type of survey matters for running Sorcha (i.e. camera footprint, filters and certain features turned off)

DICT_SURVEY_NAMES = {
    "rubin": ["rubin_sim", "lsst"],  # rubin is used for any overall rubin process.
    "rubin_sim": ["rubin_sim"],  # for rubin_sim funcitons
    "lsst": ["lsst"],  # for lsst function
    "des": ["des"],  # for des fucntions.
}
