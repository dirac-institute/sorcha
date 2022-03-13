#!/bin/python

import pandas as pd
import numpy as np
import random

#Author: Grigori Fedorets

def PPreadColoursUser(oif_out, colour, mean, stdev, indataf=None):
    """
    PPreadColoursUser.py
    
    
    Description: This task assigns a designated colour to each object in the
    input file and puts it into a
    single pandas dataframe for further use downstream by other tasks.
    Only one colour is assigned, for more colours, the user may run this
    function several times with different parameters.
    
    The user may decide to give a single colour, or a uniform distribution of 
    colours.
    In case of a single colour, the stdev parameter should be given as zero.
        
    The format of the colours is:
        
    id   colour1 colour2 etc
        
    The also may also wish to amend the existing dataFrame with colours with 
    another colour. In that case, duplicate ObjID columns will be removed.
        
    Mandatory input:      
    Output from objectsInField (oif) in text file
    colour (string)
    mean colour (float)
    standard deviation (float)
    existing colour dataframe (pandas dataFrame, optional)

    Output:               pandas dataframe
            
        
    usage: padafr=PPreadColoursUser(oif_out, 'g-X', 0.33, 0.01)
           pada3=PPreadColoursUser(pada1, 'r-X', 0.25, 0.00, indataf=pada2)
        
    """

    
    nr=oif_out.shape[0]
    
    new_padafr=oif_out[['ObjID']]
        
    clrsnp=np.random.random(size=nr)
    clrsnp=(clrsnp-0.5)*stdev+mean
    clrs=pd.DataFrame(clrsnp, columns=[colour])
    padafr=pd.concat([new_padafr,clrs], axis=1, sort=False)
    if indataf is not None:
        padafr=pd.concat([padafr,indataf], axis=1, sort=False)
        padafr=padafr.loc[:,~padafr.columns.duplicated()]
    
    
    return padafr
