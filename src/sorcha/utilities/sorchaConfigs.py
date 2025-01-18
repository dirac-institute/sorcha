import configparser
import logging
import os
import sys
from dataclasses import dataclass

import numpy as np

from sorcha.activity.activity_registration import CA_METHODS
from sorcha.lightcurves.lightcurve_registration import LC_METHODS
from sorcha.utilities.fileAccessUtils import FindFileOrExit


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
class simulationConfigs:
    """Data class for holding SIMULATION section configuration file keys and validating them"""

    ar_ang_fov: float = None
    """the field of view of our search field, in degrees"""

    ar_fov_buffer: float = None
    """the buffer zone around the field of view we want to include, in degrees"""

    ar_picket: float = None
    """imprecise discretization of time that allows us to move progress our simulations forward without getting too granular when we don't have to. the unit is number of days."""

    ar_obs_code: str = None
    """the obscode is the MPC observatory code for the provided telescope."""

    ar_healpix_order: int = None
    """the order of healpix which we will use for the healpy portions of the code."""

    ar_n_sub_intervals: int = 101
    """Number of sub-intervals for the Lagrange ephemerides interpolation (default: 101)"""

    _ephemerides_type: str = None
    """Simulation used for ephemeris input."""

    def __post_init__(self):
        """Automagically validates the simulation configs after initialisation."""
        self._validate_simulation_configs()

    def _validate_simulation_configs(self):
        """
        Validates the simulation config attributes after initialisation.

        Parameters
        -----------
        None.

        Returns
        ----------
        None
        """
        # make sure all the mandatory keys have been populated.
        check_key_exists(self._ephemerides_type, "_ephemerides_type")
        check_value_in_list(self._ephemerides_type, ["ar", "external"], "_ephemerides_type")
        if self._ephemerides_type == "ar":
            check_key_exists(self.ar_ang_fov, "ar_ang_fov")
            check_key_exists(self.ar_fov_buffer, "ar_fov_buffer")
            check_key_exists(self.ar_picket, "ar_picket")
            check_key_exists(self.ar_obs_code, "ar_obs_code")
            check_key_exists(self.ar_healpix_order, "ar_healpix_order")

            # some additional checks to make sure they all make sense!
            self.ar_ang_fov = cast_as_float(self.ar_ang_fov, "ar_ang_fov")
            self.ar_fov_buffer = cast_as_float(self.ar_fov_buffer, "ar_fov_buffer")
            self.ar_picket = cast_as_int(self.ar_picket, "ar_picket")
            self.ar_healpix_order = cast_as_int(self.ar_healpix_order, "ar_healpix_order")
            self.ar_n_sub_intervals = cast_as_int(self.ar_n_sub_intervals, "ar_n_sub_intervals")
        elif self._ephemerides_type == "external":
            # makes sure when these are not needed that they are not populated
            check_key_doesnt_exist(self.ar_ang_fov, "ar_ang_fov", "but ephemerides type is external")
            check_key_doesnt_exist(self.ar_fov_buffer, "ar_fov_buffer", "but ephemerides type is external")
            check_key_doesnt_exist(self.ar_picket, "ar_picket", "but ephemerides type is external")
            check_key_doesnt_exist(self.ar_obs_code, "ar_obs_code", "but ephemerides type is external")
            check_key_doesnt_exist(
                self.ar_healpix_order, "ar_healpix_order", "but ephemerides type is external"
            )


@dataclass
class filtersConfigs:
    """Data class for holding FILTERS section configuration file keys and validating them"""

    observing_filters: str = None
    """Filters of the observations you are interested in, comma-separated."""

    survey_name: str = None
    """survey name to be used for checking filters are correct"""

    mainfilter: str = None
    """main filter chosen in physical parameter file"""

    othercolours: str = None
    """other filters given alongside main filter"""

    def __post_init__(self):
        """Automagically validates the filters configs after initialisation."""
        self._validate_filters_configs()

    def _validate_filters_configs(self):
        """
        Validates the filters config attributes after initialisation.

        Parameters
        -----------
        None.

        Returns
        ----------
        None
        """
        # checks mandatory keys are populated
        check_key_exists(self.observing_filters, "observing_filters")
        check_key_exists(self.survey_name, "survey_name")
        self.observing_filters = [e.strip() for e in self.observing_filters.split(",")]
        self._check_for_correct_filters()

    def _check_for_correct_filters(self):
        """
        Checks the filters selected are used by the chosen survey.

        Parameters
        -----------
        None.

        Returns
        ----------
        None
        """

        if self.survey_name in ["rubin_sim", "RUBIN_SIM", "LSST", "lsst"]:
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

    bright_limit_on: bool = None

    bright_limit: float = None
    """ Upper magnitude limit on sources that will overfill the detector pixels/have counts above the non-linearity regime of the pixels where one can’t do photometry. Objects brighter than this limit (in magnitude) will be cut. """

    _observing_filters: list = None
    """Filters of the observations you are interested in, comma-separated."""

    def __post_init__(self):
        """Automagically validates the saturation configs after initialisation."""
        self._validate_saturation_configs()

    def _validate_saturation_configs(self):
        """
        Validates the saturation config attributes after initialisation.

        Parameters
        -----------
        None.

        Returns
        ----------
        None
        """
        check_key_exists(self._observing_filters, "_observing_filters")
        if self.bright_limit is not None:
            self.bright_limit_on = True

        if self.bright_limit_on:
            try:
                self.bright_limit = [float(e.strip()) for e in self.bright_limit.split(",")]
            except ValueError:
                logging.error("ERROR: could not parse brightness limits. Check formatting and try again.")
                sys.exit("ERROR: could not parse brightness limits. Check formatting and try again.")
            if len(self.bright_limit) == 1:
                # when only one value is given that value is saved as a float instead of in a list
                self.bright_limit = cast_as_float(self.bright_limit[0], "bright_limit")
            elif len(self.bright_limit) != 1 and len(self.bright_limit) != len(self._observing_filters):
                logging.error(
                    "ERROR: list of saturation limits is not the same length as list of observing filters."
                )
                sys.exit(
                    "ERROR: list of saturation limits is not the same length as list of observing filters."
                )


