#!/usr/bin/python

import sys
import logging
import pandas as pd
from astropy import units as u
from astropy.coordinates import SkyCoord

from . import PPDetectionEfficiency

# Author: Grigori Fedorets


def PPFilterSSPLinking(padain, detefficiency, minintracklets, nooftracklets, intervaltime, inSepThresHoldAsec, rng):
    """
    PPFilterSSPLinking.py

    Description: This task reads in the modified pandas dataframe
    (including colours), checks if coordinates within tracklets are far enough
    to be separated by SSP, checks against the SSP detection criterion
    (_nooftracklets_ detections over _intervaltime_ nights), and outputs only the objects
    that satisfy that criterion.

    Generally, to be applied after detection threshold.


    Mandatory input:  padain: modified pandas dataframe
                      detefficiency: float, fractional percentage of successfully linked detections
                      minintracklets: integer, minimum number of observations
                      nooftracklets: integer, number of tracklets required for linking
                      interval time: float, interval of time (in days) which should include
                                     nooftracklets to qualify for a detection.
                      inSepThresHoldAsec: float: minimum separation for SSP inside the tracklet
                                     to distinguish between two images to recognise the motion
                                     between images
                      rng: Numpy random number generator object. If not defined, uses default seeded with system time.

    Output:               pandas dataframe


    usage: padafr=PPFilterSSPCriterionEfficiency(padain,detefficiency,minintracklet,nooftracklets,intervaltime, inSepThresHoldAsec)
    """

    pplogger = logging.getLogger(__name__)

    if (minintracklets < 2):
        pplogger.error('ERROR: PPFilterSSPCriterionEfficiency: minimum number of observations in tracklet should be at least 2.')
        sys.exit('ERROR: PPFilterSSPCriterionEfficiency: minimum number of observations in tracklet should be at least 2.')

    if (nooftracklets < 1):
        pplogger.error('ERROR: PPFilterSSPCriterionEfficiency: minimum number of tracklets should be at least 1.')
        sys.exit('ERROR: PPFilterSSPCriterionEfficiency: minimum number of tracklets should be at least 1.')

    # this accounts for the fact that ~95% of detections are successfully linked
    padain = PPDetectionEfficiency.PPDetectionEfficiency(padain, detefficiency, rng)

    padain.reset_index(inplace=True)
    cols = padain.columns.tolist()
    cols.append('counter')

    objid_list = padain['ObjID'].unique().tolist()

    # below variable is never used - SM
    # minno = minintracklets * nooftracklets

    padaout = pd.DataFrame(columns=cols)

    sepThreshold = inSepThresHoldAsec / 3600.

    # Here one might think of parallelisation
    i = 0
    while(i < len(objid_list)):
        subs = padain[padain['ObjID'] == objid_list[i]]
        subs = subs.drop_duplicates(subset='FieldID').reset_index(drop=True)
        # The absolute minimum number of observations is two
        # if one, just output everything
        if len(subs.index) >= 2:
            counter = 0  # of number of tracklets per object
            r = subs.index.tolist()
            padaouttrackletcoll = pd.DataFrame(columns=cols)

            j = r[0]
            k = r[0]

            # If criterion becomes satisfied, or data end:
            # first, tracklet
            padaouttracklet = pd.DataFrame()
            subidx = subs.index.values.max()

            while(j <= r[-1]):

                # Longest night at LSST site is around 10.8 hours
                s = j

                while(subs.at[s, 'FieldMJD'] - subs.at[k, 'FieldMJD'] < 11 / 24. and s <= r[-1]):
                    # The reason why this is done in a seemingly weird way is because
                    # for some reason the values in pandas columns get mixed up
                    # (if you just put loc[j], instead of # loc[k:j] and removing duplicates
                    # down the line)

                    # padaouttracklet=padaouttracklet.append(subs.loc[k:s], sort=False)
                    padaouttracklet = pd.concat([padaouttracklet, subs.loc[k:s]], sort=False)
                    padaouttracklet['counter'] = counter

                    if (s == subidx):
                        break
                    s = s + 1

                if((j - k + 1) >= minintracklets and len(padaouttracklet.index.values) > 1):

                    # see comment above why this is done weirdly
                    padaouttracklet = padaouttracklet.drop_duplicates(subset=['FieldID'])  # .reset_index(drop=True)
                    # Check if observations within tracklets are not too close to each other
                    firstCoordTracklet = SkyCoord(padaouttracklet.at[k, 'AstRA(deg)'] * u.degree, padaouttracklet.at[k, 'AstDec(deg)'] * u.degree)
                    lastCoordTracklet = SkyCoord(padaouttracklet.at[j, 'AstRA(deg)'] * u.degree, padaouttracklet.at[j, 'AstDec(deg)'] * u.degree)

                    sep = firstCoordTracklet.separation(lastCoordTracklet).degree
                    if not isinstance(sep, float):
                        # sometimes, the output of astropy SkyCoord.separation is a size 2 ndarray wth identical values, and not a float
                        sep = float(sep[0])
                    if (sep > sepThreshold):
                        # padaouttrackletcoll=padaouttrackletcoll.append(padaouttracklet, ignore_index=True, sort=False)
                        padaouttrackletcoll = pd.concat([padaouttrackletcoll, padaouttracklet], ignore_index=True, sort=False)
                        counter = counter + 1
                    # j=j+1
                    k = j

                    padaouttracklet = pd.DataFrame()

                elif ((len(padaouttracklet.index.values) <= 1) and s != j):
                    pass
                else:
                    k = j
                    padaouttracklet = pd.DataFrame()
                j = j + 1

            # This is the collection of all tracklets for a single object

            padaouttrackletcoll = padaouttrackletcoll[cols]
            padaouttrackletcoll = padaouttrackletcoll.drop(['index'], axis=1)
            padaouttrackletcoll = padaouttrackletcoll.drop_duplicates(subset=['FieldID']).reset_index(drop=True)
            ms = pd.unique(padaouttrackletcoll['counter'])

            m = 0
            g = 0

            if (len(ms) >= nooftracklets):
                while(m <= ms[-nooftracklets]):
                    if (m in padaouttrackletcoll['counter'].values):
                        flindex = padaouttrackletcoll.loc[padaouttrackletcoll['counter'] == m].head(1).index[0]
                        llindex = padaouttrackletcoll.loc[padaouttrackletcoll['counter'] == ms[g + nooftracklets - 1]].tail(1).index[0]
                        if (padaouttrackletcoll.at[llindex, 'FieldMJD'] - padaouttrackletcoll.at[flindex, 'FieldMJD'] < intervaltime):
                            padaout = pd.concat([padaout, padaouttrackletcoll[flindex:llindex + 1]], ignore_index=True, sort=False)
                        # padaout=padaout.append(padaouttrackletcoll[flindex:llindex+1], ignore_index=True, sort=False)
                        g = g + 1
                    m = m + 1

            padaout = padaout.drop_duplicates(subset=['FieldID']).reset_index(drop=True)

        i = i + 1

    return padaout
