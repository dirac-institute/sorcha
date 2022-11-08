#!/usr/bin/python

from .PPCalculateApparentMagnitudeInFilter import PPCalculateApparentMagnitudeInFilter
from .PPCalculateSimpleCometaryMagnitude import PPCalculateSimpleCometaryMagnitude
from .PPApplyColourOffsets import PPApplyColourOffsets
import logging

# Author: Steph Merritt


def PPCalculateApparentMagnitude(observations, phasefunction, mainfilter, othercolours, observing_filters, object_type, verbose=False):

    """
    PPNewCalculateApparentMagnitude(observations, phasefunction, mainfilter, othercolours, observing_filters)

    This task applies the correct colour offset to H for the relevant filter, checks to make sure
    the correct columns are included (with additional functionality for colour-specific phase curves),
    then calculates the apparent magnitude.

    Input: observations   : pandas DataFrame
           phasefunction  : string
           mainfilter     : string
           othercolours   : array of strings
           observing_filters     : array of strings

    Output: observations: amended pandas DataFrame

    Usage: observations=PPCalculateApparentMagnitude(observations, phasefunction, mainfilter, othercolours, observing_filters)
    """

    pplogger = logging.getLogger(__name__)
    verboselog = pplogger.info if verbose else lambda *a, **k: None

    if (object_type == 'comet'):
        verboselog('Calculating cometary magnitude using a simple model and applying colour offset...')
        observations = PPCalculateSimpleCometaryMagnitude(observations, mainfilter, othercolours)
    else:
        verboselog('Selecting and applying correct colour offset...')
        observations = PPApplyColourOffsets(observations, phasefunction, othercolours, observing_filters, mainfilter)

        verboselog('Calculating apparent magnitude in filter...')
        observations = PPCalculateApparentMagnitudeInFilter(observations, phasefunction)

    return observations
