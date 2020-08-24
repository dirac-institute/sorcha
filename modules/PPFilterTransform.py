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
        ephemsdf   ... Pandas DataFrame containing output of JPL ephemeris generator
        obsdf      ... Pandas DataFrame containing simulated observing run
        popdf      ... Pandas DataFrame containing orbital elements and color type
        *Name      ... corresponding column name in obsdf
        *NameEph   ... corresponding column name in ephemsdf
        *NamePop   ... corresponding column name in popdf
        transforms ... Pandas table or other dictionary containing filter transformations
                       defaults to SDSS filters 
            
        Returns
        -------
        ephemOut ... Pandas DataFrame containing JPL ephemeris output and magnitudes 
                     in observation filters
            

        """

        if transforms == None:
            transforms = {'u': {'C': -1.614, 'S': -1.927},
                          'g': {'C': -0.302, 'S': -0.395},
                          'r': {'C':  0.172, 'S':  0.255},
                          'i': {'C':  0.291, 'S':  0.455},
                          'z': {'C':  0.298, 'S':  0.401},
                          'y': {'C':  0.303, 'S':  0.406}
                          }

        filterMags = []

        for _, row in ephemsdf.iterrows():
            asteroidColor = popdf[colorNamePop][popdf[objectIDNamePop] == row[objectIDNameEph]]
            obsFilter     = obsdf[filterName][obsdf[obsIdName] == row[obsIdNameEph]]

            newMag        = row[vMagNameEph] - transforms[obsFilter[obsFilter.index[0]]][asteroidColor[asteroidColor.index[0]]]
              
            filterMags.append(newMag)

        ephemOut = ephemsdf
        ephemOut[newFilterMagName] = filterMags

        return ephemOut

#-----------------------------------------------------------------------------------------------
