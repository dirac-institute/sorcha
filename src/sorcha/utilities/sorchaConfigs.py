from dataclasses import dataclass
import configparser
import logging
import sys
import numpy as np
from sorcha.lightcurves.lightcurve_registration import LC_METHODS
from sorcha.activity.activity_registration import CA_METHODS


@dataclass
class inputConfigs:
    """Data class for holding INPUTS section configuration file keys and validating them."""

    ephemerides_type: str = ("")
    """Simulation used for ephemeris input."""

    eph_format: str = ""
    """Format for ephemeris simulation input file."""

    size_serial_chunk: int = 0
    """Sorcha chunk size."""

    aux_format: str = ""
    """Format for the auxiliary input files."""

    pointing_sql_query: str = ""
    """SQL query for extracting data from pointing database."""

    def __post_init__(self):
        """Automagically validates the input configs after initialisation."""
        self._validate_input_configs()

    def _validate_input_configs(self):

        # make sure all the mandatory keys have been populated.
        check_key_exists(self.ephemerides_type, "ephemerides_type")
        check_key_exists(self.eph_format, "eph_format")
        check_key_exists(self.size_serial_chunk, "size_serial_chunk")
        check_key_exists(self.aux_format, "aux_format")
        check_key_exists(self.pointing_sql_query, "pointing_sql_query")

        # some additional checks to make sure they all make sense!
        check_value_in_list(self.ephemerides_type, ["ar", "external"], "ephemerides_type")
        check_value_in_list(self.eph_format, ["csv", "whitespace", "hdf5"], "eph_format")
        check_value_in_list(self.aux_format, ["comma", "whitespace", "csv"], "aux_format")
        self.size_serial_chunk = cast_as_int(self.size_serial_chunk, "size_serial_chunk")

@dataclass
class simulationConfigs:
    """Data class for holding SIMULATION section configuration file keys and validating them"""
    
    ar_ang_fov: float = 0.0
    """the field of view of our search field, in degrees"""

    ar_fov_buffer: float = 0.0
    """the buffer zone around the field of view we want to include, in degrees"""
    
    ar_picket: float = 0.0
    """imprecise discretization of time that allows us to move progress our simulations forward without getting too granular when we don't have to. the unit is number of days."""

    ar_obs_code: str = "" 
    """the obscode is the MPC observatory code for the provided telescope."""

    ar_healpix_order: int = 0
    """the order of healpix which we will use for the healpy portions of the code."""

    def __post_init__(self):
        """Automagically validates the simulation configs after initialisation."""
        self._validate_simulation_configs()

    def _validate_simulation_configs(self):

        # make sure all the mandatory keys have been populated.
        check_key_exists(self.ar_ang_fov, "ar_ang_fov")
        check_key_exists(self.ar_fov_buffer, "ar_fov_buffer")
        check_key_exists(self.ar_picket, "ar_picket")
        check_key_exists(self.ar_obs_code, "ar_obs_code")
        check_key_exists(self.ar_healpix_order, "ar_healpix_order")

        # some additional checks to make sure they all make sense!
        self.ar_ang_fov = cast_as_float(self.ar_ang_fov,"ar_ang_fov")
        self.ar_fov_buffer = cast_as_float(self.ar_fov_buffer,"ar_fov_buffer")
        self.ar_picket = cast_as_int(self.ar_picket, "ar_picket")
        self.ar_obs_code = cast_as_str(self.ar_obs_code,"ar_obs_code")
        self.ar_healpix_order = cast_as_int(self.ar_healpix_order,"ar_healpix_order")

     
