import logging
import sys
from dataclasses import dataclass
from sorcha.configs.configUtilities import check_key_exists, check_value_in_list, cast_as_int


@dataclass
class inputConfigs:
    """Data class for holding INPUTS section configuration file keys and validating them."""

    ephemerides_type: str = None
    """Simulation used for ephemeris input."""

    eph_format: str = None
    """Format for ephemeris simulation input file."""

    size_serial_chunk: int = None
    """Sorcha chunk size."""

    aux_format: str = None
    """Format for the auxiliary input files."""

    pointing_sql_query: str = None
    """SQL query for extracting data from pointing database."""

    visits_query: str = None
    """SQL query for extracting data from visits database."""

    def __post_init__(self):
        """Automagically validates the input configs after initialisation."""
        self._validate_input_configs()

    def _validate_input_configs(self):
        """
        Validates the input config attributes after initialisation.

        Parameters
        -----------
        None.

        Returns
        ----------
        None
        """
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
class outputConfigs:
    """Data class for holding OUTPUT section configuration file keys and validating them."""

    output_format: str = None
    """Output format of the output file[s]"""

    output_columns: str = None
    """Controls which columns are in the output files."""

    position_decimals: int = None
    """position decimal places"""

    magnitude_decimals: int = None
    """magnitude decimal places"""

    def __post_init__(self):
        """Automagically validates the output configs after initialisation."""
        self._validate_output_configs()

    def _validate_output_configs(self):
        """
        Validates the output config attributes after initialisation.

        Parameters
        -----------
        None.

        Returns
        ----------
        None
        """
        # make sure all the mandatory keys have been populated.
        check_key_exists(self.output_format, "output_format")
        check_key_exists(self.output_columns, "output_columns")

        # some additional checks to make sure they all make sense!
        check_value_in_list(self.output_format, ["csv", "sqlite3", "hdf5"], "output_format")

        if "," in self.output_columns:  # assume list of column names: turn into a list and strip whitespace
            self.output_columns = [colname.strip(" ") for colname in self.output_columns.split(",")]
        else:
            check_value_in_list(self.output_columns, ["basic", "all"], "output_columns")
        self._validate_decimals()

    def _validate_decimals(self):
        """
        Validates the decimal output config attributes after initialisation.

        Parameters
        -----------
        None.

        Returns
        ----------
        None
        """
        if self.position_decimals is not None:
            self.position_decimals = cast_as_int(self.position_decimals, "position_decimals")
        if self.magnitude_decimals is not None:
            self.magnitude_decimals = cast_as_int(self.magnitude_decimals, "magnitude_decimals")
        if self.position_decimals is not None and self.position_decimals < 0:
            logging.error("ERROR: decimal places config variables cannot be negative.")
            sys.exit("ERROR: decimal places config variables cannot be negative.")
        if self.magnitude_decimals is not None and self.magnitude_decimals < 0:
            logging.error("ERROR: decimal places config variables cannot be negative.")
            sys.exit("ERROR: decimal places config variables cannot be negative.")
