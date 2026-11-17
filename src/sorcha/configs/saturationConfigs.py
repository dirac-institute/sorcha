import logging
import sys
from dataclasses import dataclass
from sorcha.configs.configUtilities import check_key_exists


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

        if self.bright_limit is not None:
            self.bright_limit_on = True

        if self.bright_limit_on:
            check_key_exists(self._observing_filters, "_observing_filters")
            if isinstance(self.bright_limit, str):
                try:
                    self.bright_limit = [float(e.strip()) for e in self.bright_limit.split(",")]
                except ValueError:
                    logging.error("ERROR: could not parse brightness limits. Check formatting and try again.")
                    sys.exit("ERROR: could not parse brightness limits. Check formatting and try again.")
            elif isinstance(self.bright_limit, float):
                self.bright_limit = [self.bright_limit] * len(self._observing_filters)
            if isinstance(self.bright_limit, list):
                if len(self.bright_limit) == 1:
                    self.bright_limit = [self.bright_limit[0]] * len(self._observing_filters)
                elif len(self.bright_limit) != 1 and len(self.bright_limit) != len(self._observing_filters):
                    logging.error(
                        "ERROR: list of saturation limits is not the same length as list of observing filters."
                    )
                    sys.exit(
                        "ERROR: list of saturation limits is not the same length as list of observing filters."
                    )
