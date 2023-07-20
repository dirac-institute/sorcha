from sorcha.sorcha import runLSSTPostProcessing
from sorcha.utilities.dataUtilitiesForTests import get_demo_filepath, get_data_out_filepath

from os import path


def test_lsst_end2end():
    """run the full rubin sim to ensure there are no errors."""

    cmd_args_dict = {
        "paramsinput": get_demo_filepath("sspp_testset_colours.txt"),
        "orbinfile": get_demo_filepath("sspp_testset_orbits.des"),
        "oifoutput": get_demo_filepath("example_oif_output.txt"),
        "configfile": get_demo_filepath("PPConfig_test.ini"),
        "outpath": "./data/out",
        "makeTemporaryEphemerisDatabase": False,
        "readTemporaryEphemerisDatabase": False,
        "deleteTemporaryEphemerisDatabase": False,
        "surveyname": "LSST",
        "outfilestem": f"out_end2end",
        "verbose": False,
    }

    runLSSTPostProcessing(cmd_args_dict)

    out_path = get_data_out_filepath("out_end2end.csv")
    assert path.isfile(out_path)
