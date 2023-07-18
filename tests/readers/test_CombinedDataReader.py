import numpy as np
import pandas as pd
import pytest
from numpy.testing import assert_equal
from pandas.testing import assert_frame_equal

from surveySimPP.readers.CombinedDataReader import CombinedDataReader
from surveySimPP.readers.CSVReader import CSVDataReader
from surveySimPP.readers.OIFReader import OIFDataReader
from surveySimPP.readers.OrbitAuxReader import OrbitAuxReader
from surveySimPP.utilities.dataUtilitiesForTests import get_test_filepath


def test_CombinedDataReader():
    reader = CombinedDataReader()
    reader.add_primary_reader(OrbitAuxReader(get_test_filepath("PPReadAllInput_orbits.des"), "whitespace"))
    reader.add_reader(CSVDataReader(get_test_filepath("PPReadAllInput_params.txt"), "whitespace"))
    # reader.add_reader(OIFDataReader(get_test_filepath("PPReadAllInput_oif.txt"), "csv"))
    res_df = reader.read_block()
    assert len(res_df) == 10
