from dataclasses import dataclass
import configparser
import logging


from sorcha.configs.inputAndOutputConfigs import inputConfigs, outputConfigs
from sorcha.configs.ephemerisConfigs import simulationConfigs
from sorcha.configs.filtersConfigs import filtersConfigs
from sorcha.configs.saturationConfigs import saturationConfigs
from sorcha.configs.phasecuvesConfigs import phasecurvesConfigs
from sorcha.configs.fovConfigs import fovConfigs
from sorcha.configs.fadingfunctionConfigs import fadingfunctionConfigs
from sorcha.configs.linkingfilterConfigs import linkingfilterConfigs
from sorcha.configs.lightcurveAndActivityConfigs import lightcurveConfigs, activityConfigs
from sorcha.configs.expertConfigs import expertConfigs
from sorcha.configs.auxiliaryConfigs import auxiliaryConfigs


@dataclass
class basesorchaConfigs:
    """Dataclass which stores configuration file keywords in dataclasses,
    Usefull for using runSorchaSimulation without a dedicated config file. Use
    sorchaConfigs to read config files."""

    input: inputConfigs = None
    """inputConfigs dataclass which stores the keywords from the INPUT section of the config file."""

    simulation: simulationConfigs = None
    """simulationConfigs dataclass which stores the keywords from the SIMULATION section of the config file."""

    filters: filtersConfigs = None
    """filtersConfigs dataclass which stores the keywords from the FILTERS section of the config file."""

    saturation: saturationConfigs = None
    """saturationConfigs dataclass which stores the keywords from the SATURATION section of the config file."""

    phasecurves: phasecurvesConfigs = None
    """phasecurveConfigs dataclass which stores the keywords from the PHASECURVES section of the config file."""

    fov: fovConfigs = None
    """fovConfigs dataclass which stores the keywords from the FOV section of the config file."""

    fadingfunction: fadingfunctionConfigs = None
    """fadingfunctionConfigs dataclass which stores the keywords from the FADINGFUNCTION section of the config file."""

    linkingfilter: linkingfilterConfigs = None
    """linkingfilterConfigs dataclass which stores the keywords from the LINKINGFILTER section of the config file."""

    output: outputConfigs = None
    """outputConfigs dataclass which stores the keywords from the OUTPUT section of the config file."""

    lightcurve: lightcurveConfigs = None
    """lightcurveConfigs dataclass which stores the keywords from the LIGHTCURVE section of the config file."""

    activity: activityConfigs = None
    """activityConfigs dataclass which stores the keywords from the ACTIVITY section of the config file."""

    expert: expertConfigs = None
    """expertConfigs dataclass which stores the keywords from the EXPERT section of the config file."""

    auxiliary: auxiliaryConfigs = None
    """auxiliaryConfigs dataclass which stores the keywords from the AUXILIARY section of the config file."""

    # When adding a new config dataclass or new dataclass config parameters remember to add these to the function PrintConfigsToLog below.
    pplogger: None = None
    """The Python logger instance"""

    survey_name: str = ""
    """The name of the survey."""


class sorchaConfigs(basesorchaConfigs):
    """Set the dataclass to load from a file"""

    # this __init__ overrides a dataclass's inbuilt __init__ because we want to populate this from a file, not explicitly ourselves
    def __init__(self, config_file_location=None, survey_name=None):
        # attach the logger object so we can print things to the Sorcha logs
        self.pplogger = logging.getLogger(__name__)
        self.survey_name = survey_name

        if config_file_location:  # if a location to a config file is supplied...
            # Save a raw copy of the configuration to the logs as a backup.
            with open(config_file_location, "r") as file:
                logging.info(f"Copy of configuration file {config_file_location}:\n{file.read()}")

            config_object = configparser.ConfigParser()  # create a ConfigParser object
            config_object.read(config_file_location)  # and read the whole config file into it
            self._read_configs_from_object(
                config_object
            )  # now we call a function that populates the class attributes

    def _read_configs_from_object(self, config_object):
        """
        function that populates the class attributes

        Parameters
        -----------
        config_object: ConfigParser object
            ConfigParser object that has the config file read into it

        Returns
        ----------
        None

        """

        # list of sections and corresponding config file
        section_list = {
            "INPUT": inputConfigs,
            "SIMULATION": simulationConfigs,
            "FILTERS": filtersConfigs,
            "SATURATION": saturationConfigs,
            "PHASECURVES": phasecurvesConfigs,
            "FOV": fovConfigs,
            "FADINGFUNCTION": fadingfunctionConfigs,
            "LINKINGFILTER": linkingfilterConfigs,
            "OUTPUT": outputConfigs,
            "LIGHTCURVE": lightcurveConfigs,
            "ACTIVITY": activityConfigs,
            "EXPERT": expertConfigs,
            "AUXILIARY": auxiliaryConfigs,
        }
        # when adding new sections in config file this general function needs the name of the section in uppercase
        # to be the same as the attributes defined above in lowercase e.g. section INPUT has attribute input
        # general function that reads in config file sections into there config dataclasses
        for section, config_section in section_list.items():
            extra_args = {}
            if section == "FILTERS" or section == "FOV" or section == "EXPERT":
                extra_args["survey_name"] = self.survey_name

            if config_object.has_section(section):
                if section == "SIMULATION":
                    extra_args["_ephemerides_type"] = self.input.ephemerides_type

                if section == "SATURATION":
                    extra_args["_observing_filters"] = self.filters.observing_filters

                if section == "FOV":
                    extra_args["visits_query"] = self.input.visits_query

                if section == "EXPERT":
                    extra_args["camera_model"] = self.fov.camera_model

                section_dict = dict(config_object[section])
                config_instance = config_section(**section_dict, **extra_args)

            else:
                config_instance = config_section(
                    **extra_args
                )  # if section not in config file take default values
            section_key = section.lower()
            setattr(self, section_key, config_instance)
