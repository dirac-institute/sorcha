import pytest

from sorcha.utilities.sorchaArguments import sorchaArguments
from sorcha.utilities.dataUtilitiesForTests import get_demo_filepath, get_test_filepath

cmd_args_dict = {
    "paramsinput": get_demo_filepath("sspp_testset_colours.txt"),
    "orbinfile": get_demo_filepath("sspp_testset_orbits.des"),
    "input_ephemeris_file": get_demo_filepath("example_ephem_output.txt"),
    "configfile": get_test_filepath("PPConfig_goldens_test.ini"),
    "outpath": "./tests/out",
    "surveyname": "RUBIN_SIM",
    "outfilestem": f"out_end2end",
    "loglevel": False,
    "pointing_database": get_demo_filepath("baseline_v2.0_1yr.db"),
    "stats": "./test.csv",
    "visits_database": None,
}


def test_sorchaArguments():
    """make sure that valid args can be parsed"""
    args = sorchaArguments(cmd_args_dict)

    assert args.surveyname == "RUBIN_SIM"


def test_validate_arguments():
    """ensure we raise errors when appropriate"""

    args = sorchaArguments(cmd_args_dict)

    with pytest.raises(ValueError):
        args.paramsinput = get_demo_filepath("sspp_testset_colors.txt")

        args.validate_arguments()

    args.paramsinput = get_demo_filepath("sspp_testset_colours.txt")

    with pytest.raises(ValueError):
        args.orbinfile = get_demo_filepath("sspp_testset_orbitz.des")

        args.validate_arguments()

    args.orbinfile = get_demo_filepath("sspp_testset_orbits.des")

    with pytest.raises(ValueError):
        args.input_ephemeris_file = get_demo_filepath("example_ephem_output.txtttttt")

        args.validate_arguments()

    args.input_ephemeris_file = get_demo_filepath("example_ephem_output.txt")

    with pytest.raises(ValueError):
        args.configfile = get_demo_filepath("NOPE.txt")

        args.validate_arguments()
