# dict of surveys for a given option, These are currently used in fov,  filters , expert  configs
# Where the type of survey matters for running Sorcha (i.e. camera footprint, filters and certain features turned off)

DICT_SURVEY_NAMES = {
    "rubin": ["rubin_sim", "lsst"],  # rubin is used for any overall rubin process.
    "rubin_sim": ["rubin_sim"],  # for rubin_sim funcitons
    "lsst": ["lsst"],  # for lsst function
    "des": ["des"],  # for des fucntions.
}  # clean up comments and explain better detail.


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
