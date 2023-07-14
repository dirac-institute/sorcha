import logging
import sys

from .PPCheckInputObjectIDs import PPCheckInputObjectIDs
from .PPReadTemporaryEphemerisDatabase import PPReadTemporaryEphemerisDatabase
from .PPJoinEphemeridesAndParameters import PPJoinEphemeridesAndParameters
from .PPJoinEphemeridesAndOrbits import PPJoinEphemeridesAndOrbits
from .PPMatchPointingToObservations import PPMatchPointingToObservations
from surveySimPP.readers.CSVReader import CSVDataReader
from surveySimPP.readers.OIFReader import OIFDataReader
from surveySimPP.readers.OrbitAuxReader import OrbitAuxReader


def PPReadAllInput(cmd_args, configs, filterpointing, startChunk, incrStep, verbose=True):
    """
    Reads in the simulation data and the orbit and physical parameter files, and then
    joins them with the pointing database to create a single Pandas dataframe of simulation
    data with all necessary orbit, physical parameter and pointing information.

    Parameters:
    -----------
    cmd_args (dictionary): dictonary of command line arguments.

    configs (dictionary): dictionary of config file arguments.

    filterpointing (Pandas dataframe): dataframe of pointing database.

    startChunk (int): object number at which chunk should start.

    incrStep (int): chunk size.

    verbose (Boolean): verbose mode on or off.

    Returns:
    -----------
    observations (Pandas dataframe): dataframe of all observations with orbital
    data, physical parameters and pointing information merged on.

    """

    pplogger = logging.getLogger(__name__)
    verboselog = pplogger.info if verbose else lambda *a, **k: None

    verboselog("Reading input orbit file: " + cmd_args["orbinfile"])
    orbit_reader = OrbitAuxReader(cmd_args["orbinfile"], configs["aux_format"])
    padaor = orbit_reader.read_rows(startChunk, incrStep)

    verboselog("Reading input physical parameters: " + cmd_args["paramsinput"])
    param_reader = CSVDataReader(cmd_args["paramsinput"], configs["aux_format"])
    padacl = param_reader.read_rows(startChunk, incrStep)

    if configs["comet_activity"] == "comet":
        verboselog("Reading cometary parameters: " + cmd_args["cometinput"])
        comet_reader = CSVDataReader(cmd_args["cometinput"], configs["aux_format"])
        padaco = comet_reader.read_rows(startChunk, incrStep)

    objid_list = padacl["ObjID"].unique().tolist()

    if cmd_args["makeTemporaryEphemerisDatabase"] or cmd_args["readTemporaryEphemerisDatabase"]:
        # read from temporary database
        verboselog("Reading from temporary ephemeris database.")
        padafr = PPReadTemporaryEphemerisDatabase(cmd_args["readTemporaryEphemerisDatabase"], objid_list)
    else:
        # TODO: Once more ephemerides_types are added this should be wrapped in a EphemerisDataReader
        # That does the selection and checks. We are holding off adding this level of indirection until there
        # is a second ephemerides_type.
        ephem_type = configs["ephemerides_type"]
        if ephem_type.casefold() != "oif":
            pplogger.error(f"PPReadAllInput: Unsupported value for ephemerides_type {ephem_type}")
            sys.exit(f"PPReadAllInput: Unsupported value for ephemerides_type {ephem_type}")

        try:
            verboselog("Reading input ephemerides from: " + cmd_args["oifoutput"])
            emphem_reader = OIFDataReader(cmd_args["oifoutput"], configs["eph_format"])

            # Read everything and filter on rows. Depending on the chunksize and filtering
            # we might want to use emphem_reader.read_objects().
            padafr = emphem_reader.read_rows()
            padafr = padafr[padafr["ObjID"].isin(objid_list)]

        except MemoryError:
            pplogger.error(
                "ERROR: insufficient memory. Try to run with -dw command line flag or reduce sizeSerialChunk."
            )
            sys.exit(
                "ERROR: insufficient memory. Try to run with -dw command line flag or reduce sizeSerialChunk."
            )

    verboselog(
        "Checking if object IDs in orbits, physical parameters and pointing simulation input files match..."
    )
    PPCheckInputObjectIDs(padaor, padacl, padafr)

    if configs["comet_activity"] == "comet":
        PPCheckInputObjectIDs(padaor, padaco, padafr)

    verboselog("Joining physical parameters and orbital data with simulation data...")
    observations = PPJoinEphemeridesAndParameters(padafr, padacl)
    observations = PPJoinEphemeridesAndOrbits(observations, padaor)
    if configs["comet_activity"] == "comet":
        verboselog("Joining cometary data...")
        observations = PPJoinEphemeridesAndParameters(observations, padaco)

    verboselog(
        "Joining info from pointing database with simulation data and dropping observations in non-requested filters..."
    )
    observations = PPMatchPointingToObservations(observations, filterpointing)

    return observations
