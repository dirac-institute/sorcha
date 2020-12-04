import pandas as pd


def PPresolveFilters

"""
    Task: PPresolveFilters

    Input: pandas dataframe, including the objectsInField (format), amended with 
    filter information for each pointing, and colours calculated for each respective filter (that is,
    for example g or r, and not g-r and r-i). 
    
    
    Action: Reads in a pandas dataframe which contains the magnitude values in each given filter and
    the filters extracted from the pointing database. Then we match the derived colour
    to the existing filter, and write the matching magnitude into the new column, which is 
    called magInFilter.

    Output: pandas dataframe (modified, column magfilter added)

    Author: Grigori Fedorets
    
    usage: df=PPresolveFilters(df)
"""

    
    padain['magInFilter']== padain.apply(lambda x: x[x['filter']], axis=1)
    return padain

