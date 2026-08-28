import pytest
from sorcha.configs.fovConfigs import fovConfigs

correct_fov = {
    "camera_model": "footprint",
    "footprint_path": None,
    "visits_query": None,
    "fill_factor": None,
    "circle_radius": None,
    "footprint_edge_threshold": 2.0,
    "survey_name": "rubin_sim",
    "default_camera_config_file": "data/LSST_detector_corners_100123.csv",
}

correct_fov_read = {"camera_model": "footprint", "footprint_edge_threshold": 2.0, "survey_name": "rubin_sim"}


# fov configs test


def test_fovConfigs_camera_model_inlist():
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
        == "ERROR: value fake_model for config parameter camera_model not recognised. Expecting one of: ['circle', 'footprint', 'visits_footprint', 'none']."
    )


# tests for camera_model = footprint


def test_fovConfigs_surveyname():
    """
    Tests that error occurs when survey is not one provided with a default detector (camera_model = footprint).
    """

    fov_configs = correct_fov_read.copy()

    test_configs = fovConfigs(**fov_configs)
    assert test_configs.__dict__ == correct_fov

    fov_configs["survey_name"] = "fake"
    with pytest.raises(SystemExit) as error_text:
        test_configs = fovConfigs(**fov_configs)
    assert (
        error_text.value.code
        == "ERROR: a default detector footprint is currently only provided for LSST and DES; please provide your own footprint file."
    )


@pytest.mark.parametrize("key_name", ["visits_query", "fill_factor", "circle_radius"])
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

    if key_name == "visits_query":
        fov_configs[key_name] = "sqlite query"

        with pytest.raises(SystemExit) as error_text:
            test_configs = fovConfigs(**fov_configs)
        reason = 'but camera model is not "visits_footprint".'
        assert error_text.value.code == f"ERROR: {key_name} supplied in config file {reason}"


@pytest.mark.parametrize("key_name", ["footprint_edge_threshold"])
def test_fovConfigs_camera_footprint_float(key_name):
    fov_configs = correct_fov_read.copy()
    fov_configs[key_name] = "ten"

    with pytest.raises(SystemExit) as error_text:
        test_configs = fovConfigs(**fov_configs)
        print(test_configs)
    assert (
        error_text.value.code
        == f"ERROR: expected a float for config parameter {key_name}. Check value in config file."
    )


# tests for camera_model = visits_footprint


@pytest.mark.parametrize("key_name", ["footprint_edge_threshold", "fill_factor", "circle_radius"])
def test_fovConfigs_visits_footprint_check_dont_exist(key_name):
    """
    Makes sure the code fails when using visits_footprint with keys
    """

    fov_configs = correct_fov.copy()
    fov_configs["survey_name"] = "DES"
    fov_configs["camera_model"] = "visits_footprint"

    fov_configs["visits_query"] = "something"
    fov_configs["footprint_edge_threshold"] = None

    fov_configs[key_name] = 1

    with pytest.raises(SystemExit) as error_text:
        test_configs = fovConfigs(**fov_configs)
    if key_name == "footprint_edge_threshold":
        assert (
            error_text.value.code
            == f"ERROR: {key_name} supplied in config file But visits footprint does not use edge threshold"
        )
    else:
        assert (
            error_text.value.code
            == f'ERROR: {key_name} supplied in config file but camera model is not "circle".'
        )


def test_fovConfigs_visits_footprint_check_exist():
    fov_configs = correct_fov.copy()
    fov_configs["survey_name"] = "DES"
    fov_configs["camera_model"] = "visits_footprint"

    fov_configs["footprint_edge_threshold"] = None
    fov_configs["visits_query"] = None

    with pytest.raises(SystemExit) as error_text:
        test_configs = fovConfigs(**fov_configs)
    assert (
        error_text.value.code
        == "ERROR: No value found for required key visits_query in config file. Please check the file and try again."
    )


def test_fovConfigs_visits_footprint_wrong_survey():
    """
    tests the check_survey_name_list error out in visits_footprint. If a none compatible survey is selected then error out.
    """
    fov_configs = correct_fov.copy()
    fov_configs["survey_name"] = "bad_survey"
    fov_configs["camera_model"] = "visits_footprint"
    fov_configs["footprint_edge_threshold"] = None
    fov_configs["visits_query"] = "something"

    with pytest.raises(SystemExit) as error_text:
        test_configs = fovConfigs(**fov_configs)
    assert (
        error_text.value.code
        == "ERROR: value bad_survey for config parameter survey_name when camera_model = visits_footprint not recognised. Expecting one of: ['DES', 'des']."
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


@pytest.mark.parametrize("key_name", ["footprint_edge_threshold", "visits_query"])
def test_fovConfigs_camera_circle_notrequired(key_name):
    """
    This loops through the not required keys and makes sure the code fails correctly when they're truthy
    """

    fov_configs = correct_fov_read.copy()
    fov_configs["camera_model"] = "circle"
    fov_configs["fill_factor"] = 0.5
    fov_configs[key_name] = "value"
    with pytest.raises(SystemExit) as error_text:
        test_configs = fovConfigs(**fov_configs)
    assert (
        error_text.value.code
        == f'ERROR: footprint_edge_threshold supplied in config file but camera model is not "footprint".'
    )
