#!/usr/bin/python




import pandas as pd
import random
import sys

def PPhookBrightnessWithColour(padain, initfilter, colour, resfilter):
    """
    Task: PPHookBrightnessWithColour
    
    Input: padain: combined pandas dataframe, including objectsInField (oif) and colours
           in the 'col-X format'. 
           
           initfilter (string): designation of column which contains the apparent brightness of
           the object. The brightness is given in a specific filter.
           
           colour (string): designation of column which contains the colour in the 'col1-col2' format,
           for example 'r-i' or 'r-X'. By default, it is assumed that the H colours are
           defined in the r filter.
           
           resfilter (string): the resulting filter, in which the apparent brightness will be given.
    
    Action: Goes through every row in pandas dataframe and adds up the values in the columns 
    'initfilter' and 'colour', and adds a new column 'resfilter' with 
    
    Output: the input pandas dataframe (modified), amended with the new column, including
    the apparent brightnesses in the given 'resfilter' filter. 
    
    Author: Grigori Fedorets

    Usage: pphookbrightnesswithcolour(combdf, 'r', 'i-r', 'i')
    """
    padaout=padain
    padaout[resfilter] = padain[colour] + padain[initfilter]
    return padaout
    