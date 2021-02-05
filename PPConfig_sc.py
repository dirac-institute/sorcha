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

#### COLOURS ####

