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
        self.check_for_correct_filters()

    def check_for_correct_filters(self):

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
class fadingfunctionConfigs:
    """Data class for holding FADINGFUNCTION section configuration file keys and validating them"""
    
    fading_function_on: bool = False
    """Detection efficiency fading function on or off."""

    fading_function_width: float = 0
    """# Width parameter for fading function. Should be greater than zero and less than 0.5."""

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
            
            #boundaries conditions for both width and peak efficency
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
class sorchaConfigs:
    """Dataclass which stores configuration file keywords in dataclasses."""

    inputs: inputConfigs = None
    """inputConfigs dataclass which stores the keywords from the INPUT section of the config file."""

    simulation: simulationConfigs = None
    """simulationConfigs dataclass which stores the keywords from the SIMULATION section of the config file."""

    filters: filtersConfigs = None
    """filtersConfigs dataclass which stores the keywords from the FILTERS section of the config file."""

    phasecurve: phasecurvesConfigs = None
    """phasecurveConfigs dataclass which stores the keywords from the PHASECURVES section of the config file."""

    fadingfunction: fadingfunctionConfigs = None 
    """fadingfunctionConfigs dataclass which stores the keywords from the FADINGFUNCTION section of the config file."""

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

        inputs_dict = dict(
            config_object["INPUT"]
        )  # gets just the INPUTS section of the config file as a dictionary
        self.inputs = inputConfigs(**inputs_dict)

        simulation_dict = dict(config_object["SIMULATION"])
        self.simulation = simulationConfigs(**simulation_dict)

        filter_dict = {**config_object["FILTERS"], "survey_name": self.survey_name} 
        self.filters = filtersConfigs(**filter_dict)
        
        phasecurve_dict = dict(config_object["PHASECURVES"])
        self.phasecurve = phasecurvesConfigs(**phasecurve_dict)

        fadingfunction_dict = dict(config_object["FADINGFUNCTION"])
        self.fadingfunction = fadingfunctionConfigs(**fadingfunction_dict)

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
