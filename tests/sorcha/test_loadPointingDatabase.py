from sorcha.utilities.loadPointingDatabase import (
    _hash_sqlite_file,
    _get_cache_paths,
    _cache_is_valid,
    _save_cache,
    _load_filterpointing,
)
import hashlib
import json
import os
import sys
import pandas as pd
import logging
import pooch
from sorcha.utilities.dataUtilitiesForTests import get_test_filepath, get_demo_filepath
import shutil
import tempfile
from sorcha.utilities.sorchaArguments import sorchaArguments
from sorcha.utilities.sorchaConfigs import sorchaConfigs

import pytest

import logging
import logging.handlers
from unittest.mock import patch
import io

def test_hash_sqlite_file(): # test that hash_sqlite_file creates a unique file for different sqlite dbs

    hash = hashlib.sha256()

    pointing_db_path = get_test_filepath("baseline_10klines_2.0.db")

    with open(pointing_db_path, "rb") as f:
            x = f.read()
            hash.update(x)       
    test_result= hash.hexdigest()

    result = _hash_sqlite_file(pointing_db_path)
    # check that it creates the same fingerprint
    assert result==test_result
    #check the finerprint is a 64 character string
    assert isinstance(result, str) and len(result) == 64  # assert hash is a 64 character string

    # check that even fora slightly modifed file the fingerprint is different 
    # slightly_modified_baseline_10klines_2.0.db is a file nearly identical to baseline_10klines_2.0.db
    # but in the first row of the column observationStartMJD, the value has been increased by 0.00001
    #  ie testing that even an incrediabilty small change will result in differnt fingerprint

    # this a;so works for a test of _cache_is_valid() showing that small changes will be caught
    # as _cache_is_valid() checks stored.get("sha256") == _hash_sqlite_file(sqlite_path)
    modified_db_path = get_test_filepath("slightly_modified_baseline_10klines_2.0.db")
    modified_result = _hash_sqlite_file(modified_db_path)

    assert result!= modified_result


def test_load_filter_pointing():

    # if no hdf5 loaded start precompute_pointing_data
    with tempfile.TemporaryDirectory() as ar_data_dir:
        cmd_args_dict = {
            "paramsinput": get_test_filepath("params_small_random_mpcorb.csv"),
            "orbinfile": get_test_filepath("orbits_small_random_mpcorb.csv"),
            "configfile": get_test_filepath("config_for_ephemeris_unit_test.ini"),
            "pointing_database": get_demo_filepath("baseline_v2.0_1yr.db"),
            "output_ephemeris_file": "sorcha_ephemeris",
            "surveyname": "rubin_sim",
            "outfilestem": f"out_end2end_with_ephemeris_generation",
            "loglevel": False,
            "stats": None,
            "visits_database": None,
            "ar_data_path": ar_data_dir,
        }

        with tempfile.TemporaryDirectory() as dir_name:
            cmd_args_dict["outpath"] = dir_name
            args = sorchaArguments(cmd_args_dict)
            sconfigs = sorchaConfigs(args.configfile, args.surveyname)

            # patch must wrap the call to _load_filterpointing
            with patch("sorcha.utilities.loadPointingDatabase.precompute_pointing_information") as mock_precompute:
                filter_pointing = _load_filterpointing(args, sconfigs, verboselog=False)
                mock_precompute.assert_called_once()

    # if valid hdf5 loaded (load the results) i.e dont call precommute
    with tempfile.TemporaryDirectory() as ar_data_dir:
        cmd_args_dict = {
            "paramsinput": get_test_filepath("params_small_random_mpcorb.csv"),
            "orbinfile": get_test_filepath("orbits_small_random_mpcorb.csv"),
            "configfile": get_test_filepath("config_for_ephemeris_unit_test.ini"),
            "pointing_database": get_demo_filepath("baseline_v2.0_1yr.db"),
            "output_ephemeris_file": "sorcha_ephemeris",
            "surveyname": "rubin_sim",
            "outfilestem": f"out_end2end_with_ephemeris_generation",
            "loglevel": False,
            "stats": None,
            "visits_database": None,
            "ar_data_path": ar_data_dir,
        }
        fingerprint_path = get_test_filepath("baseline_v2.0_1yr_fingerprint.json")
        hdf5_path = get_test_filepath("baseline_v2.0_1yr.h5")
        shutil.copy(fingerprint_path, ar_data_dir)
        shutil.copy(hdf5_path, ar_data_dir)
        with tempfile.TemporaryDirectory() as dir_name:
            cmd_args_dict["outpath"] = dir_name
            args = sorchaArguments(cmd_args_dict)
            sconfigs = sorchaConfigs(args.configfile, args.surveyname)

            # patch must wrap the call to _load_filterpointing
            with patch("sorcha.utilities.loadPointingDatabase.precompute_pointing_information") as mock_precompute:
                filter_pointing = _load_filterpointing(args, sconfigs, verboselog=False)
                mock_precompute.assert_not_called()

    # if not valid hdf5 loaded (load the results) error out
    # in this unit test slightly_modified_baseline_10klines_2.0.db pointing database is different from 
    #  slightly_modified_baseline_10klines_2.0_fingerprint.json and slightly_modified_baseline_10klines_2.0.h5 
    # even thoughb they have the same names. This unit checks that if a user is making a mistake that the code will catch it 
    # an error out, informing the user that they need to restore the original pointing database, rename the new pointing database
    # or delete the cache files and re-run.  either way this check removes user error
    with tempfile.TemporaryDirectory() as ar_data_dir:
        cmd_args_dict = {
            "paramsinput": get_test_filepath("params_small_random_mpcorb.csv"),
            "orbinfile": get_test_filepath("orbits_small_random_mpcorb.csv"),
            "configfile": get_test_filepath("config_for_ephemeris_unit_test.ini"),
            "pointing_database": get_test_filepath("slightly_modified_baseline_10klines_2.0.db"),
            "output_ephemeris_file": "sorcha_ephemeris",
            "surveyname": "rubin_sim",
            "outfilestem": f"out_end2end_with_ephemeris_generation",
            "loglevel": False,
            "stats": None,
            "visits_database": None,
            "ar_data_path": ar_data_dir,
        }
        fingerprint_path = get_test_filepath("slightly_modified_baseline_10klines_2.0_fingerprint.json")
        hdf5_path = get_test_filepath("slightly_modified_baseline_10klines_2.0.h5")
        shutil.copy(fingerprint_path, ar_data_dir)
        shutil.copy(hdf5_path, ar_data_dir)
        with tempfile.TemporaryDirectory() as dir_name:
            cmd_args_dict["outpath"] = dir_name
            args = sorchaArguments(cmd_args_dict)
            sconfigs = sorchaConfigs(args.configfile, args.surveyname)

            # patch must wrap the call to _load_filterpointing

            with pytest.raises(SystemExit) as error_text:
                filter_pointing = _load_filterpointing(args, sconfigs, verboselog=False)
            assert error_text.value.code == (
                    f"The pointing database '{args.pointing_database}' does not match hdf5 file stored in '{args.ar_data_file_path}'. "
                    f"A cached HDF5 file already exists for a database with this filename. \n"
                    f"Either restore the original pointing database \n"
                    f"Rename the new pointing database \n"
                    f"or delete the cache files and re-run."
                    )
