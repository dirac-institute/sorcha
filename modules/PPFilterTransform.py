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
  #  vismag, filtercolor, asteroidcolor, transforms=None):

        """Translate visual magnitude to other bands
        Parameters
        ----------
            
            
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
        
        # get observation filters
        
        ephemOut = ephemsdf.sort_values(by=[obsIdNameEph])
        fieldIDs = set(ephemOut[obsIdNameEph])
        fields   = obsdf.loc[obsdf[obsIdName].isin(fieldIDs)]
        
        filtersC  = []
        filtersS  = []
        obsFilter = []
        count = Counter(ephemOut[obsIdNameEph])
        
        for _, row in fields.iterrows():
            n = count[row[obsIdName]]
            filtersC  += n * [transforms[row[filterName]]['C']]
            filtersS  += n * [transforms[row[filterName]]['S']]
            obsFilter += n * [row[filterName]]
            
        ephemOut['obsFilter'] = obsFilter
        
        #filters = np.array(filters)
        ephemOut['C'] = filtersC
        ephemOut['S'] = filtersS
        
        #get asteroid colors
        ephemOut = ephemOut.sort_values(by=[objectIDNameEph])
        objIDs = set(ephemOut[objectIDNameEph])
        objs = popdf.loc[popdf[objectIDNamePop].isin(objIDs)]
        
        colors = []
        count = Counter(ephemOut[objectIDNameEph])
        
        for _, row in objs.iterrows():
            n = count[row[objectIDNamePop]]
            colors += n * [row[colorNamePop]]
            
        colors = np.array(colors)
        ephemOut['colors'] = colors
        
        ephemOut['correction'] = ephemOut['C'].where(ephemOut['colors'] == 'C', ephemOut['S'])
        ephemOut.drop(labels=['C', 'S', 'colors'], axis=1, inplace=True)
        
        #ephemOut[newFilterMagName] = obsMagnitude(ephemOut[vMagNameEph], colors, filters, transforms)
        ephemOut[newFilterMagName] = ephemOut[vMagNameEph] - ephemOut['correction']
        ephemOut.drop(labels=['correction'], axis=1, inplace=True)

        return ephemOut

#-----------------------------------------------------------------------------------------------

def obsMagnitude(vMag, objColor, obsFilter, transforms):
    
    newMag = vMag - transforms[obsFilter][objColor]
    
    return newMag