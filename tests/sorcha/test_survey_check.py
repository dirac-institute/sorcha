from sorcha.utilities.survey_check import check_available_survey_configs
import pytest 


def test_all_error_out():

    expected_survey = "all"

    survey_name ="fake_survey"
    with pytest.raises(SystemExit) as error_text:
            check_available_survey_configs(survey_name,expected_survey)
    assert error_text.value.code == "ERROR: Survey name {} not recognised. Current allowed surveys are: {}".format(survey_name,
                    ["rubin_sim", "RUBIN_SIM", "des", "DES"])
    

    survey_name ="des"
    ans = check_available_survey_configs(survey_name,expected_survey)
    assert ans == True


def test_check_available_survey_configs():

    expected_survey = "des"
    bool_output = check_available_survey_configs("des",expected_survey)
    assert bool_output == True
    bool_output = check_available_survey_configs("fake_survey",expected_survey)
    assert bool_output == False

    expected_survey = "rubin"
    bool_output = check_available_survey_configs("rubin_sim",expected_survey)
    assert bool_output == True
    bool_output = check_available_survey_configs("lsst",expected_survey)
    assert bool_output == True
    bool_output = check_available_survey_configs("des",expected_survey)
    assert bool_output == False

    expected_survey = "rubin_sim"
    bool_output = check_available_survey_configs("rubin_sim",expected_survey)
    assert bool_output == True
    bool_output = check_available_survey_configs("lsst",expected_survey)
    assert bool_output == False

    expected_survey = "lsst"
    bool_output = check_available_survey_configs("rubin_sim",expected_survey)
    assert bool_output == False
    bool_output = check_available_survey_configs("lsst",expected_survey)
    assert bool_output == True
