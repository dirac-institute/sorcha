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
Calculate Astrometric and Photometric Uncertainties for ground based observations.

"""
# Numpy 
import numpy as np

__all__ = ['calcDetectionProbability']


############################################
# MODULE SPECIFIC EXCEPTION
###########################################
class Error(Exception):
    """Vector module specific exception."""
    
    pass

#-----------------------------------------------------------------------------------------------
def probdetect(self, filtermag, limmag, fillfactor, w=0.1):
        """ Find the probability of a detection given a visual magnitude, 
        limiting magnitude, and fillfactor, 
        determined by the fading function from Veres & Chesley (2017)

        Parameters
        ----------
        filtermag: float
                magnitude of object in filter used for that field
        limmag: float
                limiting magnitude of the field
        fillfactor: float
                fraction of the field detectable due to ccd seperations
	w: float
	        distribution parameter
        
	Returns
        -------
        P: float
            Probability of detection
        """
   
        P = fillfactor / (1 + np.exp((filtermag - limmag) / w))
        return P
#-----------------------------------------------------------------------------------------------