@dataclass
class phasecurvesConfigs:
    """Data class for holding PHASECURVES section configuration file keys and validating them"""

    phase_function: str = None
    """The phase function used to calculate apparent magnitude. The physical parameters input"""

    def __post_init__(self):
        """Automagically validates the phasecurve configs after initialisation."""
        self._validate_phasecurve_configs()

    def _validate_phasecurve_configs(self):
        """
        Validates the phasecurve config attributes after initialisation.

        Parameters
        -----------
        None.

        Returns
        ----------
        None
        """
        # make sure all the mandatory keys have been populated.
        check_key_exists(self.phase_function, "phase_function")

        check_value_in_list(self.phase_function, ["HG", "HG1G2", "HG12", "linear", "none"], "phase_function")


@dataclass
class fovConfigs:
    """Data class for holding FOV section configuration file keys and validating them"""

    camera_model: str = None
    """Choose between circular or actual camera footprint, including chip gaps."""

    footprint_path: str = None
    """Path to camera footprint file. Uncomment to provide a path to the desired camera detector configuration file if not using the default built-in LSSTCam detector configuration for the actual camera footprint."""

    fill_factor: str = None
    """Fraction of detector surface area which contains CCD -- simulates chip gaps for OIF output. Comment out if using camera footprint."""

    circle_radius: float = None
    """Radius of the circle for a circular footprint (in degrees). Float. Comment out or do not include if using footprint camera model."""

    footprint_edge_threshold: float = None
    """The distance from the edge of a detector (in arcseconds on the focal plane) at which we will not correctly extract an object. By default this is 10px or 2 arcseconds. Comment out or do not include if not using footprint camera model."""

    survey_name: str = None
    """name of survey"""

    def __post_init__(self):
        """Automagically validates the fov configs after initialisation."""
        self._validate_fov_configs()

    def _validate_fov_configs(self):
        """
        Validates the fov config attributes after initialisation.

        Parameters
        -----------
        None.

        Returns
        ----------
        None
        """
        check_key_exists(self.camera_model, "camera_model")
        check_value_in_list(self.camera_model, ["circle", "footprint", "none"], "camera_model")

        if self.camera_model == "footprint":
            self._camera_footprint()

        elif self.camera_model == "circle":
            self._camera_circle()

    def _camera_footprint(self):
        """
        Validates the fov config attributes for a footprint camera model.

        Parameters
        -----------
        None.

        Returns
        ----------
        None
        """
        if self.footprint_path is not None:
            FindFileOrExit(self.footprint_path, "footprint_path")
        elif self.survey_name.lower() not in ["lsst", "rubin_sim"]:
            logging.error(
                "ERROR: a default detector footprint is currently only provided for LSST; please provide your own footprint file."
            )
            sys.exit(
                "ERROR: a default detector footprint is currently only provided for LSST; please provide your own footprint file."
            )
        if self.footprint_edge_threshold is not None:
            self.footprint_edge_threshold = cast_as_float(
                self.footprint_edge_threshold, "footprint_edge_threshold"
            )
        check_key_doesnt_exist(self.fill_factor, "fill_factor", 'but camera model is not "circle".')
        check_key_doesnt_exist(self.circle_radius, "circle_radius", 'but camera model is not "circle".')

    def _camera_circle(self):
        """
        Validates the fov config attributes for a circle camera model.

        Parameters
        -----------
        None.

        Returns
        ----------
        None
        """
        if self.fill_factor is not None:
            self.fill_factor = cast_as_float(self.fill_factor, "fill_factor")
            if self.fill_factor < 0.0 or self.fill_factor > 1.0:
                logging.error("ERROR: fill_factor out of bounds. Must be between 0 and 1.")
                sys.exit("ERROR: fill_factor out of bounds. Must be between 0 and 1.")

        if self.circle_radius is not None:
            self.circle_radius = cast_as_float(self.circle_radius, "circle_radius")
            if self.circle_radius < 0.0:
                logging.error("ERROR: circle_radius is negative.")
                sys.exit("ERROR: circle_radius is negative.")

        if self.fill_factor is None and self.circle_radius is None:
            logging.error(
                'ERROR: either "fill_factor" or "circle_radius" must be specified for circular footprint.'
            )
            sys.exit(
                'ERROR: either "fill_factor" or "circle_radius" must be specified for circular footprint.'
            )
        check_key_doesnt_exist(
            self.footprint_edge_threshold, "footprint_edge_threshold", 'but camera model is not "footprint".'
        )


@dataclass
class fadingfunctionConfigs:
    """Data class for holding FADINGFUNCTION section configuration file keys and validating them"""

    fading_function_on: bool = None
    """Detection efficiency fading function on or off. Default True"""

    fading_function_width: float = None
    """Width parameter for fading function. Should be greater than zero and less than 0.5."""

    fading_function_peak_efficiency: float = None
    """Peak efficiency for the fading function, called the 'fill factor' in Chesley and Veres (2017)."""

    def __post_init__(self):
        """Automagically validates the fading function configs after initialisation."""
        self._validate_fadingfunction_configs()

    def _validate_fadingfunction_configs(self):
        """
        Validates the fadindfunction config attributes after initialisation.

        Parameters
        -----------
        None.

        Returns
        ----------
        None
        """

        if self.fading_function_width is not None and self.fading_function_peak_efficiency is not None:
            self.fading_function_on = True
            # when fading_function_on = true, fading_function_width and fading_function_peak_efficiency now mandatory

            self.fading_function_width = cast_as_float(self.fading_function_width, "fading_function_width")
            self.fading_function_peak_efficiency = cast_as_float(
                self.fading_function_peak_efficiency, "fading_function_peak_efficiency"
            )

            # boundary conditions for both width and peak efficency
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
                sys.exit("ERROR: fading_function_peak_efficiency out of bounds. Must be between 0 and 1.")

        elif self.fading_function_width is None and self.fading_function_peak_efficiency is None:
            self.fading_function_on = False

        else:
            logging.error(
                "ERROR: Both fading_function_peak_efficiency and fading_function_width are needed to be supplied for fading function"
            )
            sys.exit(
                "ERROR: Both fading_function_peak_efficiency and fading_function_width are needed to be supplied for fading function"
            )


