import pytest
from sorcha.utilities.dataUtilitiesForTests import get_demo_filepath

from sorcha.configs.sorchaConfigs import *

# these are the results we expect from sorcha_config_demo.ini, in there respective unit tests
from test_inputAndOutputConfigs import correct_inputs, correct_output
from test_ephemerisConfigs import correct_simulation
from test_filtersConfigs import correct_filters
from test_saturationConfigs import correct_saturation
from test_phasecurvesConfigs import correct_phasecurve
from test_fovConfigs import correct_fov
from test_fadingfunctionConfigs import correct_fadingfunction
from test_linkingfilterConfigs import correct_linkingfilter
from test_lightcurveAndActivityConfigs import correct_lc_model, correct_activity
from test_expertConfigs import correct_expert
from test_auxiliaryConfigs import correct_auxciliary_filenames, correct_auxciliary_URLs


# SORCHA Configs test


def test_sorchaConfigs():
    """
    tests that sorchaConfigs reads in config file correctly
    """
    # general test to make sure, overall, everything works. checks just one file: sorcha_config_demo.ini

    config_file_location = get_demo_filepath("sorcha_config_demo.ini")
    test_configs_file = sorchaConfigs(config_file_location, "rubin_sim")

    # test we can make a config without needing to read a file
    test_configs_nofile = basesorchaConfigs(
        survey_name="rubin_sim",
        input=inputConfigs(**correct_inputs),
        simulation=simulationConfigs(**correct_simulation),
        filters=filtersConfigs(**correct_filters),
        saturation=saturationConfigs(**correct_saturation),
        phasecurves=phasecurvesConfigs(**correct_phasecurve),
        fov=fovConfigs(**correct_fov),
        fadingfunction=fadingfunctionConfigs(**correct_fadingfunction),
        linkingfilter=linkingfilterConfigs(**correct_linkingfilter),
        output=outputConfigs(**correct_output),
        lightcurve=lightcurveConfigs(**correct_lc_model),
        activity=activityConfigs(**correct_activity),
        expert=expertConfigs(**correct_expert),
        auxiliary=auxiliaryConfigs(),
    )
    # check each section to make sure you get what you expect
    for test_configs in [test_configs_file, test_configs_nofile]:
        assert correct_inputs == test_configs.input.__dict__
        assert correct_simulation == test_configs.simulation.__dict__
        assert correct_filters == test_configs.filters.__dict__
        assert correct_saturation == test_configs.saturation.__dict__
        assert correct_phasecurve == test_configs.phasecurves.__dict__
        assert correct_fov == test_configs.fov.__dict__
        assert correct_fadingfunction == test_configs.fadingfunction.__dict__
        assert correct_linkingfilter == test_configs.linkingfilter.__dict__
        assert correct_output == test_configs.output.__dict__
        assert correct_lc_model == test_configs.lightcurve.__dict__
        assert correct_activity == test_configs.activity.__dict__
        assert correct_expert == test_configs.expert.__dict__
        assert correct_auxciliary_URLs == test_configs.auxiliary.__dict__["urls"]
        assert correct_auxciliary_filenames == test_configs.auxiliary.__dict__["data_file_list"]
