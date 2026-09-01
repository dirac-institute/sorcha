from sorcha.utilities.survey_constants import DICT_SURVEY_NAMES


def is_survey_valid(survey_name, expected_survey):
    """
    Passes arguments that match the expected survey into if statements in config classes

    Parameters
    ------------

    survey_name : str
        The name of the survey.

    expected_survey: str
        Checks survey_name is in given list in dict (options are ["rubin", "des","rubin_sim","lsst"]).

    Returns
    ---------
    boolen

    """

    return survey_name in DICT_SURVEY_NAMES[expected_survey]
