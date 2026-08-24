import sqlite3
import pandas as pd
import logging
import sys


def PPReadPointingDatabase(bsdbname, observing_filters, dbquery, per_obs_fading_function_on=None):
    """
    Reads in the pointing database as a Pandas dataframe.

    Parameters
    -----------
    bsdbname : string
        File location of pointing database.

    observing_filters : list of strings
        List of observation filters of interest.

    dbquery : string
        Databse query to perform on pointing database.


    Returns
    -----------
    dfo : pandas dataframe
        Dataframe of pointing database.

    """

    pplogger = logging.getLogger(__name__)

    con = sqlite3.connect("file:" + bsdbname + "?mode=ro", uri=True)

    try:
        df = pd.read_sql_query(dbquery, con)
    except pd.errors.DatabaseError:
        pplogger.error(
            "ERROR: PPReadPointingDatabase: SQL query on pointing database failed. Check that the query is correct in the config file."
        )
        sys.exit(
            "ERROR: PPReadPointingDatabase: SQL query on pointing database failed. Check that the query is correct in the config file."
        )
    except Exception as e:  # pragma: no cover
        pplogger.error(f"ERROR: PPReadPointingDatabase: error reading from pointing database: {e}")
        sys.exit(f"ERROR: PPReadPointingDatabase: error reading from pointing database: {e}")

    df["observationId_"] = df["observationId"]
    df = df.rename(columns={"observationId": "FieldID"})
    df = df.rename(columns={"filter": "optFilter"})  # not to confuse with the pandas filter command
    df["optFilter"] = df["optFilter"].astype("category")  # save memory

    dfo = df[df.optFilter.isin(observing_filters)].copy()
    if dfo.empty:
        pplogger.error(
            "No detections with config file filters in the pointing db. check your specifying the right column for your filters."
        )
        sys.exit(
            "No detections with config file filters in the pointing db. check your specifying the right column for your filters."
        )
    # at the moment the RubinSim pointing databases don't record the observation
    # midpoint and the opposite for DES, so we calculate the missing column. Depending on what we are given
    # we calculate the opposite

    if "observationMidpointMJD_TAI" not in dfo.columns:
        dfo["observationMidpointMJD_TAI"] = dfo["observationStartMJD_TAI"] + (
            (dfo["visitTime"] / 2.0) / 86400.0
        )
    elif "observationStartMJD_TAI" not in dfo.columns:
        dfo["observationStartMJD_TAI"] = dfo["observationMidpointMJD_TAI"] - (
            (dfo["visitExposureTime"] / 2.0) / 86400.0
        )
    else:
        pplogger.error(
            "ERROR: PPReadPointingDatabase: column name observationMidpointMJD_TAI or observationStartMJD_TAI missing from pointing query."
        )
        sys.exit(
            "ERROR: PPReadPointingDatabase: column name observationMidpointMJD_TAI or observationStartMJD_TAI missing from pointing query."
        )
    print(per_obs_fading_function_on)
    if per_obs_fading_function_on:
        missing_cols = [col for col in ["c", "k"] if col not in dfo.columns]

        if missing_cols:
            pplogger.error(
                f"ERROR: Fading Function has been turned on for DES but the following columns are missing "
                f"from the pointing database: {', '.join(missing_cols)}."
            )
            sys.exit(
                f"ERROR: Fading Function has been turned on for DES but the following columns are missing "
                f"from the pointing database: {', '.join(missing_cols)}."
            )

        if dfo[["c", "k"]].isnull().any().any():
            pplogger.error(
                "ERROR: Fading Function has been turned on for DES but some values for scaling factor 'c' "
                "and/or transition sharpness 'k' are missing in the pointing database."
            )
            sys.exit(
                "ERROR: Fading Function has been turned on for DES but some values for scaling factor 'c' "
                "and/or transition sharpness 'k' are missing in the pointing database."
            )
    return dfo
