#!/usr/bin/python

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

    args = parser.parse_args()

    cmd_args_dict = {}

    cmd_args_dict['paramsinput'] = PPFindFileOrExit(args.l, '-l, --params')
    cmd_args_dict['orbinfile'] = PPFindFileOrExit(args.o, '-o, --orbit')
    cmd_args_dict['oifoutput'] = PPFindFileOrExit(args.p, '-p, --pointing')
    cmd_args_dict['configfile'] = PPFindFileOrExit(args.c, '-c, --config')
    cmd_args_dict['outpath'] = PPFindFileOrExit(args.u, '-u, --outfile')

    if args.m:
        cmd_args_dict['cometinput'] = PPFindFileOrExit(args.m, '-m, --comet')

    cmd_args_dict['makeIntermediatePointingDatabase'] = bool(args.d)
    cmd_args_dict['surveyname'] = args.s
    cmd_args_dict['outfilestem'] = args.t
    cmd_args_dict['verbose'] = args.v

    return cmd_args_dict
