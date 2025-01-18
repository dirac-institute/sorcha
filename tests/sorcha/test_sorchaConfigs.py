import pytest

from sorcha.activity.activity_registration import CA_METHODS
from sorcha.lightcurves.lightcurve_registration import LC_METHODS
from sorcha.utilities.dataUtilitiesForTests import get_demo_filepath
from sorcha.utilities.sorchaArguments import sorchaArguments
from sorcha.utilities.sorchaConfigs import (activityConfigs, auxiliaryConfigs,
                                            expertConfigs,
                                            fadingfunctionConfigs,
                                            filtersConfigs, fovConfigs,
                                            inputConfigs, lightcurveConfigs,
                                            linkingfilterConfigs,
                                            outputConfigs, phasecurvesConfigs,
                                            saturationConfigs,
                                            simulationConfigs, sorchaConfigs)

# these are the results we expect from sorcha_config_demo.ini
correct_inputs = {
    "ephemerides_type": "ar",
    "eph_format": "csv",
    "size_serial_chunk": 5000,
    "aux_format": "whitespace",
    "pointing_sql_query": "SELECT observationId, observationStartMJD as observationStartMJD_TAI, visitTime, visitExposureTime, filter, seeingFwhmGeom as seeingFwhmGeom_arcsec, seeingFwhmEff as seeingFwhmEff_arcsec, fiveSigmaDepth as fieldFiveSigmaDepth_mag , fieldRA as fieldRA_deg, fieldDec as fieldDec_deg, rotSkyPos as fieldRotSkyPos_deg FROM observations order by observationId",
}
correct_simulation = {
    "_ephemerides_type": "ar",
    "ar_ang_fov": 2.06,
    "ar_fov_buffer": 0.2,
    "ar_picket": 1,
    "ar_obs_code": "X05",
    "ar_healpix_order": 6,
    "ar_n_sub_intervals": 101,
}

correct_filters_read = {"observing_filters": "r,g,i,z,u,y", "survey_name": "rubin_sim"}
correct_filters = {
    "observing_filters": ["r", "g", "i", "z", "u", "y"],
    "survey_name": "rubin_sim",
    "mainfilter": None,
    "othercolours": None,
}

correct_saturation = {
    "bright_limit_on": True,
    "bright_limit": 16.0,
    "_observing_filters": ["r", "g", "i", "z", "u", "y"],
}
correct_saturation_read = {"bright_limit": "16.0", "_observing_filters": ["r", "g", "i", "z", "u", "y"]}

correct_phasecurve = {"phase_function": "HG"}

correct_fadingfunction = {
    "fading_function_on": True,
    "fading_function_width": 0.1,
    "fading_function_peak_efficiency": 1.0,
}

correct_linkingfilter = {
    "ssp_linking_on": True,
    "drop_unlinked": True,
    "ssp_detection_efficiency": 0.95,
    "ssp_number_observations": 2,
    "ssp_separation_threshold": 0.5,
    "ssp_maximum_time": 0.0625,
    "ssp_number_tracklets": 3,
    "ssp_track_window": 15,
    "ssp_night_start_utc": 16.0,
}

correct_fov = {
    "camera_model": "footprint",
    "footprint_path": None,
    "fill_factor": None,
    "circle_radius": None,
    "footprint_edge_threshold": 2.0,
    "survey_name": "rubin_sim",
}

correct_fov_read = {"camera_model": "footprint", "footprint_edge_threshold": 2.0, "survey_name": "rubin_sim"}

correct_output = {
    "output_format": "csv",
    "output_columns": "basic",
    "position_decimals": None,
    "magnitude_decimals": None,
}

correct_lc_model = {"lc_model": None}

correct_activity = {"comet_activity": None}

correct_expert = {
    "snr_limit": None,
    "snr_limit_on": False,
    "mag_limit": None,
    "mag_limit_on": False,
    "trailing_losses_on": True,
    "default_snr_cut": True,
    "randomization_on": True,
    "vignetting_on": True,
    "brute_force": True,
    "ar_use_integrate": False,
}

