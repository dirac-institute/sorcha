# Creates config files for post-processing from the command line, for use in scripts.
# python makeConfigFilePP.py --help will give usage instructions
# Needs some error handling.

import argparse
import configparser


def makeConfigFile(args):

    config = configparser.ConfigParser()

    filtering_raw = {'brightLimit': str(args.brightlimit),
                     'fadingFunctionOn': str(args.fadingfunction),
                     'fadingFunctionWidth': str(args.fadingwidth),
                     'fillfactor': str(args.fillfactor),
                     'SSPDetectionEfficiency': str(args.detectionefficiency),
                     'minTracklet': str(args.mintracklet),
                     'noTracklets': str(args.notracklets),
                     'trackletInterval': str(args.trackletinterval),
                     'inSepThreshold': str(args.insepthreshold)}

    filtering_dict = {k: v for k, v in filtering_raw.items() if v != 'None'}

    config_dict = {
            'OBJECTS':
            {'cometactivity': args.cometactivity},
            'INPUTFILES':
            {'ephemerides_type': args.ephemeridestype,
                'pointingdatabase': args.pointingdatabase,
                'footprintPath': args.footprintpath,
                'ppsqldbquery': args.ppsqldbquery,
                'ephFormat': args.ephformat,
                'auxFormat': args.auxformat},
            'FILTERS':
            {'observing_filters': args.observingfilters},
            'PHASE':
            {'phasefunction': args.phasefunction},
            'PERFORMANCE':
            {'cameraModel': args.cameramodel},
            'FILTERINGPARAMETERS': filtering_dict,
            'OUTPUTFORMAT':
            {'outputformat': args.outputformat,
                'outputsize': args.outputsize,
                'position_decimals': str(args.positiondecimals),
                'magnitude_decimals': str(args.magnitudedecimals)},
            'GENERAL':
            {'sizeSerialChunk': str(args.sizeserialchunk)},
            'EXPERT':
            {'SNRLimit': str(args.snrlimit),
             'magLimit': str(args.maglimit),
             'trailingLossesOn': str(args.trailinglosseson)}
                  }

    config.read_dict(config_dict)

    with open(args.filename, 'w') as f:
        config.write(f)

#    for filename in filenames:
#        with open(filename, 'w') as f:
#            config.write(f)