@dataclass
class filtersConfigs:
    """Data class for holding FILTERS section configuration file keys and validating them"""
   
    observing_filters: str = ""
    """Filters of the observations you are interested in, comma-separated."""

    survey_name : str =""
    """survey name to be used for checking filters are correct"""

    def __post_init__(self):
        """Automatically validates the filters configs after initialisation."""
        self._validate_filters_configs()

    def _validate_filters_configs(self):
        
        check_key_exists(self.observing_filters,"observing_filters")
        self.observing_filters = cast_as_str(self.observing_filters,"obsering_filters")
        check_key_exists(self.survey_name,"survey_name")
        self.observing_filters= [e.strip() for e in self.observing_filters.split(",")]
        self._check_for_correct_filters()

    def _check_for_correct_filters(self):

        if self.survey_name in ["rubin_sim", "RUBIN_SIM","LSST","lsst"]:
            lsst_filters = ["u", "g", "r", "i", "z", "y"]
            filters_ok = all(elem in lsst_filters for elem in self.observing_filters)

            if not filters_ok:
                bad_list = np.setdiff1d(self.observing_filters, lsst_filters)
                logging.error(
                    "ERROR: Filter(s) {} given in config file are not recognised filters for {} survey.".format(
                        bad_list, self.survey_name
                    )
                )
                logging.error("Accepted {} filters: {}".format("LSST", lsst_filters))
                logging.error("Change observing_filters in config file or select another survey.")
                sys.exit(
                    "ERROR: Filter(s) {} given in config file are not recognised filters for {} survey.".format(
                        bad_list, self.survey_name
                    )
                )

@dataclass
class saturationConfigs:
    """Data class for holding SATURATION section configuration file keys and validating them"""
    
    bright_limit_on: bool = False

    bright_limit: float = 0
    """ Upper magnitude limit on sources that will overfill the detector pixels/have counts above the non-linearity regime of the pixels where one can’t do photometry. Objects brighter than this limit (in magnitude) will be cut. """

    observing_filters: list = 0
    """Filters of the observations you are interested in, comma-separated."""

    def __post_init__(self):
        """Automatically validates the filters configs after initialisation."""
        self._validate_saturation_configs()

    def _validate_saturation_configs(self):
        check_key_exists(self.observing_filters,"observing_filters")
        if self.bright_limit:
            self.bright_limit_on = True
        
        if self.bright_limit_on:
            try:
                self.bright_limit = [float(e.strip()) for e in self.bright_limit.split(",")]
            except ValueError:
                logging.error("ERROR: could not parse brightness limits. Check formatting and try again.")
                sys.exit("ERROR: could not parse brightness limits. Check formatting and try again.")
            if len(self.bright_limit) != 1 and len(self.bright_limit) != len(self.observing_filters):
                    logging.error(
                            "ERROR: list of saturation limits is not the same length as list of observing filters."
                        )
                    sys.exit(
                            "ERROR: list of saturation limits is not the same length as list of observing filters."
                        )
                    
@dataclass
class phasecurvesConfigs:
    """Data class for holding PHASECURVES section configuration file keys and validating them"""
    
    phase_function: str = ""
    """The phase function used to calculate apparent magnitude. The physical parameters input"""
    
    def __post_init__(self):
        """Automatically validates the phasecurve configs after initialisation."""
        self._validate_phasecurve_configs()

    def _validate_phasecurve_configs(self):

        # make sure all the mandatory keys have been populated.
        check_key_exists(self.phase_function, "phase_function")

        check_value_in_list(self.phase_function, ["HG","HG1G2","HG12","linear","none"], "phase_function")

