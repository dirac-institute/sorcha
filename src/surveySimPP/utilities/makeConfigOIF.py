import configparser
import argparse
import pandas as pd
import numpy as np
import os
import sqlite3 as sql
import sys


def makeConfig(args):
    """
    Makes an OIF config file from the variables defined at the command line.

    Parameters:
    -----------
    args (argparse ArgumentParser object): command line arguments.

    Returns:
    -----------
    None.

    """

    # grab defaults from a template config file
    config = configparser.ConfigParser()

    # get database info
    con = sql.connect(args.pointing)
    database = pd.read_sql_query(args.query, con)
    # maxFields = len(database.index)

    # get what dates to check in database
    survey_days = database["observationStartMJD"].astype(int).unique()

    day1 = survey_days[args.day1 - 1]

    # get the final day and the total number of days to run over
    if (args.ndays == -1) or (args.ndays + args.day1 >= survey_days.iloc[-1]):
        dayf = survey_days[-1]
        ndays = int(np.floor(survey_days[-1] - day1) + 1)
    else:
        dayf = day1 + args.ndays
        ndays = args.ndays

    # get range of fields for those days
    field1 = database.loc[(database["observationStartMJD"] - day1) < 1.0]["observationId"].iloc[0]
    fieldf = database.loc[(database["observationStartMJD"] - dayf) < 2.0]["observationId"].iloc[
        -1
    ]  # this will likely overshoot a little bit

    # do stuff for parellizing

    if args.inputformat == "whitespace":
        orbits = pd.read_csv(args.o, delim_whitespace=True)
    else:
        orbits = pd.read_csv(args.o)

    nOrbitsTotal = len(orbits.index)
    nOrbitsPerFile = args.no
    remainder = nOrbitsTotal % nOrbitsPerFile

    if nOrbitsPerFile == -1:
        nOrbitsPerFile = nOrbitsTotal
        startingOrbits = [1]
    else:
        if nOrbitsTotal % nOrbitsPerFile == 0:
            startingOrbits = (
                np.linspace(0, nOrbitsTotal - nOrbitsPerFile, nOrbitsTotal // nOrbitsPerFile, dtype=int) + 1
            )
        else:
            startingOrbits = (
                np.linspace(
                    0,
                    nOrbitsTotal - nOrbitsTotal % nOrbitsPerFile,
                    nOrbitsTotal // nOrbitsPerFile + 1,
                    dtype=int,
                )
                + 1
            )

    orbitsName = args.o.split("/")[-1].split(".")[0]

    m = len(startingOrbits)
    for i in range(m):
        if (i == (m - 1)) and (remainder != 0):
            nOrbits = remainder
        else:
            nOrbits = nOrbitsPerFile

        config.read_dict(
            {
                "CONF": {
                    "Cache dir": args.cache
                    + "/"
                    + orbitsName
                    + "/"
                    + str(startingOrbits[i])
                    + "-"
                    + str(nOrbits),  # Directory where to place generated temporary files
                },
                "ASTEROID": {
                    "population model": args.o,
                    "SPK T0": str(day1 - 30),
                    "nDays": str(ndays + 30),
                    "Object1": str(startingOrbits[i]),
                    "nObjects": str(nOrbits),
                    "SPK step": str(args.spkstep),
                    "nbody": "T",
                    "input format": args.inputformat,
                },
                "SURVEY": {
                    "Survey database": args.pointing,
                    "Field1": str(field1 + 1),
                    "nFields": str(fieldf - field1),
                    "MPCobscode file": args.mpcfile,
                    "Telescope": args.telescope,
                    "Surveydbquery": args.query,
                },
                "CAMERA": {
                    "Threshold": "5",
                    "Camera": args.camerafov,
                },
                "OUTPUT": {"Output file": "stdout", "Output format": "csv"},
            }
        )

        ndigits = len(str(len(orbits.index)))

        print(
            os.path.join(
                args.prefix,
                orbitsName
                + "-"
                + str(startingOrbits[i]).zfill(ndigits)
                + "-"
                + str(startingOrbits[i] + nOrbits - 1).zfill(ndigits)
                + ".ini",
            )
        )

        with open(
            os.path.join(
                args.prefix,
                orbitsName
                + "-"
                + str(startingOrbits[i]).zfill(ndigits)
                + "-"
                + str(startingOrbits[i] + nOrbits - 1).zfill(ndigits)
                + ".ini",
            ),
            "w",
        ) as file:
            config.write(file)


def main():
    """
    Creates an OIF config file from variables defined at the command line.

    usage: makeConfigOIF [-h] [-no NO] [-ndays NDAYS] [-day1 DAY1] [-prefix PREFIX] [-camerafov CAMERAFOV] [-inputformat INPUTFORMAT] [-cache CACHE] [-mpcfile MPCFILE]
                     [-spkstep SPKSTEP] [-telescope TELESCOPE] [-query QUERY]
                     o pointing
        positional arguments:
          o                     orbits file
          pointing              pointing database
        arguments:
          -h, --help                show this help message and exit
          -no NO                    number of orbits per config file, -1 runs all the orbits in one config file. Default value = 300
          -ndays NDAYS              number of days in survey to run, -1 runs entire survey. Default value = -1
          -day1 DAY1                first day in survey to run. Default value = 1
          -prefix PREFIX            config file name prefix, Default value is an empty string
          -camerafov CAMERAFOV      path and file name of the camera fov. Default value = instrument_polygon.dat
          -inputformat INPUTFORMAT  input format (CSV or whitespace). Default value = whitespace
          -cache CACHE              base cache directory name. Default value = _cache
          -mpcfile MPCFILE          name of the file containing the MPC observatory codes. Default value = obslist.dat
          -spkstep SPKSTEP          Integration step in days. Default value = 30
          -telescope TELESCOPE      Observatory MPC Code. Default value = I11 (Gemini South to be changed to Rubin Observatory)
          -query QUERY              SQL query for pointing database.

    """

    parser = argparse.ArgumentParser(description="creating config file(s) for Objects in Field")
    parser.add_argument("o", help="orbits file", type=str)
    parser.add_argument("pointing", help="pointing database", type=str)
    parser.add_argument(
        "-no",
        help="number of orbits per config file, -1 runs all the orbits in one config file. Default value = 300",
        type=int,
        default=300,
    )
    parser.add_argument(
        "-ndays",
        help="number of days in survey to run, -1 runs entire survey. Default value = -1",
        type=int,
        default=-1,
    )
    parser.add_argument("-day1", help="first day in survey to run. Default value = 1", type=int, default=1)
    parser.add_argument(
        "-prefix", help="config file name prefix, Default value is an empty string", type=str, default=""
    )
    parser.add_argument(
        "-camerafov",
        help="path and file name of the camera fov. Default value = instrument_polygon.dat",
        type=str,
        default="instrument_polygon.dat",
    )
    parser.add_argument(
        "-inputformat",
        help="input format (CSV or whitespace). Default value = whitespace",
        type=str,
        default="whitespace",
    )
    parser.add_argument(
        "-cache", help="base cache directory name. Default value = _cache", type=str, default="_cache"
    )
    parser.add_argument(
        "-mpcfile",
        help="name of the file containing the MPC observatory codes. Default value = obslist.dat",
        type=str,
        default="obslist.dat",
    )
    parser.add_argument("-spkstep", help="Integration step in days. Default value = 30", type=int, default=30)
    parser.add_argument(
        "-telescope",
        help="Observatory MPC Code. Default value = I11 (Gemini South to be changed to Rubin Observatory)",
        type=str,
        default="I11",
    )
    parser.add_argument(
        "-query",
        help="SQL query for pointing database.",
        type=str,
        default="SELECT observationId,observationStartMJD,fieldRA,fieldDEC,rotSkyPos FROM observations order by observationStartMJD",
    )

    args = parser.parse_args()

    # error checks that optional inputs are within the right range

    if (args.inputformat != "whitespace") and (args.inputformat != "CSV"):
        sys.exit(
            "ERROR: Invalid option for input format of the orbits file.  Try --help to see the command line options"
        )

    if args.no < -1:
        sys.exit(
            "ERROR: Invalid option for number of orbits per config file.  Try --help to see the command line options"
        )

    if args.day1 < 1:
        sys.exit(
            "ERROR: Invalid option for first day in survey to run.  Try --help to see the command line options"
        )

    if (args.ndays == 0) or (args.ndays < -1):
        sys.exit(
            "ERROR: Invalid option for number of days in survey to run.  Try --help to see the command line options"
        )

    # make config file
    makeConfig(args)


if __name__ == "__main__":
    main()
