 
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

__all__ = ['filtermag']

############################################
# MODULE SPECIFIC EXCEPTION
###########################################
class Error(Exception):
    """Vector module specific exception."""
    
    pass

#-----------------------------------------------------------------------------------------------

def filtermag(vismag, filtercolor, asteroidcolor, transforms=None):

        """Translate visual magnitude to other bands
        Parameters
        ----------
            filtercolor : string
                key to filter in transform dictionary
            asteroidcolor : string
                key to asteroid color in transform dictionary
            vismag : float
                apparent visual magnitude of the asteroid
            transforms: float dictionary
                dictionary or pandas table with transformations for filter-color combinations
                filter should be the first key
                defaults to S and C types using SDSS filters 
            
        Returns
        -------
            V : float
                Apparent magnitude in specified filter

        """

        if transforms == None:
            transforms = {'u': {'C': -1.614, 'S': -1.927},
                          'g': {'C': -0.302, 'S': -0.395},
                          'r': {'C':  0.172, 'S':  0.255},
                          'i': {'C':  0.291, 'S':  0.455},
                          'z': {'C':  0.298, 'S':  0.401},
                          'y': {'C':  0.303, 'S':  0.406}
                          }

        V = vismag - transforms[filtercolor][asteroidcolor]
        return V

#-----------------------------------------------------------------------------------------------