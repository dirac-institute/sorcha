import numpy as np
from dataclasses import dataclass
import time
from os import path, urandom
import logging
from typing import Tuple

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

    process_subset: Tuple[int, int] = (1, 1)
    """the subset of the file to process, in form of (split, nsplits)"""

    surveyname: str = ""
    """name of the survey (`rubin_sim` is only one implemented currently)"""

    extra_object_data: str = ""
    """optional, extra physical parameter input files"""

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
        self.process_subset = args["process_subset"]

        self.surveyname = args["surveyname"]

        if "extra_object_data" in args.keys():
            self.extra_object_data = args["extra_object_data"]

        # WARNING: Take care if manually setting the seed. Re-using seeds between
        # simulations may result in hard-to-detect correlations in simulation
        # outputs.
        seed = args.get("seed", int.from_bytes(urandom(4), "big"))
        self._rngs = PerModuleRNG(seed, self.pplogger)

    def validate_arguments(self):
        if not path.isfile(self.paramsinput):
            raise ValueError("`paramsinput` is not a valid file path.")

        if not path.isfile(self.orbinfile):
            raise ValueError("`orbinfile` is not a valid file path.")

        if self.oifoutput and not path.isfile(self.oifoutput):
            raise ValueError("`oifoutput` is not a valid file path.")

        if not path.isfile(self.configfile):
            raise ValueError("`configfile` is not a valid file path.")

        if not path.isfile(self.pointing_database):
            raise ValueError("`pointing_database` is not a valid file path.")

        if self.ar_data_file_path and not path.isdir(self.ar_data_file_path):
            raise ValueError("`ar_data_path` is not a valid directory.")