@dataclass
class fovConfigs:
    """Data class for holding FOV section configuration file keys and validating them"""

    camera_model: str = ""
    """Choose between circular or actual camera footprint, including chip gaps."""

    footprint_path: str = ""
    """Path to camera footprint file. Uncomment to provide a path to the desired camera detector configuration file if not using the default built-in LSSTCam detector configuration for the actual camera footprint."""

    fill_factor: str = ""
    """Fraction of detector surface area which contains CCD -- simulates chip gaps for OIF output. Comment out if using camera footprint."""

    circle_radius: float = 0
    """Radius of the circle for a circular footprint (in degrees). Float. Comment out or do not include if using footprint camera model."""

    footprint_edge_threshold: float = 0
    """The distance from the edge of a detector (in arcseconds on the focal plane) at which we will not correctly extract an object. By default this is 10px or 2 arcseconds. Comment out or do not include if not using footprint camera model."""

    survey_name: str = ""
    """name of survey"""

    def __post_init__(self):
        self._validate_fov_configs()
    
    def _validate_fov_configs(self):

        check_key_exists(self.camera_model,"camera_model")
        check_value_in_list(self.camera_model,["circle", "footprint"],"camera_model")

        if self.camera_model == "footprint":
            self._camera_footprint()
        
        elif self.camera_model == "circle":
            self._camera_circle()

    def _camera_footprint(self):

        if self.footprint_path:
             PPFindFileOrExit(self.footprint_path,"footprint_path")
        elif self.survey_name.lower() not in ["lsst","rubin_sim"]:
            logging.error("a default detector footprint is currently only provided for LSST; please provide your own footprint file.")
            sys.exit("a default detector footprint is currently only provided for LSST; please provide your own footprint file.")

        check_key_exists(self.footprint_edge_threshold,"footprint_edge_threshold")
        self.footprint_edge_threshold = cast_as_float(self.footprint_edge_threshold,"footprint_edge_threshold")
        check_key_doesnt_exist(self.fill_factor,"fill_factor",'but camera model is not "circle".')
        check_key_doesnt_exist(self.circle_radius,"circle_radius",'but camera model is not "circle".')
    
    def _camera_circle(self):

        if self.fill_factor:
            self.fill_factor = cast_as_float(self.fill_factor,"fill_factor")
            if self.fill_factor < 0.0 or self.fill_factor > 1.0:
                logging.error("ERROR: fill_factor out of bounds. Must be between 0 and 1.")
                sys.exit("ERROR: fill_factor out of bounds. Must be between 0 and 1.")
        elif self.circle_radius:
            self.circle_radius = cast_as_float(self.circle_radius,"circle_radius")
            if self.circle_radius < 0.0:
                logging.error("ERROR: circle_radius is negative.")
                sys.exit("ERROR: circle_radius is negative.")
        elif not self.fill_factor and not self.circle_radius:
            logging.error(
                'ERROR: either "fill_factor" or "circle_radius" must be specified for circular footprint.'
            )
            sys.exit(
                'ERROR: either "fill_factor" or "circle_radius" must be specified for circular footprint.'
            )
        check_key_doesnt_exist(self.footprint_edge_threshold,"footprint_edge_threshold",'but camera model is not "footprint".')

@dataclass
class fadingfunctionConfigs:
    """Data class for holding FADINGFUNCTION section configuration file keys and validating them"""
    
    fading_function_on: bool = False
    """Detection efficiency fading function on or off."""

    fading_function_width: float = 0
    """Width parameter for fading function. Should be greater than zero and less than 0.5."""

    fading_function_peak_efficiency: float = 0
    """Peak efficiency for the fading function, called the 'fill factor' in Chelsey and Veres (2017)."""

    def __post_init__(self):
        """Automagically validates the fading function configs after initialisation."""
        self._validate_fadingfunction_configs()

    def _validate_fadingfunction_configs(self):

        # make sure all the mandatory keys have been populated.
        check_key_exists(self.fading_function_on, "fading_function_on")
        self.fading_function_on = cast_as_bool(self.fading_function_on,"fading_function_on")
        
        if self.fading_function_on == True:

            #when fading_function_on = true, fading_function_width and fading_function_peak_efficiency now mandatory
            check_key_exists(self.fading_function_width, "fading_function_width")
            check_key_exists(self.fading_function_peak_efficiency, "fading_function_peak_efficiency")
            self.fading_function_width = cast_as_float(self.fading_function_width,"fading_function_width")
            self.fading_function_peak_efficiency = cast_as_float(self.fading_function_peak_efficiency,"fading_function_efficiency")
            
            #boundary conditions for both width and peak efficency
            if self.fading_function_width <= 0.0 or self.fading_function_width > 0.5:
                
                logging.error(
                    "ERROR: fading_function_width out of bounds. Must be greater than zero and less than 0.5."
                )
                sys.exit(
                    "ERROR: fading_function_width out of bounds. Must be greater than zero and less than 0.5."
                )

            if self.fading_function_peak_efficiency < 0.0 or self.fading_function_peak_efficiency > 1.0:
                logging.error(
                    "ERROR: fading_function_peak_efficiency out of bounds. Must be between 0 and 1."
                    )
                sys.exit(
                    "ERROR: fading_function_peak_efficiency out of bounds. Must be between 0 and 1."
                    )
        
        elif self.fading_function_on == False:
            #making sure these aren't populated when self.fading_function_on = False
            check_key_doesnt_exist(self.fading_function_width,"fading_function_width","but fading_function_on is False.")
            check_key_doesnt_exist(self.fading_function_peak_efficiency,"fading_function_peak_efficiency","but fading_function_on is False.")

