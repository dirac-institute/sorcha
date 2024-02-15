def print_demo_command(printall=True):
    """
    Prints the current working version of the demo command to the terminal, with
    optional functionality to also tell the user how to copy the demo files.

    Parameters
    -----------
    printall : boolean
        When True, prints the demo command plus the instructions for copying the demo files.
        When False, prints the demo command only.

    Returns
    -----------
    None.

    """

    print("\nThe command to run the Sorcha demo in this version of Sorcha is:\n")

    print(
        "\033[1;32;40msorcha -c sorcha_config_demo.ini -p sspp_testset_colours.txt -ob sspp_testset_orbits.des -pd baseline_v2.0_1yr.db -o ./ -t testrun_e2e\033[0m\n"
    )

    print("WARNING: This command assumes that the demo files are in your working directory.\n")

    if printall:
        print("You can copy the demo files into your working directory by running:\n")

        print("\033[1;32;40msorcha_copy_demo_files\033[0m\n")

        print("Or, to copy them into a directory of your choice, run:\n")

        print("\033[1;32;40msorcha_copy_demo_files -p /path/to/files \033[0m\n")

    print(
        "If copying into a directory of your choice, you will need to modify the demo command to path to your files.\n"
    )


if __name__ == "__main__":
    print_demo_command()
