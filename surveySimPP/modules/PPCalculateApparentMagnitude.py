#!/usr/bin/python

from . import PPCalculateApparentMagnitudeInFilter, PPResolveMagnitudeInFilter
import logging
import pandas as pd

# Author: Grigori Fedorets

def PPCalculateApparentMagnitude(observations, phasefunction, mainfilter, othercolours, resfilters):

    """
    PPCalculateApparentMagnitude(observations, phasefunction, mainfilter, othercolours, resfilters)
    
    This task combines calculating the apparent magnitude in the main filter, combining the brightness information with
    colours for appropriate filter, and then, finally, selecting the correct colour and applying the correct offset.
 
    Input: observations   : pandas DataFrame
           phasefunction  : string
           mainfilter     : string
           othercolours   : array of strings
           resfilters     : array of strings
   
    Output: observations: amended pandas DataFrame
 
    Usage: observations=PPCalculateApparentMagnitude(observations, phasefunction, mainfilter, othercolours, resfilters)
    """
    
    pplogger = logging.getLogger(__name__)
 
    pplogger.info('Calculating apparent magnitudes...')
    observations=PPCalculateApparentMagnitudeInFilter.PPCalculateApparentMagnitudeInFilter(observations, phasefunction, mainfilter)        
    
    pplogger.info('Selecting and applying correct colour offset...')
    observations=PPResolveMagnitudeInFilter.PPResolveMagnitudeInFilter(observations,mainfilter,othercolours,resfilters)
    
    return observations