@dataclass
class linkingfilterConfigs:
    """Data class for holding LINKINGFILTER section configuration file keys and validating them."""

    SSP_linking_on: bool = False
    """checks to see if model should run SSP linking filter"""

    drop_unlinked: bool = True

    SSP_detection_efficiency: float = 0
    """SSP detection efficiency. Which fraction of the observations of an object will the automated solar system processing pipeline successfully link? Float."""

    SSP_number_observations: int = 0
    """Length of tracklets. How many observations of an object during one night are required to produce a valid tracklet?"""
    SSP_separation_threshold: float = 0
    """Minimum separation (in arcsec) between two observations of an object required for the linking software to distinguish them as separate and therefore as a valid tracklet."""

    SSP_maximum_time: float = 0
    """Maximum time separation (in days) between subsequent observations in a tracklet. Default is 0.0625 days (90mins)."""
   
    SSP_number_tracklets: int = 0
    """Number of tracklets for detection. How many tracklets are required to classify an object as detected?  """

    SSP_track_window: int = 0
    """The number of tracklets defined above must occur in <= this number of days to constitute a complete track/detection."""

    SSP_night_start_utc: float = 0
    """The time in UTC at which it is noon at the observatory location (in standard time). For the LSST, 12pm Chile Standard Time is 4pm UTC."""

    def __post_init__(self):
        self._validate_linkingfilter_configs

    def _validate_linkingfilter_configs(self):
        
        SSPvariables = [
            self.SSP_separation_threshold,
            self.SSP_number_observations,
            self.SSP_number_tracklets,
            self.SSP_track_window,
            self.SSP_detection_efficiency,
            self.SSP_maximum_time,
            self.SSP_night_start_utc
        ]
        # the below if-statement explicitly checks for None so a zero triggers the correct error
        if all(v is not None for v in SSPvariables):
            if self.SSP_number_observations < 1:
                logging.error("ERROR: SSP_number_observations is zero or negative.")
                sys.exit("ERROR: SSP_number_observations is zero or negative.")

            if self.SSP_number_tracklets < 1:
                logging.error("ERROR: SSP_number_tracklets is zero or less.")
                sys.exit("ERROR: SSP_number_tracklets is zero or less.")

            if self.SSP_track_window <= 0.0:
                logging.error("ERROR: SSP_track_window is negative.")
                sys.exit("ERROR: SSP_track_window is negative.")

            if self.SSP_detection_efficiency > 1.0 or self.SSP_detection_efficiency > 1.0:
                logging.error("ERROR: SSP_detection_efficiency out of bounds (should be between 0 and 1).")
                sys.exit("ERROR: SSP_detection_efficiency out of bounds (should be between 0 and 1).")

            if self.SSP_separation_threshold <= 0.0:
                logging.error("ERROR: SSP_separation_threshold is zero or negative.")
                sys.exit("ERROR: SSP_separation_threshold is zero or negative.")

            if self.SSP_maximum_time < 0:
                logging.error("ERROR: SSP_maximum_time is negative.")
                sys.exit("ERROR: SSP_maximum_time is negative.")

            if self.SSP_night_start_utc > 24.0 or self.SSP_night_start_utc < 0.0:
                logging.error("ERROR: SSP_night_start_utc must be a valid time between 0 and 24 hours.")
                sys.exit("ERROR: SSP_night_start_utc must be a valid time between 0 and 24 hours.")

            self.SSP_linking_on = True
        elif not any(SSPvariables):
            self.SSP_linking_on = False
        else: 
            logging.error(
            "ERROR: only some SSP linking variables supplied. Supply all five required variables for SSP linking filter, or none to turn filter off."
            )
        sys.exit(
            "ERROR: only some SSP linking variables supplied. Supply all five required variables for SSP linking filter, or none to turn filter off."
            )
        self.drop_unlinked = cast_as_bool(self.drop_unlinked,"drop_unlinked")

