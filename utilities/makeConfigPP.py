# Creates config files for post-processing from the command line, for use in scripts.
# python makeConfigFilePP.py --help will give usage instructions
# Needs some error handling.

import argparse
import configparser

def makeConfigFile(args):

	config = configparser.ConfigParser()

	config.read_dict({
            'OBJECTS':
                {
                'objecttype':				args.objecttype
                },
            'INPUTFILES': 
                {
                'pointingdatabase':  		args.pointingdatabase, 
                'footprintPath':        	args.footprintpath,
                'ppsqldbquery':				'SELECT observationId, observationStartMJD, filter, seeingFwhmGeom, seeingFwhmEff, fiveSigmaDepth, fieldRA, fieldDec, rotSkyPos FROM SummaryAllProps order by observationId',
                'pointingFormat':			args.pointingformat,
                'auxFormat':				args.auxformat
                },
            'FILTERS':
                {
                'mainfilter':   			args.mainfilter,
                'othercolours':         	args.othercolours,
                'resfilters':				args.resfilter
                },
            'PHASE':
                {
                'phasefunction':   			args.phasefunction
                },
            'PERFORMANCE':
                {
                'trailingLossesOn':   		args.trailinglosseson,
                'cameraModel':          	args.cameramodel
                },
            'FILTERINGPARAMETERS':
                {
                'SSPDetectionEfficiency':   args.detectionefficiency,
                'fillfactor':         		args.fillfactor,
                'minTracklet':				args.mintracklet,
                'noTracklets':				args.notracklets,
                'trackletInterval':			args.trackletinterval,
                'brightLimit':				args.brightlimit,
                'inSepThreshold':			args.insepthreshold
                },
            'OUTPUTFORMAT':
                {
                'outpath':   				args.outpath,
                'outfilestem':         		args.outfilestem,
                'outputformat':				args.outputformat,
                'separatelyCSV':			args.separatelycsv
                },
            'GENERAL':
                {
                'sizeSerialChunk':   		args.sizeserialchunk,
                'testValue':				1			
                }
					})
	
	with open(args.filename, 'w') as filename:
		config.write(filename)
		

def main():

	parser = argparse.ArgumentParser(description='Creating the config file for SSP.')
	
	parser.add_argument('filename', help='Filepath where you want to store the config file.', type=str)
	
	# OBJECTS
	parser.add_argument('--objecttype', '-obj', help='Type of object: asteroid or comet. Default is "asteroid".', type=str, default='asteroid')
	
	# INPUTFILES
	parser.add_argument('-pointingdatabase', '-inpt', help='Path to pointing database. Default is "./data/test/baseline_10yrs_10klines.db".', type=str, default='./data/test/baseline_10yrs_10klines.db')
	parser.add_argument('--footprintpath', '-infoot', help='Path to camera footprint file. Default is "./data/detectors_corners.csv".', type=str, default='./data/detectors_corners.csv')
	parser.add_argument('--pointingformat', '-inptf', help='Separator in pointing database: csv, whitespace, hdf5. Default is "whitespace".', type=str, default='whitespace')
	parser.add_argument('--auxformat', '-inauxf', help='Separator in orbit/colour/brightness/cometary data files: comma or whitespace. Default is "whitespace".', type=str, default='whitespace')
	
	# FILTERS
	parser.add_argument('--mainfilter', '-mfilt', help='The main filter in the colour file to which all other colours are compared. Default is "r".', type=str, default='r')
	parser.add_argument('--othercolours', '-ofilt', help='Other colours with respect to the main filter, e.g g-r. Should be given separated by comma. Default is "g-r,i-r,z-r".', type=str, default='g-r,i-r,z-r')
	parser.add_argument('--resfilter', '-rfilt', help='resulting filters; main filter, followed by resolved colours, such as, e.g. \'r\'+\'g-r\'=\'g\'. Should be given in the following order: main filter, resolved filters in the same order as respective other colours. Should be separated by comma. Default is "r,g,i,z"', 
									type=str, default='r,g,i,z')
										
	# PHASE
	parser.add_argument('--phasefunction', '-phfunc', help='Define the used input phase function. Options: HG, HG1G2, HG12, linear, none. Default is "HG".', type=str, default='HG')
	
	# PERFORMANCE
	parser.add_argument('--trailinglosseson', '-tloss', help='Switch on trailing losses. Revelant for close-approaching NEOs. Default False.', action="store_true")
	parser.add_argument('--cameramodel', '-cammod', help='Choose between surface area equivalent or actual camera footprint, including chip gaps. Options: circle, footprint. Default is "footprint".', type=str, default='footprint')
	
	# FILTERINGPARAMETERS
	parser.add_argument('--detectionefficiency', '-deteff', help='Which fraction of the detections will the automated solar system processing pipeline recognise? Expects a float. Default is 0.95.', type=float, default=0.95)	
	parser.add_argument('--fillfactor', '-ff', help='Fraction of detector surface area which contains CCD -- simulates chip gaps. Expects a float. Default is 0.9.', type=float, default=0.9)
	parser.add_argument('--mintracklet', '-mintrk', help='How many observations during one night are required to produce a valid tracklet? Expects an int. Default 2.', type=int, default=2)
	parser.add_argument('--notracklets', '-ntrk', help='How many tracklets are required to classify as a detection? Expects an int. Default 3.', type=int, default=3)
	parser.add_argument('--trackletinterval', '-inttrk', help='In what amount of time does the aforementioned number of tracklets needs to be discovered to constitute a complete detection? In days. Expects a float. Default 15.0.', type=float, default=15.0)
	parser.add_argument('--brightlimit', '-brtlim', help='Limit of brightness: detections brighter than this are omitted assuming saturation. Expects a float. Default is 16.0.', type=float, default=16.0)
	parser.add_argument('--insepthreshold', '-minsep', help='Minimum separation inside the tracklet for SSP distinguish motion between two images, in arcsec. Expects a float. Default is 0.5.', type=float, default=0.5)
	
	# OUTPUTFORMAT
	parser.add_argument('--outpath', '-out', help='Path to output. Default is "./data/out".', type=str, default='./data/out/')
	parser.add_argument('--outfilestem', '-outstem', help='Output file name stem. Default is "hundredcomets"', type=str, default='hundredcomets')
	parser.add_argument('--outputformat', '-outf', help="Output format. Options: csv, sqlite3, hdf5. Default is csv.", type=str, default='csv')
	parser.add_argument('--separatelycsv', '-sepcsv', help="Toggle to write out the CSV file for each object separately. Default is False.", action="store_true")
	
	# GENERAL
	parser.add_argument('--sizeserialchunk', '-chunk', help="Size of chunk of objects to be processed serially. Default is 10.", type=int, default=10)
	
	args = parser.parse_args()
	
	makeConfigFile(args)

if __name__=='__main__':
    main()
