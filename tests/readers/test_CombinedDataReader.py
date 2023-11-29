import pytest
from numpy.testing import assert_equal

from sorcha.readers.CombinedDataReader import CombinedDataReader
from sorcha.readers.CSVReader import CSVDataReader
from sorcha.readers.OIFReader import OIFDataReader
from sorcha.readers.OrbitAuxReader import OrbitAuxReader
from sorcha.utilities.dataUtilitiesForTests import get_test_filepath


def test_CombinedDataReader():
    reader = CombinedDataReader()
    reader.add_ephem_reader(OIFDataReader(get_test_filepath("PPReadAllInput_oif.txt"), "csv"))
    reader.add_aux_data_reader(OrbitAuxReader(get_test_filepath("PPReadAllInput_orbits.des"), "whitespace"))
    reader.add_aux_data_reader(CSVDataReader(get_test_filepath("PPReadAllInput_params.txt"), "whitespace"))

    # Read the first 5 objects from the orbits file. This corresponds to 4 objects and 668 rows
    # in the ephemeris file.
    res_df = reader.read_block(block_size=5)
    assert len(res_df["ObjID"].unique().tolist()) == 4
    assert len(res_df) == 334

    # Check that the first line matches.
    expected_data = {
        "ObjID": "632",
        "FieldID": 38059,
        "FieldMJD_TAI": 60277.351867,
        "AstRange(km)": 983057302.988296,
        "AstRangeRate(km/s)": -27.914,
        "AstRA(deg)": 143.141481,
        "AstRARate(deg/day)": 0.024483,
        "AstDec(deg)": 8.677660,
        "AstDecRate(deg/day)": -0.022025,
        "Ast-Sun(J2000x)(km)": -718755527.053,
        "Ast-Sun(J2000y)(km)": 707115399.940,
        "Ast-Sun(J2000z)(km)": 202146766.832,
        "Ast-Sun(J2000vx)(km/s)": -9.461,
        "Ast-Sun(J2000vy)(km/s)": -9.435,
        "Ast-Sun(J2000vz)(km/s)": -3.858,
        "Obs-Sun(J2000x)(km)": 58803455.841,
        "Obs-Sun(J2000y)(km)": 124187416.914,
        "Obs-Sun(J2000z)(km)": 53827633.096,
        "Obs-Sun(J2000vx)(km/s)": -28.129,
        "Obs-Sun(J2000vy)(km/s)": 10.565,
        "Obs-Sun(J2000vz)(km/s)": 4.677,
        "Sun-Ast-Obs(deg)": 8.010336,
        "epochMJD_TDB": 54800.0,
        "t_p_MJD_TDB": 23466.22367,
        "argPeri": 284.5519,
        "node": 217.91073,
        "inc": 5.37133,
        "e": 0.4966,
        "q": 6.88417,
        "H_r": 14.23,
        "u-r": 1.72,
        "g-r": 0.48,
        "i-r": -0.11,
        "z-r": -0.12,
        "y-r": -0.12,
        "GS": 0.15,
        "FORMAT": "COM",
    }
    assert_equal(set(res_df.columns.values), set(expected_data.keys()))
    for col in expected_data.keys():
        assert expected_data[col] == res_df.iloc[0][col]

    # Read the next 5 objects from the orbits file. This corresponds to 5 objects and 334 rows
    # in the ephemeris file.
    res_df = reader.read_block(block_size=5)
    assert len(res_df["ObjID"].unique().tolist()) == 5
    assert len(res_df) == 334

    # Check that the id in the first row is '39262'
    assert res_df.iloc[0]["ObjID"] == "39262"

    # Any further reads will return None.
    res_df = reader.read_block(block_size=5)
    assert res_df is None


