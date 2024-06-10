import numpy as np
import pandas as pd
from sorcha.utilities.dataUtilitiesForTests import get_test_filepath, get_demo_filepath
from sorcha.modules.PPConfigParser import PPConfigFileParser
from sorcha.modules.PPGetLogger import PPGetLogger
from sorcha.utilities.sorchaArguments import sorchaArguments
from sorcha.modules.PPReadPointingDatabase import PPReadPointingDatabase
from sorcha.ephemeris.simulation_setup import (
    precompute_pointing_information,
    create_assist_ephemeris,
    generate_simulations,
    furnish_spiceypy,
)
from sorcha.ephemeris.pixel_dict import PixelDict
from sorcha.ephemeris.simulation_parsing import Observatory
from sorcha.ephemeris.simulation_geometry import ecliptic_to_equatorial, vec2ra_dec
from sorcha.ephemeris.simulation_constants import SPEED_OF_LIGHT, AU_KM


def test_pixeldict(tmp_path):
    # this test function will test out a bunch of different things inside
    # the PixelDict class
    # everything will be done inside this test function, because creating
    # the PixelDict class requires a lot of auxiliary stuff

    # copied from the end-to-end test, but modified for Barycentric coordinates
    data = [
        "6",
        "BCART",
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

    orbits_df = pd.DataFrame([data], columns=cols)

    cmd_args_dict = {
        "paramsinput": get_test_filepath("PPReadAllInput_params.txt"),
        "orbinfile": get_test_filepath("PPReadAllInput_orbits.des"),
        "configfile": get_test_filepath("test_ephem_config.ini"),
        "pointing_database": get_demo_filepath("baseline_v2.0_1yr.db"),
        "outpath": tmp_path,
        "makeTemporaryEphemerisDatabase": False,
        "readTemporaryEphemerisDatabase": False,
        "deleteTemporaryEphemerisDatabase": False,
        "surveyname": "rubin_sim",
        "outfilestem": f"out_400k",
        "verbose": False,
        "stats": None,
    }

    args = sorchaArguments(cmd_args_dict)

    configs = PPConfigFileParser(
        args.configfile,
        args.surveyname,
    )
    configs["seed"] = 24601

    filterpointing = PPReadPointingDatabase(
        args.pointing_database, configs["observing_filters"], configs["pointing_sql_query"], "rubin_sim"
    )

    filterpointing = precompute_pointing_information(filterpointing, args, configs)
    args = sorchaArguments(cmd_args_dict)

    ephem, gm_sun, gm_total = create_assist_ephemeris(args)
    furnish_spiceypy(args)

    sim_dict = generate_simulations(ephem, gm_sun, gm_total, orbits_df, args)
    observatory = Observatory(args=None, oc_file=get_test_filepath("ObsCodes_test.json"))

    pixdict = PixelDict(54800.0 + 2400000.5, sim_dict, ephem, "Z20", observatory, picket_interval=1, nside=32)

    # jpl computed Z20 position at the reference epoch
    X_obs = 3.670898068454065e-01
    Y_obs = 9.192335416877380e-01
    Z_obs = -4.184005038986956e-05
    r_obs = np.array([X_obs, Y_obs, Z_obs])

    # check if we're getting the right observatory position
    assert np.isclose(
        np.linalg.norm(pixdict.get_observatory_position(54800.0 + 2400000.5) - ecliptic_to_equatorial(r_obs)),
        0,
    )

    # let's compare the predicted ra/dec by hand
    # by first doing all operations manually and, when possible,
    # with externally computed quantities
    reference = np.array([orbits_df.x[0], orbits_df.y[0], orbits_df.z[0]])
    reference -= r_obs
    # do one newton step in the light-time correction
    lt = np.linalg.norm(reference) / SPEED_OF_LIGHT  # this is in days
    reference -= lt * np.array([orbits_df.xdot[0], orbits_df.ydot[0], orbits_df.zdot[0]])
    reference = ecliptic_to_equatorial(reference)
    reference /= np.linalg.norm(reference)

    # now let's query our object
    unit_vec = pixdict.interpolate_unit_vectors(pixdict.sim_dict.keys(), 54800.0 + 2400000.5)

    # note this also means that the predicted RA/Dec are equal
    assert np.isclose(np.linalg.norm(reference - unit_vec["6"]), 0)

    pixdict.compute_pixel_traversed()

    # computed directly
    pixels = [4432, 4433, 4434, 4435, 4436, 4437, 4438, 4439, 4440, 4441, 4444, 4445]

    # check if lists are subsets of each other
    crossed = []
    for i in pixdict.pixel_dict:
        assert i in pixels
        crossed.append(i)
    for i in pixels:
        assert i in crossed

    # use proper ra/dec to try and recover the object
    obj = pixdict.get_designations(54800.0 + 2400000.5, 39.81424, -0.18774, 2)

    assert "6" in obj

    # finally, let's test the Lagrange interpolation
    # with a really simple construction:
    # t = [-1, 0, 1] for the intervals, points computed at t_p = [-1,0,1]
    # therefore, the interpolation coefficients should be
    # just the Kronecker delta(t, t_p)

    Lm, L0, Lp = pixdict.get_interp_factors(-1, 0, 1, 3)
    assert Lm[0, 0] == 1
    assert L0[1, 0] == 1
    assert Lp[2, 0] == 1

    assert Lm[1, 0] == 0
    assert Lm[2, 0] == 0

    assert L0[0, 0] == 0
    assert L0[2, 0] == 0

    assert Lp[0, 0] == 0
    assert Lp[1, 0] == 0