@dataclass
class outputConfigs:
    """Data class for holding OUTPUT section configuration file keys and validating them."""

    output_format: str = ""
    """Output format of the output file[s]"""

    output_columns: str = ""
    """Controls which columns are in the output files."""

    position_decimals: float = 0
    """position decimal places"""

    magnitude_decimals: float = 0
    """magnitude decimal places"""

    def __post_init__(self):
        """Automagically validates the input configs after initialisation."""
        self._validate_output_configs()

    def _validate_output_configs(self):

        # make sure all the mandatory keys have been populated.
        check_key_exists(self.output_format, "output_format")
        check_key_exists(self.output_columns, "output_columns")


        # some additional checks to make sure they all make sense!
        check_value_in_list(self.output_format, ["csv", "sqlite3","hdf5"], "output_format")

        if (
        "," in self.output_columns
        ):  # assume list of column names: turn into a list and strip whitespace
            self.output_columns = [
            colname.strip(" ") for colname in self.output_columns.split(",")
        ]
        else:
            check_value_in_list(self.output_columns, ["basic", "all"], "output_columns")
        self._validate_decimals()
    def _validate_decimals(self):
        self.position_decimals = cast_as_float(self.position_decimals,"position_decimals")
        self.magnitude_decimals = cast_as_float(self.magnitude_decimals,"magnitude_decimals")
        if self.position_decimals and self.position_decimals < 0:
            logging.error("ERROR: decimal places config variables cannot be negative.")
            sys.exit("ERROR: decimal places config variables cannot be negative.")
        if self.magnitude_decimals and self.magnitude_decimals < 0:
            logging.error("ERROR: decimal places config variables cannot be negative.")
            sys.exit("ERROR: decimal places config variables cannot be negative.")
        
@dataclass
class lightcurveConfigs:
    """Data class for holding LIGHTCURVE section configuration file keys and validating them."""

    lc_model: str = ""
    """The unique name of the lightcurve model to use. Defined in the ``name_id`` method of the subclasses of AbstractLightCurve. If not none, the complex physical parameters file must be specified at the command line.lc_model = none"""

    def __post_init__(self):
        self._validate_lightcurve_configs(self)

    def _validate_lightcurve_configs(self):
        self.lc_model = None if self.lc_model == "none" else self.lc_model
        if self.lc_model and self.lc_model not in LC_METHODS:
            logging.error(f"The requested light curve model, '{self.lc_model}', is not registered. Available lightcurve options are: {list(LC_METHODS.keys())}")
            sys.exit(f"The requested light curve model, '{self.lc_model}', is not registered. Available lightcurve options are: {list(LC_METHODS.keys())}")

@dataclass
class activityConfigs:
    """Data class for holding Activity section configuration file keys and validating them."""

    comet_activity: str = ""
    """The unique name of the actvity model to use. Defined in the ``name_id`` method of the subclasses of AbstractCometaryActivity.  If not none, a complex physical parameters file must be specified at the command line."""
    
    def __post_init__(self):
        self._validate_activity_configs(self)

    def _validate_activity_configs(self):
        self.comet_activity = None if self.comet_activity == "none" else self.comet_activity
        if self.comet_activity and self.comet_activity not in CA_METHODS:
            logging.error(f"The requested comet activity model, '{self.comet_activity}', is not registered. Available comet activity models are: {list(CA_METHODS.keys())}")
            sys.exit(f"The requested comet activity model, '{self.comet_activity}', is not registered. Available comet activity models are: {list(CA_METHODS.keys())}")

