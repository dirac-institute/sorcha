from sorcha.utilities.survey_check import is_survey_valid


def test_is_survey_valid():

    expected_survey = "des"
    bool_output = is_survey_valid("des",expected_survey)
    assert bool_output == True
    bool_output = is_survey_valid("fake_survey",expected_survey)
    assert bool_output == False

    expected_survey = "rubin"
    bool_output = is_survey_valid("rubin_sim",expected_survey)
    assert bool_output == True
    bool_output = is_survey_valid("lsst",expected_survey)
    assert bool_output == True
    bool_output = is_survey_valid("des",expected_survey)
    assert bool_output == False

    expected_survey = "rubin_sim"
    bool_output = is_survey_valid("rubin_sim",expected_survey)
    assert bool_output == True
    bool_output = is_survey_valid("lsst",expected_survey)
    assert bool_output == False

    expected_survey = "lsst"
    bool_output = is_survey_valid("rubin_sim",expected_survey)
    assert bool_output == False
    bool_output = is_survey_valid("lsst",expected_survey)
    assert bool_output == True
