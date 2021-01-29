# Configuration file for solar system post processing package


#### INPUT FILES #####

# When full pipeline will work, here will be the orbit input file [des format]

# intermediate input file (oif output file)
oifoutput='./data/test/oiftestoutput'

# colour input file
colourinput='./data/test/testcolour_sdss'

# pointing database
pointingdatabase='./data/baseline_10yrs_10klines.db' #'baseline_v1.3_10yrs.db'

#### GENERAL PARAMETERS ####


#verbosity level: [0 | 1]
verbosity=0

#### FILTERS ####


#### CAMERA ####


#### SOFTWARE ####


# SSP detection efficiency: default == 0.95. Which fraction of the detections will
# the automated solar system processing pipeline recognise?
SSPDetectionEfficiency = 0.95

# length of trackets: default == 2. How many observations during one night are required to produce 
# a valid tracklet? 
minTracklet = 2

# Number of tracklets for detection: ndefault == 3. How many tracklets are required
# to classify as a detection?
noTracklets = 3

# Interval of tracklets (days): default + 15.0 (days). In what amount of time does the aforementioned
# number of tracklets needs to be discovered to constitute a complete detection?
trackletInterval = 15.0


#### COLOURS ####




#### MISCELANEOUS #######

# Do not change, value for test assertion, should always be 1
testValue = 1