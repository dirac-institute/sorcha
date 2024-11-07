import pytest

from sorcha.utilities.dataUtilitiesForTests import get_demo_filepath
from sorcha.utilities.sorchaConfigs import sorchaConfigs, inputConfigs

# these are the results we expect from sorcha_config_demo.ini
correct_inputs =     {'ephemerides_type': 'ar',
                     'eph_format': 'csv',
                     'size_serial_chunk': 5000,
                     'aux_format': 'whitespace',
                     'pointing_sql_query': 'SELECT observationId, observationStartMJD as observationStartMJD_TAI, visitTime, visitExposureTime, filter, seeingFwhmGeom as seeingFwhmGeom_arcsec, seeingFwhmEff as seeingFwhmEff_arcsec, fiveSigmaDepth as fieldFiveSigmaDepth_mag , fieldRA as fieldRA_deg, fieldDec as fieldDec_deg, rotSkyPos as fieldRotSkyPos_deg FROM observations order by observationId'}

def test_sorchaConfigs():
    # general test to make sure, overall, everything works. checks just one file: sorcha_config_demo.ini

    config_file_location = get_demo_filepath("sorcha_config_demo.ini")
    test_configs = sorchaConfigs(config_file_location)
    
    # check each section to make sure you get what you expect
    assert correct_inputs == test_configs.inputs.__dict__

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

@pytest.mark.parametrize("key_name", ["ephemerides_type", "eph_format", "size_serial_chunk", "aux_format", "pointing_sql_query"])
def test_inputConfigs_mandatory(key_name):
    # this loops through the mandatory keys and makes sure the code fails correctly when each is missing

    input_configs = correct_inputs.copy()

    del input_configs[key_name]
    
    with pytest.raises(SystemExit) as error_text:
        test_configs = inputConfigs(**input_configs)
    
    assert error_text.value.code == f"ERROR: No value found for required key {key_name} in config file. Please check the file and try again."


@pytest.mark.parametrize("key_name, expected_list", [("ephemerides_type", "['ar', 'external']"), ("aux_format", "['comma', 'whitespace', 'csv']"), ("eph_format", "['csv', 'whitespace', 'hdf5']")])
def test_inputConfigs_inlist(key_name, expected_list):
    # this loops through the inputs keys that need to have one of several set values and makes sure the correct error message triggers when they're not
    
    input_configs = correct_inputs.copy()
    
    input_configs[key_name] = "definitely_fake_bad_key"
    
    with pytest.raises(SystemExit) as error_text:
        test_configs = inputConfigs(**input_configs)
    
    assert error_text.value.code == f"ERROR: value definitely_fake_bad_key for config parameter {key_name} not recognised. Expecting one of: {expected_list}."
    