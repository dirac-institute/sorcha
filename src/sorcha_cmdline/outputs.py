import argparse

#
# sorcha outputs create-sqlite
#


def cmd_outputs_create_sqlite(args):  # pragma: no cover
    #
    # NOTE: DO NOT MOVE THESE IMPORTS TO THE TOP LEVEL OF THE MODULE !!!
    #
    #       Importing sorcha from the function and not at the top-level of the module
    #       allows us to exit quickly and print the help/error message (in case there
    #       was a mistake on the command line). Importing sorcha can take 5 seconds or
    #       more, and making the user wait that long just to print out an erro message
    #       is poor user experience.
    #
    from sorcha.utilities.createResultsSQLDatabase import create_results_database
    from sorcha.modules.PPConfigParser import PPFindDirectoryOrExit
    import os

    args.filename = os.path.abspath(args.filename)
    args.inputs = os.path.abspath(args.inputs)
    args.outputs = os.path.abspath(args.outputs)

    _ = PPFindDirectoryOrExit(args.inputs, "-i, --inputs")
    _ = PPFindDirectoryOrExit(args.outputs, "-o, --outputs")

    return create_results_database(args)


#
# sorcha outputs
#


def main():
    # Create the top-level parser
    parser = argparse.ArgumentParser(prog="sorcha-config", description="Sorcha outputs manipulation utility")
    subparsers = parser.add_subparsers(
        title="commands", description="Available commands", help="Command to execute", dest="command"
    )

    # Add the `create_sqlite` subcommand
    outputs_create_sqlite_parser = subparsers.add_parser(
        "create-sqlite", help="Creating a combined results+inputs SQL database."
    )
    outputs_create_sqlite_parser.set_defaults(func=cmd_outputs_create_sqlite)

    outputs_create_sqlite_parser.add_argument(
        "-f",
        "--filename",
        type=str,
        required=True,
        help="Filepath and name where you want to save the database.",
    )
    outputs_create_sqlite_parser.add_argument(
        "-i",
        "--inputs",
        type=str,
        required=True,
        help="Path location of input text files (orbits, colours and config files).",
    )
    outputs_create_sqlite_parser.add_argument(
        "-o",
        "--outputs",
        type=str,
        required=True,
        help="Path location of SSPP output files/folders. Code will search subdirectories recursively.",
    )
    outputs_create_sqlite_parser.add_argument(
        "-s",
        "--stem",
        type=str,
        help="Stem filename of outputs. Used to find output filenames. Use if you want to specify.",
    )
    outputs_create_sqlite_parser.add_argument(
        "-c",
        "--comet",
        default=False,
        action="store_true",
        help="Toggle whether to look for cometary activity files. Default False.",
    )

    # Parse the command-line arguments
    args = parser.parse_args()

    # Call the appropriate function based on the subcommand
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
