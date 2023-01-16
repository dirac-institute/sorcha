# Creates temporary ephemeris databases in SQL. These can take a while to create,
# especially for large OIF/ephemeris files, but greatly speed up the actual
# running of SSPP. The databases will be named temp_[input_filename].db and will
# be saved in the same folder.

import glob
import argparse
import os
import sys
from surveySimPP.modules.PPConfigParser import PPFindDirectoryOrExit
from surveySimPP.modules.PPMakeTemporaryEphemerisDatabase import PPMakeTemporaryEphemerisDatabase


def make_temporary_databases(args):

    input_path = os.path.abspath(args.inputs)
    file_list = glob.glob(os.path.join(input_path, args.stem) + '*')

    if not file_list:
        sys.exit('Could not find any files using given input path and stem.')

    for input_name in file_list:
        stem_filename = 'temp_' + os.path.basename(input_name).split('.')[0]
        PPMakeTemporaryEphemerisDatabase(input_name, input_path, 'csv', stemname=stem_filename)


def main():

    parser = argparse.ArgumentParser(description='Creating the temporary SQL ephemeris databses.')

    # path to inputs
    parser.add_argument('-i', '--inputs', help='Path location of input ephemeris text files.', type=str, required=True)
    # stem filename for outputs
    parser.add_argument('-s', '--stem', help='Stem filename of input ephemeris text files. Default is "oif_".', type=str, default='oif_')
    # chunk size for creating databases
    parser.add_argument('-c', '--chunk', help="Chunking size for creation, where chunk=number of rows per chunk. Don't change this unless you know what you're doing.", type=int, default=10000)

    args = parser.parse_args()

    _ = PPFindDirectoryOrExit(args.inputs, '-i, --inputs')

    make_temporary_databases(args)


if __name__ == '__main__':
    main()