@dataclass
class linkingfilterConfigs:
    """Data class for holding LINKINGFILTER section configuration file keys and validating them."""

    ssp_linking_on: bool = None
    """flag to see if model should run ssp linking filter"""

    drop_unlinked: bool = None
    """Decides if unlinked objects will be dropped."""

    ssp_detection_efficiency: float = None
    """ssp detection efficiency. Which fraction of the observations of an object will the automated solar system processing pipeline successfully link? Float."""

    ssp_number_observations: int = None
    """Length of tracklets. How many observations of an object during one night are required to produce a valid tracklet?"""

    ssp_separation_threshold: float = None
    """Minimum separation (in arcsec) between two observations of an object required for the linking software to distinguish them as separate and therefore as a valid tracklet."""

    ssp_maximum_time: float = None
    """Maximum time separation (in days) between subsequent observations in a tracklet. Default is 0.0625 days (90mins)."""

    ssp_number_tracklets: int = None
    """Number of tracklets for detection. How many tracklets are required to classify an object as detected?  """

    ssp_track_window: int = None
    """The number of tracklets defined above must occur in <= this number of days to constitute a complete track/detection."""

    ssp_night_start_utc: float = None
    """The time in UTC at which it is noon at the observatory location (in standard time). For the LSST, 12pm Chile Standard Time is 4pm UTC."""

    def __post_init__(self):
        """Automagically validates the linking filter configs after initialisation."""
        self._validate_linkingfilter_configs()

    def _validate_linkingfilter_configs(self):
        """
        Validates the linkingfilter config attributes after initialisation.

        Parameters
        -----------
        None.

        Returns
        ----------
        None
        """

        sspvariables = [
            self.ssp_separation_threshold,
            self.ssp_number_observations,
            self.ssp_number_tracklets,
            self.ssp_track_window,
            self.ssp_detection_efficiency,
            self.ssp_maximum_time,
            self.ssp_night_start_utc,
        ]

        # the below if-statement explicitly checks for None so a zero triggers the correct error
        if all(v != None for v in sspvariables):

            self.ssp_detection_efficiency = cast_as_float(
                self.ssp_detection_efficiency, "ssp_detection_efficiency"
            )
            self.ssp_number_observations = cast_as_int(
                self.ssp_number_observations, "ssp_number_observations"
            )
            self.ssp_separation_threshold = cast_as_float(
                self.ssp_separation_threshold, "ssp_separation_threshold"
            )
            self.ssp_maximum_time = cast_as_float(self.ssp_maximum_time, "ssp_maximum_time")
            self.ssp_number_tracklets = cast_as_int(self.ssp_number_tracklets, "ssp_number_tracklets")
            self.ssp_track_window = cast_as_int(self.ssp_track_window, "ssp_track_window")
            self.ssp_night_start_utc = cast_as_float(self.ssp_night_start_utc, "ssp_night_start_utc")
            if self.ssp_number_observations < 1:
                logging.error("ERROR: ssp_number_observations is zero or negative.")
                sys.exit("ERROR: ssp_number_observations is zero or negative.")

            if self.ssp_number_tracklets < 1:
                logging.error("ERROR: ssp_number_tracklets is zero or less.")
                sys.exit("ERROR: ssp_number_tracklets is zero or less.")

            if self.ssp_track_window <= 0.0:
                logging.error("ERROR: ssp_track_window is negative.")
                sys.exit("ERROR: ssp_track_window is negative.")

            if self.ssp_detection_efficiency > 1.0 or self.ssp_detection_efficiency < 0:
                logging.error("ERROR: ssp_detection_efficiency out of bounds (should be between 0 and 1).")
                sys.exit("ERROR: ssp_detection_efficiency out of bounds (should be between 0 and 1).")

            if self.ssp_separation_threshold <= 0.0:
                logging.error("ERROR: ssp_separation_threshold is zero or negative.")
                sys.exit("ERROR: ssp_separation_threshold is zero or negative.")

            if self.ssp_maximum_time < 0:
                logging.error("ERROR: ssp_maximum_time is negative.")
                sys.exit("ERROR: ssp_maximum_time is negative.")

            if self.ssp_night_start_utc > 24.0 or self.ssp_night_start_utc < 0.0:
                logging.error("ERROR: ssp_night_start_utc must be a valid time between 0 and 24 hours.")
                sys.exit("ERROR: ssp_night_start_utc must be a valid time between 0 and 24 hours.")

            self.ssp_linking_on = True
        elif all(v == None for v in sspvariables):
            self.ssp_linking_on = False
        else:
            logging.error(
                "ERROR: only some ssp linking variables supplied. Supply all five required variables for ssp linking filter, or none to turn filter off."
            )
            sys.exit(
                "ERROR: only some ssp linking variables supplied. Supply all five required variables for ssp linking filter, or none to turn filter off."
            )
        self.drop_unlinked = cast_as_bool_or_set_default(self.drop_unlinked, "drop_unlinked", True)


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


@dataclass
class lightcurveConfigs:
    """Data class for holding LIGHTCURVE section configuration file keys and validating them."""

    lc_model: str = None
    """The unique name of the lightcurve model to use. Defined in the ``name_id`` method of the subclasses of AbstractLightCurve. If not none, the complex physical parameters file must be specified at the command line.lc_model = none"""

    def __post_init__(self):
        """Automagically validates the lightcurve configs after initialisation."""
        self._validate_lightcurve_configs()

    def _validate_lightcurve_configs(self):
        """
        Validates the lightcurve config attributes after initialisation.

        Parameters
        -----------
        None.

        Returns
        ----------
        None
        """
        self.lc_model = None if self.lc_model == "none" else self.lc_model
        if self.lc_model is not None and self.lc_model not in LC_METHODS:
            logging.error(
                f"The requested light curve model, '{self.lc_model}', is not registered. Available lightcurve options are: {list(LC_METHODS.keys())}"
            )
            sys.exit(
                f"The requested light curve model, '{self.lc_model}', is not registered. Available lightcurve options are: {list(LC_METHODS.keys())}"
            )


