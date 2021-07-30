import configparser
import argparse
import pandas as pd
import numpy as np
import os
import sqlite3 as sql

def makeConfig():
    #grab defaults from a template config file
    args = parser.parse_args()
    config = configparser.ConfigParser()

    #get database info
    con = sql.connect(args.opsim)
    database = pd.read_sql_query("SELECT observationStartMJD, observationId FROM SummaryAllProps ORDER BY observationStartMJD", con)
    maxFields = len(database.index)

    #get what dates to check in database
    survey_days = database["observationStartMJD"].astype(int).unique()
    day1 = survey_days[args.day1 - 1]
    if (args.ndays == -1) or (args.ndays + args.day1 >= survey_days.iloc[-1]):
        dayf = survey_days[-1]
    else:
        dayf = day1 + args.ndays

    #get range of fields for those days
    field1 = database.loc[(database["observationStartMJD"] - day1) < 1.0]["observationId"].iloc[0]
    fieldf = database.loc[(database["observationStartMJD"] - dayf) < 2.0]["observationId"].iloc[-1] #this will likely overshoot a little bit

    #do stuff for parellizing
    orbits=pd.read_csv(args.o, delim_whitespace=True)
    nOrbitsTotal = len(orbits.index)
    nOrbitsPerFile = args.no
    remainder = nOrbitsTotal % nOrbitsPerFile

    if nOrbitsPerFile == -1:
        nOrbitsPerFile = nOrbitsTotal
        startingOrbits = [1]
    else:
        if nOrbitsTotal%nOrbitsPerFile==0:
            startingOrbits=np.linspace(0, nOrbitsTotal - nOrbitsPerFile, nOrbitsTotal//nOrbitsPerFile, dtype=int) + 1
        else:
            startingOrbits=np.linspace(0, nOrbitsTotal - nOrbitsTotal%nOrbitsPerFile, nOrbitsTotal//nOrbitsPerFile+1, dtype=int) + 1

    orbitsName = args.o.split('/')[-1].split('.')[0]

    m = len(startingOrbits)
    for i in range(m):
        if i == m and remainder!= 0:
            nOrbits = remainder
        else:
            nOrbits = nOrbitsPerFile

        config.read_dict({
            'CONF': {
                'Cache dir':        '_cache' + "/" + orbitsName + "/" + str(startingOrbits[i]) + '-' + str(nOrbits),       # Directory where to place generated temporary files
            },
            'ASTEROID' : {
                'SPK T0':            str(day1-30),
                'nDays':             str(args.ndays + 30),
                'Object1':           str(startingOrbits[i]),
                'nObjects':          str(nOrbits),
                'SPK step':          '30'

            },
            'SURVEY': {
                'Survey database':   args.opsim,
                'Field1':            str(field1 + 1),
                'nFields':           str(fieldf - field1),
                'MPCobscode file':   'obslist.dat',
                'Telescope':         'I11',
                'Surveydbquery':     'SELECT observationId,observationStartMJD,fieldRA,fieldDEC,rotSkyPos FROM SummaryAllProps order by observationStartMJD'
            },
            'CAMERA': {
                'Threshold': '5',
                'SPICE IK':  'camera.ti',
            },
            'OUTPUT': {
                'Output file':           'stdout',
                'Output format':         'csv'
            }
        })

        ndigits = len(str(len(orbits.index)))
        with open(os.path.join(args.prefix, orbitsName + "-" + str(startingOrbits[i]).zfill(ndigits) + '-' + str(startingOrbits[i] + nOrbits).zfill(ndigits) + '.ini'), 'w') as file:
            config.write(file)

if (__name__=='__main__'):

    parser=argparse.ArgumentParser()
    parser.add_argument("-o", help="orbits file", type=str)
    parser.add_argument("-no", help="number of orbits per config file", type=int, default=-1)
    parser.add_argument("-ndays", help="number of days in survey to run, -1 runs entire survey", type=int, default=-1)
    parser.add_argument("-day1", help="first day in survey to run", type=int, default=1)
    parser.add_argument("-opsim", help="path to opsim file", type=str)
    parser.add_argument("-prefix", help="config file name prefix", type=str, default='')

    makeConfig()
