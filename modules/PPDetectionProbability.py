# Developed for the Vera C. Rubin Observatory/LSST Data Management System.
# This product includes software developed by the 
# Vera C. Rubin Observatory/LSST Project (https://www.lsst.org).
#
# Copyright 2020 University of Washington
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
Calculate probability of detection due to fading

"""
# Numpy 
import numpy as np
# Pandas
import pandas as pd
#Counter
from collections import Counter

from . import PPTrailingLoss

__all__ = ['calcDetectionProbability']


############################################
# MODULE SPECIFIC EXCEPTION
###########################################
class Error(Exception):
    """Vector module specific exception."""
    
    pass

#-----------------------------------------------------------------------------------------------
def calcDetectionProbability(mag, limmag, w):
        """ Find the probability of a detection given a visual magnitude, 
        limiting magnitude, and fillfactor, 
        determined by the fading function from Veres & Chesley (2017).

        Parameters
        ----------
        mag: float
                magnitude of object in filter used for that field
        limmag: float
                limiting magnitude of the field
	w: float
	        distribution parameter
        
	Returns
        -------
        P: float
            Probability of detection
        """
   
        P = 1 / (1 + np.exp((mag - limmag) / w))

        return P

#-----------------------------------------------------------------------------------------------

def filterFadingFunction(ephemsdf, obsdf,
                        magNameEph='Filtermag', obsIDNameEph='FieldID',
                        dRaNameEph='AstRARate(deg/day)', dDecNameEph='AstDecRate(deg/day)',
                        limMagName='fiveSigmaDepth', obsIDName='observationId', 
                        seeingName='seeingFwhmEff',
                        w=0.1):

        """Removes pointings from observation table based on a probabilistic 
        fading function, and adjusts magnitudes to reflect fading and trailing
        losses.

        Parameters
        ----------
        ephemsdf        ... Pandas dataFrame containing output of JPL ephemeris simulator
        obsdf           ... Pandas dataFrame containing survey simulator output such as LSST opsim
        *Name           ... relevant column names in obsdf
        *NameEph        ... relevant column names in ephemsdf
        fillFactor      ... fraction of FOV covered by the detector
        w               ... fading function width
        
        Returns
        -------
        ephemsOut       ... Pandas dataFrame containing rejected observations
        """

        ephemsdf.sort_values(by=[obsIDNameEph], inplace=True)
        ephemsdf.reset_index(drop=True, inplace=True)
        fieldIDs = set(ephemsdf[obsIDNameEph])
        fields   = obsdf.loc[obsdf[obsIDName].isin(fieldIDs)]

        limMag = []
        seeing = []
        count = Counter(ephemsdf[obsIDNameEph])
        for _, row in fields.iterrows():
                n = count[row[obsIDName]]
                limMag += n * [row[limMagName]]
                seeing += n * [row[seeingName]]
        
        limMag = np.array(limMag)
        seeing = np.array(seeing)

        #apply trailing losses
        obsMag = ephemsdf[magNameEph] + PPTrailingLoss.calcTrailingLoss(ephemsdf[dRaNameEph]/86400, ephemsdf[dDecNameEph]/86400, seeing)

        #calculate probability of detection
        probability = calcDetectionProbability(obsMag, limMag, w)

        #remove observations below limiting magnitude
        randomNum = np.random.random(len(ephemsdf))
        ephemsOut = ephemsdf[probability < randomNum]
        
        ephemsdf.drop(ephemsdf.index[probability < randomNum], inplace=True)
        
        return ephemsOut

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