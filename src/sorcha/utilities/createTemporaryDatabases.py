# Creates temporary ephemeris databases in SQL. These can take a while to create,
# especially for large OIF/ephemeris files, but greatly speed up the actual
# running of SSPP. The databases will be named temp_[input_filename].db and will
# be saved in the same folder as the OIF files.

import glob
import argparse
import os
import sys
from sorcha.modules.PPConfigParser import PPFindDirectoryOrExit
from sorcha.modules.PPMakeTemporaryEphemerisDatabase import PPMakeTemporaryEphemerisDatabase


def make_temporary_databases(args):
    """
    Creates temporary ephemeris SQLite databases.

    Parameters:
    -----------
    args (argparse ArgumentParser object): command line arguments.

    Returns:
    -----------
    None.

    """

    print("Making temporary ephemerides databases.")

    input_path = os.path.abspath(args.inputs)
    file_list = glob.glob(os.path.join(input_path, args.stem) + "*")
    output_list = [
        os.path.join(input_path, "temp_" + os.path.basename(input_name).split(".")[0]) + ".db"
        for input_name in file_list
    ]

    if any([os.path.exists(out_name) for out_name in output_list]) and not args.f:
        sys.exit(
            "Temporary ephemeris databases already found in input location. Run with -f flag to overwrite."
        )

    if not file_list:
        sys.exit("Could not find any ephemerides files using given input path and stem.")

    for input_name in file_list:
        print("Creating temporary database for file: {}".format(input_name))
        stem_filename = "temp_" + os.path.basename(input_name).split(".")[0] + ".db"
        PPMakeTemporaryEphemerisDatabase(input_name, os.path.join(input_path, stem_filename), "csv")

    print("Done.")


def main():
    """
    Creates temporary ephemeris databases in SQL. These can take a while to create,
    especially for large OIF/ephemeris files, but greatly speed up the actual
    running of SSPP. The databases will be named temp_[input_filename].db and will
    be saved in the same folder as the OIF files.

    usage: createTemporaryDatabases [-h] -i INPUTS [-s STEM] [-c CHUNK] [-f]
        arguments:
          -h, --help                    show this help message and exit
          -i INPUTS, --inputs INPUTS    Path location of input ephemeris text files.
          -s STEM, --stem STEM          Stem filename of input ephemeris text files. Default is `oif_`.
          -c CHUNK, --chunk CHUNK       Chunking size for creation, where chunk=number of rows per chunk. Don't change this unless you know what you're doing.
          -f, --force                   Force deletion/overwrite of existing output file(s). Default False.

    """

    parser = argparse.ArgumentParser(description="Creating the temporary SQL ephemeris databses.")

    # path to inputs
    parser.add_argument(
        "-i", "--inputs", help="Path location of input ephemeris text files.", type=str, required=True
    )
    # stem filename for outputs
    parser.add_argument(
        "-s",
        "--stem",
        help='Stem filename of input ephemeris text files. Default is "oif_".',
        type=str,
        default="oif_",
    )
    # chunk size for creating databases
    parser.add_argument(
        "-c",
        "--chunk",
        help="Chunking size for creation, where chunk=number of rows per chunk. Don't change this unless you know what you're doing.",
        type=int,
        default=1e6,
    )
    # force overwrite?
    parser.add_argument(
        "-f",
        "--force",
        help="Force deletion/overwrite of existing output file(s). Default False.",
        dest="f",
        action="store_true",
        default=False,
    )

    args = parser.parse_args()

    _ = PPFindDirectoryOrExit(args.inputs, "-i, --inputs")

    make_temporary_databases(args)


if __name__ == "__main__":
    main()
