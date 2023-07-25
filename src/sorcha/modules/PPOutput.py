import pandas as pd
import os
import sqlite3
import logging


def PPOutWriteCSV(padain, outf):
    """
    Writes a pandas dataframe out to a CSV file at a location given by the user.

    Parameters:
    -----------
    padain (Pandas dataframe): dataframe of output.

    outf (string): location to which file should be written.

    Returns:
    -----------
    None.

    """

    padain = padain.to_csv(path_or_buf=outf, mode="a", header=not os.path.exists(outf), index=False)

    return


def PPOutWriteHDF5(pp_results, outf, keyin):
    """
    Writes a pandas dataframe out to a HDF5 file at a location given by the user.

    Parameters:
    -----------
    padain (Pandas dataframe): dataframe of output.

    outf (string): location to which file should be written.

    keyin (string): key at which data will be located.

    Returns:
    -----------
    None.

    """

    of = pp_results.to_hdf(outf, mode="a", format="table", append=True, key=keyin)

    return of


def PPOutWriteSqlite3(pp_results, outf):
    """
    Writes a pandas dataframe out to a CSV file at a location given by the user.

    Parameters:
    -----------
    pp_results (Pandas dataframe): dataframe of output.

    outf (string): location to which file should be written.

    Returns:
    -----------
    None.

    """

    pp_results = pp_results.drop("level_0", axis=1, errors="ignore")

    cnx = sqlite3.connect(outf)

    pp_results.to_sql("pp_results", con=cnx, if_exists="append", index=False)


def PPWriteOutput(cmd_args, configs, observations_in, endChunk=0, verbose=False):
    """
    Writes the output in the format specified in the config file to a location
    specified by the user.

    Parameters:
    -----------
    cmd_args (dictionary): dictonary of command line arguments.

    configs (dictionary): dictionary of config file arguments.

    observations_in (Pandas dataframe): dataframe of output.

    endChunk (int): integer of last object in chunk. Used only for HDF5 output key.

    verbose (Boolean): verbose mode on or off.

    Returns:
    -----------
    None.

    """

    pplogger = logging.getLogger(__name__)
    verboselog = pplogger.info if verbose else lambda *a, **k: None

    if configs["output_size"] == "basic":
        observations = observations_in.copy()[
            [
                "ObjID",
                "FieldMJD",
                "fieldRA",
                "fieldDec",
                "AstRA(deg)",
                "AstDec(deg)",
                "AstrometricSigma(deg)",
                "optFilter",
                "observedPSFMag",
                "observedTrailedSourceMag",
                "PhotometricSigmaPSF(mag)",
                "PhotometricSigmaTrailedSource(mag)",
                "fiveSigmaDepth",
                "fiveSigmaDepthAtSource",
            ]
        ]
    elif configs["output_size"] == "all":
        observations = observations_in.copy()

    observations["FieldMJD"] = observations["FieldMJD"].round(decimals=5)

    for position_col in ["fieldRA", "fieldDec", "AstRA(deg)", "AstDec(deg)", "AstrometricSigma(deg)"]:
        observations[position_col] = observations[position_col].round(decimals=configs["position_decimals"])

    for magnitude_col in [
        "observedPSFMag",
        "observedTrailedSourceMag",
        "PhotometricSigmaPSF(mag)",
        "PhotometricSigmaTrailedSource(mag)",
        "fiveSigmaDepth",
        "fiveSigmaDepthAtSource",
    ]:
        observations[magnitude_col] = observations[magnitude_col].round(
            decimals=configs["magnitude_decimals"]
        )

    verboselog("Constructing output path...")

    if configs["output_format"] == "csv":
        outputsuffix = ".csv"
        out = os.path.join(cmd_args.outpath, cmd_args.outfilestem + outputsuffix)
        verboselog("Output to CSV file...")
        observations = PPOutWriteCSV(observations, out)

    elif configs["output_format"] == "separatelycsv":
        outputsuffix = ".csv"
        objid_list = observations["ObjID"].unique().tolist()
        verboselog("Output to " + str(len(objid_list)) + " separate output CSV files...")

        i = 0
        while i < len(objid_list):
            single_object_df = pd.DataFrame(observations[observations["ObjID"] == objid_list[i]])
            out = os.path.join(
                cmd_args.outpath, str(objid_list[i]) + "_" + cmd_args.outfilestem + outputsuffix
            )
            observations = PPOutWriteCSV(single_object_df, out)
            i = i + 1

    elif configs["output_format"] == "sqlite3":
        outputsuffix = ".db"
        out = os.path.join(cmd_args.outpath, cmd_args.outfilestem + outputsuffix)
        verboselog("Output to sqlite3 database...")
        observations = PPOutWriteSqlite3(observations, out)

    elif configs["output_format"] == "hdf5" or configs["output_format"] == "h5":
        outputsuffix = ".h5"
        out = os.path.join(cmd_args.outpath, cmd_args.outfilestem + outputsuffix)
        verboselog("Output to HDF5 binary file...")
        observations = PPOutWriteHDF5(observations, out, str(endChunk))
