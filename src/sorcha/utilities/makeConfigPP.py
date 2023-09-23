# Creates config files for post-processing from the command line, for use in scripts.
# python makeConfigFilePP.py --help will give usage instructions

import argparse
import configparser
import os
import sys


def makeConfigFile(args):
    """
    Makes an sorcha config file from the variables defined at the command line.

    Parameters:
    -----------
    args (argparse ArgumentParser object): command line arguments.

    Returns:
    -----------
    None.

    """

    config = configparser.ConfigParser()

    bright_raw = {"bright_limit": str(args.brightlimit)}

    linking_raw = {
        "SSP_detection_efficiency": str(args.detectionefficiency),
        "SSP_number_observations": str(args.numobservations),
        "SSP_number_tracklets": str(args.numtracklets),
        "SSP_track_window": str(args.trackwindow),
        "SSP_separation_threshold": str(args.septhreshold),
        "SSP_maximum_time": str(args.maxtime),
    }

    simulation_raw = {
        "ar_ang_fov": str(args.ar_ang_fov),
        "ar_fov_buffer": str(args.ar_fov_buffer),
        "ar_picket": str(args.ar_picket),
        "ar_obs_code": str(args.ar_obs_code),
        "ar_healpix_order": str(args.ar_healpix_order),
    }

    fov_raw = {
        "camera_model": str(args.cameramodel),
        "footprint_path": str(args.footprintpath),
        "fill_factor": str(args.fillfactor),
        "circle_radius": str(args.circleradius),
    }

    fading_raw = {
        "fading_function_on": str(args.fadingfunction),
        "fading_function_width": str(args.fadingwidth),
        "fading_function_peak_efficiency": str(args.fadingpeak),
    }

    expert_raw = {
        "SNR_limit": str(args.snrlimit),
        "mag_limit": str(args.maglimit),
        "trailing_losses_on": str(args.trailinglosseson),
        "pointing_sql_query": str(args.sqlquery),
        "lc_model": str(args.lcmodel),
    }

    bright_dict = {k: v for k, v in bright_raw.items() if v != "None"}
    fov_dict = {k: v for k, v in fov_raw.items() if v != "None"}
    linking_dict = {k: v for k, v in linking_raw.items() if v != "None"}
    simulation_dict = {k: v for k, v in simulation_raw.items() if v != "None"}
    fading_dict = {k: v for k, v in fading_raw.items() if v != "None"}
    expert_dict = {k: v for k, v in expert_raw.items() if v != "None"}

    config_dict = {
        "ACTIVITY": {"comet_activity": args.cometactivity},
        "INPUT": {
            "ephemerides_type": args.ephemeridestype,
            "eph_format": args.ephformat,
            "aux_format": args.auxformat,
            "size_serial_chunk": str(args.sizeserialchunk),
        },
        "FILTERS": {"observing_filters": args.observingfilters},
        "SATURATION": bright_dict,
        "PHASECURVES": {"phase_function": args.phasefunction},
        "FOV": fov_dict,
        "FADINGFUNCTION": fading_dict,
        "LINKINGFILTER": linking_dict,
        "SIMULATION": simulation_dict,
        "OUTPUT": {
            "output_format": args.outputformat,
            "output_size": args.outputsize,
            "position_decimals": str(args.positiondecimals),
            "magnitude_decimals": str(args.magnitudedecimals),
        },
        "EXPERT": expert_dict,
    }

    config.read_dict(config_dict)

    with open(os.path.abspath(args.filename), "w") as f:
        config.write(f)


