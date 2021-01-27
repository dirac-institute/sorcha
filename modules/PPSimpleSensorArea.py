"""
Remove a portion of the observations to simulate the losses due to gaps between
CCD chips and rafts on the sensor. 
"""

# Numpy 
import numpy as np
# Pandas
import pandas as pd

#------------------------------------------------------------------------------

def filterSimpleSensorArea(ephemsdf, fillfactor=0.9):

        '''Randomly removes a number of observations proportional to the
        fraction of the field not covered by the detector.

        Parameters
        ----------
        ephemsdf   ... pandas dataFrame containing observations
        fillfactor ... fraction of FOV covered by the sensor

        Returns
        -------
        ephemsOut  ... pandas dataFrame

        '''
        n = len(ephemsdf)
        ramdomNum = np.random.random(n)
        fillArray = np.zeros(n) + fillfactor
        dropObs = np.where(ramdomNum > fillArray)[0]

        ephemsOut = ephemsdf.drop(dropObs)
        ephemsOut = ephemsOut.reset_index(drop=True)

        return ephemsOut
#------------------------------------------------------------------------------