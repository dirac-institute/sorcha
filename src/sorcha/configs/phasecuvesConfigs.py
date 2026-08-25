from dataclasses import dataclass
from sorcha.configs.configUtilities import check_key_exists, check_value_in_list


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
