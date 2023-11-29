# This code creates a very basic SLURM script for use with supercomputers.
#
# The resulting script will probably need to be edited to include the correct
# #SBATCH keywords for your specific setup.
#
# The code assumes that your physical parameters and orbits files (plus any other
# input files such as ephemeris files or complex physical parameters files) are
# all in the same folder and have a coherent naming scheme consisting of two identifiers:
# one for the file type and one for the object set. It then searches for files using
# the patterns you specify at the command line.

# For example: if you have orbits_b1.txt, orbits_b2.txt, params_b1.txt and params_b2.txt
# then supply "orbits_*" and "params_*" for the -ob and -p command line arguments respectively
# and the code will do the rest.

# This is quite flexible, so batch1_orbitfiles.txt  and '-ob *orbitfiles*' is fine too.

import os
import re
import sys
import glob
import argparse
from sorcha.modules.PPConfigParser import PPFindFileOrExit, PPFindDirectoryOrExit


def makeSLURM(args):
    """
    Generates a SLURM script from the arguments supplied at the command line.

    Parameters:
    -----------
    args (ArgumentParser object): command line arguments.

    Returns:
    -----------
    None.

    """

    sorcha_base_command = "srun --exclusive -N1 -n1 -c1 sorcha"

    orbits = get_sorted_list_of_files(args.inputs, args.orbits_stem)
    params = get_sorted_list_of_files(args.inputs, args.params_stem)

    if args.complex_stem:
        complexes = get_sorted_list_of_files(args.inputs, args.complex_stem)

    if args.ephem_read_stem:
        ephems = get_sorted_list_of_files(args.inputs, args.ephem_read_stem)

    if args.ncores:
        numcores = args.ncores
    else:
        numcores = len(orbits)

    with open(args.filename, "a") as the_file:
        the_file.write("#!/bin/bash\n")
        the_file.write("#SBATCH --job-name=" + args.jobname + "\n")
        the_file.write("#SBATCH --ntasks=" + str(numcores) + "\n")
        the_file.write("\n")
        the_file.write("\n")

    for i, orbits_fn in enumerate(orbits):
        # this uses re to strip the orbits_stem pattern from the base filename of the orbits file
        # hence getting the unique identifier of that object set. also removes any trailing underscores.

        root_fn = re.sub(
            re.escape(args.orbits_stem), "", os.path.basename(os.path.splitext(orbits_fn)[0])
        ).strip("_")

        # the lists were sorted, so this should be fine.
        params_fn = params[i]

        output_folder = os.path.join(args.outfile, root_fn)

        mkdir_command = " ".join(["mkdir", output_folder])

        full_command = [
            sorcha_base_command,
            "-c",
            args.config,
            "-ob",
            orbits_fn,
            "-p",
            params_fn,
            "-pd",
            args.pointing_database,
            "-o",
            output_folder,
            "-t",
            "_".join([args.output_stem, root_fn]),
        ]

        if args.ephem_write_stem:
            ephem_out = os.path.join(output_folder, "_".join([args.ephem_write_stem, root_fn + ".txt"]))
            full_command.extend(["-ew", ephem_out])
        if args.ephem_read_stem:
            full_command.extend(["-er", ephems[i]])
        if args.complex_stem:
            full_command.extend(["-cp", complexes[i]])
        if args.ar_data_path:
            full_command.extend(["-ar", args.ar_data_path])
        if args.force:
            full_command.extend("-f")

        command_out = " ".join(full_command)

        with open(args.filename, "a") as the_file:
            the_file.write(mkdir_command + "\n")
            the_file.write(command_out + " & \n")

    with open(args.filename, "a") as the_file:
        the_file.write("wait\n")


def convert_args_to_absolute_paths(args):
    """Ensures all filepaths given at command line are absolute paths.

    Parameters:
    -----------
    args (ArgumentParser object): dictionary of command line arguments

    Returns:
    -----------
    args (ArgumentParser object): dictionary of command line arguments with all filepaths absolute

    """

    args.filename = os.path.abspath(args.filename)
    args.inputs = os.path.abspath(args.inputs)
    args.config = os.path.abspath(args.config)
    args.pointing_database = os.path.abspath(args.pointing_database)
    args.outfile = os.path.abspath(args.outfile)

    if args.ar_data_path:
        args.ar_data_path = os.path.abspath(args.ar_data_path)

    return args


def get_sorted_list_of_files(filepath, stem):
    """Globs for a list of files using the suggested filepath and stem (which should
    include wildcards) then sorts the list. If no files are found, the code exits.

    Parameters:
    -----------
    filepath (string): filepath of folder where files are located

    stem (string): string containing filename pattern to search for

    Returns:
    -----------
    globbed_list (list): sorted list of filename strings

    """

    globbed_list = glob.glob(os.path.join(filepath, stem))
    globbed_list.sort()

    if not globbed_list:
        print("Could not find any files on given input path {} using stem {}.".format(filepath, stem))

    return globbed_list


