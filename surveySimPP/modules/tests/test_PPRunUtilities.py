#!/bin/python

from surveySimPP.tests.data import get_test_filepath


def test_PPConfigFileParser():

    from surveySimPP.modules.PPRunUtilities import PPConfigFileParser

    configs = PPConfigFileParser(get_test_filepath('test_PPConfig.ini'), 'lsst')

    test_configs = {'ephFormat': 'whitespace',
                    'filesep': 'whitespace',
                    'ephemerides_type': 'oif',
                    'pointingdatabase': './surveySimPP/tests/data/baseline_10yrs_10klines.db',
                    'ppdbquery': 'SELECT observationId, observationStartMJD, filter, seeingFwhmGeom, seeingFwhmEff, fiveSigmaDepth, fieldRA, fieldDec, rotSkyPos FROM SummaryAllProps order by observationId',
                    'cometactivity': 'none',
                    'observing_filters': ['r', 'g', 'i', 'z'],
                    'mainfilter': 'r',
                    'othercolours': ['g-r', 'i-r', 'z-r'],
                    'phasefunction': 'HG',
                    'trailingLossesOn': True,
                    'cameraModel': 'footprint',
                    'footprintPath': './data/detectors_corners.csv',
                    'fillfactor': 1.0,
                    'brightLimit': 16.0,
                    'brightLimitOn': True,
                    'SNRLimit': None,
                    'SNRLimitOn': False,
                    'magLimit': None,
                    'magLimitOn': False,
                    'fadingFunctionOn': True,
                    'inSepThreshold': 0.5,
                    'minTracklet': 2,
                    'noTracklets': 3,
                    'trackletInterval': 15.0,
                    'SSPDetectionEfficiency': 0.95,
                    'SSPLinkingOn': True,
                    'outputformat': 'csv',
                    'outputsize': 'default',
                    'sizeSerialChunk': 10,
                    'rng_seed': None}

    assert configs == test_configs