@dataclass
class activityConfigs:
    """Data class for holding Activity section configuration file keys and validating them."""

    comet_activity: str = None
    """The unique name of the actvity model to use. Defined in the ``name_id`` method of the subclasses of AbstractCometaryActivity.  If not none, a complex physical parameters file must be specified at the command line."""

    def __post_init__(self):
        """Automagically validates the activity configs after initialisation."""
        self._validate_activity_configs()

    def _validate_activity_configs(self):
        """
        Validates the activity config attributes after initialisation.

        Parameters
        -----------
        None.

        Returns
        ----------
        None
        """
        self.comet_activity = None if self.comet_activity == "none" else self.comet_activity
        if self.comet_activity is not None and self.comet_activity not in CA_METHODS:
            logging.error(
                f"The requested comet activity model, '{self.comet_activity}', is not registered. Available comet activity models are: {list(CA_METHODS.keys())}"
            )
            sys.exit(
                f"The requested comet activity model, '{self.comet_activity}', is not registered. Available comet activity models are: {list(CA_METHODS.keys())}"
            )


@dataclass
class expertConfigs:
    """Data class for holding expert section configuration file keys and validating them."""

    snr_limit: float = None
    """Drops observations with signal to noise ratio less than limit given"""

    snr_limit_on: bool = None
    """flag for when an SNR limit is given"""

    mag_limit: float = None
    """Drops observations with magnitude less than limit given"""

    mag_limit_on: bool = None
    """flag for when a magnitude limit is given"""

    trailing_losses_on: bool = None
    """flag for trailing losses"""

    default_snr_cut: bool = None
    """flag for default SNR"""

    randomization_on: bool = None
    """flag for randomizing astrometry and photometry"""

    vignetting_on: bool = None
    """flag for calculating effects of vignetting on limiting magnitude"""

    brute_force: bool = None
    """brute-force ephemeris generation on all objects without running a first-pass"""

    ar_use_integrate: bool = None
    """flag for using the integrate method instead of integrate_or_interpolate"""

    def __post_init__(self):
        """Automagically validates the expert configs after initialisation."""
        self._validate_expert_configs()

    def _validate_expert_configs(self):
        """
        Validates the expert config attributes after initialisation.

        Parameters
        -----------
        None.

        Returns
        ----------
        None
        """
        if self.snr_limit is not None:
            self.snr_limit = cast_as_float(self.snr_limit, "snr_limit")
            self.snr_limit_on = True
            if self.snr_limit < 0:
                logging.error("ERROR: SNR limit is negative.")
                sys.exit("ERROR: SNR limit is negative.")
        else:
            self.snr_limit_on = False

        if self.mag_limit is not None:
            self.mag_limit = cast_as_float(self.mag_limit, "mag_limit")
            self.mag_limit_on = True
            if self.mag_limit < 0:
                logging.error("ERROR: magnitude limit is negative.")
                sys.exit("ERROR: magnitude limit is negative.")
        else:
            self.mag_limit_on = False

        if self.mag_limit_on and self.snr_limit_on:
            logging.error(
                "ERROR: SNR limit and magnitude limit are mutually exclusive. Please delete one or both from config file."
            )
            sys.exit(
                "ERROR: SNR limit and magnitude limit are mutually exclusive. Please delete one or both from config file."
            )

        self.trailing_losses_on = cast_as_bool_or_set_default(
            self.trailing_losses_on, "trailing_losses_on", True
        )
        self.default_snr_cut = cast_as_bool_or_set_default(self.default_snr_cut, "default_snr_cut", True)
        self.randomization_on = cast_as_bool_or_set_default(self.randomization_on, "randomization_on", True)
        self.vignetting_on = cast_as_bool_or_set_default(self.vignetting_on, "vignetting_on", True)
        self.brute_force = cast_as_bool_or_set_default(self.brute_force, "brute_force", True)
        self.ar_use_integrate = cast_as_bool_or_set_default(self.ar_use_integrate, "ar_use_integrate", False)


