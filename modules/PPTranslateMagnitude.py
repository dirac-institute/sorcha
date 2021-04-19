import pandas as pd
import numpy as np

__all__=['PPTranslateMagnitude']

def PPTranslateMagnitude(oif_output, survey_db, colors,
                         oifFieldIDName='FieldID', surveyFieldIDName='observationId',
                         surveyFilterName='filter',
                         oifObjIDName='objID', colorsObjIDName='ObjID',
                         oif_filter='V'
                         ):
    """
    Uses filter and color information from survey and color tables
    to translate V band magnitude to appropriate sdss filter magnitude.
    
    Input
    -----
    oif_output   ...   pandas table containing output of objectsInField simulator
    survey_db    ...   pandas table containing field conditions for each observation
    colors       ...   pandas table containing color difference between V band 
                       appropriate filter bands for each object.
                       
    Returns
    -------
    MaginFil     ...   pandas series containing translated magnitudes
    """
    
    l = len(oif_output.index)
    obs_filter = survey_db.lookup(oif_output[oifFieldIDName], [surveyFilterName]*l)
    obs_color  = colors.set_index(colorsObjIDName).lookup(oif_output[colorsObjIDName], oif_filter+'-'+obs_filter)
    
    return (oif_output[oif_filter] - obs_color)