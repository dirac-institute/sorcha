import pytest
from sorcha.configs.auxiliaryConfigs import auxiliaryConfigs

# tests auxiliary configs class


correct_auxciliary_URLs = {
    "de440s.bsp": "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/de440s.bsp",
    "earth_2026_260806_2126_predict.bpc": "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/earth_2026_260806_2126_predict.bpc",
    "earth_620120_260806.bpc": "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/earth_620120_260806.bpc",
    "earth_latest_high_prec.bpc": "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/earth_latest_high_prec.bpc",
    "linux_p1550p2650.440": "https://ssd.jpl.nasa.gov/ftp/eph/planets/Linux/de440/linux_p1550p2650.440",
    "sb441-n16.bsp": "https://ssd.jpl.nasa.gov/ftp/eph/small_bodies/asteroids_de441/sb441-n16.bsp",
    "naif0012.tls": "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/lsk/naif0012.tls",
    "ObsCodes.json.gz": "https://minorplanetcenter.net/Extended_Files/obscodes_extended.json.gz",
    "pck00010.pck": "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/pck00010.tpc",
}
correct_auxciliary_filenames = [
    "de440s.bsp",
    "earth_2026_260806_2126_predict.bpc",
    "earth_620120_260806.bpc",
    "earth_latest_high_prec.bpc",
    "linux_p1550p2650.440",
    "sb441-n16.bsp",
    "naif0012.tls",
    "meta_kernel.txt",
    "ObsCodes.json",
    "ObsCodes.json.gz",
    "pck00010.pck",
]

test_registry = {
    "de440s.bsp": None,
    "earth_2026_260806_2126_predict.bpc": None,
    "earth_620120_260806.bpc": None,
    "earth_latest_high_prec.bpc": None,
    "linux_p1550p2650.440": None,
    "sb441-n16.bsp": None,
    "naif0012.tls": None,
    "meta_kernel.txt": None,
    "ObsCodes.json": None,
    "ObsCodes.json.gz": None,
    "pck00010.pck": None,
}

# auxiliary config test


def test_default_files_created_populate_correctly():
    """
    tests empty auxiliaryConfigs() and ensure the defaults are
    created correctly
    """
    config = auxiliaryConfigs()

    assert config.registry == test_registry
    assert config.urls == correct_auxciliary_URLs
    assert config.data_file_list == correct_auxciliary_filenames


@pytest.mark.parametrize(
    "file",
    [
        "planet_ephemeris",
        "earth_predict",
        "earth_historical",
        "jpl_planets",
        "leap_seconds",
        "observatory_codes_compressed",
        "orientation_constants",
    ],
)

# This unit test is for when a url is guven but a filename is not given, (should error out)
def test_auxiliary_config_url_given_filename_not(file):
    aux_configs = {file + "_url": "new_url"}
    with pytest.raises(SystemExit) as error_text:
        test_configs = auxiliaryConfigs(**aux_configs)
    assert error_text.value.code == f"ERROR: url for {file} given but filename for {file} not given"


@pytest.mark.parametrize(
    "file",
    [
        "planet_ephemeris",
        "earth_predict",
        "earth_historical",
        "jpl_planets",
        "leap_seconds",
        "observatory_codes_compressed",
        "orientation_constants",
    ],
)

# this unit test tests that if a new file is specified but not a url then the url is set as None.
# i.e. its assumed the file is in the cache ar directory, a new one shouldn't be downloaded and is read from there.
def test_auxiliary_config_making_url_none(file):
    aux_configs = {file: "new_filename"}

    test_configs = auxiliaryConfigs(**aux_configs)
    assert getattr(test_configs, file + "_url") == None
