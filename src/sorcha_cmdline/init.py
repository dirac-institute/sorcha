from sorcha_cmdline.sorchaargumentparser import SorchaArgumentParser
import sys

#
# sorcha init
#


def parse_file_selection(file_select):
    """Turns the number entered by the user at the command line into a string
    prompt. Also performs error handling.

    Parameters
    -----------
    file_select : int
        Integer entered by the user at command line.

    Returns
    -----------
    which_configs : string
        String indicating which configuration files to retrieve. Should be "rubin", "demo" or "all".

    """

    try:
        file_select = int(file_select)
    except ValueError:
        sys.exit("Input could not be converted to a valid integer. Please try again.")

    if file_select not in [1, 2, 3, 4]:
        sys.exit("Input could not be converted to a valid integer. Please input an integer between 1 and 4.")

    selection_dict = {1: "rubin_circle", 2: "rubin_footprint", 3: "rubin_known", 4: "all"}

    which_configs = selection_dict[file_select]

    return which_configs


def execute(args):  # pragma: no cover
    print("\nWhich configuration file(s) would you like to copy?:\n")
    print("1. Rubin-specific configuration file using circular approximation of camera footprint (faster).\n")
    print("2. Rubin-specific configuration file using full camera footprint (slower, but more accurate).\n")
    print(
        "3. Rubin-specific configuration file using full camera footprint but with all filters turned off, for known object detection. WARNING: do not use this unless you are sure you know what you are doing!\n"
    )
    print("4. All.\n")
    file_select = input("Please enter a number and hit Return/Enter.\n")

    which_configs = parse_file_selection(file_select)

    #
    # NOTE: DO NOT MOVE THESE IMPORTS TO THE TOP LEVEL OF THE MODULE !!!
    #
    #       Importing sorcha from the function and not at the top-level of the module
    #       allows us to exit quickly and print the help/error message (in case there
    #       was a mistake on the command line). Importing sorcha can take 5 seconds or
    #       more, and making the user wait that long just to print out an erro message
    #       is poor user experience.
    #
    from sorcha.utilities.sorcha_copy_configs import copy_demo_configs
    import os

    copy_location = os.path.abspath(args.path)
    return copy_demo_configs(copy_location, which_configs, args.force)


#
# sorcha init
#


def main():
    # Create the top-level parser
    parser = SorchaArgumentParser(
        prog="sorcha init", description="Initialize configuration files for a new simulation."
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument(
        "-p",
        "--path",
        type=str,
        default="./",
        help="Filepath where you want to copy the config files. Default is current working directory.",
    )
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        default=False,
        help="Force deletion/overwrite of existing config file(s). Default False.",
    )

    args = parser.parse_args()
    return execute(args)


if __name__ == "__main__":
    main()
