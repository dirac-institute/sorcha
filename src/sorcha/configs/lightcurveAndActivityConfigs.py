import logging
import sys
from dataclasses import dataclass
from sorcha.lightcurves.lightcurve_registration import LC_METHODS
from sorcha.activity.activity_registration import CA_METHODS


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