@dataclass
class auxiliaryConfigs:
    """Data class for holding auxiliary section configuration file keys and validating them."""

    planet_ephemeris: str = "de440s.bsp"
    """filename of planet_ephemeris"""
    planet_ephemeris_url: str = "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/de440s.bsp"
    """url for planet_ephemeris"""

    earth_predict: str = "earth_200101_990827_predict.bpc"
    """filename of earth_predict"""
    earth_predict_url: str = (
        "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/earth_200101_990827_predict.bpc"
    )
    """url for earth_predict"""

    earth_historical: str = "earth_620120_240827.bpc"
    """filename of earth_histoical"""
    earth_historical_url: str = (
        "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/earth_620120_240827.bpc"
    )
    """url for earth_historical"""

    earth_high_precision: str = "earth_latest_high_prec.bpc"
    """filename of earth_high_precision"""
    earth_high_precision_url: str = (
        "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/earth_latest_high_prec.bpc"
    )
    """url of earth_high_precision"""

    jpl_planets: str = "linux_p1550p2650.440"
    """filename of jpl_planets"""
    jpl_planets_url: str = "https://ssd.jpl.nasa.gov/ftp/eph/planets/Linux/de440/linux_p1550p2650.440"
    """url of jpl_planets"""

    jpl_small_bodies: str = "sb441-n16.bsp"
    """filename of jpl_small_bodies"""
    jpl_small_bodies_url: str = "https://ssd.jpl.nasa.gov/ftp/eph/small_bodies/asteroids_de441/sb441-n16.bsp"
    """url of jpl_small_bodies"""

    leap_seconds: str = "naif0012.tls"
    """filename of leap_seconds"""
    leap_seconds_url: str = "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/lsk/naif0012.tls"
    """url of leap_seconds"""

    meta_kernel: str = "meta_kernel.txt"
    """filename of meta_kernal"""

    observatory_codes: str = "ObsCodes.json"
    """filename of observatory_codes"""

    observatory_codes_compressed: str = "ObsCodes.json.gz"
    """filename of observatory_codes_compressed"""
    observatory_codes_compressed_url: str = (
        "https://minorplanetcenter.net/Extended_Files/obscodes_extended.json.gz"
    )
    """url of observatory_codes_compressed"""

    orientation_constants: str = "pck00010.pck"
    """filename of observatory_constants"""
    orientation_constants_url: str = "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/pck00010.tpc"
    """url of observatory_constants"""

    data_file_list: list = None
    """convenience list of all the file names"""

    urls: dict = None
    """dictionary of filename: url"""

    data_files_to_download: list = None
    """list of files that need to be downloaded"""

    ordered_kernel_files: list = None
    """list of kernels ordered from least to most precise - used to assemble meta_kernel file"""

    registry: list = None
    """Default Pooch registry to define which files will be tracked and retrievable"""

    @property
    def default_url(self):
        """returns a dictionary of the default urls used in this version of sorcha"""
        return {
            "planet_ephemeris": self.__class__.planet_ephemeris_url,
            "earth_predict": self.__class__.earth_predict_url,
            "earth_historical": self.__class__.earth_historical_url,
            "earth_high_precision": self.__class__.earth_high_precision_url,
            "jpl_planets": self.__class__.jpl_planets_url,
            "jpl_small_bodies": self.__class__.jpl_small_bodies_url,
            "leap_seconds": self.__class__.leap_seconds_url,
            "observatory_codes_compressed": self.__class__.observatory_codes_compressed_url,
            "orientation_constants": self.__class__.orientation_constants_url,
        }

    @property
    def default_filenames(self):
        """returns a dictionary of the default filenames used in this version"""
        return {
            "planet_ephemeris": self.__class__.planet_ephemeris,
            "earth_predict": self.__class__.earth_predict,
            "earth_historical": self.__class__.earth_historical,
            "earth_high_precision": self.__class__.earth_high_precision,
            "jpl_planets": self.__class__.jpl_planets,
            "jpl_small_bodies": self.__class__.jpl_small_bodies,
            "leap_seconds": self.__class__.leap_seconds,
            "meta_kernel": self.__class__.meta_kernel,
            "observatory_codes": self.__class__.observatory_codes,
            "observatory_codes_compressed": self.__class__.observatory_codes_compressed,
            "orientation_constants": self.__class__.orientation_constants,
        }

    def __post_init__(self):
        """Automagically validates the auxiliary configs after initialisation."""
        self._create_lists_auxiliary_configs()
        self._validate_auxiliary_configs()

    def _validate_auxiliary_configs(self):
        """
        validates the auxililary config attributes after initialisation.
        """
        for file in self.default_filenames:
            if file != "meta_kernel" and file != "observatory_codes":
                if (
                    self.default_filenames[file] == getattr(self, file)
                    and getattr(self, file + "_url") != self.default_url[file]
                ):
                    logging.error(f"ERROR: url for {file} given but filename for {file} not given")
                    sys.exit(f"ERROR: url for {file} given but filename for {file} not given")

                elif (
                    self.default_filenames[file] != getattr(self, file)
                    and getattr(self, file + "_url") == self.default_url[file]
                ):
                    setattr(self, file + "_url", None)

    def _create_lists_auxiliary_configs(self):
        """
        creates lists of the auxililary config attributes after initialisation.

        Parameters
        -----------
        None.

        Returns
        ----------
        None
        """

        self.urls = {
            self.planet_ephemeris: self.planet_ephemeris_url,
            self.earth_predict: self.earth_predict_url,
            self.earth_historical: self.earth_historical_url,
            self.earth_high_precision: self.earth_high_precision_url,
            self.jpl_planets: self.jpl_planets_url,
            self.jpl_small_bodies: self.jpl_small_bodies_url,
            self.leap_seconds: self.leap_seconds_url,
            self.observatory_codes_compressed: self.observatory_codes_compressed_url,
            self.orientation_constants: self.orientation_constants_url,
        }

        self.data_file_list = [
            self.planet_ephemeris,
            self.earth_predict,
            self.earth_historical,
            self.earth_high_precision,
            self.jpl_planets,
            self.jpl_small_bodies,
            self.leap_seconds,
            self.meta_kernel,
            self.observatory_codes,
            self.observatory_codes_compressed,
            self.orientation_constants,
        ]

        self.data_files_to_download = [
            self.planet_ephemeris,
            self.earth_predict,
            self.earth_historical,
            self.earth_high_precision,
            self.jpl_planets,
            self.jpl_small_bodies,
            self.leap_seconds,
            self.observatory_codes_compressed,
            self.orientation_constants,
        ]

        self.ordered_kernel_files = [
            self.leap_seconds,
            self.earth_historical,
            self.earth_predict,
            self.orientation_constants,
            self.planet_ephemeris,
            self.earth_high_precision,
        ]

        self.registry = {data_file: None for data_file in self.data_file_list}


