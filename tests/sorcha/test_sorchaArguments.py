import pytest

from sorcha.utilities.sorchaArguments import sorchaArguments
from sorcha.utilities.dataUtilitiesForTests import get_demo_filepath

cmd_args_dict = {
    "paramsinput": get_demo_filepath("sspp_testset_colours.txt"),
    "orbinfile": get_demo_filepath("sspp_testset_orbits.des"),
    "oifoutput": get_demo_filepath("example_oif_output.txt"),
    "configfile": get_demo_filepath("PPConfig_test.ini"),
    "outpath": "./data/out",
    "surveyname": "LSST",
    "outfilestem": f"out_end2end",
    "verbose": False,
    "pointing_database": get_demo_filepath("baseline_v2.0_1yr.db"),
}


def test_sorchaArguments():
    """make sure that valid args can be parsed"""
    args = sorchaArguments(cmd_args_dict)

    assert args.surveyname == "LSST"


def test_validate_arguments():
    """ensure we raise errors when appropriate"""

    args = sorchaArguments(cmd_args_dict)

    with pytest.raises(ValueError, match="paramsinput"):
        args.paramsinput = get_demo_filepath("sspp_testset_colors.txt")

        args.validate_arguments()

    args.paramsinput = get_demo_filepath("sspp_testset_colours.txt")

    with pytest.raises(ValueError, match="orbinfile"):
        args.orbinfile = get_demo_filepath("sspp_testset_orbitz.des")

        args.validate_arguments()

    args.orbinfile = get_demo_filepath("sspp_testset_orbits.des")

    with pytest.raises(ValueError, match="oifoutput"):
        args.oifoutput = get_demo_filepath("example_oif_output.txtttttt")

        args.validate_arguments()

    args.oifoutput = get_demo_filepath("example_oif_output.txt")

    with pytest.raises(ValueError, match="configfile"):
        args.configfile = get_demo_filepath("NOPE.txt")

        args.validate_arguments()

    args.configfile = get_demo_filepath("PPConfig_test.ini")

    args.validate_arguments()
