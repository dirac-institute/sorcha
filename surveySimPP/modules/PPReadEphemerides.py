#!/bin/python

import os
import sys
import pandas as pd
import logging
from . import PPReadOif


# Author: Grigori Fedorets


def PPReadEphemerides(eph_output, ephemerides_type, inputformat):
    """
    PPReadEphemerides.py


    Description: This task reads in the ephemerides as output by the pointing simulation.
    The type of ephemerides is assigned in the PPConfig.ini file.


    For correct performance, the read-in data needs to contain all of the following columns:

    ['ObjID', 'FieldID', 'FieldMJD', 'AstRange(km)', 'AstRangeRate(km/s)', 'AstRA(deg)', 
    'AstRARate(deg/day)', 'AstDec(deg)', 'AstDecRate(deg/day)', 'Ast-Sun(J2000x)(km)', 'Ast-Sun(J2000y)(km)',
    'Ast-Sun(J2000z)(km)', 'Ast-Sun(J2000vx)(km/s)', 'Ast-Sun(J2000vy)(km/s)', 'Ast-Sun(J2000vz)(km/s)', 
    'Obs-Sun(J2000x)(km)', 'Obs-Sun(J2000y)(km)', 'Obs-Sun(J2000z)(km)', 'Obs-Sun(J2000vx)(km/s)', 
    'Obs-Sun(J2000vy)(km/s)', 'Obs-Sun(J2000vz)(km/s)', 'Sun-Ast-Obs(deg)']





    Mandatory input:      string, eph_output, name of text file including Output from ephemerides file
                          string, ephemerides_type, type of ephemerides pointing simulation (oif) 
                          string, inputformat, input format of pointing putput (csv, whitespace, hdf5)



    Output:               pandas dataframe


    usage: PPReadEphemerides(padafr, ephemerides_type, inputformat)
    """
    from surveySimPP.modules.PPRunUtilities import PPGetLogger
    pplogger = PPGetLogger()

    if (ephemerides_type == 'oif'):
        padafr = PPReadOif.PPReadOif(eph_output, inputformat)

    # Functions for adding alternative types of ephemerides can be added here
    # See below for self-explanatory columns required for the ephemerides input

    # check the necessary columns exist

    cols = ['ObjID', 'FieldID', 'FieldMJD', 'AstRange(km)', 'AstRangeRate(km/s)', 'AstRA(deg)',
            'AstRARate(deg/day)', 'AstDec(deg)', 'AstDecRate(deg/day)', 'Ast-Sun(J2000x)(km)', 'Ast-Sun(J2000y)(km)',
            'Ast-Sun(J2000z)(km)', 'Ast-Sun(J2000vx)(km/s)', 'Ast-Sun(J2000vy)(km/s)', 'Ast-Sun(J2000vz)(km/s)',
            'Obs-Sun(J2000x)(km)', 'Obs-Sun(J2000y)(km)', 'Obs-Sun(J2000z)(km)', 'Obs-Sun(J2000vx)(km/s)',
            'Obs-Sun(J2000vy)(km/s)', 'Obs-Sun(J2000vz)(km/s)', 'Sun-Ast-Obs(deg)']

    for col in cols:
        if col not in padafr:
            pplogger.error('ERROR: PPReadEphemerides: essential columns missing from ephemerides input: ', col)
            sys.exit('ERROR: PPReadEphemerides: essential columns missing from ephemerides input: ', col)

    return padafr