def main():
    """
    This code creates a very basic SLURM script for use with supercomputers.

    The resulting script will probably need to be edited to include the correct
    #SBATCH keywords for your specific setup. Or feel free to edit this script
    directly!

    The code assumes that your input files are in the same folder.

    Note that instead of implementing loops in bash/shell the script lists every command
    explicitly. This was DELIBERATE and allows a user to copy/paste commands
    from the script if they want to rerun a specific part. I do know how to write
    a for-loop in bash, promise.

    usage: makeSLURMscript [-h] -f FILENAME -i INPUTS [-del] [-os] [-ss] [-c SSPPCON] -oo OIFOUT [-ao ALLOUT] [-m] [-dr] [-dc] [-dw] [-dl] [-n NCORES] [-jn JOBNAME] [-fo FORCE]
        arguments:
          -h, --help                            show this help message and exit
          -f FILENAME, --filename FILENAME      Filepath and name where you want to save the SLURM script.
          -i INPUTS, --inputs INPUTS            Path location of input text files (orbits, colours and config files).
          -del, --deletecache                   Delete the OIF cache once OIF has been run.
          -os, -oifonly                         Include only commands for OIF.
          -ss, -sspponly                        Include only commands for SSPP.
          -c SSPPCON, --ssppcon SSPPCON         Filepath and name of SSPP config file.
          -oo OIFOUT, --oifout OIFOUT           Path where OIF output is/will be stored.
          -ao ALLOUT, --allout ALLOUT           Path where final output will be stored.
          -m, --comet                           Include cometary activity files?
          -dr                                   Read from existing temporary ephemeris databases.
          -dc                                   Creates the temporary ephemeris databases in output folder before SSPP code execution.
          -dw                                   Make temporary ephemeris database in output folder during SSPP code execution. Overwrites existing database if present.
          -dl                                   Delete the temporary ephemeris databases after code has completed.
          -n NCORES, --ncores NCORES            Number of cores. Default will be one core per orbits input file.
          -jn JOBNAME, --jobname JOBNAME        Job name. Default is OIF+SSPP.
          -fo, --force                          Force deletion/overwrite of existing output file(s). Default False.

    """

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="Creating a SLURM script for Sorcha.",
    )

    required = parser.add_argument_group("Required arguments")

    required.add_argument(
        "-fn",
        "--filename",
        help="Filepath and name where you want to save the SLURM script.",
        type=str,
        dest="filename",
        required=True,
    )
    required.add_argument(
        "-in",
        "--inputs",
        help="Path location of input text files (orbits, colours and config files).",
        type=str,
        dest="inputs",
        required=True,
    )
    required.add_argument(
        "-c",
        "--config",
        help="Filepath and name of Sorcha config file.",
        type=str,
        dest="config",
        required=True,
    )
    required.add_argument(
        "-o",
        "--outfile",
        help="Path of folder where final output will be stored.",
        type=str,
        dest="outfile",
        required=True,
    )
    required.add_argument(
        "-pd",
        "--pointing_database",
        help="Survey pointing information",
        type=str,
        dest="pointing_database",
        required=True,
    )

    optional = parser.add_argument_group("Optional arguments")

    optional.add_argument(
        "-ob",
        "--orbits_stem",
        help="Orbit filename pattern. Use regex. Default is 'orbits*'.",
        type=str,
        dest="orbits_stem",
        required=False,
        default="orbits*",
    )
    optional.add_argument(
        "-p",
        "--params_stem",
        help="Physical parameters filename pattern. Use regex. Default is 'params*'.",
        type=str,
        dest="params_stem",
        required=False,
        default="params*",
    )
    optional.add_argument(
        "-er",
        "--ephem_read_stem",
        help="Previously generated ephemeris simulation file name pattern, required if ephemerides_type in config file is 'external'. Use regex, eg: 'ephem*'.",
        type=str,
        dest="ephem_read_stem",
        required=False,
        default=None,
    )
    optional.add_argument(
        "-ew",
        "--ephem_write_stem",
        help="Output stem file name for newly generated ephemeris simulation, required if ephemerides_type in config file is not 'external'.",
        type=str,
        dest="ephem_write_stem",
        required=False,
        default=None,
    )
    optional.add_argument(
        "-ar",
        "--ar_data_path",
        help="Directory path where Assist+Rebound data files where stored when running bootstrap_sorcha_data_files from the command line.",
        type=str,
        dest="ar_data_path",
        required=False,
    )
    optional.add_argument(
        "-cp",
        "--complex_stem",
        help="Complex physical parameters filename pattern, if using. Please use regex. Default is None.",
        type=str,
        dest="complex_stem",
        required=False,
        default=None,
    )
    optional.add_argument(
        "-n",
        "--ncores",
        help="Number of cores. Default will be one core per orbits input file.",
        type=int,
        dest="ncores",
        required=False,
        default=None,
    )
    optional.add_argument(
        "-jn", "--jobname", help="Job name. Default is Sorcha.", dest="jobname", type=str, default="Sorcha"
    )
    optional.add_argument(
        "-f",
        "--force",
        help="Force deletion/overwrite of existing output file(s). Default False.",
        dest="force",
        action="store_true",
        default=False,
    )
    optional.add_argument(
        "-t",
        "--output_stem",
        help="Output file name stem.",
        type=str,
        dest="output_stem",
        default="SorchaOutput",
    )

    args = parser.parse_args()

    args = convert_args_to_absolute_paths(args)

    _ = PPFindDirectoryOrExit(args.inputs, "-i, --inputs")
    _ = PPFindDirectoryOrExit(args.outfile, "-o, --outfile")
    _ = PPFindFileOrExit(args.pointing_database, "-pd, --pointing_database")
    _ = PPFindFileOrExit(args.config, "-c, --config")

    if args.ar_data_path:
        _ = PPFindDirectoryOrExit(args.ar_data_path, "-ar, --ar_data_path")

    makeSLURM(args)


if __name__ == "__main__":
    main()
