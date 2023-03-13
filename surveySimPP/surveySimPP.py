#!/usr/bin/python

import sys
import time
import numpy as np
import argparse
import os

from surveySimPP.modules.PPReadPointingDatabase import PPReadPointingDatabase
from surveySimPP.modules.PPLinkingFilter import PPLinkingFilter
from surveySimPP.modules.PPTrailingLoss import PPTrailingLoss
from surveySimPP.modules.PPBrightLimit import PPBrightLimit
from surveySimPP.modules.PPMakeTemporaryEphemerisDatabase import PPMakeTemporaryEphemerisDatabase
from surveySimPP.modules.PPCalculateApparentMagnitude import PPCalculateApparentMagnitude
from surveySimPP.modules.PPApplyFOVFilter import PPApplyFOVFilter
from surveySimPP.modules.PPSNRLimit import PPSNRLimit
from surveySimPP.modules import PPAddUncertainties, PPRandomizeMeasurements
from surveySimPP.modules import PPVignetting
from surveySimPP.modules.PPFadingFunctionFilter import PPFadingFunctionFilter
from surveySimPP.modules.PPConfigParser import PPConfigFileParser, PPPrintConfigsToLog
from surveySimPP.modules.PPGetLogger import PPGetLogger
from surveySimPP.modules.PPCommandLineParser import PPCommandLineParser
from surveySimPP.modules.PPReadAllInput import PPReadAllInput
from surveySimPP.modules.PPMagnitudeLimit import PPMagnitudeLimit
from surveySimPP.modules.PPOutput import PPWriteOutput
from surveySimPP.modules.PPGetMainFilterAndColourOffsets import PPGetMainFilterAndColourOffsets


# Author: Samuel Cornwall, Siegfried Eggl, Grigori Fedorets, Steph Merritt, Meg Schwamb

