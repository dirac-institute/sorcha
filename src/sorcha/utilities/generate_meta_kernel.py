import os
import pooch

from sorcha.ephemeris.simulation_data_files import (
    META_KERNEL,
    ORDERED_KERNEL_FILES,
)

"""
    An example output from running `build_meta_kernel_file` might look like
    the following:

    \begindata

    PATH_VALUES = ('/Users/scientist/sorcha/data_files/assist_and_rebound')

    PATH_SYMBOLS = ('A')

    KERNELS_TO_LOAD=(
        '$A/naif0012.tls',
        '$A/earth_720101_230601.bpc',
        '$A/earth_200101_990825_predict.bpc',
        '$A/pck00010.pck',
        '$A/de440s.bsp',
        '$A/earth_latest_high_prec.bpc',
    )

    \begintext
"""


def build_meta_kernel_file(retriever: pooch.Pooch) -> None:
    """Builds a specific text file that will be fed into `spiceypy` that defines
    the list of spice kernel to load, as well as the order to load them.

    Parameters
    ----------
    retriever : pooch.Pooch
        Pooch object that maintains the registry of files to download
    """
    # build meta_kernel file path
    meta_kernel_file_path = os.path.join(retriever.abspath, META_KERNEL)

    # build a meta_kernel.txt file
    with open(meta_kernel_file_path, "w") as meta_file:
        meta_file.write("\\begindata\n\n")
        meta_file.write(f"PATH_VALUES = ('{retriever.abspath}')\n\n")
        meta_file.write("PATH_SYMBOLS = ('A')\n\n")
        meta_file.write("KERNELS_TO_LOAD=(\n")
        for file_name in ORDERED_KERNEL_FILES:
            shortened_file_name = _build_file_name(retriever.abspath, retriever.fetch(file_name))
            meta_file.write(f"    '{shortened_file_name}',\n")
        meta_file.write(")\n\n")
        meta_file.write("\\begintext\n")


def _build_file_name(cache_dir: str, file_path: str) -> str:
    """Given a string defining the cache directory, and a string defining the full
    path to a given file. This function will strip out the cache directory from
    the file path and replace it with the required meta_kernel directory
    substitution character.

    Parameters
    ----------
    cache_dir : str
        The full path to the cache directory used when retrieving files for Assist
        and Rebound.
    file_path : str
        The full file path for a given file that will have the cache directory
        segment replace.

    Returns
    -------
    str
        Shortened file path, appropriate for use in kernel_meta files.
    """

    return file_path.replace(str(cache_dir), "$A")
