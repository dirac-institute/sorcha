import logging
import sys
from dataclasses import dataclass


@dataclass
class auxiliaryConfigs:
    """Data class for holding auxiliary section configuration file keys and validating them."""

    planet_ephemeris: str = "de440s.bsp"
    """filename of planet_ephemeris"""
    planet_ephemeris_url: str = "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/de440s.bsp"
    """url for planet_ephemeris"""

    earth_predict: str = "earth_2026_260806_2126_predict.bpc"
    """filename of earth_predict"""
    earth_predict_url: str = (
        "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/earth_2026_260806_2126_predict.bpc"
    )
    """url for earth_predict"""

    earth_historical: str = "earth_620120_260806.bpc"
    """filename of earth_histoical"""
    earth_historical_url: str = (
        "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/earth_620120_260806.bpc"
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
                    # if a new file is specified but not a url then the url is set as None.
                    # i.e. its assumed the file is in the cache ar directory and should not be downloaded.
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
