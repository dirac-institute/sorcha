import hashlib
import json
import os
import sys
import pandas as pd
import logging
import pooch

from sorcha.ephemeris.simulation_setup import precompute_pointing_information
from sorcha.modules.PPReadPointingDatabase import PPReadPointingDatabase


def _hash_sqlite_file(path):
    """Creates a SHA256 hash of the pointing database sqlite file."""
    h = hashlib.sha256()
    with open(path, "rb") as f:  # rb (r)ead (b)inary mode
        while chunk := f.read(
            2**13
        ):  # reads the pointings in chunks of 2^13 bytes (which is 8192 bytes/8kb, faster using powers of 2). avoids memory issues from reading whole file
            h.update(chunk)
    return (
        h.hexdigest()
    )  # creates a 64 character hexidecimal string. which is highly dependant on all bytes in the pointing database file. (even a small change should largely change this string)


def _get_cache_paths(sqlite_path, cache_dir):
    """
    The hdf5 and fingerprint stems should match the given pointing database filename stem. So this gets the file path from that
    """
    stem = os.path.splitext(os.path.basename(sqlite_path))[0]
    base = os.path.join(cache_dir, stem)
    return base + ".h5", base + "_fingerprint.json"


def _cache_is_valid(sqlite_path, cache_dir):
    """checks that valid HDF5 cache exists for the given pointing database file."""
    hdf5_path, fingerprint_path = _get_cache_paths(sqlite_path, cache_dir)

    if not os.path.exists(hdf5_path) or not os.path.exists(fingerprint_path):
        return False

    with open(fingerprint_path) as f:
        stored = json.load(f)
    # this checks if the key in the fingerprint file matchs the key created from the pointing file
    return stored.get("sha256") == _hash_sqlite_file(sqlite_path)


def _save_cache(sqlite_path, filterpointing, cache_dir):
    """
    Save the filterpointing DataFrame and pointing database fingerprint to cache/ar directory.

    This saves hdf5 file to the cache/directory as well as a "fingerprint". This fingerprint is a SHA256 hash of the pointing database.
    This fingerprint must match the pointing database given for a Sorcha run, for the cached hdf5 to work. This is essentially my method to stop a user
    from making a new pointing database file with the same file name and mistakenly using the old cache.
    """
    hdf5_path, fingerprint_path = _get_cache_paths(sqlite_path, cache_dir)

    filterpointing.to_hdf(hdf5_path, key="filterpointing", mode="w", format="table")

    # store unique fingerprint of pointing database in fingerprint file. needs to match pointing database SHA256 for sorcha to run
    with open(fingerprint_path, "w") as f:
        json.dump({"sha256": _hash_sqlite_file(sqlite_path)}, f)

    return hdf5_path


def _load_filterpointing(args, sconfigs, verboselog=False):
    """

    Either, loads the filterpointing pandas DataFrame from a cached HDF5 file.

    If one doesn't exist, function reads and precomputes the pointing database,
    then saves the result as an HDF5 cache with a SHA256 fingerprint.

    On future runs, if the pointing file does not match the cached hdf5 file, Sorcha will
    error out to prevent use of a mismatched cache/pointing from the user.

    Parameters
    -----------
    args : dictionary or `sorchaArguments` object
        dictionary of command-line arguments.
    sconfigs: dataclass
        Dataclass of configuration file arguments.
    Returns
    --------
    pointings_df : pandas dataframe
        The original dataframe with several additional columns of precomputed values.
    """

    pplogger = logging.getLogger(__name__)
    verboselog = pplogger.info if verboselog else lambda *a, **k: None
    if args.ar_data_file_path is None:
        args.ar_data_file_path = pooch.os_cache("sorcha")

    verboselog("Checking for valid HDF5 cache of pointing database...")

    # gets the hdf5 filepath
    hdf5_path, _ = _get_cache_paths(args.pointing_database, args.ar_data_file_path)

    # checks if file path is valid
    if _cache_is_valid(args.pointing_database, args.ar_data_file_path):
        pplogger.info(f"Valid HDF5 cache found. Loading filterpointing from: {hdf5_path}")
        return pd.read_hdf(hdf5_path, key="filterpointing")
    if os.path.exists(hdf5_path):
        # this deals with the case of a user making and usering a pointing database with the same filestem name
        pplogger.error(
            f"The pointing database '{args.pointing_database}' does not match hdf5 file stored in '{args.ar_data_file_path}'. A cached HDF5 file already exists for a database with this filename. \nEither restore the original pointing database \nRename the new pointing database \nor delete the cache files and re-run."
        )
        sys.exit(
            f"The pointing database '{args.pointing_database}' does not match hdf5 file stored in '{args.ar_data_file_path}'. A cached HDF5 file already exists for a database with this filename. \nEither restore the original pointing database \nRename the new pointing database \nor delete the cache files and re-run."
        )

    pplogger.info("No HDF5 cache found. Reading from SQLite pointing database.")
    verboselog("Reading pointing database...")
    filterpointing = PPReadPointingDatabase(
        args.pointing_database,
        sconfigs.filters.observing_filters,
        sconfigs.input.pointing_sql_query,
        args.surveyname,
    )
    if sconfigs.input.ephemerides_type.casefold() != "external":
        verboselog("Pre-computing pointing information for ephemeris generation.")
        filterpointing = precompute_pointing_information(filterpointing, args, sconfigs)

    saved_path = _save_cache(args.pointing_database, filterpointing, args.ar_data_file_path)
    pplogger.info(f"filterpointing cached to: {saved_path}")

    return filterpointing