@dataclass
class sorchaConfigs:
    """Dataclass which stores configuration file keywords in dataclasses."""

    input: inputConfigs = None
    """inputConfigs dataclass which stores the keywords from the INPUT section of the config file."""

    simulation: simulationConfigs = None
    """simulationConfigs dataclass which stores the keywords from the SIMULATION section of the config file."""

    filters: filtersConfigs = None
    """filtersConfigs dataclass which stores the keywords from the FILTERS section of the config file."""

    saturation: saturationConfigs = None
    """saturationConfigs dataclass which stores the keywords from the SATURATION section of the config file."""

    phasecurves: phasecurvesConfigs = None
    """phasecurveConfigs dataclass which stores the keywords from the PHASECURVES section of the config file."""

    fov: fovConfigs = None
    """fovConfigs dataclass which stores the keywords from the FOV section of the config file."""

    fadingfunction: fadingfunctionConfigs = None
    """fadingfunctionConfigs dataclass which stores the keywords from the FADINGFUNCTION section of the config file."""

    linkingfilter: linkingfilterConfigs = None
    """linkingfilterConfigs dataclass which stores the keywords from the LINKINGFILTER section of the config file."""

    output: outputConfigs = None
    """outputConfigs dataclass which stores the keywords from the OUTPUT section of the config file."""

    lightcurve: lightcurveConfigs = None
    """lightcurveConfigs dataclass which stores the keywords from the LIGHTCURVE section of the config file."""

    activity: activityConfigs = None
    """activityConfigs dataclass which stores the keywords from the ACTIVITY section of the config file."""

    expert: expertConfigs = None
    """expertConfigs dataclass which stores the keywords from the EXPERT section of the config file."""

    auxiliary: auxiliaryConfigs = None
    """auxiliaryConfigs dataclass which stores the keywords from the AUXILIARY section of the config file."""

    # When adding a new config dataclass or new dataclass config parameters remember to add these to the function PrintConfigsToLog below.
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
            # Save a raw copy of the configuration to the logs as a backup.
            with open(config_file_location, "r") as file:
                logging.info(f"Copy of configuration file {config_file_location}:\n{file.read()}")

            config_object = configparser.ConfigParser()  # create a ConfigParser object
            config_object.read(config_file_location)  # and read the whole config file into it
            self._read_configs_from_object(
                config_object
            )  # now we call a function that populates the class attributes

    def _read_configs_from_object(self, config_object):
        """
        function that populates the class attributes

        Parameters
        -----------
        config_object: ConfigParser object
            ConfigParser object that has the config file read into it

        Returns
        ----------
        None

        """

        # list of sections and corresponding config file
        section_list = {
            "INPUT": inputConfigs,
            "SIMULATION": simulationConfigs,
            "FILTERS": filtersConfigs,
            "SATURATION": saturationConfigs,
            "PHASECURVES": phasecurvesConfigs,
            "FOV": fovConfigs,
            "FADINGFUNCTION": fadingfunctionConfigs,
            "LINKINGFILTER": linkingfilterConfigs,
            "OUTPUT": outputConfigs,
            "LIGHTCURVE": lightcurveConfigs,
            "ACTIVITY": activityConfigs,
            "EXPERT": expertConfigs,
            "AUXILIARY": auxiliaryConfigs,
        }
        # when adding new sections in config file this general function needs the name of the section in uppercase
        # to be the same as the attributes defined above in lowercase e.g. section INPUT has attribute input
        # general function that reads in config file sections into there config dataclasses
        for section, config_section in section_list.items():
            if config_object.has_section(section):
                extra_args = {}
                if section == "SIMULATION":
                    extra_args["_ephemerides_type"] = self.input.ephemerides_type
                elif section == "FILTERS":
                    extra_args["survey_name"] = self.survey_name
                elif section == "SATURATION":
                    extra_args["_observing_filters"] = self.filters.observing_filters
                elif section == "FOV":
                    extra_args["survey_name"] = self.survey_name
                section_dict = dict(config_object[section])
                config_instance = config_section(**section_dict, **extra_args)

            else:
                config_instance = config_section()  # if section not in config file take default values
            section_key = section.lower()
            setattr(self, section_key, config_instance)


## below are the utility functions used to help validate the keywords, add more as needed


def check_key_exists(value, key_name):
    """
    Checks to confirm that a mandatory config file value is present and has been read into the dataclass as truthy. Returns an error if value is falsy

    Parameters
    -----------
    value : object attribute
        value of the config file attribute

    key_name : string
        The key being checked.

    Returns
    ----------
    None.

    """

    if value is None:
        logging.error(
            f"ERROR: No value found for required key {key_name} in config file. Please check the file and try again."
        )
        sys.exit(
            f"ERROR: No value found for required key {key_name} in config file. Please check the file and try again."
        )


def check_key_doesnt_exist(value, key_name, reason):
    """
    Checks to confirm that a config file value is not present and has been read into the dataclass as falsy. Returns an error if value is truthy

    Parameters
    -----------
    value : object attribute
        value of the config file attribute

    key_name : string
        The key being checked.

    reason : string
        reason given in the error message on why this value shouldn't be in the config file

    Returns
    ----------
    None.
    """

    # checks to make sure value doesn't exist
    if value is not None:
        logging.error(f"ERROR: {key_name} supplied in config file {reason}")
        sys.exit(f"ERROR: {key_name} supplied in config file {reason}")


def cast_as_int(value, key):
    # replaces PPGetIntOrExit: checks to make sure the value can be cast as an integer.
    """
    Checks to see if value can be cast as an interger.

    Parameters
    -----------
    value : object attribute
        value of the config file attribute

    key : string
        The key being checked.
    Returns
    ----------
    value as an integer

    """

    try:
        int(value)
    except ValueError:
        logging.error(f"ERROR: expected an int for config parameter {key}. Check value in config file.")
        sys.exit(f"ERROR: expected an int for config parameter {key}. Check value in config file.")

    return int(value)


def cast_as_float(value, key):
    # replaces PPGetFloatOrExit: checks to make sure the value can be cast as a float.
    """
    Checks to see if value can be cast as a float.

    Parameters
    -----------
    value : object attribute
        value of the config file attribute

    key : string
        The key being checked.
    Returns
    ----------
    value as a float

    """

    try:
        float(value)
    except ValueError:
        logging.error(f"ERROR: expected a float for config parameter {key}. Check value in config file.")
        sys.exit(f"ERROR: expected a float for config parameter {key}. Check value in config file.")

    return float(value)


def cast_as_bool(value, key):
    # replaces PPGetBoolOrExit: checks to make sure the value can be cast as a bool.
    """
    Checks to see if value can be cast as a boolen.

    Parameters
    -----------
    value : object attribute
        value of the config file attribute

    key : string
        The key being checked.
    Returns
    ----------
    value as a boolen
    """

    str_value = str(value).strip()

    if str_value in ["true", "1", "yes", "y", "True"]:
        return True
    elif str_value in ["false", "0", "no", "n", "False"]:
        return False
    else:
        logging.error(f"ERROR: expected a bool for config parameter {key}. Check value in config file.")
        sys.exit(f"ERROR: expected a bool for config parameter {key}. Check value in config file.")