correct_auxciliary_URLs = {
    "de440s.bsp": "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/de440s.bsp",
    "earth_200101_990827_predict.bpc": "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/earth_200101_990827_predict.bpc",
    "earth_620120_240827.bpc": "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/earth_620120_240827.bpc",
    "earth_latest_high_prec.bpc": "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/earth_latest_high_prec.bpc",
    "linux_p1550p2650.440": "https://ssd.jpl.nasa.gov/ftp/eph/planets/Linux/de440/linux_p1550p2650.440",
    "sb441-n16.bsp": "https://ssd.jpl.nasa.gov/ftp/eph/small_bodies/asteroids_de441/sb441-n16.bsp",
    "naif0012.tls": "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/lsk/naif0012.tls",
    "ObsCodes.json.gz": "https://minorplanetcenter.net/Extended_Files/obscodes_extended.json.gz",
    "pck00010.pck": "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/pck00010.tpc",
}
correct_auxciliary_filenames = [
    "de440s.bsp",
    "earth_200101_990827_predict.bpc",
    "earth_620120_240827.bpc",
    "earth_latest_high_prec.bpc",
    "linux_p1550p2650.440",
    "sb441-n16.bsp",
    "naif0012.tls",
    "meta_kernel.txt",
    "ObsCodes.json",
    "ObsCodes.json.gz",
    "pck00010.pck",
]
##################################################################################################################################

# SORCHA Configs test


def test_sorchaConfigs():
    """
    tests that sorchaConfigs reads in config file correctly
    """
    # general test to make sure, overall, everything works. checks just one file: sorcha_config_demo.ini

    config_file_location = get_demo_filepath("sorcha_config_demo.ini")
    test_configs = sorchaConfigs(config_file_location, "rubin_sim")
    # check each section to make sure you get what you expect
    assert correct_inputs == test_configs.input.__dict__
    assert correct_simulation == test_configs.simulation.__dict__
    assert correct_filters == test_configs.filters.__dict__
    assert correct_saturation == test_configs.saturation.__dict__
    assert correct_phasecurve == test_configs.phasecurves.__dict__
    assert correct_fov == test_configs.fov.__dict__
    assert correct_fadingfunction == test_configs.fadingfunction.__dict__
    assert correct_linkingfilter == test_configs.linkingfilter.__dict__
    assert correct_output == test_configs.output.__dict__
    assert correct_lc_model == test_configs.lightcurve.__dict__
    assert correct_activity == test_configs.activity.__dict__
    assert correct_expert == test_configs.expert.__dict__
    assert correct_auxciliary_URLs == test_configs.auxiliary.__dict__["urls"]
    assert correct_auxciliary_filenames == test_configs.auxiliary.__dict__["data_file_list"]


##################################################################################################################################

# Inputs section test


def test_inputConfigs_int():
    """
    tests that wrong inputs for inputConfigs int attributes is caught correctly
    """

    input_configs = correct_inputs.copy()
    # make sure everything populated correctly
    test_configs = inputConfigs(**input_configs)
    assert test_configs.__dict__ == input_configs

    # now we check some wrong inputs to make sure they're caught correctly. size_serial_chunk has to be castable as an integer
    input_configs["size_serial_chunk"] = "five thousand"

    # we're telling pytest that we expect this command to fail with a SystemExit
    with pytest.raises(SystemExit) as error_text:
        test_configs = inputConfigs(**input_configs)

    # and this checks that the error message is what we expect.
    assert (
        error_text.value.code
        == "ERROR: expected an int for config parameter size_serial_chunk. Check value in config file."
    )


@pytest.mark.parametrize(
    "key_name", ["ephemerides_type", "eph_format", "size_serial_chunk", "aux_format", "pointing_sql_query"]
)
def test_inputConfigs_mandatory(key_name):
    """
    this loops through the mandatory keys and makes sure the code fails correctly when each is missing
    """

    input_configs = correct_inputs.copy()

    del input_configs[key_name]

    with pytest.raises(SystemExit) as error_text:
        test_configs = inputConfigs(**input_configs)

    assert (
        error_text.value.code
        == f"ERROR: No value found for required key {key_name} in config file. Please check the file and try again."
    )


@pytest.mark.parametrize(
    "key_name, expected_list",
    [
        ("ephemerides_type", "['ar', 'external']"),
        ("aux_format", "['comma', 'whitespace', 'csv']"),
        ("eph_format", "['csv', 'whitespace', 'hdf5']"),
    ],
)
def test_inputConfigs_inlist(key_name, expected_list):
    """
    this loops through the keys that need to have one of several set values and makes sure the correct error message triggers when they're not
    """

    input_configs = correct_inputs.copy()

    input_configs[key_name] = "definitely_fake_bad_key"

    with pytest.raises(SystemExit) as error_text:
        test_configs = inputConfigs(**input_configs)

    assert (
        error_text.value.code
        == f"ERROR: value definitely_fake_bad_key for config parameter {key_name} not recognised. Expecting one of: {expected_list}."
    )


