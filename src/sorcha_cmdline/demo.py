from sorcha_cmdline.sorchaargumentparser import SorchaArgumentParser

#
# sorcha demo prepare
#


def cmd_demo_prepare(args):  # pragma: no cover
    #
    # NOTE: DO NOT MOVE THESE IMPORTS TO THE TOP LEVEL OF THE MODULE !!!
    #
    #       Importing sorcha from the function and not at the top-level of the module
    #       allows us to exit quickly and print the help/error message (in case there
    #       was a mistake on the command line). Importing sorcha can take 5 seconds or
    #       more, and making the user wait that long just to print out an erro message
    #       is poor user experience.
    #
    from sorcha.utilities.sorcha_copy_demo_files import copy_demo_files
    import os

    copy_location = os.path.abspath(args.path)
    copy_demo_files(copy_location, args.force)


#
# sorcha demo howto
#
def cmd_demo_howto(args):  # pragma: no cover
    #
    # NOTE: DO NOT MOVE THESE IMPORTS TO THE TOP LEVEL OF THE MODULE !!!
    #
    #       Importing sorcha from the function and not at the top-level of the module
    #       allows us to exit quickly and print the help/error message (in case there
    #       was a mistake on the command line). Importing sorcha can take 5 seconds or
    #       more, and making the user wait that long just to print out an erro message
    #       is poor user experience.
    #
    from sorcha.utilities.sorcha_demo_command import print_demo_command

    return print_demo_command()


#
# sorcha demo
#


def main():
    # Create the top-level parser
    parser = SorchaArgumentParser(
        prog="sorcha demo", description="Prepare and explain how to run sorcha demos"
    )
    subparsers = parser.add_subparsers(
        title="commands",
        description="Available commands",
        help="Command to execute",
        dest="command",
    )

    # Add the `prepare` subcommand
    demo_prepare_parser = subparsers.add_parser(
        "prepare", help="Prepares the files necessary to run the demo"
    )
    demo_prepare_parser.set_defaults(func=cmd_demo_prepare)
    demo_prepare_parser.add_argument(
        "-p",
        "--path",
        type=str,
        default="./",
        help="Filepath where you want to copy the demo files. Default is current working directory.",
    )
    demo_prepare_parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        default=False,
        help="Force deletion/overwrite of existing demo file(s). Default False.",
    )

    # Add the `howto` subcommand
    demo_howto_parser = subparsers.add_parser("howto", help="Show the command to run the sorcha demo")
    demo_howto_parser.set_defaults(func=cmd_demo_howto)

    # Parse the command-line arguments
    args = parser.parse_args()

    # Call the appropriate function based on the subcommand
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
