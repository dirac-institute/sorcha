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


def DEScalcDetectionProbability(mag, limmag, c, k, c_sharp):
    """
    Find the probability of a detection given a visual magnitude,
    limiting magnitude, a scaling factor c, transition sharpness k and a transient efficiency. Equation from
    Bernardinelli et al., 2022

    Parameters
    -----------
    mag : float or array of floats
        Magnitude of object in filter used for that field.

    limmag : float or array of floats
        Limiting magnitude of the field.

    c : float or array of floats
        scaling factor

    k : float or array of floats
        transition sharpness

    c_sharp: float
        transient efficiency.
    Returns
    ----------
    P : float or array of floats
        Probability of detection
    """

    P = c_sharp * (c / (1 + np.exp(k * (mag - limmag))))

    return P


def DESDetectionProbability(
    eph_df,
    transient_efficiency,
    magnitude_name="PSFMag",
    limiting_magnitude_name="fiveSigmaDepth_mag",
    scaling_factor_name="c",
    transition_sharpness_name="k",
):
    """
    Find probability of observations being observable for objectInField output.
    Wrapper for calcDetectionProbability which takes into account column names. Used by DESFadingFunctionFilter.

    Parameters
    -----------
    eph_df : Pandas dataframe
        Dataframe of observations.


    magnitude_name : string, optional
        eph_df column name for observation limiting magnitude
        Default = PSFMag

    limiting_magnitude_name : string, optional
        eph_df column used for observation limiting magnitude.
        Default = fiveSigmaDepth_mag

    field ID : string, optional
        eph_df column name for observation field_id
        Default = FieldID

    scaling_factor_name: str, optional
        eph_df column name for scaling factor
        Default: c

    transition_sharpness_name: str, optional
        eph_df column name for transition_sharpness
        DEfault: k

    transient_efficiency: float
        overall transient efficiency for moving object detection

    Returns
    ----------
     : float or array of floats
        Probability of detection.

    """

    return DEScalcDetectionProbability(
        eph_df[magnitude_name],
        eph_df[limiting_magnitude_name],
        eph_df[scaling_factor_name],
        eph_df[transition_sharpness_name],
        transient_efficiency,
    )
