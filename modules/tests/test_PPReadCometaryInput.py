#!/bin/python

import pytest
import pandas as pd

from ..PPReadCometaryInput import PPReadCometaryInput


def test_PPReadCometaryInput():
     
     rescol=1552
     
     padafr=PPReadCometaryInput('./data/test/testcomet', 0, 1, " ")
     val=padafr.at[0,'afrho1']
     
     assert rescol==val
     
     return