#!/usr/bin/python

import os
import sys
import logging
from .PPConfigParser import PPFindFileOrExit


def PPCMDLineParser(parser):
    """
    Author: Steph Merritt

    Description: Parses the command line arguments, makes sure the filenames given actually exist,
    then stores them in a single dict.

    Will only look for the comet parameters file if it's actually given at the command line.

    Mandatory input:    ArgumentParser object, parser, of command line arguments

    output:             dictionary of variables taken from command line arguments

    """

    pplogger = logging.getLogger(__name__)

    args = parser.parse_args()

    cmd_args_dict = {}

    cmd_args_dict['paramsinput'] = PPFindFileOrExit(args.l, '-l, --params')
    cmd_args_dict['orbinfile'] = PPFindFileOrExit(args.o, '-o, --orbit')
    cmd_args_dict['oifoutput'] = PPFindFileOrExit(args.p, '-p, --pointing')
    cmd_args_dict['configfile'] = PPFindFileOrExit(args.c, '-c, --config')
    cmd_args_dict['outpath'] = PPFindFileOrExit(args.u, '-u, --outfile')

    if args.m:
        cmd_args_dict['cometinput'] = PPFindFileOrExit(args.m, '-m, --comet')

    cmd_args_dict['makeIntermediateEphemerisDatabase'] = bool(args.dw)
    cmd_args_dict['readIntermediateEphemerisDatabase'] = args.dr
    cmd_args_dict['deleteIntermediateEphemerisDatabase'] = bool(args.dl)
    cmd_args_dict['surveyname'] = args.s
    cmd_args_dict['outfilestem'] = args.t
    cmd_args_dict['verbose'] = args.v

    if args.dr and args.dw:
        pplogger.error('ERROR: both -dr and -dw flags set at command line. Please use only one.')
        sys.exit('ERROR: both -dr and -dw flags set at command line. Please use only one.')

    if args.dl and not args.dr and not args.dw:
        pplogger.error('ERROR: -dl flag set without either -dr or -dw.')
        sys.exit('ERROR: -dl flag set without either -dr or -dw.')

    if args.dr and not os.path.exists(args.dr):
        pplogger.error('ERROR: interim ephemeris database not found at ' + args.dr + '. Rerun with command line flag -dw to create one.')
        sys.exit('ERROR: interim ephemeris database not found at ' + args.dr + '. Rerun with command line flag -dw to create one.')

    return cmd_args_dict
