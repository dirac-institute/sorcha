import argparse
import concurrent.futures
import os
import pooch

from functools import partial
from sorcha.ephemeris.simulation_data_files import (
    make_retriever,
    DATA_FILES_TO_DOWNLOAD,
    DATA_FILE_LIST,
)
from sorcha.utilities.generate_meta_kernel import build_meta_kernel_file


def _decompress(fname, action, pup):
    """Override the functionality of Pooch's `Decompress` class so that the resulting
    decompressed file uses the original file name without the compression extension.
    For instance `filename.json.bz` will be decompressed and saved as `filename.json`.

    Parameters
    ----------
    fname : str
        Original filename
    action : str
        One of []"download", "update", "fetch"]
    pup : pooch.Pooch
        The Pooch object that defines the location of the file.
    """
    known_extentions = [".gz", ".bz2", ".xz"]
    if os.path.splitext(fname)[-1] in known_extentions:
        pooch.Decompress(method="auto", name=os.path.splitext(fname)[0]).__call__(fname, action, pup)


def _remove_files(retriever: pooch.Pooch) -> None:
    """Utility to remove all the files tracked by the pooch retriever. This includes
    the decompressed ObservatoryCodes.json file as well as the META_KERNEL file
    that are created after downloading the files in the DATA_FILES_TO_DOWNLOAD
    list.

    Parameters
    ----------
    retriever : pooch.Pooch
        Pooch object that maintains the registry of files to download.
    """

    for file_name in DATA_FILE_LIST:
        file_path = retriever.fetch(file_name)
        print(f"Deleting file: {file_path}")
        os.remove(file_path)


def _check_for_existing_files(retriever: pooch.Pooch, file_list: list[str]) -> bool:
    """Will check for existing local files, any file not found will be printed
    to the terminal.

    Parameters
    ----------
    retriever : pooch.Pooch
        Pooch object that maintains the registry of files to download.
    file_list : list[str]
        A list of file names look for in the local cache.

    Returns
    -------
    bool
        Returns True if all files are found in the local cache, False otherwise.
    """

    # choosing clarity over brevity with these variables.
    # we could have used `!bool(len(missing_files)) as the return, but that's hard to read.
    found_all_files = True
    missing_files = []
    for file_name in file_list:
        if not os.path.exists(os.path.join(retriever.abspath, file_name)):
            missing_files.append(file_name)
            found_all_files = False

    if found_all_files:
        print(f"All expected files were found in the local cache: {retriever.abspath}/")
    else:
        print(f"The following file(s) were not found in the local cache: {retriever.abspath}/")
        for file_name in missing_files:
            print(f"- {file_name}")

    return found_all_files


def main():
    # parse the input arguments
    parser = argparse.ArgumentParser(
        description="Fetch the NAIF high precision EOP kernel file store its checksum."
    )
    parser.add_argument(
        "--cache",
        type=str,
        default=pooch.os_cache("sorcha"),
        help="Local directory where downloaded files will be stored.",
    )
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="Delete and re-download data files.",
    )
    args = parser.parse_args()

    # create the Pooch retriever that tracks and retrieves the requested files
    retriever = make_retriever(args.cache)

    # determine if we should attempt to download or create any files.
    found_all_files = False
    if args.force:
        _remove_files(retriever)
    else:
        print("Checking cache for existing files.")
        found_all_files = _check_for_existing_files(retriever, DATA_FILE_LIST)

    if not found_all_files:
        # create a partial function of `Pooch.fetch` including the `_decompress` method
        fetch_partial = partial(retriever.fetch, processor=_decompress, progressbar=True)

        # download the data files in parallel
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(fetch_partial, DATA_FILES_TO_DOWNLOAD)

        # build the meta_kernel.txt file
        build_meta_kernel_file(retriever)

        print("Checking cache after attempting to download and create files.")
        _check_for_existing_files(retriever, DATA_FILE_LIST)


if __name__ == "__main__":
    main()
