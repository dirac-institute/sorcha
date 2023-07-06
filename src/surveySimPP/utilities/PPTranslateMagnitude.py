import pandas as pd
import numpy as np


def PPTranslateMagnitude(
    oif_output,
    survey_db,
    colors,
    oifFieldIDName="FieldID",
    surveyFieldIDName="observationId",
    surveyFilterName="filter",
    oifObjIDName="ObjID",
    colorsObjIDName="ObjID",
    oif_filter="V",
):
    """
    Uses filter and color information from survey and color tables
    to translate V band magnitude to appropriate sdss filter magnitude.

    Parameters:
    -----------
    oif_output (Pandas dataframe): dataframe containing output of objectsInField simulator

    survey_db (Pandas dataframe): dataframe of pointing database

    colors (Pandas dataframe):  dataframe containing color difference between V band
    appropriate filter bands for each object.

    *Name (strings): column names for field ID in OIf, field ID in the pointing database,
    the filters in the pointing database, the ObjectID in OIF and the ObjectID in the colours dataframe.

    oif_filter (string): The filter in which the magnitude is given in the OIF output.

    Returns:
    -----------
    MaginFil (Pandas series): series of translated magnitudes.

    """

    df = pd.merge(
        oif_output[[oifObjIDName, oifFieldIDName]],
        survey_db[[surveyFieldIDName, surveyFilterName]],
        left_on=oifFieldIDName,
        right_on=surveyFieldIDName,
        how="left",
    ).drop(columns=[surveyFieldIDName])

    df = pd.merge(df, colors, left_on=oifObjIDName, right_on=colorsObjIDName, how="left")

    df["filter diff name"] = oif_filter + "-" + df[surveyFilterName]
    idx, cols = pd.factorize(df["filter diff name"])

    filterDiff = df.reindex(cols, axis=1).to_numpy()[np.arange(len(df)), idx]

    return oif_output[oif_filter] - filterDiff
