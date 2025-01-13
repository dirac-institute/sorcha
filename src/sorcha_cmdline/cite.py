#
# The `sorcha cite` subcommand implementation
#
import argparse
from sorcha_cmdline.sorchaargumentparser import SorchaArgumentParser
import os


def main():
    parser = SorchaArgumentParser(
        prog="sorcha cite",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="Providing the bibtex, AAS Journals software latex command, and acknowledgement statements for Sorcha and the associated packages that power it in a file called sorcha_citation.txt.",
    )

    optional = parser.add_argument_group("Optional arguments")
    optional.add_argument(
        "-cf",
        "--cite-file-path",
        help="File path to store citation file sorcha_citation.txt.",
        type=str,
        dest="cf",
        required=False,
        default=os.getcwd(),
    )

    optional.add_argument(
        "-p",
        "--print",
        help="Prints citation to terminal.",
        dest="p",
        action="store_true",
        required=False,
    )

    args = parser.parse_args()

    return execute(args)


def execute(args):
    import sys
    import io
    from sorcha.utilities.citation_text import cite_sorcha

    if args.p:  # prints citation to terminal
        cite_sorcha()

    if not os.path.isdir(args.cf):
        sys.exit(f"ERROR: file path {args.cf} does not exist or isn't a directory")

    output_file_path = os.path.join(args.cf, "sorcha_citation.txt")

    # Makes sdtdout output the print statements into a temporary file
    output_capture = io.StringIO()
    sys.stdout = output_capture

    cite_sorcha()

    # writes the outputs in the temporary file to a text file
    with open(output_file_path, "w") as output_file:
        output_file.write(output_capture.getvalue())

    # Resets stdout back to normal
    sys.stdout = sys.__stdout__
    output_capture.close()

    print(f"Citations have been written into {os.path.abspath(output_file_path)}")
