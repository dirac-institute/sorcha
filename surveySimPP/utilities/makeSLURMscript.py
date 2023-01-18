# This code creates a very basic SLURM script for use with supercomputers.

# The resulting script will probably need to be edited to include the correct
# #SBATCH keywords for your specific setup.

# The code assumes that your physical parameters and orbits files are
# in the same folder and have filenames beginning with 'params' and 'orbits'
# respectively. COmetary activity files must begin with 'comets', and
# temporary ephemeris simulation databases must begin with "temp_" and then the
# filename of the ephemeris file they were created from.

# Note that instead of implementing loops in bash the script lists every command
# explicitly. This was DELIBERATE and allows a user to copy/paste commands
# from the script if they want to rerun a specific part.

import os
import sys
import glob
import argparse
from surveySimPP.modules.PPConfigParser import PPFindFileOrExit, PPFindDirectoryOrExit


def makeSLURM(args):

    configfiles = glob.glob(os.path.join(args.inputs, 'config_*.ini'))

    if not configfiles:
        sys.exit('Could not find any OIF config files files on given input path.')

    if args.ncores:
        numcores = args.ncores
    else:
        numcores = len(configfiles)

    with open(args.filename, 'a') as the_file:
        the_file.write('#!/bin/bash\n')
        the_file.write('#SBATCH --job-name=' + args.jobname + '\n')
        the_file.write('#SBATCH --ntasks=' + str(numcores) + '\n')
        the_file.write('\n')
        the_file.write('\n')

    for config in configfiles:
        rootname = 'oif_' + os.path.basename(os.path.splitext(config)[0])[7:]

        os_command = 'nice -n 10 oif -f ' + config + ' > ' + os.path.join(args.oifout, rootname + '.txt') + ' &'

        with open(args.filename, 'a') as the_file:
            the_file.write(os_command + '\n')

    with open(args.filename, 'a') as the_file:
        the_file.write('wait\n')

    orbits = glob.glob(args.inputs + 'orbits*.txt')

    if not orbits:
        sys.exit('Could not find any orbits files on given input path.')

    for orbits_fn in orbits:

        rootname = os.path.basename(os.path.splitext(orbits_fn)[0])[7:]

        params_fn = os.path.join(args.inputs, 'params_' + rootname + '.txt')
        _ = PPFindFileOrExit(params_fn, 'physical parameters file')

        oif_fn = os.path.join(args.oifout, 'oif_' + rootname + '.txt')

        output_path = os.path.join(args.allout, rootname)
        mkdir_command = 'mkdir ' + output_path

        call_command = 'nice -n 10 surveySimPP -c {} -p {} -o {} -e {} -u {} -t {}'.format(args.ssppcon,
                                                                                           params_fn, orbits_fn,
                                                                                           oif_fn, output_path,
                                                                                           rootname)

        if args.comet:
            comets_fn = os.path.join(args.inputs, 'comet_' + rootname + '.txt')
            _ = PPFindFileOrExit(comets_fn, 'cometary activity parameters file')
            call_command = call_command + ' -m ' + comets_fn

        if args.dr:
            temp_fn = os.path.join(args.oifout, 'temp_oif_' + rootname + '.db')
            _ = PPFindFileOrExit(temp_fn, 'temporary ephemeris database')
            call_command = call_command + ' -dr ' + temp_fn

        if args.dw:
            call_command = call_command + ' -dw'

        if args.dl:
            call_command = call_command + ' -dl'

        with open(args.filename, 'a') as the_file:
            the_file.write(mkdir_command + '\n')
            the_file.write(call_command + ' & \n')

    with open(args.filename, 'a') as the_file:
        the_file.write('wait\n')


def main():

    parser = argparse.ArgumentParser(description='Creating a SLURM script for OIF+SSPP.')

    # filepath/name to save script as
    parser.add_argument('-f', '--filename', help='Filepath and name where you want to save the SLURM script.', type=str, required=True)
    # path to inputs
    parser.add_argument('-i', '--inputs', help='Path location of input text files (orbits, colours and config files).', type=str, required=True)
    # SSPP config pathname
    parser.add_argument('-c', '--ssppcon', help='Filepath and name of SSPP config file.', type=str, required=True)
    # path where oif output will be stored
    parser.add_argument('-oo', '--oifout', help='Path where OIF output will be stored.', type=str, required=True)
    # final output pathname
    parser.add_argument('-ao', '--allout', help='Path where final output will be stored.', type=str, required=True)
    # cometary activity?
    parser.add_argument('-m', '--comet', help="Include cometary activity files?", action='store_true', default=False)
    # read from temporary databases?
    parser.add_argument("-dr", help="Read from existing temporary ephemeris databases.", action='store_true', default=False)
    # write temporary databases?
    parser.add_argument("-dw", help="Make temporary ephemeris database in output folder. Overwrites existing database if present.", default=False, action='store_true')
    # delete temporary databases?
    parser.add_argument("-dl", help="Delete the temporary ephemeris databases after code has completed.", action='store_true', default=False)
    # cores to utilise (default: one core per orbits input file)
    parser.add_argument('-n', '--ncores', help='Number of cores. Default will be one core per orbits input file.', type=int, default=0)
    # job name
    parser.add_argument('-jn', '--jobname', help='Job name. Default is OIF+SSPP.', type=str, default='OIF+SSPP')

    args = parser.parse_args()

    if args.dr and args.dw:
        sys.exit('Cannot have both -dr and -dw command flag arguments.')

    _ = PPFindDirectoryOrExit(args.inputs, '-i, --inputs')
    _ = PPFindDirectoryOrExit(args.oifout, '-oo, --oifout')
    _ = PPFindDirectoryOrExit(args.allout, '-ao, --allout')

    makeSLURM(args)


if __name__ == '__main__':
    main()