##################################################################################################################################

# simulation configs test


@pytest.mark.parametrize("key_name", ["ar_ang_fov", "ar_fov_buffer"])
def test_simulationConfigs_float(key_name):
    """
    Tests that wrong inputs for simulationConfigs float attributes is caught correctly
    """

    simulation_configs = correct_simulation.copy()
    test_configs = simulationConfigs(**simulation_configs)
    assert test_configs.__dict__ == simulation_configs

    simulation_configs[key_name] = "one"

    with pytest.raises(SystemExit) as error_text:
        test_configs = simulationConfigs(**simulation_configs)

    assert (
        error_text.value.code
        == f"ERROR: expected a float for config parameter {key_name}. Check value in config file."
    )


@pytest.mark.parametrize("key_name", ["ar_picket", "ar_healpix_order", "ar_n_sub_intervals"])
def test_simulationConfigs_int(key_name):
    """
    Tests that wrong inputs for simulationConfigs int attributes is caught correctly
    """

    simulation_configs = correct_simulation.copy()
    test_configs = simulationConfigs(**simulation_configs)
    assert test_configs.__dict__ == simulation_configs

    simulation_configs[key_name] = "one"

    with pytest.raises(SystemExit) as error_text:
        test_configs = simulationConfigs(**simulation_configs)

    assert (
        error_text.value.code
        == f"ERROR: expected an int for config parameter {key_name}. Check value in config file."
    )


@pytest.mark.parametrize(
    "key_name", ["ar_ang_fov", "ar_fov_buffer", "ar_picket", "ar_obs_code", "ar_healpix_order"]
)
def test_simulationConfigs_mandatory(key_name):
    """
    This loops through the mandatory keys and makes sure the code fails correctly when each is missing
    """

    simulation_configs = correct_simulation.copy()

    del simulation_configs[key_name]

    with pytest.raises(SystemExit) as error_text:
        test_configs = simulationConfigs(**simulation_configs)

    assert (
        error_text.value.code
        == f"ERROR: No value found for required key {key_name} in config file. Please check the file and try again."
    )


@pytest.mark.parametrize(
    "key_name", ["ar_ang_fov", "ar_fov_buffer", "ar_picket", "ar_obs_code", "ar_healpix_order"]
)
def test_simulationConfigs_notrequired(key_name):
    """
    This loops through the not required keys and makes sure the code fails correctly when they're truthy
    """

    simulation_configs = correct_simulation.copy()

    for name in simulation_configs:
        if key_name != name and name != "_ephemerides_type":
            simulation_configs[name] = None
    simulation_configs["_ephemerides_type"] = "external"

    with pytest.raises(SystemExit) as error_text:
        test_configs = simulationConfigs(**simulation_configs)

    assert (
        error_text.value.code == f"ERROR: {key_name} supplied in config file but ephemerides type is external"
    )


##################################################################################################################################

# filters config test


def test_filtersConfigs_check_filters():
    """
    Makes sure that when filters are not recognised for survey that error message shows
    """

    filters_configs = correct_filters_read.copy()

    test_configs = filtersConfigs(**filters_configs)
    assert test_configs.__dict__ == correct_filters

    filters_configs["observing_filters"] = "a,f,u,g"
    with pytest.raises(SystemExit) as error_text:
        test_configs = filtersConfigs(**filters_configs)
    assert (
        error_text.value.code
        == "ERROR: Filter(s) ['a' 'f'] given in config file are not recognised filters for rubin_sim survey."
    )


@pytest.mark.parametrize("key_name", ["observing_filters", "survey_name"])
def test_filtersConfigs_mandatory(key_name):
    """
    this loops through the mandatory keys and makes sure the code fails correctly when each is missing
    """

    filter_configs = correct_filters_read.copy()
    del filter_configs[key_name]

    with pytest.raises(SystemExit) as error_text:
        test_configs = filtersConfigs(**filter_configs)

    assert (
        error_text.value.code
        == f"ERROR: No value found for required key {key_name} in config file. Please check the file and try again."
    )


##################################################################################################################################
# saturation configs test


