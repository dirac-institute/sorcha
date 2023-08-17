import argparse
import concurrent.futures
import os
import pooch

from functools import partial
from sorcha.ephemeris.simulation_data_files import make_retriever, DATA_FILE_LIST


def _decompressor(fname, action, pup):
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


if __name__ == "__main__":
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

    # create the Pooch retriever that will save files to the user defined directory
    retriever = make_retriever(args.cache)

    # remove files if the user has requested re-downloading the files
    if args.force:
        for file_name in DATA_FILE_LIST:
            os.remove(retriever.fetch(file_name))

    # create a partial function of `Pooch.fetch` including the `_decompressor` method
    fetch_partial = partial(retriever.fetch, processor=_decompressor, progressbar=True)

    # download the files in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(fetch_partial, DATA_FILE_LIST)
