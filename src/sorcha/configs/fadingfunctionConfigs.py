import logging
import sys
from dataclasses import dataclass

from sorcha.configs.configUtilities import check_key_doesnt_exist, cast_as_float


@dataclass
class fadingfunctionConfigs:
    """Data class for holding FADINGFUNCTION section configuration file keys and validating them"""

    fading_function_on: bool = None
    """Detection efficiency fading function on or off. Default True"""

    fading_function_type: str = None
    """Type of fading function used for sorcha (currently either general or pero_obs)"""

    fading_function_width: float = None
    """Width parameter for fading function. Should be greater than zero and less than 0.5."""

    fading_function_peak_efficiency: float = None
    """Peak efficiency for the fading function, called the 'fill factor' in Chesley and Veres (2017)."""

    des_transient_efficency: float = None
    """Overall transient efficiency for moving object detection"""

    def __post_init__(self):
        """Automagically validates the fading function configs after initialisation."""

        self._validate_fadingfunction_configs_general()
        self._validate_fadingfunction_configs_des_per_obs()

        if self.fading_function_type is not None:
            self.fading_function_on = True
        else:
            self.fading_function_on = False

    def _validate_fadingfunction_configs_des_per_obs(self):
        """
        Validates the fadindfunction config attributes after initialisation for per observation footprint.

        Parameters
        -----------
        None.

        Returns
        ----------
        None
        """

        if self.des_transient_efficency is not None:
            self.fading_function_type = "des_per_obs"
            # des moving source efficency added as a flat constant across all possible detections
            self.des_transient_efficency = cast_as_float(
                self.des_transient_efficency, "des_transient_efficency"
            )
            if self.des_transient_efficency > 1 or self.des_transient_efficency < 0:
                sys.exit("ERROR: des_transient_efficency out of bounds. Must be between 0 and 1.")
                logging.error("ERROR: des_transient_efficency out of bounds. Must be between 0 and 1.")
            check_key_doesnt_exist(
                self.fading_function_peak_efficiency,
                "fading_function_peak_efficiency",
                "but fading function option is per footprint.",
            )
            check_key_doesnt_exist(
                self.fading_function_width,
                "fading_function_width",
                "but fading function option is per footprint.",
            )

    def _validate_fadingfunction_configs_general(self):
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
            self.fading_function_type = "general"

            # when fading_function_on = true, fading_function_width and fading_function_peak_efficiency now mandatory

            self.fading_function_width = cast_as_float(self.fading_function_width, "fading_function_width")
            self.fading_function_peak_efficiency = cast_as_float(
                self.fading_function_peak_efficiency, "fading_function_peak_efficiency"
            )
            check_key_doesnt_exist(
                self.des_transient_efficency,
                "des_transient_efficency",
                "which is not compatible with fading function fading_function_peak_efficiency and fading_function_width.",
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
        if (self.fading_function_width is None and self.fading_function_peak_efficiency is not None) or (
            self.fading_function_width is not None and self.fading_function_peak_efficiency is None
        ):
            logging.error(
                "ERROR: Both fading_function_peak_efficiency and fading_function_width are needed to be supplied for fading function"
            )
            sys.exit(
                "ERROR: Both fading_function_peak_efficiency and fading_function_width are needed to be supplied for fading function"
            )
