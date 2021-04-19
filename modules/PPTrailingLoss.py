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

__all__ = ['PPTrailingLoss']


############################################
# MODULE SPECIFIC EXCEPTION
###########################################
class Error(Exception):
    """Vector module specific exception."""
    
    pass


#-----------------------------------------------------------------------------------------------

def calcTrailingLoss(dRaCosDec, dDec, seeing, texp=30.0, a_trail=0.761, b_trail=1.162, a_det=0.420, b_det=0.003):
        """
         Find the trailing loss from trailing and detection (Veres & Chesley 2017)

        Parameters
        ----------
            dRa: float
                on sky velocity component in RA*Cos(Dec), deg/day
            
            dDec: float
                on sky velocity component in Dec, deg/day
            
            seeing: float
                Fwhm of the seeing disk, arcseconds
            
            texp: float
                exposure length, defaults to 30 seconds
	    *_trail: float 
       
            trail fit dmag parameters
            *_det: float 
		detection dmag parameters

        Returns
        -------
            dmag: float
                loss in detection magnitude
        
        """

        vel = np.sqrt(dRaCosDec ** 2 + dDec ** 2)
        vel = vel / 24.  # convert to arcsec / sec

        # stanadard parameters from (Veres & Chesley 2017)
        # a_trail = 0.761
        # b_trail = 1.162
        # a_det = 0.420
        # b_det = 0.003

        x = vel * texp / seeing 
        dmagTrail = 1.25 * np.log10(1. + a_trail * x ** 2 / (1. + b_trail * x))
        dmagDetect = 1.25 * np.log10(1. + a_det * x ** 2 / (1. + b_det * x))

        return (dmagDetect, dmagTrail)

#-----------------------------------------------------------------------------------------------

def PPTrailingLoss(oif_df, survey_df, dra_name='AstRARate(deg/day)',
                   ddec_name='AstDecRate(deg/day)', dec_name='AstDec(deg)',
                   seeing_name_oif="seeing", field_id_name_oif="FieldID",
                   seeing_name_survey='seeingFwhmGeom'):
    """
    Calculates Detection trailing loss for objectInField output.
    """

    #out_df = oif_df.join(seeing_df.set_index(field_id_name), on=field_id_name)
    #out_df["dmagDetect"], out_df['dmagTrail'] = calcTrailingLoss(out_df[dra_name]*np.cos(out_df['AstDec(deg)']*np.pi/180.), out_df[ddec_name], out_df[seeing_name])
    #out_df.drop(columns=[seeing_name], inplace=True)

    l = len(oif_df.index)
    seeing = survey_df.lookup(oif_df[field_id_name_oif], [seeing_name_survey]*l)
    dmagDetect, dmagTrail = calcTrailingLoss(oif_df[dra_name] * np.cos(oif_df[dec_name]*np.pi/180), oif_df[ddec_name], seeing)
    
    return (dmagDetect, dmagTrail)

#-----------------------------------------------------------------------------------------------
