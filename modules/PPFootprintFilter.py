########################################################
#
# This module filters simulated observations 
# that would not be observed due to the LSST camera
# footprint (chip gaps etc.)
# Requires the LSST stack.
#
# S. Eggl 2020/12/10
#######################################################

# LSST STACK
from lsst.sims.utils import ObservationMetaData
from lsst.sims.coordUtils import lsst_camera
from lsst.sims.coordUtils import chipNameFromRaDecLSST
from lsst.afw.cameraGeom import DetectorType

# numpy
import numpy as np
# pandas
import pandas as pd
# matplotlib
import matplotlib.pyplot as plt


__all__=['cameraFootprintFilter','plotFootprintFiltering']

def cameraFootprintFilter(observations,pointings,raPointings='fieldRA',decPointings='fieldDec',
                          epochPointings='observationStartMJD',rotSkyPointings='rotSkyPos',
                          raObs='AstRA(deg)',decObs='AstDec(deg)',
                          epochObs='FieldMJD',dtlim=31/86400):


    """Filter observations generated through JPL survey_simulator according the LSST camera footprint. 
    Requires LSST stack.
    
    Parameters:
    -----------
    observations ... Pandas DataFrame containing observations (e.g. simulated output of JPL survey_simulator OIF)
    pointings    ... Pandas DataFrame containing LSST opsim survey simulation output
    
    Returns: 
    --------
    obsOut ... filtered ephems Pandas dataFrame 
                 (observations that do not fall onto a science CCD are omitted)
    """
 
    
    #Check whether the observations dataframe covers the whole ephemeris time
    tpointmin=pointings[epochPointings].min()
    tpointmax=pointings[epochPointings].max()
    tobsmin=observations[epochObs].min()
    tobsmax=observations[epochObs].max()
    
    if(tobsmin<tpointmin or tobsmax>tpointmax):
        print('observations tmin, pointings tmin:',tobsmin, tpointmin)
        print('observations tmax, pointings tmax:',tobsmax, tpointax)
        raise ValueError('Observations do not cover the entire ephemeris timespan.')
    
    camera = lsst_camera()
    ccd_type_dict = {DetectorType.SCIENCE: 'science', DetectorType.WAVEFRONT: 'wavefront',
                 DetectorType.GUIDER: 'guider', DetectorType.FOCUS: 'focus'}
    
    # Preselect only those pointings mentioned in the observations dataframe
    
    ptSel=pointings[(pointings[epochPointings]>=tobsmin) & (pointings[epochPointings]<=tobsmax)]
    
    obsFiltered=[]
        
    # Iterate over all selected observations from opsim database
    for index, row in ptSel.iterrows(): 
        
       
        metadata = ObservationMetaData(pointingRA=row[raPointings],
                                           pointingDec=row[decPointings],
                                           rotSkyPos=row[rotSkyPointings],
                                           mjd=row[epochPointings])

        
        obs_sel=observations[(np.abs(observations[epochObs]-row[epochPointings])<=dtlim)].reset_index(drop=True)
        
        # obs_sel=observations[observations[obsIdNameObs] == row[obsIdName]].reset_index(drop=True)
        
        chipName = chipNameFromRaDecLSST(ra=obs_sel[raObs].values.astype(float),
                                         dec=obs_sel[decObs].values.astype(float),
                                         epoch=2000.0, obs_metadata=metadata)

        idx=np.where(chipName != None)[0]
        idxObs=[i for i in idx if (ccd_type_dict[camera[chipName[i]].getType()] == 'science')]
        
        obsFiltered.append(obs_sel[obs_sel.index.isin(idxObs)])
    
    obsOut=pd.concat(obsFiltered).reset_index(drop=True)
    return obsOut

def plotFootprintFiltering(df_old, df_new, ra='AstRA(deg)', dec='AstDec(deg)'):
    """Plot difference between camera footprint filtered and unfiltered LSST observations.

    Parameters:
    -----------
    df_old ... Pandas dataFrame of unfiltered observations
    df_new ... Pandas dataFrame of filtered observations

    """
    xmax=df_old[ra].max()
    xmin=df_old[ra].min()
    ymax=df_old[dec].max()
    ymin=df_old[dec].min()
    
    scale=(xmax-xmin)/(ymax-ymin)
    
    label1='dropped: '+str(len(df_old.index)-len(df_new.index))
    label2='kept: '+str(len(df_new.index))
    plt.figure(dpi=300, figsize=(scale*6,6))
    plt.scatter(df_old[ra],df_old[dec],s=0.5, color='r',label=label1)
    plt.scatter(df_new[ra],df_new[dec],s=0.5, color='b',label=label2)
    plt.xlabel(ra)
    plt.ylabel( dec)
    plt.title('LSST Camera Footprint Filtering')
    plt.legend()
    plt.show()