def runLSSTPostProcessing(cmd_args):
    """
    Runs the post processing survey simulator functions that apply a series of
    filters to bias a model Solar System small body population to what the
    Vera C. Rubin Observatory Legacy Survey of Space and Time would observe.

    Parameters:
    -----------
    cmd_args (dictionary): dictionary of command-line arguments.

    Returns:
    -----------
    None.

    """

    # Initialise argument parser and assign command line arguments

    pplogger = PPGetLogger(cmd_args['outpath'])
    pplogger.info('Post-processing begun.')

    # if verbosity flagged, the verboselog function will log the message specified
    # if not, verboselog does absolutely nothing
    verboselog = pplogger.info if cmd_args['verbose'] else lambda *a, **k: None

    verboselog('Reading configuration file...')
    configs = PPConfigFileParser(cmd_args['configfile'], cmd_args['surveyname'])

    verboselog('Configuration file successfully read.')

    configs['mainfilter'], configs['othercolours'] = PPGetMainFilterAndColourOffsets(cmd_args['paramsinput'],
                                                                                     configs['observing_filters'],
                                                                                     configs['aux_format'])

    PPPrintConfigsToLog(configs, cmd_args)

    # End of config parsing

    if cmd_args['makeTemporaryEphemerisDatabase']:
        verboselog('Creating temporary ephemeris database...')
        cmd_args['readTemporaryEphemerisDatabase'] = PPMakeTemporaryEphemerisDatabase(cmd_args['oifoutput'], cmd_args['makeTemporaryEphemerisDatabase'], configs['eph_format'])

    verboselog('Reading pointing database...')

    filterpointing = PPReadPointingDatabase(configs['pointing_database'], configs['observing_filters'], configs['pointing_sql_query'])

    verboselog('Instantiating random number generator ... ')

    if configs['rng_seed']:
        rng_seed = configs['rng_seed']
    else:
        rng_seed = int(time.time())

    verboselog('Random number seed is {}.'.format(rng_seed))
    rng = np.random.default_rng(rng_seed)

    # In case of a large input file, the data is read in chunks. The
    # "sizeSerialChunk" parameter in PPConfig.ini assigns the chunk.

    # Here, add loop which reads only a portion of input file to
    # avoid memory overflow
    startChunk = 0
    endChunk = 0
    # number of rows in an entire orbit file

    ii = -1
    with open(cmd_args['orbinfile']) as f:
        for ii, l in enumerate(f):
            pass
    lenf = ii

    while (endChunk < lenf):
        endChunk = startChunk + configs['size_serial_chunk']
        if (lenf - startChunk > configs['size_serial_chunk']):
            incrStep = configs['size_serial_chunk']
        else:
            incrStep = lenf - startChunk

        verboselog('Working on objects {}-{}.'.format(startChunk, endChunk))

        # Processing begins, all processing is done for chunks

        observations = PPReadAllInput(cmd_args, configs, filterpointing,
                                      startChunk, incrStep, verbose=cmd_args['verbose'])

        verboselog('Calculating apparent magnitudes...')
        observations = PPCalculateApparentMagnitude(observations,
                                                    configs['phase_function'],
                                                    configs['mainfilter'],
                                                    configs['othercolours'],
                                                    configs['observing_filters'],
                                                    configs['comet_activity'],
                                                    verbose=cmd_args['verbose'])

        if configs['trailing_losses_on']:
            verboselog('Calculating trailing losses...')
            dmagDetect = PPTrailingLoss(observations, "circularPSF")
            observations['PSFMag'] = dmagDetect + observations['TrailedSourceMag']
        else:
            observations['PSFMag'] = observations['TrailedSourceMag']

        verboselog('Calculating effects of vignetting on limiting magnitude...')
        observations['fiveSigmaDepthAtSource'] = PPVignetting.vignettingEffects(observations)

        verboselog('Applying field-of-view filters...')
        observations = PPApplyFOVFilter(observations, configs, rng, verbose=cmd_args['verbose'])

        # Note that the below code creates observedTrailedSourceMag and observedPSFMag
        # as columns in the observations dataframe.
        # These are the columns that should be used moving forward for filters etc.
        # Do NOT use TrailedSourceMag or PSFMag, these are cut later.
        verboselog('Calculating astrometric and photometric uncertainties, randomizing photometry...')
        observations = PPAddUncertainties.addUncertainties(observations, configs, rng)

        verboselog('Applying astrometric uncertainties...')
        observations["AstRATrue(deg)"] = observations["AstRA(deg)"]
        observations["AstDecTrue(deg)"] = observations["AstDec(deg)"]
        observations["AstRA(deg)"], observations["AstDec(deg)"] = PPRandomizeMeasurements.randomizeAstrometry(observations, rng, sigName='AstrometricSigma(deg)', sigUnits='deg')

        if configs['camera_model'] == 'footprint':
            verboselog('Re-applying field-of-view filter...')
            observations = PPApplyFOVFilter(observations, configs, rng, verbose=cmd_args['verbose'])

        if configs['SNR_limit_on']:
            verboselog('Dropping observations with signal to noise ratio less than {}...'.format(configs['SNR_limit']))
            observations = PPSNRLimit(observations, configs['SNR_limit'])

        if configs['mag_limit_on']:
            verboselog('Dropping detections fainter than user-defined magnitude limit... ')
            observations = PPMagnitudeLimit(observations, configs['mag_limit'])

        if configs['fading_function_on']:
            verboselog('Applying detection efficiency fading function...')
            observations = PPFadingFunctionFilter(observations, configs['fading_function_peak_efficiency'], configs['fading_function_width'], rng, verbose=cmd_args['verbose'])

        if configs['bright_limit_on']:
            verboselog('Dropping observations that are too bright...')
            observations = PPBrightLimit(observations, configs['observing_filters'], configs['bright_limit'])

        if len(observations) == 0:
            verboselog('No observations left in chunk. Skipping to next chunk...')
            startChunk = startChunk + configs['size_serial_chunk']
            continue

        if configs['SSP_linking_on']:
            verboselog('Applying SSP linking filter...')
            verboselog('Number of rows BEFORE applying SSP linking filter: ' + str(len(observations.index)))

            observations = PPLinkingFilter(observations,
                                           configs['SSP_detection_efficiency'],
                                           configs['SSP_number_observations'],
                                           configs['SSP_number_tracklets'],
                                           configs['SSP_track_window'],
                                           configs['SSP_separation_threshold'],
                                           rng)

            observations.reset_index(drop=True, inplace=True)
            verboselog('Number of rows AFTER applying SSP linking filter: ' + str(len(observations.index)))

        # write output
        PPWriteOutput(cmd_args, configs, observations, endChunk, verbose=cmd_args['verbose'])

        startChunk = startChunk + configs['size_serial_chunk']
        # end for

    if cmd_args['deleteTemporaryEphemerisDatabase']:
        verboselog('Deleting the temporary ephemeris database...')
        os.remove(cmd_args['readTemporaryEphemerisDatabase'])

    pplogger.info('Post processing completed.')


