import logging
import sys
from dataclasses import dataclass

from sorcha.configs.configUtilities import (
    cast_as_float,
    cast_as_int,
    cast_as_bool_or_set_default,
    check_key_exists,
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

    discovery_filter_on: bool = None
    """flag to see if model should run a discovery/linking filter"""

    des_discovery_on: bool = None
    """flag to see if model should run des discovery filter"""

    survey_name: str = None
    """name of survey"""

    des_distance_cut_on: bool = None
    """flag for DES for object-sun light-time-corrected distance cuts """

    des_distance_cut_upper: float = None
    """The upper distance limit for object-sun light-time-corrected distance for DES to detect objects. in km"""

    des_distance_cut_lower: float = None
    """The lower distance limit for object-sun light-time-corrected distance for DES to detect objects. in km"""
    des_motion_cut_on: bool = None
    """flag for when DES motion cuts are selected"""

    des_motion_cut_upper: float = None
    """The upper motion limit for DES to detect objects in (deg/day)"""

    des_motion_cut_lower: float = None
    """The lower motion limit for DES to detect objects (deg/day)"""

    def __post_init__(self):
        """Automagically validates the linking filter configs after initialisation."""
        self._validate_ssp_linkingfilter_configs()
        self._validate_des_linkingfilter_configs()

        if any([self.ssp_linking_on, self.des_discovery_on]):
            self.discovery_filter_on = True
        else:
            self.discovery_filter_on = False

    def _validate_ssp_linkingfilter_configs(self):
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

            if self.ssp_number_observations > 1 and self.ssp_separation_threshold == 0.0:
                logging.error("ERROR: ssp_separation_threshold is zero.")
                sys.exit("ERROR: ssp_separation_threshold is zero.")
            if self.ssp_separation_threshold < 0.0:
                logging.error("ERROR: ssp_separation_threshold is negative.")
                sys.exit("ERROR: ssp_separation_threshold is negative.")

            if self.ssp_number_tracklets < 1:
                logging.error("ERROR: ssp_number_tracklets is zero or less.")
                sys.exit("ERROR: ssp_number_tracklets is zero or less.")

            if self.ssp_track_window <= 0.0:
                logging.error("ERROR: ssp_track_window is negative.")
                sys.exit("ERROR: ssp_track_window is negative.")

            if self.ssp_detection_efficiency > 1.0 or self.ssp_detection_efficiency < 0:
                logging.error("ERROR: ssp_detection_efficiency out of bounds (should be between 0 and 1).")
                sys.exit("ERROR: ssp_detection_efficiency out of bounds (should be between 0 and 1).")

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

    def _validate_des_linkingfilter_configs(self):
        """
        Validates the des discovery filter config attributes after initialisation.

        Parameters
        -----------
        None.

        Returns
        ----------
        None
        """

        # if discovery or motion varibles on in config then des_discovery_on is True
        if self.des_distance_cut_upper is not None or self.des_distance_cut_lower is not None:
            self.des_distance_cut_on = True
            check_key_exists(self.des_distance_cut_upper, "des_distance_cut_upper")
            check_key_exists(self.des_distance_cut_lower, "des_distance_cut_lower")
            self.des_distance_cut_upper = cast_as_float(self.des_distance_cut_upper, "des_distance_cut_upper")
            self.des_distance_cut_lower = cast_as_float(self.des_distance_cut_lower, "des_distance_cut_lower")
        if self.des_motion_cut_upper is not None or self.des_motion_cut_lower is not None:
            self.des_motion_cut_on = True
            check_key_exists(self.des_motion_cut_upper, "des_motion_cut_upper")
            check_key_exists(self.des_motion_cut_lower, "des_motion_cut_lower")
            self.des_motion_cut_upper = cast_as_float(self.des_motion_cut_upper, "des_motion_cut_upper")
            self.des_motion_cut_lower = cast_as_float(self.des_motion_cut_lower, "des_motion_cut_lower")

        if any([self.des_motion_cut_on, self.des_distance_cut_on]):
            self.des_discovery_on = True
