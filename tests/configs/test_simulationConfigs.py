import pytest
from sorcha.configs.simulationConfigs import simulationConfigs

correct_simulation = {
    "_ephemerides_type": "ar",
    "ar_ang_fov": 2.06,
    "ar_fov_buffer": 0.2,
    "ar_picket": 1,
    "ar_obs_code": "X05",
    "ar_healpix_order": 6,
    "ar_n_sub_intervals": 101,
}



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

