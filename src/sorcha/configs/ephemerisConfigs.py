from dataclasses import dataclass

from sorcha.configs.configUtilities import (
    check_key_exists,
    check_value_in_list,
    cast_as_float,
    cast_as_int,
    check_key_doesnt_exist,
)


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