@dataclass
class expertConfigs:
    """Data class for holding expert section configuration file keys and validating them."""

    SNR_limit: float = 0

    SNR_limit_on: bool = False

    mag_limit: float = 0

    mag_limit_on: bool = False

    trailing_losses_on: bool = True

    default_SNR_cut: bool = True
    
    randomization_on: bool = True

    vignetting_on: bool = True

    def __post_init__(self):
        self._validate_expert_configs
        
    def _validate_expert_configs(self):

        if self.SNR_limit:
            self.SNR_limit_on = True
        
        if self.mag_limit:
            self.mag_limit_on = True

        if self.SNR_limit < 0:
            logging.error("ERROR: SNR limit is negative.")
            sys.exit("ERROR: SNR limit is negative.")

        if self.mag_limit < 0:
            logging.error("ERROR: magnitude limit is negative.")
            sys.exit("ERROR: magnitude limit is negative.")

        if self.mag_limit_on and self.SNR_limit_on:
            logging.error(
                "ERROR: SNR limit and magnitude limit are mutually exclusive. Please delete one or both from config file."
            )
            sys.exit(
                "ERROR: SNR limit and magnitude limit are mutually exclusive. Please delete one or both from config file."
            )  

        self.trailing_losses_on = cast_as_bool(self.trailing_losses_on,"trailing_losses_on")
        self.default_SNR_cut = cast_as_bool(self.default_SNR_cut,"default_SNR_cut")
        self.randomization_on = cast_as_bool(self.randomization_on,"randomization_on")
        self.vignetting_on  = cast_as_bool(self.vignetting_on,"vignetting_on")  
@dataclass
class sorchaConfigs:
    """Dataclass which stores configuration file keywords in dataclasses."""

    inputs: inputConfigs = None
    """inputConfigs dataclass which stores the keywords from the INPUT section of the config file."""

    simulation: simulationConfigs = None
    """simulationConfigs dataclass which stores the keywords from the SIMULATION section of the config file."""

    filters: filtersConfigs = None
    """filtersConfigs dataclass which stores the keywords from the FILTERS section of the config file."""

    saturation: saturationConfigs = None
    """saturationConfigs dataclass which stores the keywords from the SATURATION section of the config file."""

    phasecurve: phasecurvesConfigs = None
    """phasecurveConfigs dataclass which stores the keywords from the PHASECURVES section of the config file."""

    fov: fovConfigs = None
    """fovConfigs dataclass which stores the keywords from the FOV section of the config file."""

    fadingfunction: fadingfunctionConfigs = None 
    """fadingfunctionConfigs dataclass which stores the keywords from the FADINGFUNCTION section of the config file."""

    linkingfilter: linkingfilterConfigs = None
    """linkingfilterConfigs dataclass which stores the keywords from the LINKINGFILTER section of the config file."""

    output: outputConfigs = None
    """outputConfigs dataclass which stores the keywords from the OUTPUT section of the config file."""
    
    lightcure: lightcurveConfigs = None
    """lightcurveConfigs dataclass which stores the keywords from the LIGHTCURVE section of the config file."""
   
    activity: activityConfigs = None
    """activityConfigs dataclass which stores the keywords from the ACTIVITY section of the config file."""
   
    expert: expertConfigs = None
    """expertConfigs dataclass which stores the keywords from the EXPERT section of the config file."""
   
    pplogger: None = None
    """The Python logger instance"""

    survey_name: str = ""
    """The name of the survey."""

    # this __init__ overrides a dataclass's inbuilt __init__ because we want to populate this from a file, not explicitly ourselves
    def __init__(self, config_file_location=None, survey_name=None):

        # attach the logger object so we can print things to the Sorcha logs
        self.pplogger = logging.getLogger(__name__)
        self.survey_name = survey_name

        if config_file_location:  # if a location to a config file is supplied...
            config_object = configparser.ConfigParser()  # create a ConfigParser object
            config_object.read(config_file_location)  # and read the whole config file into it
            self._read_configs_from_object(
                config_object
            )  # now we call a function that populates the class attributes

    def _read_configs_from_object(self, config_object):
        """function that populates the class attributes"""

        inputs_dict = dict(config_object["INPUT"])
        self.inputs = inputConfigs(**inputs_dict)

        simulation_dict = dict(config_object["SIMULATION"])
        self.simulation = simulationConfigs(**simulation_dict)

        filter_dict = {**config_object["FILTERS"], "survey_name": self.survey_name} 
        self.filters = filtersConfigs(**filter_dict)

        saturation_dict= {**config_object["SATURATION"], "observing_filters":self.filters.observing_filters}
        self.saturation = saturationConfigs(**saturation_dict)

        phasecurve_dict = dict(config_object["PHASECURVES"])
        self.phasecurve = phasecurvesConfigs(**phasecurve_dict)

        fov_dict = {**config_object["FOV"], "survey_name": self.survey_name}
        self.fov = fovConfigs(**fov_dict)

        fadingfunction_dict = dict(config_object["FADINGFUNCTION"])
        self.fadingfunction = fadingfunctionConfigs(**fadingfunction_dict)

        linkingfilter_dict = dict(config_object["LINKINGFILTER"])
        self.linkingfilter = linkingfilterConfigs(**linkingfilter_dict)

        output_dict = dict(config_object["OUTPUT"])
        self.output = outputConfigs(**output_dict)

        lightcurve_dict = dict(config_object["LIGHTCURVE"])
        self.lightcure = lightcurveConfigs(**lightcurve_dict)

        activity_dict = dict(config_object["ACTIVITY"])
        self.activity = activityConfigs(**activity_dict)

        expert_dict = dict(config_object["EXPERT"])
        self.expert = expertConfigs(**expert_dict)

