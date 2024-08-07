import argparse
import subprocess
import sys
import shutil
import os

#
# Generic verb dispatcher code
#


def find_sorcha_verbs():
    """Find available sorcha commands in the system's PATH."""
    sorcha_verbs = []
    for directory in os.environ.get("PATH", "").split(os.pathsep):
        if os.path.isdir(directory):
            for item in os.listdir(directory):
                if item.startswith("sorcha-") and os.access(os.path.join(directory, item), os.X_OK):
                    sorcha_verbs.append(item[len("sorcha-") :])
    return sorted(set(sorcha_verbs))


def main():
    # Discover available sorcha verbs
    available_verbs = find_sorcha_verbs()

    if not available_verbs:
        print("Error: No available 'sorcha-' utilities found.")
        sys.exit(1)

    # Set up the argument parser with epilog text
    description = "Sorcha survey simulator suite."
    epilog_text = (
        "These are the most common sorcha verbs:\n\n"
        "   init      Initialize a new simulation\n"
        "   run       Run a simulation\n"
        "   outputs   Manipulate/package sorcha outputs\n"
        "   demo      Set up a demo simulation\n"
        "   bootstrap Download datafiles required to run sorcha\n"
        "\n"
        "To get more information, run the verb with --help. For example:\n\n"
        "   sorcha run --help\n"
        " "
    )

    parser = argparse.ArgumentParser(
        description=description, epilog=epilog_text, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--version",
        help="Print version information",
        dest="version",
        action="store_true",
    )
    parser.add_argument("verb", nargs="?", choices=available_verbs, help="Verb to execute")
    parser.add_argument("args", nargs=argparse.REMAINDER, help="Arguments for the verb")

    args = parser.parse_args()

    if args.version:
        import sorcha

        print(sorcha.__version__)
        return

    # Ensure a verb is provided if not just checking the version
    if not args.verb:
        parser.print_help()
        sys.exit(1)

    # Construct the full command name
    utility = f"sorcha-{args.verb}"

    # Ensure the command is available
    if not shutil.which(utility):
        print(f"Error: '{utility}' is not available.")
        sys.exit(1)

    # Execute the command with the remaining arguments
    try:
        result = subprocess.run([utility] + args.args, check=True)
        sys.exit(result.returncode)
    except subprocess.CalledProcessError as e:
        print(f"Error: Command '{utility}' failed with exit code {e.returncode}.")
        sys.exit(e.returncode)


if __name__ == "__main__":
    main()
