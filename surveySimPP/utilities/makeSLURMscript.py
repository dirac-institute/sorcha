# This code creates a very basic SLURM script for use with supercomputers.

# The resulting script will probably need to be edited to include the correct
# #SBATCH keywords for your specific setup.

# The code assumes that your physical parameters and orbits files are
# in the same folder and have filenames beginning with 'params' and 'orbits'
# respectively.

# Not that instead of implementing loops in bash the script lists every command
# explicitly. This was DELIBERATE and allows a user to copy/paste commands
# from the script if they want to rerun a specific part.

import os
import glob
import argparse


def makeSLURM(args):

    configfiles = glob.glob(args.inputs + 'config_*.ini')

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

        os_command = 'nice -n 10 oif -f ' + config + ' > ' + args.oifout + rootname + '.txt &'

        with open(args.filename, 'a') as the_file:
            the_file.write(os_command + '\n')

    with open(args.filename, 'a') as the_file:
        the_file.write('wait\n')

    orbits = glob.glob(args.inputs + 'orbits*.txt')

    for orbits_fn in orbits:

        rootname = os.path.basename(os.path.splitext(orbits_fn)[0])[7:]

        params_fn = args.inputs + 'params_' + rootname + '.txt'
        oif_fn = args.oifout + 'oif_' + rootname + '.txt'

        mkdir_command = 'mkdir ' + args.allout + rootname

        output_path = args.allout + rootname + '/'

        call_command = 'nice -n 10 surveySimPP -c {} -p {} -o {} -e {} -u {} -t {} -dw &'.format(args.ssppcon,
                                                                                                 params_fn, orbits_fn,
                                                                                                 oif_fn, output_path,
                                                                                                 rootname)

        with open(args.filename, 'a') as the_file:
            the_file.write(mkdir_command + '\n')
            the_file.write(call_command + '\n')


def main():

    parser = argparse.ArgumentParser(description='Creating a SLURM script for OIF+SSPP.')

    # filepath/name to save script as
    parser.add_argument('-f', '--filename', help='Filepath and name where you want to save the SLURM script.', type=str, required=True)
    # path to inputs
    parser.add_argument('-i', '--inputs', help='Path location of input text files (orbits, colours and config files). Default is current folder.', type=str, default="./")
    # SSPP config pathname
    parser.add_argument('-c', '--ssppcon', help='Name of SSPP config file. Default is PPConfig.ini', type=str, default='PPConfig.ini')
    # path where oif output will be stored
    parser.add_argument('-oo', '--oifout', help='Path where OIF output will be stored.', type=str, required=True)
    # final output pathname
    parser.add_argument('-ao', '--allout', help='Path where final output will be stored.', type=str, required=True)
    # cores to utilise (default: one core per orbits input file)
    parser.add_argument('-n', '--ncores', help='Number of cores. Default will be one core per orbits input file.', type=int, default=0)
    # job name
    parser.add_argument('-jn', '--jobname', help='Job name. Default is OIF+SSPP.', type=str, default='OIF+SSPP')

    args = parser.parse_args()

    makeSLURM(args)


if __name__ == '__main__':
    main()