def check_value_in_list(value, valuelist, key):
    # PPConfigParser often checks to see if a config variable is in a list of permissible variables, so this abstracts it out.
    """
    Checks to see if a config variable is in a list of permissible variables.

    Parameters
    -----------
    value : object attribute
        value of the config file value

    valuelist: list
        list of permissible values for attribute

    key : string
        The key being checked.
    Returns
    ----------
    None.

    """

    if value not in valuelist:
        logging.error(
            f"ERROR: value {value} for config parameter {key} not recognised. Expecting one of: {valuelist}."
        )
        sys.exit(
            f"ERROR: value {value} for config parameter {key} not recognised. Expecting one of: {valuelist}."
        )


def cast_as_bool_or_set_default(value, key, default):

    # replaces PPGetBoolOrExit: checks to make sure the value can be cast as a bool.
    """
    Checks to see if value can be cast as a boolen and if not set (equals None) gives default bool.

    Parameters
    -----------
    value : object attribute
        value of the config file attribute

    key : string
        The key being checked.

    default : bool
        default bool if value is None

    Returns
    ----------
    value as a boolen
    """

    if value is not None:

        str_value = str(value).strip()

        if str_value in ["true", "1", "yes", "y", "True"]:
            return True
        elif str_value in ["false", "0", "no", "n", "False"]:
            return False
        else:
            logging.error(f"ERROR: expected a bool for config parameter {key}. Check value in config file.")
            sys.exit(f"ERROR: expected a bool for config parameter {key}. Check value in config file.")
    elif value is None:
        return default