def test_saturationConfigs():
    """
    Tests that error occurs when list of saturation limits is not the same length as list of observing filters.
    Also tests that error occurs when brightness limits can't be parsed.
    """

    saturation_configs = correct_saturation_read.copy()

    # make sure everything populated correctly
    test_configs = saturationConfigs(**saturation_configs)
    assert test_configs.__dict__ == correct_saturation

    saturation_configs["bright_limit"] = "10,2"

    with pytest.raises(SystemExit) as error_text:
        test_configs = saturationConfigs(**saturation_configs)

    assert (
        error_text.value.code
        == "ERROR: list of saturation limits is not the same length as list of observing filters."
    )
    saturation_configs["bright_limit"] = "10;2"

    with pytest.raises(SystemExit) as error_text:
        test_configs = saturationConfigs(**saturation_configs)

    assert (
        error_text.value.code == "ERROR: could not parse brightness limits. Check formatting and try again."
    )


@pytest.mark.parametrize("key_name", ["_observing_filters"])
def test_saturationConfigs_mandatory(key_name):
    """
    this loops through the mandatory keys and makes sure the code fails correctly when each is missing
    """

    saturation_configs = correct_saturation_read.copy()

    del saturation_configs[key_name]

    with pytest.raises(SystemExit) as error_text:
        test_configs = saturationConfigs(**saturation_configs)

    assert (
        error_text.value.code
        == f"ERROR: No value found for required key {key_name} in config file. Please check the file and try again."
    )


##################################################################################################################################

# phasecurve configs tests


@pytest.mark.parametrize("key_name", ["phase_function"])
def test_phasecurveConfigs_mandatory(key_name):
    """
    this loops through the mandatory keys and makes sure the code fails correctly when each is missing
    """

    phasecurves_configs = correct_phasecurve.copy()

    del phasecurves_configs[key_name]

    with pytest.raises(SystemExit) as error_text:
        test_configs = phasecurvesConfigs(**phasecurves_configs)

    assert (
        error_text.value.code
        == f"ERROR: No value found for required key {key_name} in config file. Please check the file and try again."
    )


@pytest.mark.parametrize(
    "key_name, expected_list",
    [("phase_function", "['HG', 'HG1G2', 'HG12', 'linear', 'none']")],
)
def test_phasecurveConfigs_inlist(key_name, expected_list):
    """
    this loops through the keys that need to have one of several set values and makes sure the correct error message triggers when they're not
    """

    phasecurve_configs = correct_phasecurve.copy()

    phasecurve_configs[key_name] = "definitely_fake_bad_key"

    with pytest.raises(SystemExit) as error_text:
        test_configs = phasecurvesConfigs(**phasecurve_configs)
    print(error_text.value.code)
    print(
        f"ERROR: value definitely_fake_bad_key for config parameter {key_name} not recognised. Expecting one of: {expected_list}."
    )
    assert (
        error_text.value.code
        == f"ERROR: value definitely_fake_bad_key for config parameter {key_name} not recognised. Expecting one of: {expected_list}."
    )


##################################################################################################################################

# fov configs test


def test_fovConfigs_inlist():
    """
    this loops through the keys that need to have one of several set values and makes sure the correct error message triggers when they're not
    """

    fov_configs = correct_fov_read.copy()

    test_configs = fovConfigs(**fov_configs)
    assert test_configs.__dict__ == correct_fov

    fov_configs["camera_model"] = "fake_model"
    with pytest.raises(SystemExit) as error_text:
        test_configs = fovConfigs(**fov_configs)
    assert (
        error_text.value.code
        == "ERROR: value fake_model for config parameter camera_model not recognised. Expecting one of: ['circle', 'footprint', 'none']."
    )


def test_fovConfigs_surveyname():
    """
    Tests that error occurs when survey is not one provided with a default detector.
    """

    fov_configs = correct_fov_read.copy()

    test_configs = fovConfigs(**fov_configs)
    assert test_configs.__dict__ == correct_fov

    fov_configs["survey_name"] = "fake"
    with pytest.raises(SystemExit) as error_text:
        test_configs = fovConfigs(**fov_configs)
    assert (
        error_text.value.code
        == "ERROR: a default detector footprint is currently only provided for LSST; please provide your own footprint file."
    )