def main():

    parser = argparse.ArgumentParser(description='Creating the config file for SSP.')

    parser.add_argument('filename', help='Filepath where you want to store the config file.', type=str)

    # OBJECTS
    parser.add_argument('--cometactivity', '-com', help='Type of cometary activity. Options are "comet" or None. Default is none.', type=str, default='none')

    # INPUTFILES
    parser.add_argument('--ephemeridestype', '-eph', help='Type of input ephemerides: default = oif. Options: currently only oif.', type=str, default='oif')
    parser.add_argument('--pointingdatabase', '-inpt', help='Path to pointing database. Default is "./demo/baseline_v2.0_1yr.db".', type=str, default='./demo/baseline_v2.0_1yr.db')
    parser.add_argument('--footprintpath', '-infoot', help='Path to camera footprint file. Default is "./data/detectors_corners.csv".', type=str, default='./data/detectors_corners.csv')
    parser.add_argument('--ephformat', '-inptf', help='Separator in ephemeris database: csv, whitespace, hdf5. Default is "whitespace".', type=str, default='whitespace')
    parser.add_argument('--auxformat', '-inauxf', help='Separator in orbit/colour/brightness/cometary data files: comma or whitespace. Default is "whitespace".', type=str, default='whitespace')
    parser.add_argument('--ppsqldbquery', '-query', help='Database query for extracting data for pointing database.', type=str, default='SELECT observationId, observationStartMJD, filter, seeingFwhmGeom, seeingFwhmEff, fiveSigmaDepth, fieldRA, fieldDec, rotSkyPos FROM observations order by observationId')

    # FILTERS
    parser.add_argument('--observingfilters', '-rfilt', help='Observing filters: main filter in which H is calculated, followed by resolved colours, such as, e.g. \'r\'+\'g-r\'=\'g\'. Should be separated by comma. Default is "r,g,i,z"', type=str, default='r,g,i,z')

    # PHASE
    parser.add_argument('--phasefunction', '-phfunc', help='Define the used input phase function. Options: HG, HG1G2, HG12, linear, none. Default is "HG".', type=str, default='HG')

    # PERFORMANCE
    parser.add_argument('--trailinglosseson', '-tloss', help='Switch on trailing losses. Relevant for close-approaching NEOs. Default False.', type=bool, default=False)
    parser.add_argument('--cameramodel', '-cammod', help='Choose between surface area equivalent or actual camera footprint, including chip gaps. Options: circle, footprint. Default is "footprint".', type=str, default='footprint')

    # FILTERINGPARAMETERS
    parser.add_argument('--snrlimit', '-snr', help='SNR limit: drop observations below this SNR threshold. Omit/None for default 2.0 SNR cut.', type=float, default=None)
    parser.add_argument('--maglimit', '-mag', help='Magnitude threshold: drop observations below this magnitude. Omit/None for no magnitude cut.', type=float, default=None)
    parser.add_argument('--fadingfunction', '-fade', help='Detection efficiency fading function on or off.', type=bool, default=True)
    parser.add_argument('--fadingwidth', '-fadew', help='Width parameter for fading function. Default is 0.1 after Chelsey and Vereš (2017) or None to omit.', type=float, default=0.1)
    parser.add_argument('--detectionefficiency', '-deteff', help='Which fraction of the detections will the automated solar system processing pipeline recognise? Expects a float. Default is 0.95.', type=float, default=0.95)
    parser.add_argument('--fillfactor', '-ff', help='Fraction of detector surface area which contains CCD -- simulates chip gaps. Expects a float or None to omit. Default is None.', type=float, default=None)
    parser.add_argument('--mintracklet', '-mintrk', help='How many observations during one night are required to produce a valid tracklet? Expects an int or None to omit. Default 2.', type=int, default=2)
    parser.add_argument('--notracklets', '-ntrk', help='How many tracklets are required to classify as a detection? Expects an int or None to omit. Default 3.', type=int, default=3)
    parser.add_argument('--trackletinterval', '-inttrk', help='In what amount of time does the aforementioned number of tracklets needs to be discovered to constitute a complete detection? In days. Expects a float or None to omit. Default 15.0.', type=float, default=15.0)
    parser.add_argument('--brightlimit', '-brtlim', help='Limit of brightness: detections brighter than this are omitted assuming saturation. Expects a float or None to omit. Default is 16.0.', type=float, default=16.0)
    parser.add_argument('--insepthreshold', '-minsep', help='Minimum separation inside the tracklet for SSP distinguish motion between two images, in arcsec. Expects a float or None to omit. Default is 0.5.', type=float, default=0.5)

    # OUTPUTFORMAT
    parser.add_argument('--outputformat', '-outf', help='Output format. Options: csv, sqlite3, hdf5. Default is csv.', type=str, default='csv')
    parser.add_argument('--outputsize', '-outs', help='Size of output. Controls which columns are in the output files. Options are "default" only.', type=str, default='default')
    parser.add_argument('--positiondecimals', '-posd', help='Decimal places RA and Dec should be rounded to in output. Default is 7.', type=int, default=7)
    parser.add_argument('--magnitudedecimals', '-magd', help='Decimal places magnitudes should be rounded to in output. Default is 3.', type=int, default=3)

    # GENERAL
    parser.add_argument('--sizeserialchunk', '-chunk', help='Size of chunk of objects to be processed serially. Default is 10.', type=int, default=10)

    args = parser.parse_args()

    makeConfigFile(args)


if __name__ == '__main__':
    main()
