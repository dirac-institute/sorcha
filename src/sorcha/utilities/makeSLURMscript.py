# This code creates a very basic SLURM script for use with supercomputers.
#
# The resulting script will probably need to be edited to include the correct
# #SBATCH keywords for your specific setup.
#
# The code assumes that your physical parameters and orbits files are
# in the same folder and have filenames beginning with 'params' and 'orbits'
# respectively. COmetary activity files must begin with 'comets', and
# temporary ephemeris simulation databases must begin with "temp_" and then the
# filename of the ephemeris file they were created from.
#
# Note that instead of implementing loops in bash the script lists every command
# explicitly. This was DELIBERATE and allows a user to copy/paste commands
# from the script if they want to rerun a specific part.

import os
import sys
import glob
import argparse
from sorcha.modules.PPConfigParser import PPFindFileOrExit, PPFindDirectoryOrExit


def makeSLURM(args):
    """
    Generates a SLURM script from the arguments supplied at the command line.

    Parameters:
    -----------
    args (argparse ArgumentParser object): command line arguments.

    Returns:
    -----------
    None.

    """

    configfiles = glob.glob(os.path.join(args.inputs, "config_*.ini"))
    configfiles.sort()

    if not configfiles:
        sys.exit("Could not find any OIF config files on given input path: {}".format(args.inputs))

    if args.ncores:
        numcores = args.ncores
    else:
        numcores = len(configfiles)

    with open(args.filename, "a") as the_file:
        the_file.write("#!/bin/bash\n")
        the_file.write("#SBATCH --job-name=" + args.jobname + "\n")
        the_file.write("#SBATCH --ntasks=" + str(numcores) + "\n")
        the_file.write("\n")
        the_file.write("\n")

    if not args.ss:
        for config in configfiles:
            rootname = "oif_" + os.path.basename(os.path.splitext(config)[0])[7:]

            os_command = (
                "srun --exclusive -N1 -n1 -c1 oif -f "
                + config
                + " > "
                + os.path.join(args.oifout, rootname + ".txt")
                + " &"
            )

            with open(args.filename, "a") as the_file:
                the_file.write(os_command + "\n")

        with open(args.filename, "a") as the_file:
            the_file.write("wait\n")

    if args.deletecache:
        with open(args.filename, "a") as the_file:
            the_file.write("rm -r " + os.path.join(args.oifout, "_cache") + "\n")
            the_file.write("wait\n")

    if not args.os:
        if args.dc:
            with open(args.filename, "a") as the_file:
                the_file.write("createTemporaryDatabases -i {} &\n".format(args.oifout))
                the_file.write("wait\n")

        orbits = glob.glob(os.path.join(args.inputs, "orbits*"))
        orbits.sort()

        if not orbits:
            sys.exit(
                "Could not find any orbits files on given input path {}.".format(args.inputs + "orbits*")
            )

        for orbits_fn in orbits:
            rootname = os.path.basename(os.path.splitext(orbits_fn)[0])[7:]

            params_fn = os.path.join(args.inputs, "params_" + rootname + ".txt")
            _ = PPFindFileOrExit(params_fn, "physical parameters file")

            oif_fn = os.path.join(args.oifout, "oif_" + rootname + ".txt")

            output_path = os.path.join(args.allout, rootname)
            mkdir_command = "mkdir " + output_path

            call_command = "srun --exclusive -N1 -n1 -c1 sorcha -c {} -p {} -o {} -e {} -u {} -t {}".format(
                args.ssppcon, params_fn, orbits_fn, oif_fn, output_path, rootname
            )

            if args.comet:
                comets_fn = os.path.join(args.inputs, "comet_" + rootname + ".txt")
                _ = PPFindFileOrExit(comets_fn, "cometary activity parameters file")
                call_command = call_command + " -m " + comets_fn

            if args.dr or args.dc:
                temp_fn = os.path.join(args.oifout, "temp_oif_" + rootname + ".db")
                call_command = call_command + " -dr " + temp_fn

            if args.dw:
                call_command = call_command + " -dw"

            if args.dl:
                call_command = call_command + " -dl"

            with open(args.filename, "a") as the_file:
                the_file.write(mkdir_command + "\n")
                the_file.write(call_command + " & \n")

        with open(args.filename, "a") as the_file:
            the_file.write("wait\n")


def convert_args_to_absolute_paths(args):
    args.filename = os.path.abspath(args.filename)
    args.inputs = os.path.abspath(args.inputs)
    args.ssppcon = os.path.abspath(args.ssppcon)
    args.oifout = os.path.abspath(args.oifout)
    args.allout = os.path.abspath(args.allout)

    return args