@pytest.mark.parametrize("key_name", ["fill_factor", "circle_radius"])
def test_fovConfigs_camera_footprint_notrequired(key_name):
    """
    this loops through the mandatory keys and keys that shouldn't exist and makes sure the code fails correctly when each is missing
    """

    fov_configs = correct_fov_read.copy()

    # check these dont exist
    if key_name == "fill_factor" or key_name == "circle_raidus":
        fov_configs[key_name] = 0.5
        with pytest.raises(SystemExit) as error_text:
            test_configs = fovConfigs(**fov_configs)
        reason = 'but camera model is not "circle".'
        assert error_text.value.code == f"ERROR: {key_name} supplied in config file {reason}"


def test_fovConfigs_circle_mandatory():
    """
    Makes sure the code fails when either "fill_factor" or "circle_radius" is missing
    """

    fov_configs = correct_fov_read.copy()
    fov_configs["camera_model"] = "circle"

    with pytest.raises(SystemExit) as error_text:
        test_configs = fovConfigs(**fov_configs)
    assert (
        error_text.value.code
        == 'ERROR: either "fill_factor" or "circle_radius" must be specified for circular footprint.'
    )


@pytest.mark.parametrize("key_name", ["fill_factor", "circle_radius"])
def test_fovConfigs_bounds(key_name):
    """
    Tests that values in fovConfigs are creating error messages when out of bounds
    """

    fov_configs = correct_fov_read.copy()
    fov_configs["camera_model"] = "circle"
    fov_configs[key_name] = -0.1
    if key_name == "fill_factor":

        with pytest.raises(SystemExit) as error_text:
            test_configs = fovConfigs(**fov_configs)
        assert error_text.value.code == "ERROR: fill_factor out of bounds. Must be between 0 and 1."
    elif key_name == "circle_radius":
        with pytest.raises(SystemExit) as error_text:
            test_configs = fovConfigs(**fov_configs)
        assert error_text.value.code == "ERROR: circle_radius is negative."


def test_fovConfigs_camera_circle_notrequired():
    """
    This loops through the not required keys and makes sure the code fails correctly when they're truthy
    """

    fov_configs = correct_fov_read.copy()
    fov_configs["camera_model"] = "circle"
    fov_configs["fill_factor"] = 0.5
    with pytest.raises(SystemExit) as error_text:
        test_configs = fovConfigs(**fov_configs)
    assert (
        error_text.value.code
        == f'ERROR: footprint_edge_threshold supplied in config file but camera model is not "footprint".'
    )


##################################################################################################################################

# fadingfunction config tests


@pytest.mark.parametrize("key_name", ["fading_function_width", "fading_function_peak_efficiency"])
def test_fadingfunctionConfig_on_float(key_name):
    """
    Tests that wrong inputs for fadingfunctionConfig float attributes is caught correctly
    """

    fadingfunction_configs = correct_fadingfunction.copy()
    test_configs = fadingfunctionConfigs(**fadingfunction_configs)
    assert test_configs.__dict__ == fadingfunction_configs

    fadingfunction_configs[key_name] = "ten"
    with pytest.raises(SystemExit) as error_text:
        test_configs = fadingfunctionConfigs(**fadingfunction_configs)

    assert (
        error_text.value.code
        == f"ERROR: expected a float for config parameter {key_name}. Check value in config file."
    )



@pytest.mark.parametrize("key_name", ["fading_function_width", "fading_function_peak_efficiency"])
def test_fadingfunction_outofbounds(key_name):
    """
    Tests that values in fadingfunctionConfigs are creating error messages when out of bounds
    """

    fadingfunction_configs = correct_fadingfunction.copy()
    fadingfunction_configs[key_name] = 10
    if key_name == "fading_function_width":
        with pytest.raises(SystemExit) as error_text:
            test_configs = fadingfunctionConfigs(**fadingfunction_configs)
        assert (
            error_text.value.code
            == "ERROR: fading_function_width out of bounds. Must be greater than zero and less than 0.5."
        )
    if key_name == "fading_function_peak_efficiency":
        with pytest.raises(SystemExit) as error_text:
            test_configs = fadingfunctionConfigs(**fadingfunction_configs)
        assert (
            error_text.value.code
            == "ERROR: fading_function_peak_efficiency out of bounds. Must be between 0 and 1."
        )

