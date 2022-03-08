#!/usr/bin/python

from . import PPhookBrightnessWithColour, PPCalculateApparentMagnitudeInFilter, PPMatchPointingsAndColours
import logging
import pandas as pd


def PPCalculateApparentMagnitude(observations, phasefunction, mainfilter, othercolours, resfilters, filterpointing):

    """
    PPCalculateApparentMagnitude(observations, phasefunction, mainfilter, othercolours, resfilters, filterpointing)
    
    This task combines calculating the apparent magnitude in the main filter, combining the brightness information with
    colours for appropriate filter, and then, finally, selecting the correct colour and applying the correct offset.
 
    Input: observations   : pandas DataFrame
           phasefunction  : string
           mainfilter     : string
           othercolours   : array of strings
           resfilters     : array of strings
           filterpointing : string
   
    Output: observations: amended pandas DataFrame
 
    Usage: observations=PPCalculateApparentMagnitude(observations, phasefunction, mainfilter, othercolours, resfilters, filterpointing)
    """
    
    pplogger = logging.getLogger(__name__)
 
    pplogger.info('Calculating apparent magnitudes...')
    observations=PPCalculateApparentMagnitudeInFilter.PPCalculateApparentMagnitudeInFilter(observations, phasefunction, mainfilter)        
    

    
    pplogger.info('Hooking colour and brightness information...')
    i=0
    while (i<len(othercolours)):
         observations=PPhookBrightnessWithColour.PPhookBrightnessWithColour(observations, mainfilter, othercolours[i], resfilters[i+1])         
         i=i+1
 
    observations=observations.reset_index(drop=True)

    
    pplogger.info('Resolving the apparent brightness in a given optical filter corresponding to the pointing...')
    observations=PPMatchPointingsAndColours.PPMatchPointingsAndColours(observations,filterpointing)
    
    return observations
