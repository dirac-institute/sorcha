import sqlite3
import pandas as pd

from sorcha.modules.LoggingUtils import logErrorAndExit


def PPReadPointingDatabase(bsdbname, observing_filters, dbquery):
    """
    Reads in the pointing database as a Pandas dataframe.

    Parameters:
    -----------
    bsdbname (string): file location of pointing database.

    observing_filters (list of strings): list of observation filters of interest.

    dbquery (string): database query to perform on pointing database.

    Returns:
    -----------
    dfo (Pandas dataframe): dataframe of pointing database.

    """
    con = sqlite3.connect(bsdbname)

    try:
        df = pd.read_sql_query(dbquery, con)
    except Exception:
        logErrorAndExit(
            "ERROR: PPReadPointingDatabase: SQL query on pointing database failed. Check that the query is correct in the config file."
        )

    df["observationId_"] = df["observationId"]
    df = df.rename(columns={"observationId": "FieldID"})
    df = df.rename(columns={"filter": "optFilter"})  # not to confuse with the pandas filter command
    dfo = df[df.optFilter.isin(observing_filters)]

    return dfo
