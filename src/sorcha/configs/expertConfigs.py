import logging
import sys
from dataclasses import dataclass
from sorcha.configs.configUtilities import cast_as_bool_or_set_default, cast_as_float
from sorcha.utilities.survey_check import is_survey_valid


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

    uncertainties_on: bool = None
    """flag for generating astrometric and photometric uncertainties. These uncertainties are used to randomize the photometry, calulate SNR and account for trailing losses."""

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

    survey_name: str = None
    """survey name to be used for checking flags are correct"""

    camera_model: str = None
    """camera model chosen in fovConfigs"""

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
                logging.error("ERROR: SNRPSFMag limit is negative.")
                sys.exit("ERROR: SNRPSFMag limit is negative.")
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

        self.default_snr_cut = cast_as_bool_or_set_default(self.default_snr_cut, "default_snr_cut", True)
        self.brute_force = cast_as_bool_or_set_default(self.brute_force, "brute_force", True)

        if is_survey_valid(self.survey_name, "rubin"):
            self.uncertainties_on = cast_as_bool_or_set_default(
                self.uncertainties_on, "uncertainties_on", True
            )
            self.randomization_on = cast_as_bool_or_set_default(
                self.randomization_on, "randomization_on", True
            )
            self.vignetting_on = cast_as_bool_or_set_default(self.vignetting_on, "vignetting_on", True)
            self.trailing_losses_on = cast_as_bool_or_set_default(
                self.trailing_losses_on, "trailing_losses_on", True
            )
        if is_survey_valid(self.survey_name, "des"):
            logging.warning(
                "WARNING: DES simulation does not support uncertainties, trailing losses, vignetting and randomization. These are off by default"
            )
            self.uncertainties_on = cast_as_bool_or_set_default(
                self.uncertainties_on, "uncertainties_on", False
            )
            self.randomization_on = cast_as_bool_or_set_default(
                self.randomization_on, "randomization_on", False
            )
            self.vignetting_on = cast_as_bool_or_set_default(self.vignetting_on, "vignetting_on", False)
            self.trailing_losses_on = cast_as_bool_or_set_default(
                self.trailing_losses_on, "trailing_losses_on", False
            )
            if (
                self.uncertainties_on == True
                or self.randomization_on == True
                or self.vignetting_on == True
                or self.trailing_losses_on == True
            ):
                logging.error(
                    "ERROR: DES simulation does not support uncertainties, trailing losses, vignetting and randomization."
                )
                sys.exit(
                    "ERROR: DES simulation does not support uncertainties, trailing losses, vignetting and randomization."
                )

        if self.camera_model == "visits_footprint":
            logging.warning(
                "WARNING: fov camera model 'visits_footprint' does not support vignetting. This is off by default"
            )
            self.vignetting_on = cast_as_bool_or_set_default(self.vignetting_on, "vignetting_on", False)
            if self.vignetting_on == True:
                logging.error("ERROR: fov camera model 'visits_footprint' does not support vignetting.")
                sys.exit("ERROR: fov camera model 'visits_footprint' does not support vignetting.")

        if self.uncertainties_on == False and self.randomization_on == True:
            logging.error("ERROR: uncertainties_on must be true if randomization_on is true.")
            sys.exit("ERROR: uncertainties_on must be true if randomization_on is true.")
