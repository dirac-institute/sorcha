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

import pytest
import numpy as np
import pandas as pd


from ..PPAddUncertainties import addUncertainties
from ..PPAddUncertainties import calcAstrometricUncertainty
from ..PPAddUncertainties import calcPhotometricUncertainty


def test_calcAstrometricUncertainty():
    # Test the function calcAstrometricUncertainty
    mag = 20
    m5 = 23.5
    result_nominal = (10.85937575072431, 99.19895320080636, 4.233915645760927)

    result = calcAstrometricUncertainty(mag, m5)
    
    assert result == result_nominal

    return

def test_calcPhotometricUncertainty():
    # Test the function calcPhotometricUncertainty
    snr = 7
    result_nominal = 0.14497986744421684

    result=calcPhotometricUncertainty(snr)
    
    assert result == result_nominal

    return

