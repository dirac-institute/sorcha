"""
This package contains all of surveySimPP's test data.
"""
import os
from pathlib import Path

from astropy.utils.data import get_pkg_data_filename

import surveySimPP

__all__ = ["rootdir", "get_test_filepath"]

rootdir = Path(os.path.dirname(surveySimPP.__file__)) / "tests" / "data"


def get_test_filepath(filename, **kwargs):
    """Return the full path to a test file in the ``tests/data`` directory.

    Parameters
    ----------
    filename : `str`
        The name of the file inside the ``tests/data`` directory.

    Returns
    -------
    filepath : `str`
        The full path to the file.

    Notes
    -----
    This is a wrapper around `astropy.utils.data.get_pkg_data_filename` which
    sets the ``package`` kwarg to be `surveySimPP.tests.data`.
    """
    if isinstance(filename, Path):
        # NOTE: get_pkg_data_filename does not accept Path objects
        filename = filename.as_posix()
    return get_pkg_data_filename(filename, package="surveySimPP.tests.data", **kwargs)
