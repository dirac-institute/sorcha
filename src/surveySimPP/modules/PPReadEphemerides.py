import sys
import logging
from . import PPReadOif


def PPReadEphemerides(eph_output, ephemerides_type, inputformat):
    """
    Reads in the ephemerides as output by simulation (whether OIF or otherwise).
    The type of ephemerides is assigned in the PPConfig.ini file.

    For correct performance, the read-in data needs to contain all of the following columns:

    ['ObjID', 'FieldID', 'FieldMJD', 'AstRange(km)', 'AstRangeRate(km/s)', 'AstRA(deg)',
    'AstRARate(deg/day)', 'AstDec(deg)', 'AstDecRate(deg/day)', 'Ast-Sun(J2000x)(km)', 'Ast-Sun(J2000y)(km)',
    'Ast-Sun(J2000z)(km)', 'Ast-Sun(J2000vx)(km/s)', 'Ast-Sun(J2000vy)(km/s)', 'Ast-Sun(J2000vz)(km/s)',
    'Obs-Sun(J2000x)(km)', 'Obs-Sun(J2000y)(km)', 'Obs-Sun(J2000z)(km)', 'Obs-Sun(J2000vx)(km/s)',
    'Obs-Sun(J2000vy)(km/s)', 'Obs-Sun(J2000vz)(km/s)', 'Sun-Ast-Obs(deg)']

    Parameters:
    -----------
    eph_output (string): location/name of ephemerides output file.

    ephemerides_type (string): type of ephemerides pointing simulation. Currently only
    "oif" allowed.

    inputformat (string): format of input file ("whitespace"/"comma"/"csv"/"h5"/"hdf5").

    Returns:
    -----------
    padafr (Pandas dataframe): dataframe of ephemerides simulation data.

    """

    pplogger = logging.getLogger(__name__)

    ephtypeci = ephemerides_type.casefold()

    if ephtypeci == "oif":
        padafr = PPReadOif.PPReadOif(eph_output, inputformat)
    else:
        pplogger.error("PPReadEphemerides: invalid value for ephemerides_type: " + str(ephemerides_type))
        sys.exit("PPReadEphemerides: invalid value for ephemerides_type: " + str(ephemerides_type))

    # Functions for adding alternative types of ephemerides can be added here
    # See below for self-explanatory columns required for the ephemerides input

    # check the necessary columns exist

    cols = [
        "ObjID",
        "FieldID",
        "FieldMJD",
        "AstRange(km)",
        "AstRangeRate(km/s)",
        "AstRA(deg)",
        "AstRARate(deg/day)",
        "AstDec(deg)",
        "AstDecRate(deg/day)",
        "Ast-Sun(J2000x)(km)",
        "Ast-Sun(J2000y)(km)",
        "Ast-Sun(J2000z)(km)",
        "Ast-Sun(J2000vx)(km/s)",
        "Ast-Sun(J2000vy)(km/s)",
        "Ast-Sun(J2000vz)(km/s)",
        "Obs-Sun(J2000x)(km)",
        "Obs-Sun(J2000y)(km)",
        "Obs-Sun(J2000z)(km)",
        "Obs-Sun(J2000vx)(km/s)",
        "Obs-Sun(J2000vy)(km/s)",
        "Obs-Sun(J2000vz)(km/s)",
        "Sun-Ast-Obs(deg)",
    ]

    if not all(col in padafr.columns for col in cols):
        pplogger.error(
            "ERROR: PPReadEphemerides: essential columns missing from ephemerides input. Required columns are: {}".format(
                cols
            )
        )
        sys.exit(
            "ERROR: PPReadEphemerides: essential columns missing from ephemerides input. Required columns are: {}".format(
                cols
            )
        )

    return padafr[cols]
