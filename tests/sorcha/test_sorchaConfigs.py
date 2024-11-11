import pytest

from sorcha.utilities.dataUtilitiesForTests import get_demo_filepath
from sorcha.utilities.sorchaConfigs import sorchaConfigs, inputConfigs, simulationConfigs, filtersConfigs,phasecurvesConfigs ,fadingfunctionConfigs

# these are the results we expect from sorcha_config_demo.ini
correct_inputs = {
    "ephemerides_type": "ar",
    "eph_format": "csv",
    "size_serial_chunk": 5000,
    "aux_format": "whitespace",
    "pointing_sql_query": "SELECT observationId, observationStartMJD as observationStartMJD_TAI, visitTime, visitExposureTime, filter, seeingFwhmGeom as seeingFwhmGeom_arcsec, seeingFwhmEff as seeingFwhmEff_arcsec, fiveSigmaDepth as fieldFiveSigmaDepth_mag , fieldRA as fieldRA_deg, fieldDec as fieldDec_deg, rotSkyPos as fieldRotSkyPos_deg FROM observations order by observationId",
}
correct_simulation= {
    "ar_ang_fov" : 2.06,
    "ar_fov_buffer" : 0.2,
    "ar_picket" : 1,
    "ar_obs_code" : "X05",
    "ar_healpix_order" : 6
    }

correct_filters= {
    "observing_filters" : "r,g,i,z,u,y",
    "survey_name" : "rubin_sim"

}
correct_filters_read= {
    "observing_filters" : ['r','g','i','z','u','y'],
    "survey_name" : "rubin_sim"

}

correct_phasecurve= {"phase_function": "HG"}

correct_fadingfunction = {
    "fading_function_on" : True,
    "fading_function_width" : 0.1,
    "fading_function_peak_efficiency" : 1.
}


def test_sorchaConfigs():
    # general test to make sure, overall, everything works. checks just one file: sorcha_config_demo.ini

    config_file_location = get_demo_filepath("sorcha_config_demo.ini")
    test_configs = sorchaConfigs(config_file_location,'rubin_sim')

    # check each section to make sure you get what you expect
    assert correct_inputs == test_configs.inputs.__dict__
    assert correct_simulation == test_configs.simulation.__dict__
    assert correct_filters_read == test_configs.filters.__dict__
    assert correct_phasecurve == test_configs.phasecurve.__dict__
    assert correct_fadingfunction == test_configs.fadingfunction.__dict__

def test_inputConfigs():

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
    # this loops through the mandatory keys and makes sure the code fails correctly when each is missing

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
    # this loops through the inputs keys that need to have one of several set values and makes sure the correct error message triggers when they're not

    input_configs = correct_inputs.copy()

    input_configs[key_name] = "definitely_fake_bad_key"

    with pytest.raises(SystemExit) as error_text:
        test_configs = inputConfigs(**input_configs)

    assert (
        error_text.value.code
        == f"ERROR: value definitely_fake_bad_key for config parameter {key_name} not recognised. Expecting one of: {expected_list}."
    )


def test_filtersConfigs():

    filters_configs=correct_filters.copy()

    test_configs= filtersConfigs(**filters_configs)
    assert test_configs.__dict__ == correct_filters_read
    
    filters_configs["observing_filters"]='a,f,u,g'
    with pytest.raises(SystemExit) as error_text:
        test_configs = filtersConfigs(**filters_configs)
    assert (error_text.value.code == "ERROR: Filter(s) ['a' 'f'] given in config file are not recognised filters for rubin_sim survey.")

@pytest.mark.parametrize(
    "key_name", ["observing_filters","survey_name"] )
def test_filtersConfigs_mandatory(key_name):
    # this loops through the mandatory keys and makes sure the code fails correctly when each is missing

    filter_configs = correct_filters.copy()
    del filter_configs[key_name]

    with pytest.raises(SystemExit) as error_text:
        test_configs = filtersConfigs(**filter_configs)

    assert (
        error_text.value.code
        == f"ERROR: No value found for required key {key_name} in config file. Please check the file and try again."
    )

def test_simulationConfigs():

    simulation_configs=correct_simulation.copy()
    test_configs= simulationConfigs(**simulation_configs)
    assert test_configs.__dict__ == simulation_configs
    
    simulation_configs["ar_picket"]="one"

    with pytest.raises(SystemExit) as error_text:
        test_configs = simulationConfigs(**simulation_configs)
    
    assert (error_text.value.code == "ERROR: expected an int for config parameter ar_picket. Check value in config file.")

@pytest.mark.parametrize(
    "key_name", ["ar_ang_fov" , "ar_fov_buffer", "ar_picket", "ar_obs_code", "ar_healpix_order"])
def test_simulationConfigs_mandatory(key_name):
    # this loops through the mandatory keys and makes sure the code fails correctly when each is missing

    simulation_configs = correct_simulation.copy()

    del simulation_configs[key_name]

    with pytest.raises(SystemExit) as error_text:
        test_configs = simulationConfigs(**simulation_configs)

    assert (
        error_text.value.code
        == f"ERROR: No value found for required key {key_name} in config file. Please check the file and try again."
    )



