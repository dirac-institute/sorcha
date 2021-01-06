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
Transform Johnson V-band magnitudes to other filter systems
"""

import numpy as np
import pandas as pd
from collections import Counter

__all__ = ['addFilterMag']

############################################
# MODULE SPECIFIC EXCEPTION
###########################################
class Error(Exception):
    """Vector module specific exception."""
    
    pass

#-----------------------------------------------------------------------------------------------

def addFilterMag( ephemsdf, obsdf, popdf, transforms=None,
                  objectIDNameEph='ObjID', obsIdNameEph='FieldID', vMagNameEph='V',
                  filterName='filter', obsIdName='observationId',
                  objectIDNamePop='!!OID', colorNamePop='color',
                  newFilterMagName='Filtermag'
                  ):

        """Adds magnitude in observation filter to oif table
        Parameters
        ----------
            ephemsdf    ... 
            obsdf       ... 
            popdf       ...
            *NameEph    ... 
            *Name       ...
            *NamePop    ...
            
        Returns
        -------
            

        """

        if transforms == None:
            transforms = {'u': {'C': -1.614, 'S': -1.927},
                          'g': {'C': -0.302, 'S': -0.395},
                          'r': {'C':  0.172, 'S':  0.255},
                          'i': {'C':  0.291, 'S':  0.455},
                          'z': {'C':  0.298, 'S':  0.401},
                          'y': {'C':  0.303, 'S':  0.406}
                          }
            transforms = pd.DataFrame(transforms)
        
        #get asteroid colors
        ephemsdf.sort_values(by=[objectIDNameEph], inplace=True)
        objIDs = set(ephemsdf[objectIDNameEph])
        objs   = popdf.loc[popdf[objectIDNamePop].isin(objIDs)]

        objTypes = []
        count = Counter(ephemsdf[objectIDNameEph])
        
        for _, row in objs.iterrows():
            n = count[row[objectIDNamePop]]
            objTypes += n * [row[colorNamePop]]
            
        ephemsdf["objType"] = objTypes
        
        #get field filters
        ephemsdf.sort_values(by=[obsIdNameEph], inplace=True)
        fieldIDs = set(ephemsdf[obsIdNameEph])
        fields   = obsdf.loc[obsdf[obsIdName].isin(fieldIDs)]
        
        filters = []
        count = Counter(ephemsdf[obsIdNameEph])
        
        for _, row in fields.iterrows():
            n = count[row[obsIdName]]
            filters += n * [row[filterName]]
            
        ephemsdf["obsFilter"] = filters
        
        correction = ephemsdf.apply(lambda x: transforms[x["obsFilter"]][x["objType"]], axis=1)
        ephemsdf[newFilterMagName] = ephemsdf[vMagNameEph] - correction

        ephemsdf.reset_index(drop=True, inplace=True)

#-----------------------------------------------------------------------------------------------

def obsMagnitude(vMag, objColor, obsFilter, transforms):
    
    newMag = vMag - transforms[obsFilter][objColor]
    
    return newMag