#!/bin/python

import pytest


from modules import PPConfig
from ..PPReadConfigFile import PPReadConfigFile




def test_PPFilterSSPCriterionEfficiency():

    
    testvalue,oifoutput,colourinput,pointingdatabase,SSPDetectionEfficiency, \
    minTracklet,noTracklets,trackletInterval \
    =PPReadConfigFile()
        
    nlc=1
    nlco=testvalue
    
    assert nlc==nlco
    return