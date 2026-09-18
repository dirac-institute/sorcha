import pytest

from sorcha.configs.filtersConfigs import filtersConfigs

correct_filters_read = {"observing_filters": "r,g,i,z,u,y", "survey_name": "rubin_sim"}
correct_filters_read_des = {"observing_filters": "r,g,i,z,Y", "survey_name": "des"}

correct_filters = {
    "observing_filters": ["r", "g", "i", "z", "u", "y"],
    "survey_name": "rubin_sim",
    "mainfilter": None,
    "othercolours": None,
}

correct_filters_des = {
    "observing_filters": ["r", "g", "i", "z", "Y"],
    "survey_name": "des",
    "mainfilter": None,
    "othercolours": None,
}


# filters config test


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


def test_filtersConfigs_check_filters_rubin():
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


def test_filtersConfigs_check_filters_des():
    filters_configs = correct_filters_read_des.copy()
    test_configs = filtersConfigs(**filters_configs)
    assert test_configs.__dict__ == correct_filters_des

    filters_configs["observing_filters"] = "a,f,u,g"
    with pytest.raises(SystemExit) as error_text:
        test_configs = filtersConfigs(**filters_configs)
    assert (
        error_text.value.code
        == "ERROR: Filter(s) ['a' 'f' 'u'] given in config file are not recognised filters for des survey."
    )
