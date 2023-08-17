import argparse
import os
import pooch

from multiprocessing import Pool, cpu_count

from sorcha.ephemeris.simulation_data_files import make_retriever, DATA_FILE_LIST

if __name__ == "__main__":
    # Parse arguments
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

    # Create the Pooch retriever
    retriever = make_retriever(args.cache)

    # Remove the files if the user has requested re-downloading the files
    if args.force:
        for file_name in DATA_FILE_LIST:
            os.remove(retriever.fetch(file_name))

    # download the files in parallel
    pool = Pool(cpu_count())
    results = pool.map(retriever.fetch, DATA_FILE_LIST)
    pool.close()
    pool.join()