def main():
    """
    This code creates a very basic SLURM script for use with supercomputers.

    The resulting script will probably need to be edited to include the correct
    #SBATCH keywords for your specific setup. Or feel free to edit this script
    directly!

    The code assumes that your physical parameters and orbits files are
    in the same folder and have filenames beginning with 'params' and 'orbits'
    respectively. Cometary activity files must begin with 'comets', and
    temporary ephemeris simulation databases must begin with `temp_` and then the
    filename of the ephemeris file they were created from.

    Note that instead of implementing loops in bash the script lists every command
    explicitly. This was DELIBERATE and allows a user to copy/paste commands
    from the script if they want to rerun a specific part.

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

    parser = argparse.ArgumentParser(description="Creating a SLURM script for OIF+SSPP.")

    # filepath/name to save script as
    parser.add_argument(
        "-f",
        "--filename",
        help="Filepath and name where you want to save the SLURM script.",
        type=str,
        required=True,
    )
    # path to inputs
    parser.add_argument(
        "-i",
        "--inputs",
        help="Path location of input text files (orbits, colours and config files).",
        type=str,
        required=True,
    )
    # flag to delete OIF cache
    parser.add_argument(
        "-del",
        "--deletecache",
        help="Delete the OIF cache once OIF has been run.",
        action="store_true",
        default=False,
    )
    # flag to run only OIF
    parser.add_argument(
        "-os", "-oifonly", help="Include only commands for OIF.", action="store_true", default=False
    )
    # flag to run only SSPP
    parser.add_argument(
        "-ss", "-sspponly", help="Include only commands for SSPP.", action="store_true", default=False
    )
    # SSPP config pathname
    parser.add_argument(
        "-c", "--ssppcon", help="Filepath and name of SSPP config file.", type=str, default=False
    )
    # path where oif output will be stored
    parser.add_argument(
        "-oo", "--oifout", help="Path where OIF output is/will be stored.", type=str, required=True
    )
    # final output pathname
    parser.add_argument(
        "-ao", "--allout", help="Path where final output will be stored.", type=str, default=False
    )
    # cometary activity?
    parser.add_argument(
        "-m", "--comet", help="Include cometary activity files?", action="store_true", default=False
    )
    # read from temporary databases?
    parser.add_argument(
        "-dr", help="Read from existing temporary ephemeris databases.", action="store_true", default=False
    )
    # create temporary ephemeris database in advance?
    parser.add_argument(
        "-dc",
        help="Creates the temporary ephemeris databases in output folder before SSPP code execution.",
        default=False,
        action="store_true",
    )
    # write temporary databases?
    parser.add_argument(
        "-dw",
        help="Make temporary ephemeris database in output folder during SSPP code execution. Overwrites existing database if present.",
        default=False,
        action="store_true",
    )
    # delete temporary databases?
    parser.add_argument(
        "-dl",
        help="Delete the temporary ephemeris databases after code has completed.",
        action="store_true",
        default=False,
    )
    # cores to utilise (default: one core per orbits input file)
    parser.add_argument(
        "-n",
        "--ncores",
        help="Number of cores. Default will be one core per orbits input file.",
        type=int,
        default=0,
    )
    # job name
    parser.add_argument(
        "-jn", "--jobname", help="Job name. Default is OIF+SSPP.", type=str, default="OIF+SSPP"
    )
    # force?
    parser.add_argument(
        "-fo",
        "--force",
        help="Force deletion/overwrite of existing output file(s). Default False.",
        dest="f",
        action="store_true",
        default=False,
    )

    args = parser.parse_args()

    # NOTE: it would be nice to move all of the error handling into a function
    # so it can be unit tested.

    if args.dr and args.dw:
        sys.exit("Cannot have both -dr and -dw command flag arguments.")
    if args.dw and args.dc:
        sys.exit("Cannot have both -dc and -dw command flag arguments.")
    if args.os and args.ss:
        sys.exit("Cannot have both -os and -ss command flag arguments.")

    if not args.os and not args.allout:
        sys.exit("-ao argument is required if running SSPP.")
    elif not args.os and not args.ssppcon:
        sys.exit("-c argument is required if running SSPP.")

    if os.path.isfile(os.path.abspath(args.filename)) and not args.f:
        sys.exit("File already exists at given location/name.")
    elif os.path.isfile(os.path.abspath(args.filename)) and args.f:
        os.remove(args.filename)

    args = convert_args_to_absolute_paths(args)

    _ = PPFindDirectoryOrExit(args.inputs, "-i, --inputs")
    _ = PPFindDirectoryOrExit(args.oifout, "-oo, --oifout")

    if not args.ss:
        _ = PPFindDirectoryOrExit(args.allout, "-ao, --allout")

    makeSLURM(args)


if __name__ == "__main__":
    main()
