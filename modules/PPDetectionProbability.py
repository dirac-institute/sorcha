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

__all__ = ['PPDetectionProbability']


############################################
# MODULE SPECIFIC EXCEPTION
###########################################
class Error(Exception):
    """Vector module specific exception."""
    
    pass

#-----------------------------------------------------------------------------------------------
def calcDetectionProbability(mag, limmag, fillFactor=1.0, w=0.1):
        """ Find the probability of a detection given a visual magnitude, 
        limiting magnitude, and fillfactor, 
        determined by the fading function from Veres & Chesley (2017).

        Parameters
        ----------
        mag: float
                magnitude of object in filter used for that field
        limmag: float
             limiting magnitude of the field
        fillfactor: float
             fraction of FOV covered by the camera sensor   
        w: float
             distribution parameter
        
        Returns
        -------
        P: float
            Probability of detection
        """
   
        P = fillFactor / (1. + np.exp((mag - limmag) / w))

        return P

#-----------------------------------------------------------------------------------------------

def PPDetectionProbability(oif_df, survey_df, trailing_losses=False, trailing_loss_name='dmagDetect', 
                           magnitude_name="MaginFil", 
                           limiting_magnitude_name="limiting magnitude",
                           field_id_name="FieldID", fillFactor=0.9, w=0.1):

        """
        probability probability of observations being observable for objectInField output
        """
        
        l=len(oif_df.index)
        limMag = survey_df.lookup(oif_df[field_id_name], ['fiveSigmaDepth']*l)
        
        if (trailing_losses==False):
            return calcDetectionProbability(oif_df[magnitude_name], limMag, fillFactor, w)
        elif (trailing_losses==True):
            return calcDetectionProbability(oif_df[magnitude_name] + oif_df[trailing_loss_name], limMag, fillFactor, w)
        else:
            print('trailing_loss has to be True or False')