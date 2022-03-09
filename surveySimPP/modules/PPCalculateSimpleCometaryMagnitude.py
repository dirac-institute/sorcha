#!/usr/bin/python

from lsstcomet import Comet
from math import sqrt
import pandas as pd
import numpy as np

# Author: Grigori Fedorets
# Using lsstcomet code my Mike Kelley
# (C)  LSST Solar System Scientific Collaboration 2019

def PPCalculateSimpleCometaryMagnitude(padain, mainfilter):
    """
    PPCalculateSimpleCometaryMagnitude.py
    
    Description: This task calculates the brightness of the comet at a given pointing
    according to a simple model by A'Hearn et al. (1984).
    
    The brightness is here calculated in the main filter, and the colour offset is
    applied later using the PPhookBrightnessWithColour function.
    
    Mandatory input:      string, padain, name of input pandas daraframe   
                          string, mainfilter, name of the main filter in which
                                  the brightness is calculated

    Output:               
      
    usage: padaout=PPCalculateSimpleCometaryMagnitude(padain) 
    
    
    """
    # calculate rho and delta in au
    padain['delta']=padain['AstRange(km)']/1.495978707e8
    padain['rho']=(padain['Ast-Sun(J2000x)(km)']*padain['Ast-Sun(J2000x)(km)'] 
               + padain['Ast-Sun(J2000y)(km)']*padain['Ast-Sun(J2000y)(km)']
               + padain['Ast-Sun(J2000z)(km)']*padain['Ast-Sun(J2000z)(km)']).pow(1./2)/1.495978707e8 


    com=Comet(Hv=padain[mainfilter], afrho1=padain.afrho1, q=padain.q, k=padain.k)

    g = {'rh': padain['rho'], 'delta': padain['delta'], 'phase': padain['Sun-Ast-Obs(deg)']}
    # Here, only the coma contribution is calculated in the main filter
    try:
        padain['coma']=com.mag(g, mainfilter, rap=1, nucleus=False)
    except:
        print(g)
    # The contribution of the nucleus is taken from the absolute brightness
    padain[mainfilter] = -2.5 * np.log10(10**(-0.4 * padain['coma']) + 10**(-0.4 * padain[mainfilter]))

    return padain