def test_fadingfunction_allnone():
    """
    This loops through the not required keys and makes sure the code fails correctly when all attributes are none
    """
    fadingfunction_configs = correct_fadingfunction.copy()
    fadingfunction_configs["fading_function_on"] = None
    fadingfunction_configs["fading_function_width"] = 5.0
    fadingfunction_configs["fading_function_peak_efficiency"] = None
    with pytest.raises(SystemExit) as error_text:
        test_configs = fadingfunctionConfigs(**fadingfunction_configs)
    assert (
        error_text.value.code == "ERROR: Both fading_function_peak_efficiency and fading_function_width are needed to be supplied for fading function"
    )
##################################################################################################################################

# linkingfilter tests


@pytest.mark.parametrize(
    "key_name",
    ["ssp_detection_efficiency", "ssp_separation_threshold", "ssp_maximum_time", "ssp_night_start_utc"],
)
def test_linkingfilterConfigs_float(key_name):
    """
    Tests that wrong inputs for linkingfilterConfigs float attributes is caught correctly
    """

    linkingfilter_configs = correct_linkingfilter.copy()
    test_configs = linkingfilterConfigs(**linkingfilter_configs)
    assert test_configs.__dict__ == linkingfilter_configs

    linkingfilter_configs[key_name] = "one"

    with pytest.raises(SystemExit) as error_text:
        test_configs = linkingfilterConfigs(**linkingfilter_configs)

    assert (
        error_text.value.code
        == f"ERROR: expected a float for config parameter {key_name}. Check value in config file."
    )


@pytest.mark.parametrize("key_name", ["ssp_number_observations", "ssp_number_tracklets", "ssp_track_window"])
def test_linking_filter_int(key_name):
    """
    Tests that wrong inputs for linkingfilterConfigs int attributes is caught correctly
    """

    linkingfilter_configs = correct_linkingfilter.copy()
    test_configs = linkingfilterConfigs(**linkingfilter_configs)
    assert test_configs.__dict__ == linkingfilter_configs

    linkingfilter_configs[key_name] = "one"

    with pytest.raises(SystemExit) as error_text:
        test_configs = linkingfilterConfigs(**linkingfilter_configs)

    assert (
        error_text.value.code
        == f"ERROR: expected an int for config parameter {key_name}. Check value in config file."
    )


@pytest.mark.parametrize(
    "key_name",
    [
        "ssp_detection_efficiency",
        "ssp_separation_threshold",
        "ssp_maximum_time",
        "ssp_night_start_utc",
        "ssp_number_observations",
        "ssp_number_tracklets",
        "ssp_track_window",
    ],
)
def test_linkingfilter_bounds(key_name):
    """
    Tests that values in linkingfilterConfigs are creating error messages when out of bounds
    """

    linkingfilter_configs = correct_linkingfilter.copy()

    if key_name == "ssp_maximum_time" or key_name == "ssp_track_window":
        linkingfilter_configs[key_name] = -5
        with pytest.raises(SystemExit) as error_text:
            test_configs = linkingfilterConfigs(**linkingfilter_configs)

        assert error_text.value.code == f"ERROR: {key_name} is negative."
    elif key_name == "ssp_separation_threshold" or key_name == "ssp_number_observations":
        linkingfilter_configs[key_name] = -5
        with pytest.raises(SystemExit) as error_text:
            test_configs = linkingfilterConfigs(**linkingfilter_configs)

        assert error_text.value.code == f"ERROR: {key_name} is zero or negative."
    elif key_name == "ssp_number_tracklets":
        linkingfilter_configs[key_name] = -5
        with pytest.raises(SystemExit) as error_text:
            test_configs = linkingfilterConfigs(**linkingfilter_configs)

        assert error_text.value.code == "ERROR: ssp_number_tracklets is zero or less."
    elif key_name == "ssp_detection_efficiency":
        linkingfilter_configs[key_name] = -5
        with pytest.raises(SystemExit) as error_text:
            test_configs = linkingfilterConfigs(**linkingfilter_configs)

        assert (
            error_text.value.code
            == "ERROR: ssp_detection_efficiency out of bounds (should be between 0 and 1)."
        )
    elif key_name == "ssp_night_start_utc":
        linkingfilter_configs[key_name] = -5
        with pytest.raises(SystemExit) as error_text:
            test_configs = linkingfilterConfigs(**linkingfilter_configs)

        assert (
            error_text.value.code == "ERROR: ssp_night_start_utc must be a valid time between 0 and 24 hours."
        )


