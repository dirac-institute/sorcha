#
# The `sorcha run` subcommand implementation
#
import pooch
from sorcha_cmdline.sorchaargumentparser import SorchaArgumentParser


def main():  # pragma: no cover
    # parse the input arguments
    parser = SorchaArgumentParser(
        prog="sorcha bootstrap",
        description="Fetch the NAIF high precision EOP kernel file store its checksum.",
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

    return execute(args)


def execute(args):
    #
    # NOTE: DO NOT MOVE THESE IMPORTS TO THE TOP LEVEL OF THE MODULE !!!
    #
    #       Importing sorcha from the function and not at the top-level of the module
    #       allows us to exit quickly and print the help/error message (in case there
    #       was a mistake on the command line). Importing sorcha can take 5 seconds or
    #       more, and making the user wait that long just to print out an erro message
    #       is poor user experience.
    #
    from sorcha.utilities.retrieve_ephemeris_data_files import (
        make_retriever,
        _check_for_existing_files,
        _decompress,
        _remove_files,
        build_meta_kernel_file,
    )
    from functools import partial
    import concurrent.futures
    from sorcha.utilities.sorchaConfigs import sorchaConfigs, auxiliaryConfigs

    # default file names and urls (stored in auxiliaryConfigs)
    default_files = sorchaConfigs()
    default_files.auxiliary = auxiliaryConfigs()
    # create the Pooch retriever that tracks and retrieves the requested files
    retriever = make_retriever(default_files, args.cache)

    # determine if we should attempt to download or create any files.
    found_all_files = False
    if args.force:
        _remove_files(default_files, retriever)
    else:
        print("Checking cache for existing files.")
        found_all_files = _check_for_existing_files(retriever, default_files.auxiliary.data_file_list)

    if not found_all_files:
        # create a partial function of `Pooch.fetch` including the `_decompress` method
        fetch_partial = partial(retriever.fetch, processor=_decompress, progressbar=True)

        # download the data files in parallel
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(fetch_partial, default_files.auxiliary.data_files_to_download)

        # build the meta_kernel.txt file
        build_meta_kernel_file(default_files, retriever)

        print("Checking cache after attempting to download and create files.")
        _check_for_existing_files(retriever, default_files.auxiliary.data_file_list)


if __name__ == "__main__":
    main()
