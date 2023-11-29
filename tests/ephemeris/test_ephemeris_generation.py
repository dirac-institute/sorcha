import pandas as pd
import pytest
import os
import re

from sorcha.utilities.dataUtilitiesForTests import get_test_filepath, get_demo_filepath
from sorcha.modules.PPConfigParser import PPConfigFileParser
from sorcha.utilities.sorchaArguments import sorchaArguments
from sorcha.ephemeris.simulation_driver import create_ephemeris
from sorcha.modules.PPReadPointingDatabase import PPReadPointingDatabase
from sorcha.ephemeris.simulation_setup import precompute_pointing_information


@pytest.fixture
def single_synthetic_pointing():
    data = [
        "6",
        "CART",
        2.1104488106737045,
        2.243673193848455,
        -0.584288362126351,
        -0.0069432745240377,
        0.006600241186202,
        -0.0005961942865623,
        54800.0,
    ]

    cols = [
        "ObjID",
        "FORMAT",
        "x",
        "y",
        "z",
        "xdot",
        "ydot",
        "zdot",
        "epochMJD_TDB",
    ]

    orbit_df = pd.DataFrame([data], columns=cols)
    return orbit_df


def test_ephemeris_end2end(single_synthetic_pointing, tmp_path):
    cmd_args_dict = {
        "paramsinput": get_test_filepath("PPReadAllInput_params.txt"),
        "orbinfile": get_test_filepath("PPReadAllInput_orbits.des"),
        "configfile": get_test_filepath("test_ephem_config.ini"),
        "pointing_database": get_demo_filepath("baseline_v2.0_1yr.db"),
        "outpath": tmp_path,
        "makeTemporaryEphemerisDatabase": False,
        "readTemporaryEphemerisDatabase": False,
        "deleteTemporaryEphemerisDatabase": False,
        "surveyname": "LSST",
        "outfilestem": f"out_400k",
        "verbose": False,
    }
    args = sorchaArguments(cmd_args_dict)

    configs = PPConfigFileParser(
        args.configfile,
        args.surveyname,
    )
    configs["seed"] = 24601

    filterpointing = PPReadPointingDatabase(
        args.pointing_database, configs["observing_filters"], configs["pointing_sql_query"], "lsst"
    )

    filterpointing = precompute_pointing_information(filterpointing, args, configs)

    observations = create_ephemeris(
        single_synthetic_pointing,
        filterpointing,
        args,
        configs,
    )

    assert len(observations) == 10

    # ensure no ephemeris file is written
    files = os.listdir(tmp_path)
    assert len(files) == 2

    for file in files:
        assert not re.match(r".+\.csv", file)
