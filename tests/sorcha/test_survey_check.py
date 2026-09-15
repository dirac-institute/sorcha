from sorcha.utilities.survey_check import check_survey_in_available_config


def test_check_survey_in_available_config():

    expected_survey = "des"
    bool_output = check_survey_in_available_config("des",expected_survey)
    assert bool_output == True
    bool_output = check_survey_in_available_config("fake_survey",expected_survey)
    assert bool_output == False

    expected_survey = "rubin"
    bool_output = check_survey_in_available_config("rubin_sim",expected_survey)
    assert bool_output == True
    bool_output = check_survey_in_available_config("lsst",expected_survey)
    assert bool_output == True
    bool_output = check_survey_in_available_config("des",expected_survey)
    assert bool_output == False

    expected_survey = "rubin_sim"
    bool_output = check_survey_in_available_config("rubin_sim",expected_survey)
    assert bool_output == True
    bool_output = check_survey_in_available_config("lsst",expected_survey)
    assert bool_output == False

    expected_survey = "lsst"
    bool_output = check_survey_in_available_config("rubin_sim",expected_survey)
    assert bool_output == False
    bool_output = check_survey_in_available_config("lsst",expected_survey)
    assert bool_output == True
