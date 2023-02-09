#!/usr/bin/python

import logging
import sys

from .PPReadOrbitFile import PPReadOrbitFile
from .PPCheckInputObjectIDs import PPCheckInputObjectIDs
from .PPReadCometaryParameters import PPReadCometaryParameters
from .PPReadTemporaryEphemerisDatabase import PPReadTemporaryEphemerisDatabase
from .PPReadEphemerides import PPReadEphemerides
from .PPJoinEphemeridesAndParameters import PPJoinEphemeridesAndParameters
from .PPJoinEphemeridesAndOrbits import PPJoinEphemeridesAndOrbits
from .PPMatchPointingToObservations import PPMatchPointingToObservations
from .PPReadPhysicalParameters import PPReadPhysicalParameters


def PPReadAllInput(cmd_args, configs, filterpointing, startChunk, incrStep, verbose=True):
    """
    Author: Grigori Federets and Steph Merritt

    Description: Reads in the simulation data and the orbit and physical parameter files, and then
    joins them with the pointing database to create a single Pandas dataframe of simulation
    data with all necessary orbit, physical parameter and pointing information.

    Mandatory input:	dict, cmd_args, dictionary of command line variables created by PPCommandLineParser
                        dict, configs, dictionary of config variables created by PPConfigFileParser
                        pandas DataFrame, filterpointing, pointing database
                        int, startChunk, start of chunk
                        int, incrStep, size of chunk

    Output:             pandas Dataframe, observations, dataframe of simulation data with all
                        necessary orbit, physical parameter and pointing information.
    """

    pplogger = logging.getLogger(__name__)
    verboselog = pplogger.info if verbose else lambda *a, **k: None

    verboselog('Reading input orbit file: ' + cmd_args['orbinfile'])
    padaor = PPReadOrbitFile(cmd_args['orbinfile'], startChunk, incrStep, configs['filesep'])

    verboselog('Reading input physical parameters: ' + cmd_args['paramsinput'])
    padacl = PPReadPhysicalParameters(cmd_args['paramsinput'], startChunk, incrStep, configs['filesep'])
    if (configs['cometactivity'] == 'comet'):
        verboselog('Reading cometary parameters: ' + cmd_args['cometinput'])
        padaco = PPReadCometaryParameters(cmd_args['cometinput'], startChunk, incrStep, configs['filesep'])

    objid_list = padacl['ObjID'].unique().tolist()

    if cmd_args['makeTemporaryEphemerisDatabase'] or cmd_args['readTemporaryEphemerisDatabase']:
        # read from temporary database
        verboselog('Reading from temporary ephemeris database.')
        padafr = PPReadTemporaryEphemerisDatabase(cmd_args['readTemporaryEphemerisDatabase'], objid_list)
    else:
        try:
            verboselog('Reading input ephemerides from: ' + cmd_args['oifoutput'])
            padafr = PPReadEphemerides(cmd_args['oifoutput'], configs['ephemerides_type'], configs["ephFormat"])

            padafr = padafr[padafr['ObjID'].isin(objid_list)]

        except MemoryError:
            pplogger.error('ERROR: insufficient memory. Try to run with -dw command line flag or reduce sizeSerialChunk.')
            sys.exit('ERROR: insufficient memory. Try to run with -dw command line flag or reduce sizeSerialChunk.')

    verboselog('Checking if object IDs in orbits, physical parameters and pointing simulation input files match...')
    PPCheckInputObjectIDs(padaor, padacl, padafr)

    if (configs['cometactivity'] == 'comet'):
        PPCheckInputObjectIDs(padaor, padaco, padafr)

    verboselog('Joining physical parameters and orbital data with simulation data...')
    observations = PPJoinEphemeridesAndParameters(padafr, padacl)
    observations = PPJoinEphemeridesAndOrbits(observations, padaor)
    if (configs['cometactivity'] == 'comet'):
        verboselog('Joining cometary data...')
        observations = PPJoinEphemeridesAndParameters(observations, padaco)

    verboselog('Joining info from pointing database with simulation data and dropping observations in non-requested filters...')
    observations = PPMatchPointingToObservations(observations, filterpointing)

    return observations