## below are the utility functions used to help validate the keywords, add more as needed


def check_key_exists(value, key_name):
    # checks to make sure that whatever is in "value" evaluates as truthy, i.e. it isn't the default and we
    # populated this key successfully.

    if not value:
        logging.error(
            f"ERROR: No value found for required key {key_name} in config file. Please check the file and try again."
        )
        sys.exit(
            f"ERROR: No value found for required key {key_name} in config file. Please check the file and try again."
        )


def check_key_doesnt_exist(value, key_name,reason):
    #checks to make sure value doesn't exist 
    if value:
        logging.error(
            f"ERROR: {key_name} supplied in config file {reason}"
        )
        sys.exit(
            f"ERROR: {key_name} supplied in config file {reason}"
        )


def cast_as_int(value, key):
    # replaces PPGetIntOrExit: checks to make sure the value can be cast as an integer.

    try:
        int(value)
    except ValueError:
        logging.error(f"ERROR: expected an int for config parameter {key}. Check value in config file.")
        sys.exit(f"ERROR: expected an int for config parameter {key}. Check value in config file.")

    return int(value)

def cast_as_str(value, key):
   
    try:
        str(value)
    except ValueError:
        logging.error(f"ERROR: expected a str for config parameter {key}. Check value in config file.")
        sys.exit(f"ERROR: expected a str for config parameter {key}. Check value in config file.")

    return str(value)
def cast_as_float(value, key):
    # replaces PPGetFloatOrExit: checks to make sure the value can be cast as a float.

    try:
        float(value)
    except ValueError:
        logging.error(f"ERROR: expected a float for config parameter {key}. Check value in config file.")
        sys.exit(f"ERROR: expected a float for config parameter {key}. Check value in config file.")

    return float(value)

def cast_as_bool(value, key):
    # replaces PPGetBoolOrExit: checks to make sure the value can be cast as a bool.

    str_value = str(value).strip()
    
    if str_value in ['true', '1', 'yes', 'y','True']:
        return True
    elif str_value in ['false', '0', 'no', 'n','False']:
        return False
    else:
        logging.error(f"ERROR: expected a bool for config parameter {key}. Check value in config file.")
        sys.exit(f"ERROR: expected a bool for config parameter {key}. Check value in config file.")


def check_value_in_list(value, valuelist, key):
    # PPConfigParser often checks to see if a config variable is in a list of permissible variables, so this abstracts it out.

    if value not in valuelist:
        logging.error(
            f"ERROR: value {value} for config parameter {key} not recognised. Expecting one of: {valuelist}."
        )
        sys.exit(
            f"ERROR: value {value} for config parameter {key} not recognised. Expecting one of: {valuelist}."
        )


def PPFindFileOrExit(arg_fn, argname):
    """Checks to see if a file given by a filename exists. If it doesn't,
    this fails gracefully and exits to the command line.

    Parameters
    -----------
    arg_fn : string
        The filepath/name of the file to be checked.

    argname : string
        The name of the argument being checked. Used for error message.

    Returns
    ----------
    arg_fn : string
        The filepath/name of the file to be checked.

    """

    pplogger = logging.getLogger(__name__)

    if os.path.exists(arg_fn):
        return arg_fn
    else:
        pplogger.error("ERROR: filename {} supplied for {} argument does not exist.".format(arg_fn, argname))
        sys.exit("ERROR: filename {} supplied for {} argument does not exist.".format(arg_fn, argname))
