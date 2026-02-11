import os
import pooch

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


def _split_kernel_path_str(abspath: str, split=79):
    """If abspath string is longer than 79 chars, split it up in the meta kernel by inserting "+' '".
    79 is the default because the character limit in SPICE is 80 before the string needs split.

    Parameters
    ----------
    abspath: str
        The filepath string that needs split.
    Split : int
        The maximum size each part of the filepath can be before it needs split.
    Returns
    ---------
    abspath : str
    The filepath string split into chunks of required size.
    """

    n_iter = int(len(str(abspath)) / split)  # Number of splits required
    for n in range(n_iter, 0, -1):  # Goes backwards to not change the character count of the string before it
        abspath = abspath[: split * n] + "+' '" + abspath[split * n :]
    return abspath


def build_meta_kernel_file(auxconfigs, retriever: pooch.Pooch) -> None:
    """Builds a specific text file that will be fed into `spiceypy` that defines
    the list of spice kernel to load, as well as the order to load them.

    Parameters
    ----------
    auxconfigs: dataclass
        Dataclass of auxiliary configuration file arguments.
    retriever : pooch
        Pooch object that maintains the registry of files to download
    Returns
    ---------
    None
    """
    # build meta_kernel file path
    meta_kernel_file_path = os.path.join(retriever.abspath, auxconfigs.meta_kernel)
    abspath = _split_kernel_path_str(str(retriever.abspath))

    # build a meta_kernel.txt file
    with open(meta_kernel_file_path, "w") as meta_file:
        meta_file.write("\\begindata\n\n")
        meta_file.write(f"PATH_VALUES = ('{abspath}')\n\n")
        meta_file.write("PATH_SYMBOLS = ('A')\n\n")
        meta_file.write("KERNELS_TO_LOAD=(\n")
        for file_name in auxconfigs.ordered_kernel_files:
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
    cache_dir : string
        The full path to the cache directory used when retrieving files for Assist
        and Rebound.
    file_path : string
        The full file path for a given file that will have the cache directory
        segment replace.

    Returns
    -------
    : string
        Shortened file path, appropriate for use in kernel_meta files.
    """

    return file_path.replace(str(cache_dir), "$A")
