import logging
import sys
from dataclasses import dataclass
import numpy as np
from sorcha.configs.configUtilities import check_key_exists, check_survey_name_bool


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
        if isinstance(self.observing_filters, str):
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

        if check_survey_name_bool(self.survey_name, "rubin"):
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
        if check_survey_name_bool(self.survey_name, "des"):
            des_filters = ["g", "r", "i", "z", "Y"]
            filters_ok = all(elem in des_filters for elem in self.observing_filters)

            if not filters_ok:
                bad_list = np.setdiff1d(self.observing_filters, des_filters)
                logging.error(
                    "ERROR: Filter(s) {} given in config file are not recognised filters for {} survey.".format(
                        bad_list, self.survey_name
                    )
                )
                logging.error("Accepted {} filters: {}".format("DES", des_filters))
                logging.error("Change observing_filters in config file or select another survey.")
                sys.exit(
                    "ERROR: Filter(s) {} given in config file are not recognised filters for {} survey.".format(
                        bad_list, self.survey_name
                    )
                )
