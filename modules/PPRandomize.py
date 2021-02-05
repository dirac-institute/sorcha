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
# 
# Numpy 
import numpy as np
"""

"""
#Pandas
import pandas as pd

__all__ = ['randomizeAstrometry', 'randomizePhotometry']

############################################
# MODULE SPECIFIC EXCEPTION
###########################################
class Error(Exception):
    """Vector module specific exception."""
    
    pass


############################################

def randomizeAstrometry(ephemsdf, 
                        raSigName, decSigName,
                        raName='AstRA(deg)', decName='AstDec(deg)'):

    """Randomize astrometric values (in degrees) for simulated observations

    Parameters
    ----------
    ephemsdf   ... Pandas dataFrame containing output of JPL ephemeris 
                   generator and astrometric uncertainties
    Name      ... relevant column names in ephemsdf

    Returns
    -------
    ephemsOut  ... ephems Pandas dataFrame with astrometric values modifed 

    """

    ephemsOut=ephemsdf
    ephemsOut["randAstRA(deg)"]  = np.random.normal(ephemsdf[raName],  ephemsdf[raSigName]) / (3600000)
    ephemsOut["randAstDec(deg)"] = np.random.normal(ephemsdf[decName], ephemsdf[decSigName]) / (3600000)

    return ephemsOut


def randomizePhotometry(ephemsdf,
                        photSigName,
                        photName='Filtermag'):

    """ Randomize photometric values for simulated observations
    
    Parameters
    ----------
    ephemsdf   ... Pandas dataFrame containing output of JPL ephemeris 
                       generator and astrometric uncertainties
    Name      ... relevant column names in ephemsdf
        
    Returns
    -------
    ephemsOut  ... ephems Pandas dataFrame with photometric values modifed 
        
    """
    ephemsOut=ephemsdf
    newPhot = np.random.normal(ephemsdf[photName], ephemsdf[photSigName])

    ephemsOut["randFilterMag"] = newPhot
    return ephemsOut