def main():
    """
    Creates an SSPP config file from variables defined at the command line.

    usage: makeConfigPP [-h] [--ephemeridestype EPHEMERIDESTYPE] [--pointingdatabase POINTINGDATABASE] [--ephformat EPHFORMAT] [--auxformat AUXFORMAT]
                    [--sizeserialchunk SIZESERIALCHUNK] [--cometactivity COMETACTIVITY] [--observingfilters OBSERVINGFILTERS] [--brightlimit BRIGHTLIMIT]
                    [--phasefunction PHASEFUNCTION] [--cameramodel CAMERAMODEL] [--footprintpath FOOTPRINTPATH] [--fillfactor FILLFACTOR] [--circleradius CIRCLERADIUS]
                    [--fadingfunction FADINGFUNCTION] [--fadingwidth FADINGWIDTH] [--fadingpeak FADINGPEAK] [--detectionefficiency DETECTIONEFFICIENCY]
                    [--numobservations NUMOBSERVATIONS] [--numtracklets NUMTRACKLETS] [--trackwindow TRACKWINDOW] [--septhreshold SEPTHRESHOLD] [--maxtime MAXTIME]
                    [--outputformat OUTPUTFORMAT] [--outputsize OUTPUTSIZE] [--positiondecimals POSITIONDECIMALS] [--magnitudedecimals MAGNITUDEDECIMALS] [--snrlimit SNRLIMIT]
                    [--maglimit MAGLIMIT][--sqlquery SQLQUERY] [--trailinglosseson TRAILINGLOSSESON] [--lightcurve LIGHTCURVE] [--lcmodel LCMODEL]
                    filename
        positional arguments:
            filename              Filepath where you want to store the config file.
        arguments:
          -h, --help                                                                show this help message and exit
          --ephemeridestype EPHEMERIDESTYPE, -eph EPHEMERIDESTYPE                   Type of input ephemerides: default = oif. Options: currently only oif.
          --pointingdatabase POINTINGDATABASE, -inpt POINTINGDATABASE               Path to pointing database. Default is "./demo/baseline_v2.0_1yr.db".
          --ephformat EPHFORMAT, -inptf EPHFORMAT                                   Separator in ephemeris database: csv, whitespace, hdf5. Default is "whitespace".
          --auxformat AUXFORMAT, -inauxf AUXFORMAT                                  Separator in orbit/colour/brightness/cometary data files: comma or whitespace. Default is "whitespace".
          --sizeserialchunk SIZESERIALCHUNK, -chunk SIZESERIALCHUNK                 Size of chunk of objects to be processed serially. Default is 10.
          --cometactivity COMETACTIVITY, -com COMETACTIVITY                         Type of cometary activity. Options are "comet" or None. Default is none.
          --observingfilters OBSERVINGFILTERS, -rfilt OBSERVINGFILTERS              Observing filters: main filter in which H is calculated, followed by resolved colours, such as, e.g. 'r'+'g-r'='g'. Should be separated by comma. Default is "r,g,i,z"
          --brightlimit BRIGHTLIMIT, -brtlim BRIGHTLIMIT                            Limit of brightness: detections brighter than this are omitted assuming saturation. Expects a float or None to omit. Default is 16.0.
          --phasefunction PHASEFUNCTION, -phfunc PHASEFUNCTION                      Define the used input phase function. Options: HG, HG1G2, HG12, linear, none. Default is "HG".
          --cameramodel CAMERAMODEL, -cammod CAMERAMODEL                            Choose between surface area equivalent or actual camera footprint, including chip gaps. Options: circle, footprint. Default is "footprint".
          --footprintpath FOOTPRINTPATH, -infoot FOOTPRINTPATH                      Path to camera footprint file. Default is "./data/detectors_corners.csv".
          --fillfactor FILLFACTOR, -ff FILLFACTOR                                   Fraction of detector surface area which contains CCD -- simulates chip gaps. Expects a float or None to omit. Default is None.
          --circleradius CIRCLERADIUS, -circ CIRCLERADIUS                           Radius of the circle for a circular footprint (in degrees). Default is None.
          --fadingfunction FADINGFUNCTION, -fade FADINGFUNCTION                     Detection efficiency fading function on or off.
          --fadingwidth FADINGWIDTH, -fadew FADINGWIDTH                             Width parameter for fading function. Default is 0.1 after Chelsey and Vereš (2017) or None to omit.
          --fadingpeak FADINGPEAK, -fadep FADINGPEAK                                Peak efficiency parameter for fading function. Default is 1 or None to omit.
          --detectionefficiency DETECTIONEFFICIENCY, -deteff DETECTIONEFFICIENCY    Which fraction of the detections will the automated solar system processing pipeline recognise? Expects a float. Default is 0.95.
          --numobservations NUMOBSERVATIONS, -nobs NUMOBSERVATIONS                  How many observations during one night are required to produce a valid tracklet? Expects an int or None to omit. Default 2.
          --numtracklets NUMTRACKLETS, -ntrk NUMTRACKLETS                           How many tracklets are required to classify as a detection? Expects an int or None to omit. Default 3.
          --trackwindow TRACKWINDOW, -trkwin TRACKWINDOW                            In what amount of time does the aforementioned number of tracklets needs to be discovered to constitute a complete detection? In days. Expects a float or None to omit. Default 15.0.
          --septhreshold SEPTHRESHOLD, -minsep SEPTHRESHOLD                         Minimum separation inside the tracklet for SSP distinguish motion between two images, in arcsec. Expects a float or None to omit. Default is 0.5.
          --maxtime MAXTIME, -maxt MAXTIME                                          Maximum time separation (in days) between subsequent observations in a tracklet. Expects a float or None to omit. Default is 0.0625.
          --outputformat OUTPUTFORMAT, -outf OUTPUTFORMAT                           Output format. Options: csv, sqlite3, hdf5. Default is csv.
          --outputsize OUTPUTSIZE, -outs OUTPUTSIZE                                 Size of output. Controls which columns are in the output files. Options are "default" only.
          --positiondecimals POSITIONDECIMALS, -posd POSITIONDECIMALS               Decimal places RA and Dec should be rounded to in output. Default is 7.
          --magnitudedecimals MAGNITUDEDECIMALS, -magd MAGNITUDEDECIMALS            Decimal places magnitudes should be rounded to in output. Default is 3.
          --snrlimit SNRLIMIT, -snr SNRLIMIT                                        SNR limit: drop observations below this SNR threshold. Omit for no SNR cut.
          --maglimit MAGLIMIT, -mag MAGLIMIT                                        Magnitude threshold: drop observations below this magnitude. Omit for no magnitude cut.
          --sqlquery SQLQUERY, -query SQLQUERY                                      Database query for extracting data for pointing database.
          --trailinglosseson TRAILINGLOSSESON, -tloss TRAILINGLOSSESON              Switch on trailing losses. Relevant for close-approaching NEOs. Default True.
          --lightcurve LIGHTCURVE, -lc LIGHTCURVE                                   Include lightcurve model. Default False.
          --lcmodel LCMODEL -lcm LCMODEL                                            Which lightcurve model to use. Default None.

    """

    parser = argparse.ArgumentParser(description="Creating the config file for SSP.")

    parser.add_argument("filename", help="Filepath where you want to store the config file.", type=str)

    # INPUT
    parser.add_argument(
        "--ephemeridestype",
        "-eph",
        help='Type of input ephemerides: default = ar. Options: ["ar", "external"]',
        type=str,
        default="ar",
    )
    parser.add_argument(
        "--pointingdatabase",
        "-inpt",
        help='Path to pointing database. Default is "./demo/baseline_v2.0_1yr.db".',
        type=str,
        default="./demo/baseline_v2.0_1yr.db",
    )
    parser.add_argument(
        "--ephformat",
        "-inptf",
        help='Separator in ephemeris database: csv, whitespace, hdf5. Default is "whitespace".',
        type=str,
        default="whitespace",
    )
    parser.add_argument(
        "--auxformat",
        "-inauxf",
        help='Separator in orbit/colour/brightness/cometary data files: comma or whitespace. Default is "whitespace".',
        type=str,
        default="whitespace",
    )
    parser.add_argument(
        "--sizeserialchunk",
        "-chunk",
        help="Size of chunk of objects to be processed serially. Default is 10.",
        type=int,
        default=10,
    )

    # ACTIVITY
    parser.add_argument(
        "--cometactivity",
        "-com",
        help='Type of cometary activity. Options are "comet" or None. Default is none.',
        type=str,
        default="none",
    )

    # FILTERS
    parser.add_argument(
        "--observingfilters",
        "-rfilt",
        help="Observing filters: main filter in which H is calculated, followed by resolved colours, such as, e.g. 'r'+'g-r'='g'. Should be separated by comma. Default is \"r,g,i,z\"",
        type=str,
        default="r,g,i,z",
    )

    # SATURATION
    parser.add_argument(
        "--brightlimit",
        "-brtlim",
        help="Limit of brightness: detections brighter than this are omitted assuming saturation. Expects a float or None to omit. Default is 16.0.",
        type=float,
        default=16.0,
    )

    # PHASECURVES
    parser.add_argument(
        "--phasefunction",
        "-phfunc",
        help='Define the used input phase function. Options: HG, HG1G2, HG12, linear, none. Default is "HG".',
        type=str,
        default="HG",
    )

    # FOV
    parser.add_argument(
        "--cameramodel",
        "-cammod",
        help='Choose between surface area equivalent or actual camera footprint, including chip gaps. Options: circle, footprint. Default is "footprint".',
        type=str,
        default="footprint",
    )
    parser.add_argument(
        "--footprintpath",
        "-infoot",
        help='Path to camera footprint file. Default is "./data/detectors_corners.csv".',
        type=str,
        default="./data/detectors_corners.csv",
    )
    parser.add_argument(
        "--fillfactor",
        "-ff",
        help="Fraction of detector surface area which contains CCD -- simulates chip gaps. Expects a float or None to omit. Default is None.",
        type=float,
        default=None,
    )
    parser.add_argument(
        "--circleradius",
        "-circ",
        help="Radius of the circle for a circular footprint (in degrees). Default is None.",
        type=float,
        default=None,
    )

    # FADINGFUNCTION
    parser.add_argument(
        "--fadingfunction",
        "-fade",
        help="Detection efficiency fading function on or off.",
        type=bool,
        default=True,
    )
    parser.add_argument(
        "--fadingwidth",
        "-fadew",
        help="Width parameter for fading function. Default is 0.1 after Chelsey and Vereš (2017) or None to omit.",
        type=float,
        default=0.1,
    )
    parser.add_argument(
        "--fadingpeak",
        "-fadep",
        help="Peak efficiency parameter for fading function. Default is 1 or None to omit.",
        type=float,
        default=1.0,
    )

    # LINKINGFILTER
    parser.add_argument(
        "--detectionefficiency",
        "-deteff",
        help="Which fraction of the detections will the automated solar system processing pipeline recognise? Expects a float. Default is 0.95.",
        type=float,
        default=0.95,
    )
    parser.add_argument(
        "--numobservations",
        "-nobs",
        help="How many observations during one night are required to produce a valid tracklet? Expects an int or None to omit. Default 2.",
        type=int,
        default=2,
    )
    parser.add_argument(
        "--numtracklets",
        "-ntrk",
        help="How many tracklets are required to classify as a detection? Expects an int or None to omit. Default 3.",
        type=int,
        default=3,
    )
    parser.add_argument(
        "--trackwindow",
        "-trkwin",
        help="In what amount of time does the aforementioned number of tracklets needs to be discovered to constitute a complete detection? In days. Expects a float or None to omit. Default 15.0.",
        type=float,
        default=15.0,
    )
    parser.add_argument(
        "--septhreshold",
        "-minsep",
        help="Minimum separation inside the tracklet for SSP distinguish motion between two images, in arcsec. Expects a float or None to omit. Default is 0.5.",
        type=float,
        default=0.5,
    )
    parser.add_argument(
        "--maxtime",
        "-maxt",
        help="Maximum time separation (in days) between subsequent observations in a tracklet. Expects a float or None to omit. Default is 0.0625.",
        type=float,
        default=0.0625,
    )

    # SIMULATION
    parser.add_argument(
        "--ar_ang_fov",
        "-arfov",
        help="the radius of the fov for simulation purposes",
        type=float,
        default=1.8,
    )
    parser.add_argument(
        "--ar_fov_buffer", "-fovbuf", help="the buffer to the fov radius", type=float, default=0.2
    )
    parser.add_argument(
        "--ar_picket",
        "-picket",
        help="the picket of time for iterating simulations (days).",
        type=int,
        default=1,
    )
    parser.add_argument("--ar_obs_code", "-obs", help="the MPC observatory code", type=str, default="X05")
    parser.add_argument(
        "--ar_healpix_order", "-hpord", help="the healpix order for simulation purposes.", type=int, default=6
    )

    # OUTPUT
    parser.add_argument(
        "--outputformat",
        "-outf",
        help="Output format. Options: csv, sqlite3, hdf5. Default is csv.",
        type=str,
        default="csv",
    )
    parser.add_argument(
        "--outputsize",
        "-outs",
        help='Size of output. Controls which columns are in the output files. Options are "basic" or "all".',
        type=str,
        default="basid",
    )
    parser.add_argument(
        "--positiondecimals",
        "-posd",
        help="Decimal places RA and Dec should be rounded to in output. Default is 7.",
        type=int,
        default=7,
    )
    parser.add_argument(
        "--magnitudedecimals",
        "-magd",
        help="Decimal places magnitudes should be rounded to in output. Default is 3.",
        type=int,
        default=3,
    )

    # EXPERT
    parser.add_argument(
        "--snrlimit",
        "-snr",
        help="SNR limit: drop observations below this SNR threshold. Omit for no SNR cut.",
        type=float,
        default=None,
    )
    parser.add_argument(
        "--maglimit",
        "-mag",
        help="Magnitude threshold: drop observations below this magnitude. Omit for no magnitude cut.",
        type=float,
        default=None,
    )
    parser.add_argument(
        "--sqlquery",
        "-query",
        help="Database query for extracting data for pointing database.",
        type=str,
        default="SELECT observationId, observationStartMJD as observationStartMJD_TAI, filter, seeingFwhmGeom, seeingFwhmEff, fiveSigmaDepth, fieldRA, fieldDec, rotSkyPos FROM observations order by observationId",
    )
    parser.add_argument(
        "--trailinglosseson",
        "-tloss",
        help="Switch on trailing losses. Relevant for close-approaching NEOs. Default True.",
        type=bool,
        default=True,
    )
    parser.add_argument(
        "--lcmodel",
        "-lcm",
        help="Which lightcurve model to use. Default None.",
        type=str,
        default=None,
    )

    args = parser.parse_args()

    # error handling

    if not os.path.isfile(args.pointingdatabase):
        sys.exit("ERROR: file not found at supplied pointing database location.")

    if not os.path.isfile(args.footprintpath):
        sys.exit("ERROR: file not found at supplied footprint location.")

    makeConfigFile(args)


if __name__ == "__main__":
    main()
