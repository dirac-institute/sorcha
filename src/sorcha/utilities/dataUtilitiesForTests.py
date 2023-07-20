"""
This package contains all of sorcha's test data.
"""
import os
from pathlib import Path

from astropy.utils.data import get_pkg_data_filename

import sorcha

__all__ = ["get_test_filepath"]

rootdir = Path(os.path.dirname(sorcha.__file__)) / "data"


def get_test_filepath(filename):
    """Return the full path to a test file in the ``.../tests/data`` directory.

    Parameters
    ----------
    filename : `str`
        The name of the file inside the ``tests/data`` directory.

    Returns
    -------
    filepath : `str`
        The full path to the file.
    """

    # This file's path: `<base_directory>/src/sorcha/utilities/test_data_utilities.py`
    # THIS_DIR = `<base_directory>/`
    THIS_DIR = Path(__file__).parent.parent.parent.parent

    # Returned path: `<base_directory>/tests/data/filename`
    return os.path.join(THIS_DIR, "tests/data", filename)


def get_demo_filepath(filename):
    """Return the full path to a test file in the ``.../demo`` directory.

    Parameters
    ----------
    filename : `str`
        The name of the file inside the ``demo`` directory.

    Returns
    -------
    filepath : `str`
        The full path to the file.
    """

    # This file's path: `<base_directory>/src/sorcha/utilities/test_data_utilities.py`
    # THIS_DIR = `<base_directory>/`
    THIS_DIR = Path(__file__).parent.parent.parent.parent

    # Returned path: `<base_directory>/tests/data/filename`
    return os.path.join(THIS_DIR, "demo", filename)


def get_data_out_filepath(filename):
    """Return the full path to a test file in the ``.../data/out`` directory.

    Parameters
    ----------
    filename : `str`
        The name of the file inside the ``data/out`` directory.

    Returns
    -------
    filepath : `str`
        The full path to the file.
    """

    # This file's path: `<base_directory>/src/sorcha/utilities/test_data_utilities.py`
    # THIS_DIR = `<base_directory>/`
    THIS_DIR = Path(__file__).parent.parent.parent.parent

    # Returned path: `<base_directory>/tests/data/filename`
    return os.path.join(THIS_DIR, "data/out", filename)
