#!/usr/bin/python

import numpy as np

# Author: Grigori Fedorets, Meg Schwamb


def PPResolveMagnitudeInFilter(padain, mainfilter, othercolours, observing_filters):
    """
    PPResolveMagnitudeInFilter.py

    Description: This tasks selects a colour offset relevant to each filter at each given pointing
    and calculates the colour in each given filter. The apparent magnitude has already been
    calculated in the main filter.


    Mandatory input: string, padain, name of input pandas dataframe
                     string, mainfilter, name of the main filter in which the apparent magnitude has been calculated
                     array of strings, othercolours, names of colour offsets (e.g. r-i)
                     array of strings, observing_filters, names of resulting colours, main filter is the first one, followed
                     in order by resolved colours, such as, e.g. 'r'+'g-r'='g'. They should be given in the following order:
                     main filter, resolved filters in the same order as respective other colours.

    Output: updated padain

    Usage: padaout=PPResolveMagnitudeInFilter(padain,mainfilter,othercolours,observing_filters)

    """

    apparent_mag = np.zeros(len(padain), dtype=float)

    # for cases where the input filter is the main filter
    inRelevantFilterList = (padain['optFilter'] == mainfilter)
    inRelevantFilter = padain[inRelevantFilterList]
    if(len(inRelevantFilter) > 0):
        apparent_mag[inRelevantFilterList] = 0.0

    # for all other cases, where the offset is required
    for i in np.arange(len(othercolours)):
        inRelevantFilterList = (padain['optFilter'] == observing_filters[i + 1])
        inRelevantFilter = padain[inRelevantFilterList]
        if(len(inRelevantFilter) > 0):
            apparent_mag[inRelevantFilterList] = inRelevantFilter[othercolours[i]]

    padain['TrailedSourceMag'] = padain[mainfilter] + apparent_mag

    return padain