def test_linkingfilter_only_some_sspvar():
    """
    Males sure error message shows when only some SSP variables are provided
    """
    linkingfilter_configs = correct_linkingfilter.copy()

    linkingfilter_configs["ssp_separation_threshold"] = None

    with pytest.raises(SystemExit) as error_text:
        test_configs = linkingfilterConfigs(**linkingfilter_configs)

    assert (
        error_text.value.code
        == "ERROR: only some ssp linking variables supplied. Supply all five required variables for ssp linking filter, or none to turn filter off."
    )


def test_linkingfilter_bool():
    """
    Tests that wrong inputs for linkingfilterConfigs bool attributes is caught correctly
    """

    linkingfilter_configs = correct_linkingfilter.copy()

    linkingfilter_configs["drop_unlinked"] = "fake"

    with pytest.raises(SystemExit) as error_text:
        test_configs = linkingfilterConfigs(**linkingfilter_configs)

    assert (
        error_text.value.code
        == f"ERROR: expected a bool for config parameter drop_unlinked. Check value in config file."
    )


##################################################################################################################################

# output config tests


@pytest.mark.parametrize("key_name", ["output_format", "output_columns"])
def test_outputConfigs_mandatory(key_name):
    """
    this loops through the mandatory keys and keys that shouldn't exist and makes sure the code fails correctly when each is missing
    """

    output_configs = correct_output.copy()

    del output_configs[key_name]

    with pytest.raises(SystemExit) as error_text:
        test_configs = outputConfigs(**output_configs)

    assert (
        error_text.value.code
        == f"ERROR: No value found for required key {key_name} in config file. Please check the file and try again."
    )


@pytest.mark.parametrize(
    "key_name, expected_list",
    [
        ("output_format", "['csv', 'sqlite3', 'hdf5']"),
        ("output_columns", "['basic', 'all']"),
    ],
)
def test_outputConfigs_inlist(key_name, expected_list):
    """
    this loops through the keys that need to have one of several set values and makes sure the correct error message triggers when they're not
    """

    output_configs = correct_output.copy()

    output_configs[key_name] = "definitely_fake_bad_key"

    with pytest.raises(SystemExit) as error_text:
        test_configs = outputConfigs(**output_configs)
    assert (
        error_text.value.code
        == f"ERROR: value definitely_fake_bad_key for config parameter {key_name} not recognised. Expecting one of: {expected_list}."
    )


@pytest.mark.parametrize("key_name", ["position_decimals", "magnitude_decimals"])
def test_outputConfigs_decimel_check(key_name):
    """
    Checks that if decimals are not int or are negative it is caught correctly
    """
    correct_output = {
        "output_format": "csv",
        "output_columns": "basic",
        "position_decimals": 5,
        "magnitude_decimals": 5,
    }

    output_configs = correct_output.copy()

    output_configs[key_name] = "definitely_fake_bad_key"

    with pytest.raises(SystemExit) as error_text:
        test_configs = outputConfigs(**output_configs)
    assert (
        error_text.value.code
        == f"ERROR: expected an int for config parameter {key_name}. Check value in config file."
    )
    correct_output = {
        "output_format": "csv",
        "output_columns": "basic",
        "position_decimals": 5,
        "magnitude_decimals": 5,
    }
    output_configs = correct_output.copy()
    output_configs[key_name] = -5
    with pytest.raises(SystemExit) as error_text:
        test_configs = outputConfigs(**output_configs)
    assert error_text.value.code == "ERROR: decimal places config variables cannot be negative."


##################################################################################################################################

# lightcurve config test


def test_lightcurve_config():
    """
    makes sure that if lightcurve model provided is not registered an error occurs
    """

    lightcurve_configs = correct_lc_model.copy()

    lightcurve_configs["lc_model"] = "what_model"

    with pytest.raises(SystemExit) as error_text:
        test_configs = lightcurveConfigs(**lightcurve_configs)
    assert (
        error_text.value.code
        == f"The requested light curve model, 'what_model', is not registered. Available lightcurve options are: {list(LC_METHODS.keys())}"
    )


##################################################################################################################################

# activity config test


def test_activity_config():
    """
    makes sure that if comet activity model provided is not registered an error occurs
    """

    activity_configs = correct_activity.copy()

    activity_configs["comet_activity"] = "nothing"

    with pytest.raises(SystemExit) as error_text:
        test_configs = activityConfigs(**activity_configs)
    assert (
        error_text.value.code
        == f"The requested comet activity model, 'nothing', is not registered. Available comet activity models are: {list(CA_METHODS.keys())}"
    )