def test_CombinedDataReader_ephem():
    """Read with ephemeris as the primary key."""
    reader = CombinedDataReader(ephem_primary=True)
    reader.add_ephem_reader(OIFDataReader(get_test_filepath("PPReadAllInput_oif.txt"), "csv"))
    reader.add_aux_data_reader(OrbitAuxReader(get_test_filepath("PPReadAllInput_orbits.des"), "whitespace"))
    reader.add_aux_data_reader(CSVDataReader(get_test_filepath("PPReadAllInput_params.txt"), "whitespace"))

    # Read the first 200 rows from the ephemeris file which corresponds to the first three
    # object IDs.
    res_df = reader.read_block(block_size=200)
    assert len(res_df["ObjID"].unique().tolist()) == 3
    assert len(res_df) == 200

    # Check that the first line matches.
    expected_data = {
        "ObjID": "632",
        "FieldID": 38059,
        "FieldMJD_TAI": 60277.351867,
        "AstRange(km)": 983057302.988296,
        "AstRangeRate(km/s)": -27.914,
        "AstRA(deg)": 143.141481,
        "AstRARate(deg/day)": 0.024483,
        "AstDec(deg)": 8.677660,
        "AstDecRate(deg/day)": -0.022025,
        "Ast-Sun(J2000x)(km)": -718755527.053,
        "Ast-Sun(J2000y)(km)": 707115399.940,
        "Ast-Sun(J2000z)(km)": 202146766.832,
        "Ast-Sun(J2000vx)(km/s)": -9.461,
        "Ast-Sun(J2000vy)(km/s)": -9.435,
        "Ast-Sun(J2000vz)(km/s)": -3.858,
        "Obs-Sun(J2000x)(km)": 58803455.841,
        "Obs-Sun(J2000y)(km)": 124187416.914,
        "Obs-Sun(J2000z)(km)": 53827633.096,
        "Obs-Sun(J2000vx)(km/s)": -28.129,
        "Obs-Sun(J2000vy)(km/s)": 10.565,
        "Obs-Sun(J2000vz)(km/s)": 4.677,
        "Sun-Ast-Obs(deg)": 8.010336,
        "epochMJD_TDB": 54800.0,
        "t_p_MJD_TDB": 23466.22367,
        "argPeri": 284.5519,
        "node": 217.91073,
        "inc": 5.37133,
        "e": 0.4966,
        "q": 6.88417,
        "H_r": 14.23,
        "u-r": 1.72,
        "g-r": 0.48,
        "i-r": -0.11,
        "z-r": -0.12,
        "y-r": -0.12,
        "GS": 0.15,
        "FORMAT": "COM",
    }
    assert_equal(set(res_df.columns.values), set(expected_data.keys()))
    for col in expected_data.keys():
        assert expected_data[col] == res_df.iloc[0][col]

    # Read the next 10 rows from the ephemeris file.
    res_df = reader.read_block(block_size=50, ephem_primary=True)
    assert len(res_df["ObjID"].unique().tolist()) == 1
    assert len(res_df) == 50

    # Check that the id in the first row is still '12733' and
    # FieldMJD_TAI == 60325.354511.
    assert res_df.iloc[0]["ObjID"] == "12733"
    assert res_df.iloc[0]["FieldMJD_TAI"] == pytest.approx(60325.354511)

    # We fail if we try to set the ephem reader a second time.
    with pytest.raises(SystemExit) as err:
        reader.add_ephem_reader(OIFDataReader(get_test_filepath("PPReadAllInput_oif.txt"), "csv"))
    assert err.type == SystemExit


def test_CombinedDataReader_fail():
    # No ephemeris reader
    reader1 = CombinedDataReader()
    reader1.add_aux_data_reader(OrbitAuxReader(get_test_filepath("PPReadAllInput_orbits.des"), "whitespace"))
    reader1.add_aux_data_reader(CSVDataReader(get_test_filepath("PPReadAllInput_params.txt"), "whitespace"))
    with pytest.raises(SystemExit) as e1:
        _ = reader1.read_block(10)
    assert e1.type == SystemExit

    # No aux data readers
    reader2 = CombinedDataReader()
    reader2.add_ephem_reader(OIFDataReader(get_test_filepath("PPReadAllInput_oif.txt"), "csv"))
    with pytest.raises(SystemExit) as e1:
        _ = reader2.read_block(10)
    assert e1.type == SystemExit

    # Cannot set the ephemeris reader more than once.
    reader3 = CombinedDataReader()
    reader3.add_ephem_reader(OIFDataReader(get_test_filepath("PPReadAllInput_oif.txt"), "csv"))
    with pytest.raises(SystemExit) as e1:
        reader3.add_ephem_reader(
            OIFDataReader(get_test_filepath("oiftestoutput.txt"), inputformat="whitespace")
        )
    assert e1.type == SystemExit