def PrintConfigsToLog(sconfigs, cmd_args):
    """
    Prints all the values from the config file and command line to the log.

    Parameters
    -----------
    sconfigs : dataclass
        Dataclass of config file variables.

    cmd_args : dictionary
        Dictionary of command line arguments.

    Returns
    ----------
    None.

    """
    pplogger = logging.getLogger(__name__)

    pplogger.info("The config file used is located at " + cmd_args.configfile)
    pplogger.info("The physical parameters file used is located at " + cmd_args.paramsinput)
    pplogger.info("The orbits file used is located at " + cmd_args.orbinfile)
    if cmd_args.input_ephemeris_file:
        pplogger.info("The ephemerides file used is located at " + cmd_args.input_ephemeris_file)
    if cmd_args.output_ephemeris_file:
        pplogger.info("The output ephemerides file is located " + cmd_args.output_ephemeris_file)
    pplogger.info("The survey selected is: " + cmd_args.surveyname)

    if sconfigs.activity.comet_activity == "comet":
        pplogger.info("Cometary activity set to: " + str(sconfigs.activity.comet_activity))
    elif sconfigs.activity.comet_activity == None:
        pplogger.info("No cometary activity selected.")

    pplogger.info("Format of ephemerides file is: " + sconfigs.input.eph_format)
    pplogger.info("Format of auxiliary files is: " + sconfigs.input.aux_format)

    pplogger.info("Pointing database path is: " + cmd_args.pointing_database)
    pplogger.info("Pointing database required query is: " + sconfigs.input.pointing_sql_query)

    pplogger.info(
        "The number of objects processed in a single chunk is: " + str(sconfigs.input.size_serial_chunk)
    )
    pplogger.info("The main filter in which H is defined is " + sconfigs.filters.mainfilter)
    rescs = " ".join(str(f) for f in sconfigs.filters.observing_filters)
    pplogger.info("The filters included in the post-processing results are " + rescs)

    if sconfigs.filters.othercolours:
        othcs = " ".join(str(e) for e in sconfigs.filters.othercolours)
        pplogger.info("Thus, the colour indices included in the simulation are " + othcs)

    pplogger.info(
        "The apparent brightness is calculated using the following phase function model: "
        + sconfigs.phasecurves.phase_function
    )

    if sconfigs.expert.trailing_losses_on:
        pplogger.info("Computation of trailing losses is switched ON.")
    else:
        pplogger.info("Computation of trailing losses is switched OFF.")

    if sconfigs.expert.randomization_on:
        pplogger.info("Randomization of position and magnitude around uncertainties is switched ON.")
    else:
        pplogger.info("Randomization of position and magnitude around uncertainties is switched OFF.")

    if sconfigs.expert.vignetting_on:
        pplogger.info("Vignetting is switched ON.")
    else:
        pplogger.info("Vignetting is switched OFF.")

    if sconfigs.fov.camera_model == "footprint":
        pplogger.info("Footprint is modelled after the actual camera footprint.")
        if sconfigs.fov.footprint_path:
            pplogger.info("Loading camera footprint from " + sconfigs.fov.footprint_path)
        else:
            pplogger.info("Loading default LSST footprint LSST_detector_corners_100123.csv")
        if sconfigs.fov.footprint_edge_threshold:
            pplogger.info(
                "The footprint edge threshold is "
                + str(sconfigs.fov.footprint_edge_threshold)
                + " arcseconds"
            )
        else:
            pplogger.info("Default footprint edge threshold used (10px or 2 arcseconds).")
    elif sconfigs.fov.camera_model == "circle":
        pplogger.info("Footprint is circular.")
        if sconfigs.fov.fill_factor:
            pplogger.info(
                "The code will approximate chip gaps using filling factor: " + str(sconfigs.fov.fill_factor)
            )
        elif sconfigs.fov.circle_radius:
            pplogger.info(
                "A circular footprint will be applied with radius: " + str(sconfigs.fov.circle_radius)
            )
    else:
        pplogger.info("Camera footprint is turned OFF.")

    if sconfigs.saturation.bright_limit_on:
        pplogger.info("The upper saturation limit(s) is/are: " + str(sconfigs.saturation.bright_limit))
    else:
        pplogger.info("Saturation limit is turned OFF.")

    if sconfigs.expert.snr_limit_on:
        pplogger.info("The lower SNR limit is: " + str(sconfigs.expert.snr_limit))
    else:
        pplogger.info("SNR limit is turned OFF.")

    if sconfigs.expert.default_snr_cut:
        pplogger.info("Default SNR cut is ON. All observations with SNR < 2.0 will be removed.")

    if sconfigs.expert.mag_limit_on:
        pplogger.info("The magnitude limit is: " + str(sconfigs.expert.mag_limit))
    else:
        pplogger.info("Magnitude limit is turned OFF.")

    if sconfigs.fadingfunction.fading_function_on:
        pplogger.info("The detection efficiency fading function is ON.")
        pplogger.info(
            "The width parameter of the fading function has been set to: "
            + str(sconfigs.fadingfunction.fading_function_width)
        )
        pplogger.info(
            "The peak efficiency of the fading function has been set to: "
            + str(sconfigs.fadingfunction.fading_function_peak_efficiency)
        )
    else:
        pplogger.info("The detection efficiency fading function is OFF.")

    if sconfigs.linkingfilter.ssp_linking_on:
        pplogger.info("Solar System Processing linking filter is turned ON.")
        pplogger.info("For SSP linking...")
        pplogger.info(
            "...the fractional detection efficiency is: "
            + str(sconfigs.linkingfilter.ssp_detection_efficiency)
        )
        pplogger.info(
            "...the minimum required number of observations in a tracklet is: "
            + str(sconfigs.linkingfilter.ssp_number_observations)
        )
        pplogger.info(
            "...the minimum required number of tracklets to form a track is: "
            + str(sconfigs.linkingfilter.ssp_number_tracklets)
        )
        pplogger.info(
            "...the maximum window of time in days of tracklets to be contained in to form a track is: "
            + str(sconfigs.linkingfilter.ssp_track_window)
        )
        pplogger.info(
            "...the minimum angular separation between observations in arcseconds is: "
            + str(sconfigs.linkingfilter.ssp_separation_threshold)
        )
        pplogger.info(
            "...the maximum temporal separation between subsequent observations in a tracklet in days is: "
            + str(sconfigs.linkingfilter.ssp_maximum_time)
        )
        pplogger.info(
            "...the time in UTC at which it is noon at the observatory location (in standard time) is "
            + str(sconfigs.linkingfilter.ssp_night_start_utc)
        )
        if not sconfigs.linkingfilter.drop_unlinked:
            pplogger.info("Unlinked objects will not be dropped.")
    else:
        pplogger.info("Solar System Processing linking filter is turned OFF.")
    pplogger.info("The auxiliary files used for emphemris generation...")
    pplogger.info("...the leap second file is: " + str(sconfigs.auxiliary.leap_seconds))
    pplogger.info(
        "...the historical Earth orientation specification file is: "
        + str(sconfigs.auxiliary.earth_historical)
    )
    pplogger.info(
        "...the prediction of the Earth's future orientation file is: "
        + str(sconfigs.auxiliary.earth_predict)
    )
    pplogger.info(
        "...the orientation information and physical constants for other bodies file is: "
        + str(sconfigs.auxiliary.orientation_constants)
    )
    pplogger.info(
        "...the Earth's position for ephemerides file is: " + str(sconfigs.auxiliary.planet_ephemeris)
    )
    pplogger.info(
        "...the regularly updated specification of the Earth's orientation file is: "
        + str(sconfigs.auxiliary.earth_high_precision)
    )
    pplogger.info(
        "...the observatory position information and Minor Planet Center (MPC) observatory codes file is: "
        + str(sconfigs.auxiliary.observatory_codes)
        + " and compressed file is: "
        + str(sconfigs.auxiliary.observatory_codes_compressed)
    )
    pplogger.info(
        "...the ephemerides for solar-system planets from JPL's Horizon system file is: "
        + str(sconfigs.auxiliary.jpl_planets)
    )
    pplogger.info(
        "...the ephemerides for solar-system small bodies from JPL's Horizon system file is: "
        + str(sconfigs.auxiliary.jpl_small_bodies)
    )
    pplogger.info("...the meta kernal file is : " + str(sconfigs.auxiliary.meta_kernel))
    if sconfigs.input.ephemerides_type == "ar":
        pplogger.info("ASSIST+REBOUND Simulation is turned ON.")
        pplogger.info("For ASSIST+REBOUND...")
        pplogger.info("...the field's angular FOV is: " + str(sconfigs.simulation.ar_ang_fov))
        pplogger.info("...the buffer around the FOV is: " + str(sconfigs.simulation.ar_fov_buffer))
        pplogger.info("...the picket interval is: " + str(sconfigs.simulation.ar_picket))
        pplogger.info("...the observatory code is: " + str(sconfigs.simulation.ar_obs_code))
        pplogger.info("...the healpix order is: " + str(sconfigs.simulation.ar_healpix_order))
        pplogger.info("...the number of sub-intervals is: " + str(sconfigs.simulation.ar_n_sub_intervals))
    else:
        pplogger.info("ASSIST+REBOUND Simulation is turned OFF.")

    if sconfigs.lightcurve.lc_model:
        pplogger.info("A lightcurve model is being applied.")
        pplogger.info("The lightcurve model is: " + sconfigs.lightcurve.lc_model)
    else:
        pplogger.info("No lightcurve model is being applied.")

    pplogger.info(
        "Output files will be saved in path: " + cmd_args.outpath + " with filestem " + cmd_args.outfilestem
    )
    pplogger.info("Output files will be saved as format: " + sconfigs.output.output_format)
    if sconfigs.output.position_decimals:
        pplogger.info(
            "In the output, positions will be rounded to "
            + str(sconfigs.output.position_decimals)
            + " decimal places."
        )
    else:
        pplogger.info("In the output, positions will not be rounded")
    if sconfigs.output.magnitude_decimals:
        pplogger.info(
            "In the output, magnitudes will be rounded to "
            + str(sconfigs.output.magnitude_decimals)
            + " decimal places."
        )
    else:
        pplogger.info("In the output, magnitudes will not be rounded")
    if isinstance(sconfigs.output.output_columns, list):
        pplogger.info("The output columns are set to: " + " ".join(sconfigs.output.output_columns))
    else:
        pplogger.info("The output columns are set to: " + sconfigs.output.output_columns)
