import pandas as pd
import pytest
import os
import re
from numpy.testing import assert_almost_equal

from sorcha.utilities.dataUtilitiesForTests import get_test_filepath, get_demo_filepath
from sorcha.modules.PPGetLogger import PPGetLogger
from sorcha.utilities.sorchaArguments import sorchaArguments
from sorcha.ephemeris.simulation_driver import create_ephemeris, write_out_ephemeris_file
from sorcha.modules.PPReadPointingDatabase import PPReadPointingDatabase
from sorcha.ephemeris.simulation_setup import precompute_pointing_information
from sorcha.utilities.sorchaConfigs import sorchaConfigs, inputConfigs

from sorcha.readers.CombinedDataReader import CombinedDataReader
from sorcha.readers.EphemerisReader import EphemerisDataReader
from sorcha.readers.OrbitAuxReader import OrbitAuxReader
from sorcha.readers.CSVReader import CSVDataReader


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


@pytest.fixture
def single_synthetic_ephemeris():
    test_columns = [
        "ObjID",
        "FieldID",
        "fieldMJD_TAI",
        "fieldJD_TDB",
        "Range_LTC_km",
        "RangeRate_LTC_km_s",
        "RA_deg",
        "RARateCosDec_deg_day",
        "Dec_deg",
        "DecRate_deg_day",
        "Obj_Sun_x_LTC_km",
        "Obj_Sun_y_LTC_km",
        "Obj_Sun_z_LTC_km",
        "Obj_Sun_vx_LTC_km_s",
        "Obj_Sun_vy_LTC_km_s",
        "Obj_Sun_vz_LTC_km_s",
        "Obs_Sun_x_km",
        "Obs_Sun_y_km",
        "Obs_Sun_z_km",
        "Obs_Sun_vx_km_s",
        "Obs_Sun_vy_km_s",
        "Obs_Sun_vz_km_s",
        "phase_deg",
    ]

    test_values = [
        "2011_OB60",
        5733,
        60225.24582325162,
        2460225.746195981,
        5381399097.909393,
        8.908414821478392,
        1.9825876962618303,
        -0.0191044821690265,
        -11.895484353185031,
        -0.0081342233832118,
        5407508563.223875,
        216228178.85654888,
        -1094496739.3655145,
        -0.4862284491111358,
        6.195354508632129,
        0.94651384123983,
        144825951.4905347,
        34052525.78312281,
        14755265.621108454,
        -8.095015184421166,
        26.71219251349756,
        11.435360510921036,
        0.5514514639167444,
    ]

    test_ephemeris = pd.DataFrame([test_values], columns=test_columns)

    return test_ephemeris


