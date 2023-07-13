"""
This package contains all of surveySimPP's test data.
"""
import os
from pathlib import Path

from astropy.utils.data import get_pkg_data_filename

import surveySimPP

__all__ = ["get_test_filepath"]

rootdir = Path(os.path.dirname(surveySimPP.__file__)) / "data"


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

    # This file's path: `<base_directory>/src/surveySimPP/utilities/test_data_utilities.py`
    # THIS_DIR = `<base_directory>/`
    THIS_DIR = Path(__file__).parent.parent.parent.parent

    # Returned path: `<base_directory>/tests/data/filename`
    return os.path.join(THIS_DIR, "tests/data", filename)
