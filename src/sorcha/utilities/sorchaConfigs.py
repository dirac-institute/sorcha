from dataclasses import dataclass
import configparser
import logging
import sys

from sorcha.lightcurves.lightcurve_registration import LC_METHODS
from sorcha.activity.activity_registration import CA_METHODS


@dataclass
class inputConfigs:
    """Data class for holding INPUTS section configuration file keys and validating them."""

    ephemerides_type: str = (
        ""  # make sure any defaults are "falsy" so we know when one hasn't populated properly
    )
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
class sorchaConfigs:
    """Dataclass which stores configuration file keywords in dataclasses."""

    inputs: inputConfigs = (
        None  # setting empty defaults because we won't have these ready when we initialise the sorchaConfigs object
    )
    """inputConfigs dataclass which stores the keywords from the INPUT section of the config file."""

    # simulation: simulationConfigs = None

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

        # do INPUTS section first
        inputs_dict = dict(
            config_object["INPUT"]
        )  # gets just the INPUTS section of the config file as a dictionary
        self.inputs = inputConfigs(**inputs_dict)

        # SIMULATION would be next...
        # simulation_dict = dict(config_object["SIMULATION"])
        # self.simulation = simulationConfigs(**simulation_dict)


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


def cast_as_int(value, key):
    # replaces PPGetIntOrExit: checks to make sure the value can be cast as an integer.

    try:
        int(value)
    except ValueError:
        logging.error(f"ERROR: expected an int for config parameter {key}. Check value in config file.")
        sys.exit(f"ERROR: expected an int for config parameter {key}. Check value in config file.")

    return int(value)


def check_value_in_list(value, valuelist, key):
    # PPConfigParser often checks to see if a config variable is in a list of permissible variables, so this abstracts it out.

    if value not in valuelist:
        logging.error(
            f"ERROR: value {value} for config parameter {key} not recognised. Expecting one of: {valuelist}."
        )
        sys.exit(
            f"ERROR: value {value} for config parameter {key} not recognised. Expecting one of: {valuelist}."
        )
