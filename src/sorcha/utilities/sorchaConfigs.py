from dataclasses import dataclass
import logging
import sys

from sorcha.lightcurves.lightcurve_registration import LC_METHODS
from sorcha.activity.activity_registration import CA_METHODS


@dataclass
class sorchaConfigs:
    """Data class for holding configuration file keys."""

    ephemerides_type: str = ""
    """Simulation used for ephemeris input."""
    
    eph_format: str = ""
    """Format for ephemeris simulation input file."""
    
    size_serial_chunk: int = 0
    """Sorcha chunk size."""
    
    aux_format: str = ""
    """Format for the auxiliary input files."""
    
    pointing_sql_query: str = ""
    """SQL query for extracting data from pointing database."""

    def __init__(self, config_file_location=None):
        
        # attach the logger object so we can print things to the Sorcha logs
        self.pplogger = logging.getLogger(__name__)
        
        if config_file_location:
            config_object = configparser.ConfigParser()
            config_object.read(config_file_location)
            self._read_configs_from_object(config_object)

    def _read_configs_from_object(self, config_object):

        # do INPUTS section first
        inputs_dict = dict(config_object["INPUT"]) # gets just the INPUTS section of the config file as a dictionary
        self._read_and_validate_input_configs(inputs_dict)  
        
        # then continue through the sections. this makes it easier to read.
        # activity_dict = dict(config_object["ACTIVITY"])
        # self._read_and_validate_activity_configs()

    def _read_and_validate_input_configs(self, inputs_dict):
    
        self.ephemerides_type = get_value(inputs_dict, "ephemerides_type").lower()
        check_value_in_list(self.ephemerides_type, ["ar", "external"], "ephemerides_type")
    
        #...
        
        self.size_serial_chunk = get_value(inputs_dict, "size_serial_chunk")
        self.size_serial_chunk = cast_as_int(self.size_serial_chunk, "size_serial_chunk")

## below are the utility functions used to help validate the keywords, add more as needed

def get_value(configs_dict, key, required=True):
    # replaces PPGetOrExit and PPGetValueAndFlag

    value = configs_dict.get(key, None)
    
    if value is None and required:
        logging.error(f"ERROR: No value found for required key {key} in config file. Please check the file and try again.")
        sys.exit(f"ERROR: No value found for required key {key} in config file. Please check the file and try again.")

    return value

def cast_as_int(value, key):
    # replaces PPGetIntOrExit - cleaner to do the type-checking separately.

    try:
       int(value)
    except ValueError:
        logging.error(f"ERROR: expected an int for config parameter {key}. Check value in config file.")
        sys.exit(f"ERROR: expected an int for config parameter {key}. Check value in config file.")
    
    return int(value)


def check_value_in_list(value, valuelist, key):
    # PPConfigParser often checks to see if a config variable is in a list of permissible variables, so this abstracts it out.
    
    if value not in valuelist:
        logging.error(f"ERROR: value {value} for config parameter {key} not recognised. Expecting one of: {valuelist}.")
        sys.exit(f"ERROR: value {value} for config parameter {key} not recognised. Expecting one of: {valuelist}.")



 