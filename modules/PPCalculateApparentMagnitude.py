#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys
import pandas as pd
from numpy import pi, tan, log10, exp, power
import astropy.units as u
import sbpy
from sbpy.photometry import HG, HG1G2, HG12_Pen16, LinearPhaseFunc
import logging


# Author: Grigori Fedorets

def PPCalculateApparentMagnitude(padain, function, mainfilter):


    """
    PPCalculateApparentMagnitude.py

    Description: This task calculates the apparent brightness of an
    object in the mail filter (as defined in the config file) at a given pointing
    according to one of the following photometric phase function models:
          HG:                Bowell et al. (1989) Asteroids II book.
          HG1G2:             Muinonen et al. (2010) Icarus 209 542.
          HG12:              Penttilä et al. (2016) PSS 123 117.
          linear             (as implemented in sbpy)

    The brightness is here calculated in the main filter, and the colour offset is
    applied later using the PPhookBrightnessWithColour function.

    The function makes use of the implementations in the sbpy library.

    Mandatory input:      string, padain, name of input pandas daraframe
                          string, function, selected photometric phase function
                                  (HG, HG1G2, HG12, linear)
                          string, mainfilter, name of the main filter in which
                                  the brightness is calculated

    Output:        updated padain

    usage: padaout=PPCalculateApparentMagnitude(padain, function, mainfilter):

    """

    pplogger = logging.getLogger(__name__)

    # first, calculate rho, delta and phase

    padain['rho']=padain['AstRange(km)']/1.495978707e8
    # r is usually the colour, hence somewhat unconventional rho
    padain['delta']=((padain['Ast-Sun(J2000x)(km)']*padain['Ast-Sun(J2000x)(km)'] \
               + padain['Ast-Sun(J2000y)(km)']*padain['Ast-Sun(J2000y)(km)'] \
               + padain['Ast-Sun(J2000z)(km)']*padain['Ast-Sun(J2000z)(km)']).pow(1./2))/1.495978707e8

    padain['phase']=padain['Sun-Ast-Obs(deg)']#*pi/180.0


    if (function=='HG1G2'):
        #logger.error('ERROR: PPCalculateApparentMagnitude: HG1G2 treatment still under construction.')
        #sys.exit('ERROR: PPCalculateApparentMagnitude: HG1G2 treatment still under construction.')
        if set(['H','G1','G2']).issubset(padain.columns):
              Harr=padain['H'].values
              G1arr = padain['G1'].values
              G2arr = padain['G2'].values
              pharr= padain['phase'].values
              i=0
              phfarr=[]
              while(i<len(padain.index)):
                  HGm=HG1G2(H=Harr[i]*u.mag, G1=G1arr[i], G2=G2arr[i])
                  phf=HGm(pharr[i]*u.deg)
                  phfarr.append(phf.value)
                  i=i+1
              padain['phase_function']=phfarr
              # in sbpy, phase_function = H(alpha) + Phi(alpha)
              padain[mainfilter] =  5.*log10(padain['delta']) + 5.*log10(padain['rho']) + padain['phase_function']
              padain=padain.drop(['delta', 'rho', 'phase', 'phase_function'], axis = 1)

        else:
           pplogger.error('ERROR: PPCalculateApparentMagnitude: HG1G2 function requires the following input data columns: H, G1, G2.')
           sys.exit('ERROR: PPCalculateApparentMagnitude: HG1G2 function requires the following input data columns: H, G1, G2.')

    elif (function=='HG'):
         if set(['H', 'G']).issubset(padain.columns):
              Harr=padain['H'].values
              Garr = padain['G'].values
              pharr= padain['phase'].values
              i=0
              phfarr=[]
              while(i<len(padain.index)):
                  HGm=HG(H=Harr[i]*u.mag, G=Garr[i])
                  phf=HGm(pharr[i]*u.deg)
                  phfarr.append(phf.value)
                  i=i+1
              padain['phase_function']=phfarr
              # in sbpy, phase_function = H(alpha) + Phi(alpha)
              padain[mainfilter] =  5.*log10(padain['delta']) + 5.*log10(padain['rho']) + padain['phase_function']
              padain=padain.drop(['delta', 'rho', 'phase', 'phase_function'], axis = 1)

         else:
              pplogger.error('ERROR: PPCalculateApparentMagnitude: HG function requires the following input data columns: H, G.')
              sys.exit('ERROR: PPCalculateApparentMagnitude: HG function requires the following input data columns: H, G.')



    elif (function=='HG12'):
        if set(['H', 'G12']).issubset(padain.columns):
              Harr=padain['H'].values
              G12arr = padain['G12'].values
              pharr= padain['phase'].values
              i=0
              phfarr=[]
              while(i<len(padain.index)):
                  HGm=HG12_Pen16(H=Harr[i]*u.mag, G12=G12arr[i])
                  phf=HGm(pharr[i]*u.deg)
                  phfarr.append(phf.value)
                  i=i+1
              padain['phase_function']=phfarr
              # in sbpy, phase_function = H(alpha) + Phi(alpha)
              padain[mainfilter] =  5.*log10(padain['delta']) + 5.*log10(padain['rho']) + padain['phase_function']
              padain=padain.drop(['delta', 'rho', 'phase', 'phase_function'], axis = 1)

        else:
              pplogger.error('ERROR: PPCalculateApparentMagnitude: HG12 function requires the following input data columns: H, G12.')
              sys.exit('ERROR: PPCalculateApparentMagnitude: HG12 function requires the following input data columns: H, G12.')


    elif (function=='linear'):
        if set(['H', 'S']).issubset(padain.columns):

              Harr=padain['H'].values
              Sarr = padain['S'].values
              pharr= padain['phase'].values
              i=0
              phfarr=[]
              while(i<len(padain.index)):
                  HGm=LinearPhaseFunc(H=Harr[i]*u.mag, G=Sarr[i]*u.mag/u.deg)
                  phf=HGm(pharr[i]*u.deg)
                  phfarr.append(phf.value)
                  i=i+1
              padain['phase_function']=phfarr
              # in sbpy, phase_function = H(alpha) + Phi(alpha)
              padain[mainfilter] =  5.*log10(padain['delta']) + 5.*log10(padain['rho']) + padain['phase_function']
              padain=padain.drop(['delta', 'rho', 'phase', 'phase_function'], axis = 1)

        else:
              pplogger.error('ERROR: PPCalculateApparentMagnitude: linear function requires the following input data columns: H, S.')
              sys.exit('ERROR: PPCalculateApparentMagnitude: linear function requires the following input data columns: H, S.')

    else:
         pplogger.error('ERROR: PPCalculateApparentMagnitude: unknown phase function. Should be HG1G2, HG, HG12 or linear.')
         sys.exit('ERROR: PPCalculateApparentMagnitude: unknown phase function. Should be HG1G2, HG, HG12 or linear.')


    return padain
