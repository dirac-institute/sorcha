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

def PPDetectionProbability(oif_df, limiting_magnitude_df, magnitude_name="ColinFil", limiting_magnitude_name="limiting magnitude",
                           field_id_name="FieldID", trailing_loss_name="trailing loss", w=0.1):

        """
        Adds column with probability of an observation being observable
        """

        out_df = oif_df.join(limiting_magnitude_df.set_index(field_id_name), on=field_id_name)
        out_df["detection probability"] = calcDetectionProbability(out_df[magnitude_name] + out_df[trailing_loss_name],
                                                                  out_df[limiting_magnitude_name], 
                                                                  w)
        out_df.drop(columns=[limiting_magnitude_name], inplace=True)

        return out_df