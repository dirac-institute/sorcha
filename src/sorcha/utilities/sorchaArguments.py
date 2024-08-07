import numpy as np
from dataclasses import dataclass
import time
from os import path, urandom
import logging

from sorcha.modules.PPModuleRNG import PerModuleRNG
from sorcha.modules.PPGetLogger import PPGetLogger


@dataclass
class sorchaArguments:
    """Data class for holding runtime arguments"""

    paramsinput: str = ""
    """path to file with input objects"""
    orbinfile: str = ""
    """path to file with input object orbits"""
    oifoutput: str = ""
    """path the OIF output file"""
    configfile: str = ""
    """path to the config.ini file"""
    outpath: str = ""
    """path where data should be output"""
    outfilestem: str = ""
    """file system for output"""

    verbose: bool = False
    """logger verbosity"""

    surveyname: str = ""
    """name of the survey (`rubin_sim` is only one implemented currently)"""

    complex_parameters: str = ""
    """optional, extra complex physical parameter input files"""

    linking: bool = True
    """Turns on or off the rejection of unlinked sources"""

    _rngs = None
    """A collection of per-module random number generators"""

    pplogger = None
    """The Python logger instance"""

    def __init__(self, cmd_args_dict=None):
        self.pplogger = logging.getLogger(__name__)
        if cmd_args_dict is not None:
            self.read_from_dict(cmd_args_dict)

    def read_from_dict(self, args):
        """set the parameters from a cmd_args dict.

        Parameters
        ---------------
        aguments : dictionary
            dictionary of configuration parameters

        Returns
        ----------
        None

        """

        self.paramsinput = args["paramsinput"]
        self.orbinfile = args["orbinfile"]
        self.oifoutput = args.get("oifoutput")
        self.configfile = args["configfile"]
        self.outpath = args["outpath"]
        self.outfilestem = args["outfilestem"]
        self.pointing_database = args["pointing_database"]
        self.output_ephemeris_file = args.get("output_ephemeris_file")
        self.ar_data_file_path = args.get("ar_data_path")
        self.verbose = args["verbose"]
        self.stats = args["stats"]

        self.surveyname = args["surveyname"]

        if "complex_physical_parameters" in args.keys():
            self.complex_parameters = args["complex_physical_parameters"]

        # WARNING: Take care if manually setting the seed. Re-using seeds between
        # simulations may result in hard-to-detect correlations in simulation
        # outputs.
        seed = args.get("seed", int.from_bytes(urandom(4), "big"))
        self._rngs = PerModuleRNG(seed, self.pplogger)

    def validate_arguments(self):
        if not path.isfile(self.paramsinput):
            raise ValueError("File does not exist at path supplied for -p/--params argument.")

        if not path.isfile(self.orbinfile):
            raise ValueError("File does not exist at path supplied for -ob/--orbit argument.")

        if self.oifoutput and not path.isfile(self.oifoutput):
            raise ValueError("File does not exist at path supplied for -er/--ephem_read argument.")

        if not path.isfile(self.configfile):
            raise ValueError("File does not exist at path supplied for -c/--config argument.")

        if not path.isfile(self.pointing_database):
            raise ValueError("File does not exist at path supplied for -pd/--pointing_database argument.")

        if self.ar_data_file_path and not path.isdir(self.ar_data_file_path):
            raise ValueError("Directory does not exist at path supplied for -ar/--ar_data_path argument.")
