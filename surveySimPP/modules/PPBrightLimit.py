#!/usr/bin/python

# Author: Grigori Fedorets

def PPBrightLimit(padain, brlimit):

    """
    Task: PPBrightLimit

    Description: Goes through every row in pandas dataframe and drops lines the ColinFil
    of which is brighter than the defined magnitude.


    Input: padain: pandas dataframe
    upperlimit: float, upper limit for ColinFil column value in padain dataframe


    Output: pandas dataframe (modified)


    """
    padain = padain.drop(padain[padain.TrailedSourceMag < brlimit].index)
    padain.reset_index(drop=True, inplace=True)

    return padain