def test_ephemeris_end2end(single_synthetic_pointing, tmp_path):
    cmd_args_dict = {
        "paramsinput": get_test_filepath("PPReadAllInput_params.txt"),
        "orbinfile": get_test_filepath("PPReadAllInput_orbits.des"),
        "configfile": get_test_filepath("test_ephem_config.ini"),
        "pointing_database": get_demo_filepath("baseline_v2.0_1yr.db"),
        "outpath": tmp_path,
        "surveyname": "rubin_sim",
        "outfilestem": f"out_400k",
        "loglevel": False,
        "stats": None,
    }

    pplogger = PPGetLogger(cmd_args_dict["outpath"], "test_log")
    args = sorchaArguments(cmd_args_dict)

    configs = sorchaConfigs(
        args.configfile,
        args.surveyname,
    )
    # configs["seed"] = 24601

    filterpointing = PPReadPointingDatabase(
        args.pointing_database,
        configs.filters.observing_filters,
        configs.input.pointing_sql_query,
        "rubin_sim",
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

    configs["ar_use_integrate"] = True

    observations_integrate = create_ephemeris(
        single_synthetic_pointing,
        filterpointing,
        args,
        configs,
    )

    assert len(observations_integrate) == 10

    assert_almost_equal(
        observations_integrate["fieldMJD_TAI"].values, observations["fieldMJD_TAI"].values, decimal=6
    )
    assert_almost_equal(observations_integrate["RA_deg"].values, observations["RA_deg"].values, decimal=6)
    assert_almost_equal(observations_integrate["Dec_deg"].values, observations["Dec_deg"].values, decimal=6)


def test_ephemeris_writeread_csv(single_synthetic_ephemeris, tmp_path):
    """Tests to ensure the ephemeris file is written out correctly AND
    can be read back in by Sorcha. CSV version.
    """

    orb_in = get_demo_filepath("sspp_testset_orbits.des")
    params_in = get_demo_filepath("sspp_testset_colours.txt")

    class args(object):
        loglevel = False

    cmd_args = args()

    correct_inputs = {
        "ephemerides_type": "ar",
        "eph_format": "csv",
        "size_serial_chunk": 5000,
        "aux_format": "whitespace",
        "pointing_sql_query": "SELECT observationId, observationStartMJD as observationStartMJD_TAI, visitTime, visitExposureTime, filter, seeingFwhmGeom as seeingFwhmGeom_arcsec, seeingFwhmEff as seeingFwhmEff_arcsec, fiveSigmaDepth as fieldFiveSigmaDepth_mag , fieldRA as fieldRA_deg, fieldDec as fieldDec_deg, rotSkyPos as fieldRotSkyPos_deg FROM observations order by observationId",
    }
    configs = inputConfigs(**correct_inputs)
    setattr(configs, "input", configs)

    out_path = os.path.join(tmp_path, "test_ephem_out")

    write_out_ephemeris_file(single_synthetic_ephemeris, out_path, cmd_args, configs)

    reader = CombinedDataReader(ephem_primary=True, verbose=False)
    reader.add_ephem_reader(EphemerisDataReader(out_path + ".csv", "csv"))
    reader.add_aux_data_reader(OrbitAuxReader(orb_in, "whitespace"))
    reader.add_aux_data_reader(CSVDataReader(params_in, "whitespace"))

    observations = reader.read_block(1)

    assert len(observations) == 1
    assert len(observations.columns) == 37


def test_ephemeris_writeread_whitespace(single_synthetic_ephemeris, tmp_path):
    """Tests to ensure the ephemeris file is written out correctly AND
    can be read back in by Sorcha. Whitespaced CSV version.
    """

    orb_in = get_demo_filepath("sspp_testset_orbits.des")
    params_in = get_demo_filepath("sspp_testset_colours.txt")

    class args(object):
        loglevel = False

    cmd_args = args()

    correct_inputs = {
        "ephemerides_type": "ar",
        "eph_format": "whitespace",
        "size_serial_chunk": 5000,
        "aux_format": "whitespace",
        "pointing_sql_query": "SELECT observationId, observationStartMJD as observationStartMJD_TAI, visitTime, visitExposureTime, filter, seeingFwhmGeom as seeingFwhmGeom_arcsec, seeingFwhmEff as seeingFwhmEff_arcsec, fiveSigmaDepth as fieldFiveSigmaDepth_mag , fieldRA as fieldRA_deg, fieldDec as fieldDec_deg, rotSkyPos as fieldRotSkyPos_deg FROM observations order by observationId",
    }
    configs = inputConfigs(**correct_inputs)
    setattr(configs, "input", configs)

    out_path = os.path.join(tmp_path, "test_ephem_out_whitespace")

    write_out_ephemeris_file(single_synthetic_ephemeris, out_path, cmd_args, configs)

    reader = CombinedDataReader(ephem_primary=True, verbose=False)
    reader.add_ephem_reader(EphemerisDataReader(out_path + ".csv", "whitespace"))
    reader.add_aux_data_reader(OrbitAuxReader(orb_in, "whitespace"))
    reader.add_aux_data_reader(CSVDataReader(params_in, "whitespace"))

    observations = reader.read_block(1)

    assert len(observations) == 1
    assert len(observations.columns) == 37


def test_ephemeris_writeread_hdf5(single_synthetic_ephemeris, tmp_path):
    """Tests to ensure the ephemeris file is written out correctly AND
    can be read back in by Sorcha. HDF5 version.
    """

    orb_in = get_demo_filepath("sspp_testset_orbits.des")
    params_in = get_demo_filepath("sspp_testset_colours.txt")

    class args(object):
        loglevel = False

    cmd_args = args()

    correct_inputs = {
        "ephemerides_type": "ar",
        "eph_format": "hdf5",
        "size_serial_chunk": 5000,
        "aux_format": "whitespace",
        "pointing_sql_query": "SELECT observationId, observationStartMJD as observationStartMJD_TAI, visitTime, visitExposureTime, filter, seeingFwhmGeom as seeingFwhmGeom_arcsec, seeingFwhmEff as seeingFwhmEff_arcsec, fiveSigmaDepth as fieldFiveSigmaDepth_mag , fieldRA as fieldRA_deg, fieldDec as fieldDec_deg, rotSkyPos as fieldRotSkyPos_deg FROM observations order by observationId",
    }
    configs = inputConfigs(**correct_inputs)
    setattr(configs, "input", configs)

    out_path = os.path.join(tmp_path, "test_ephem_out_h5")

    write_out_ephemeris_file(single_synthetic_ephemeris, out_path, cmd_args, configs)

    reader = CombinedDataReader(ephem_primary=True, verbose=False)
    reader.add_ephem_reader(EphemerisDataReader(out_path + ".h5", "hdf5"))
    reader.add_aux_data_reader(OrbitAuxReader(orb_in, "whitespace"))
    reader.add_aux_data_reader(CSVDataReader(params_in, "whitespace"))

    observations = reader.read_block(1)

    assert len(observations) == 1
    assert len(observations.columns) == 37
