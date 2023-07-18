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

    Parameters:
    -----------
    mag (float/array of floats): magnitude of object in filter used for that field.

    limmag (float/array of floats): limiting magnitude of the field.

    fillFactor (float): fraction of FOV covered by the camera sensor.

    w (float): distribution parameter.

    Returns:
    ----------
    P (float/array of floats): probability of detection.
    """

    P = fillFactor / (1.0 + np.exp((mag - limmag) / w))

    return P


def PPDetectionProbability(
    oif_df,
    trailing_losses=False,
    trailing_loss_name="dmagDetect",
    magnitude_name="observedPSFMag",
    limiting_magnitude_name="fiveSigmaDepthAtSource",
    field_id_name="FieldID",
    fillFactor=1.0,
    w=0.1,
):
    """
    Find probability of observations being observable for objectInField output.
    Wrapper for calcDetectionProbability which takes into account column names
    and trailing losses. Used by PPFadingFunctionFilter.

    Parameters:
    -----------
    oif_df (Pandas dataframe): dataframe of observations.

    trailing_losses (Boolean): are trailing losses being applied?

    *_name (string): Column names for trailing losses, magnitude, limiting magnitude
    and field ID respectively.

    fillFactor (float): fraction of FOV covered by the camera sensor.

    w (float): distribution parameter.

    Returns:
    ----------
    P (float/array of floats): probability of detection.

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
