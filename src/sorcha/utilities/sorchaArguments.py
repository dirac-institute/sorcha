import numpy as np
from dataclasses import dataclass
import time
from os import path


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

    makeTemporaryEphemerisDatabase: bool = False
    """whether or not to make ephemeris database"""
    readTemporaryEphemerisDatabase = False
    """path to ephemeris database or `False`"""
    deleteTemporaryEphemerisDatabase: bool = False
    """whether or not to delete ephemeris database"""

    surveyname: str = ""
    """name of the survey (`lsst` is only one implemented currently)"""

    complex_parameters: str = ""
    """optional, extra complex physical parameter input files"""

    _rng = np.random.default_rng(int(time.time()))
    """
    DO NOT CHANGE THIS UNLESS YOU ARE A MEMBER OF THE DEVELOPMENT TEAM
    FOR TESTING PURPOSES ONLY
    CHANGING THE RNG SEED COULD INVALIDATE ANY SCIENCE RESULTS GAINED FROM SORCHA
    THIS IS NOT A PLACE OF HONOR
    """

    def __init__(self, cmd_args_dict=None):
        if cmd_args_dict is not None:
            self.read_from_dict(cmd_args_dict)

    def read_from_dict(self, args):
        """set the parameters from a cmd_args dict."""
        self.paramsinput = args["paramsinput"]
        self.orbinfile = args["orbinfile"]
        self.oifoutput = args["oifoutput"]
        self.configfile = args["configfile"]
        self.outpath = args["outpath"]
        self.outfilestem = args["outfilestem"]
        self.pointing_database = args["pointing_database"]

        self.verbose = args["verbose"]

        self.makeTemporaryEphemerisDatabase = args["makeTemporaryEphemerisDatabase"]
        self.readTemporaryEphemerisDatabase = args["readTemporaryEphemerisDatabase"]
        self.deleteTemporaryEphemerisDatabase = args["deleteTemporaryEphemerisDatabase"]

        self.surveyname = args["surveyname"]

        if "complex_physical_parameters" in args.keys():
            self.complex_parameters = args["complex_physical_parameters"]

    def validate_arguments(self):
        if not path.isfile(self.paramsinput):
            raise ValueError("`paramsinput` is not a valid file path.")

        if not path.isfile(self.orbinfile):
            raise ValueError("`orbinfile` is not a valid file path.")

        if not path.isfile(self.oifoutput):
            raise ValueError("`oifoutput` is not a valid file path.")

        if not path.isfile(self.configfile):
            raise ValueError("`configfile` is not a valid file path.")

        if not path.isfile(self.pointing_database):
            raise ValueError("`pointing_database` is not a valid file path.")
