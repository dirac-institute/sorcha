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

import numpy as np


def calcDetectionProbability(mag, limmag, fillFactor=1.0, w=0.1):
    """
    Find the probability of a detection given a visual magnitude,
    limiting magnitude, and fill factor, determined by the fading function
    from Veres & Chesley (2017).

    Parameters
    -----------
    mag : float or array of floats
        Magnitude of object in filter used for that field.

    limmag : float or array of floats
        Limiting magnitude of the field.

    fillFactor : float), optional
        Fraction of FOV covered by the camera sensor. Default = 1.0

    w : float
        Distribution parameter. Default = 0.1

    Returns
    ----------
    P : float or array of floats
        Probability of detection.
    """

    P = fillFactor / (1.0 + np.exp((mag - limmag) / w))

    return P


def PPDetectionProbability(
    oif_df,
    trailing_losses=False,
    trailing_loss_name="dmagDetect",
    magnitude_name="PSFMag",
    limiting_magnitude_name="fiveSigmaDepth_mag",
    field_id_name="FieldID",
    fillFactor=1.0,
    w=0.1,
):
    """
    Find probability of observations being observable for objectInField output.
    Wrapper for calcDetectionProbability which takes into account column names
    and trailing losses. Used by PPFadingFunctionFilter.

    Parameters
    -----------
    oif_df : Pandas dataframe
        Dataframe of observations.

    trailing_losses : Boolean, optional
        Are trailing losses being applied?, Default = False

    trailing_loss_name : string, optional
        oif_df column name for trailing losses, Default = dmagDetect

    magnitude_name : string, optional
        oif_df column name for observation limiting magnitude
        Default = PSFMag

    limiting_magnitude_name : string, optional
        oif_df column used for observation limiting magnitude.
        Default = fiveSigmaDepth_mag

    field ID : string, optional
        oif_df column name for observation field_id
        Default = FieldID

    fillFactor : float, optional
        Fraction of FOV covered by the camera sensor. Default = 1.0

    w : float
        Distribution parameter. Default =0.1

    Returns
    ----------
     : float or array of floats
        Probability of detection.

    """

    if not trailing_losses:
        return calcDetectionProbability(
            oif_df[magnitude_name], oif_df[limiting_magnitude_name], fillFactor, w
        )
    elif trailing_losses:
        return calcDetectionProbability(
            oif_df[magnitude_name] + oif_df[trailing_loss_name],
            oif_df[limiting_magnitude_name],
            fillFactor,
            w,
        )