##################################################################################################################################

# expert config test


@pytest.mark.parametrize("key_name", ["snr_limit", "mag_limit"])
def test_expert_config_float(key_name):
    """
    tests that wrong inputs for expertConfigs float attributes is caught correctly
    """

    expect_configs = correct_expert.copy()
    expect_configs[key_name] = "str"
    with pytest.raises(SystemExit) as error_text:
        test_configs = expertConfigs(**expect_configs)

    assert (
        error_text.value.code
        == f"ERROR: expected a float for config parameter {key_name}. Check value in config file."
    )


@pytest.mark.parametrize("key_name, error_name", [("snr_limit", "SNR"), ("mag_limit", "magnitude")])
def test_expert_config_bounds(key_name, error_name):
    """
    Tests that values in expertConfigs are creating error messages when out of bounds
    """

    expect_configs = correct_expert.copy()
    expect_configs[key_name] = -5
    with pytest.raises(SystemExit) as error_text:
        test_configs = expertConfigs(**expect_configs)

    assert error_text.value.code == f"ERROR: {error_name} limit is negative."


def test_expert_config_exclusive():
    """
    Makes sure that when both snr limit and magnitude limit are specified that an error occurs
    """

    expect_configs = correct_expert.copy()
    expect_configs["mag_limit"] = 5
    expect_configs["snr_limit"] = 5
    with pytest.raises(SystemExit) as error_text:
        test_configs = expertConfigs(**expect_configs)

    assert (
        error_text.value.code
        == "ERROR: SNR limit and magnitude limit are mutually exclusive. Please delete one or both from config file."
    )


@pytest.mark.parametrize(
    "key_name", ["trailing_losses_on", "default_snr_cut", "randomization_on", "vignetting_on"]
)
def test_expertConfig_bool(key_name):
    """
    Tests that wrong inputs for expertConfigs bool attributes is caught correctly
    """

    expect_configs = correct_expert.copy()
    expect_configs[key_name] = "fake"
    with pytest.raises(SystemExit) as error_text:
        test_configs = expertConfigs(**expect_configs)

    assert (
        error_text.value.code
        == f"ERROR: expected a bool for config parameter {key_name}. Check value in config file."
    )


##################################################################################################################################

# auxiliary config test


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
def test_auxiliary_config_making_url_none(file):
    aux_configs = {file: "new_filename"}

    test_configs = auxiliaryConfigs(**aux_configs)
    assert getattr(test_configs, file + "_url") == None


def test_PrintConfigsToLog(tmp_path):
    import glob
    import os

    from sorcha.modules.PPGetLogger import PPGetLogger
    from sorcha.utilities.dataUtilitiesForTests import get_test_filepath
    from sorcha.utilities.sorchaConfigs import PrintConfigsToLog

    test_path = os.path.dirname(get_test_filepath("test_input_fullobs.csv"))
    config_file_location = get_test_filepath("test_PPConfig.ini")
    pplogger = PPGetLogger(tmp_path, "test_log", log_format="%(name)-12s %(levelname)-8s %(message)s ")

    cmd_args = {
        "paramsinput": "testcolour.txt",
        "orbinfile": "testorb.des",
        "input_ephemeris_file": "ephemtestoutput.txt",
        "configfile": "test_PPConfig.ini",
        "pointing_database": "./baseline_10klines_2.0.db",
        "outpath": "./",
        "surveyname": "rubin_sim",
        "outfilestem": "testout",
        "loglevel": True,
        "seed": 24601,
        "stats": None,
    }
    test_configs = sorchaConfigs(config_file_location, "rubin_sim")
    test_configs.filters.mainfilter = "r"
    test_configs.filters.othercolours = ["g-r", "i-r", "z-r"]
    args = sorchaArguments(cmd_args)

    PrintConfigsToLog(test_configs, args)

    datalog = glob.glob(os.path.join(tmp_path, "*-sorcha.log"))
    # when updating PrintConfigsToLog text file test_PPPrintConfigsToLog.txt needs to be updated too.
    testfile = open(os.path.join(test_path, "test_PrintConfigsToLog.txt"), mode="r")
    newfile = open(datalog[0], mode="r")
    alltest = testfile.readlines()
    allnew = newfile.readlines()
    allnew_ = allnew[1:]  # skipping first line as that line specifies user file location
    assert alltest == allnew_

    testfile.close()
    newfile.close()

    return