def main():
    """
    A post processing survey simulator that applies a series of filters to bias a
    model Solar System small body population to what the specified wide-field
    survey would observe.

    usage: surveySimPP [-h] -c C [-dw [DW]] [-dr DR] [-dl] [-m M] -p P -o O -e E [-s S] -u U [-t T] [-v] [-f]
        arguments:
          -h, --help         show this help message and exit
          -c C, --config C   Input configuration file name
          -dw [DW]           Make temporary ephemeris database. If no filepath/name supplied, default name and ephemeris input location used.
          -dr DR             Location of existing/previous temporary ephemeris database to read from if wanted.
          -dl                Delete the temporary ephemeris database after code has completed.
          -m M, --comet M    Comet parameter file name
          -p P, --params P   Physical parameters file name
          -o O, --orbit O    Orbit file name
          -e E, --ephem E    Ephemeris simulation output file name
          -s S, --survey S   Survey to simulate
          -u U, --outfile U  Path to store output and logs.
          -t T, --stem T     Output file name stem.
          -v, --verbose      Verbosity. Default currently true; include to turn off verbosity.
          -f, --force        Force deletion/overwrite of existing output file(s). Default False.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="Input configuration file name", type=str, dest='c', default='./PPConfig.ini', required=True)
    parser.add_argument("-dw", help="Make temporary ephemeris database. If no filepath/name supplied, default name and ephemeris input location used.", dest='dw', nargs='?', const='default', type=str)
    parser.add_argument("-dr", help="Location of existing/previous temporary ephemeris database to read from if wanted.", dest='dr', type=str)
    parser.add_argument("-dl", help="Delete the temporary ephemeris database after code has completed.", action='store_true', default=False)
    parser.add_argument("-m", "--comet", help="Comet parameter file name", type=str, dest='m')
    parser.add_argument("-p", "--params", help="Physical parameters file name", type=str, dest='p', default='./data/params', required=True)
    parser.add_argument("-o", "--orbit", help="Orbit file name", type=str, dest='o', default='./data/orbit.des', required=True)
    parser.add_argument("-e", "--ephem", help="Ephemeris simulation output file name", type=str, dest='e', default='./data/oiftestoutput', required=True)
    parser.add_argument("-s", "--survey", help="Survey to simulate", type=str, dest='s', default='LSST')
    parser.add_argument("-u", "--outfile", help="Path to store output and logs.", type=str, dest="u", default='./data/out/', required=True)
    parser.add_argument("-t", "--stem", help="Output file name stem.", type=str, dest="t", default='SSPPOutput')
    parser.add_argument("-v", "--verbose", help="Verbosity. Default currently true; include to turn off verbosity.", dest='v', default=True, action='store_false')
    parser.add_argument("-f", "--force", help="Force deletion/overwrite of existing output file(s). Default False.", dest='f', action='store_true', default=False)

    args = parser.parse_args()
    cmd_args = PPCommandLineParser(args)

    if cmd_args['surveyname'] in ['LSST', 'lsst']:
        runLSSTPostProcessing(cmd_args)
    else:
        sys.exit('ERROR: Survey name not recognised. Current allowed surveys are: {}'.format(['LSST', 'lsst']))


if __name__ == '__main__':
    main()
