import logging
import sys
from dataclasses import dataclass

from sorcha.utilities.fileAccessUtils import FindFileOrExit

from sorcha.configs.configUtilities import (
    check_key_exists,
    check_value_in_list,
    cast_as_float,
    check_key_doesnt_exist,
)
from sorcha.utilities.survey_check import check_available_survey_configs


@dataclass
class fovConfigs:
    """Data class for holding FOV section configuration file keys and validating them"""

    camera_model: str = None
    """Choose between circular or general camera footprint or per visit camera footprint, including chip gaps."""

    footprint_path: str = None
    """Path to camera footprint file. Uncomment to provide a path to the desired camera detector configuration file if not using the default built-in detector configuration for the actual camera footprint."""

    default_camera_config_file: str = None
    """The default built-in detector configuration for the camera footprint."""

    visits_query: str = None
    """SQL query for extracting data from visits database."""

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
        check_value_in_list(
            self.camera_model, ["circle", "footprint", "visits_footprint", "none"], "camera_model"
        )
        if self.camera_model == "footprint":
            self._camera_footprint()
        if self.camera_model == "visits_footprint":
            self._camera_visits_footprint()
        if self.camera_model == "circle":
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
        if check_available_survey_configs(self.survey_name, "rubin"):
            self.default_camera_config_file = "data/LSST_detector_corners_100123.csv"
        elif check_available_survey_configs(self.survey_name, "des"):
            self.default_camera_config_file = "data/DES_ccd_corners.csv"
        else:
            logging.error(
                "ERROR: a default detector footprint is currently only provided for LSST and DES; please provide your own footprint file."
            )
            sys.exit(
                "ERROR: a default detector footprint is currently only provided for LSST and DES; please provide your own footprint file."
            )
        if self.footprint_edge_threshold is not None:
            self.footprint_edge_threshold = cast_as_float(
                self.footprint_edge_threshold, "footprint_edge_threshold"
            )
        check_key_doesnt_exist(
            self.visits_query, "visits_query", 'but camera model is not "visits_footprint".'
        )
        check_key_doesnt_exist(self.fill_factor, "fill_factor", 'but camera model is not "circle".')
        check_key_doesnt_exist(self.circle_radius, "circle_radius", 'but camera model is not "circle".')

    def _camera_visits_footprint(self):
        """
        Validates the fov config attributes for a per observation footprint camera model.

        Parameters
        -----------
        None.

        Returns
        ----------
        None
        """

        if check_available_survey_configs(self.survey_name, "des"):
            check_key_exists(self.visits_query, "visits_query")
            check_key_doesnt_exist(
                self.footprint_edge_threshold,
                "footprint_edge_threshold",
                "But visits footprint does not use edge threshold",
            )
            check_key_doesnt_exist(self.fill_factor, "fill_factor", 'but camera model is not "circle".')
            check_key_doesnt_exist(self.circle_radius, "circle_radius", 'but camera model is not "circle".')
        else:
            logging.error(
                f"ERROR: survey {self.survey_name} not valid for camera_model = {self.camera_model}, valid surveys are ['des']."
            )
            sys.exit(
                f"ERROR: survey {self.survey_name} not valid for camera_model = {self.camera_model}, valid surveys are ['des']."
            )

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
        check_key_doesnt_exist(
            self.visits_query, "visits_query", 'but camera model is not "visits_footprint".'
        )
