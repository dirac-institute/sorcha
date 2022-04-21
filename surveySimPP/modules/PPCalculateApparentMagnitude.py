#!/usr/bin/python

from . import PPCalculateApparentMagnitudeInFilter, PPResolveMagnitudeInFilter
from . import PPCalculateSimpleCometaryMagnitude
import logging
import pandas as pd

# Author: Grigori Fedorets

def PPCalculateApparentMagnitude(observations, phasefunction, mainfilter, othercolours, observing_filters, object_type):

    """
    PPCalculateApparentMagnitude(observations, phasefunction, mainfilter, othercolours, observing_filters)
    
    This task combines calculating the apparent magnitude in the main filter, combining the brightness information with
    colours for appropriate filter, and then, finally, selecting the correct colour and applying the correct offset.
 
    Input: observations   : pandas DataFrame
           phasefunction  : string
           mainfilter     : string
           othercolours   : array of strings
           observing_filters     : array of strings
   
    Output: observations: amended pandas DataFrame
 
    Usage: observations=PPCalculateApparentMagnitude(observations, phasefunction, mainfilter, othercolours, observing_filters)
    """
    
    pplogger = logging.getLogger(__name__)
 
    pplogger.info('Calculating apparent magnitudes...')
    observations=PPCalculateApparentMagnitudeInFilter.PPCalculateApparentMagnitudeInFilter(observations, phasefunction, mainfilter)
    
    if (object_type =='comet'):
         pplogger.info('Calculating cometary magnitude using a simple model...')
         observations=PPCalculateSimpleCometaryMagnitude.PPCalculateSimpleCometaryMagnitude(observations, mainfilter)         
    
    pplogger.info('Selecting and applying correct colour offset...')
    observations=PPResolveMagnitudeInFilter.PPResolveMagnitudeInFilter(observations,mainfilter,othercolours,observing_filters)
    
    observations_drop = observations.drop(mainfilter, axis=1)
    observations_drop.reset_index(drop=True, inplace=True)
    
    return observations_drop