def test_phasecurevConfigs():

    phasecurve_configs=correct_phasecurve.copy()
    test_configs= phasecurvesConfigs(**phasecurve_configs)
    assert test_configs.__dict__ == phasecurve_configs
    
    phasecurve_configs["phase_function"]=10

    with pytest.raises(SystemExit) as error_text:
        test_configs = phasecurvesConfigs(**phasecurve_configs)
    
    assert (error_text.value.code == "ERROR: value 10 for config parameter phase_function not recognised. Expecting one of: ['HG', 'HG1G2', 'HG12', 'linear', 'none'].")




@pytest.mark.parametrize(
    "key_name", ["phase_function"] )
def test_phasecurveConfigs_mandatory(key_name):
    # this loops through the mandatory keys and makes sure the code fails correctly when each is missing

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
    [
        ("phase_function", "['HG', 'HG1G2','HG12','linear','none']")
    ],
)
def test_phasecurveConfigs_inlist(key_name, expected_list):
    # this loops through the inputs keys that need to have one of several set values and makes sure the correct error message triggers when they're not

    phasecurve_configs = correct_phasecurve.copy()

    phasecurve_configs[key_name] = "definitely_fake_bad_key"

    with pytest.raises(SystemExit) as error_text:
        test_configs = phasecurvesConfigs(**phasecurve_configs)

    assert (
        error_text.value.code
        == f"ERROR: value definitely_fake_bad_key for config parameter {key_name} not recognised. Expecting one of: {expected_list}."
    )

def test_fadingfunctionConfig():

    fadingfunction_configs=correct_fadingfunction.copy()
    test_configs= fadingfunctionConfigs(**fadingfunction_configs)
    assert test_configs.__dict__ == fadingfunction_configs
    
    fadingfunction_configs["fading_function_width"] = 'ten'
    with pytest.raises(SystemExit) as error_text:
        test_configs = fadingfunctionConfigs(**fadingfunction_configs)
    
    assert (error_text.value.code == "ERROR: expected a float for config parameter fading_function_width. Check value in config file.")

    fadingfunction_configs=correct_fadingfunction.copy()
    test_configs= fadingfunctionConfigs(**fadingfunction_configs)
    assert test_configs.__dict__ == fadingfunction_configs
    
    fadingfunction_configs["fading_function_on"] = 'ten'
    with pytest.raises(SystemExit) as error_text:
        test_configs = fadingfunctionConfigs(**fadingfunction_configs)
    
    assert (error_text.value.code == "ERROR: expected a bool for config parameter fading_function_on. Check value in config file.")

    fadingfunction_configs=correct_fadingfunction.copy()
    test_configs= fadingfunctionConfigs(**fadingfunction_configs)
    assert test_configs.__dict__ == fadingfunction_configs
    #testing it will correctly reject fading_function_width and fading_function_peak_efficiency
    fadingfunction_configs["fading_function_on"] = "False"
    with pytest.raises(SystemExit) as error_text:
        test_configs = fadingfunctionConfigs(**fadingfunction_configs)
    assert (error_text.value.code == "ERROR: fading_function_width supplied in config file but fading_function_on is False.")

@pytest.mark.parametrize(
    "key_name", ["fading_function_on","fading_function_width","fading_function_peak_efficiency"] )
def test_fadingfunction_mandatory(key_name):
    # this loops through the mandatory keys and makes sure the code fails correctly when each is missing

    fadingfunction_configs = correct_fadingfunction.copy()

    del fadingfunction_configs[key_name]

    with pytest.raises(SystemExit) as error_text:
        test_configs = fadingfunctionConfigs(**fadingfunction_configs)

    assert (
        error_text.value.code
        == f"ERROR: No value found for required key {key_name} in config file. Please check the file and try again."
    )

@pytest.mark.parametrize(
    "key_name", ["fading_function_width","fading_function_peak_efficiency"] )
def test_fadingfunction_notrequired(key_name):
# tests that "fading_function_width" and "fading_function_peak_efficiency" are not called when "fading_function_on" is false
    fadingfunction_configs = correct_fadingfunction.copy()
    fadingfunction_configs["fading_function_on"]= "False"
    fadingfunction_configs["fading_function_width"] = 0
    fadingfunction_configs["fading_function_peak_efficiency"] = 0
    fadingfunction_configs[key_name]=0.5
    with pytest.raises(SystemExit) as error_text:
        test_configs = fadingfunctionConfigs(**fadingfunction_configs)
    assert (
        error_text.value.code
        == f"ERROR: {key_name} supplied in config file but fading_function_on is False."
    )

@pytest.mark.parametrize(
    "key_name", ["fading_function_width","fading_function_peak_efficiency"] )
def test_fadingfunction_outofbounds(key_name):
    fadingfunction_configs = correct_fadingfunction.copy()
    fadingfunction_configs[key_name]=10
    if key_name =="fading_function_width":
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
        == "ERROR: fading_function_peak_efficiency out of bounds. Must be between 0 and 1.")
