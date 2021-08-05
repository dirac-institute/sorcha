
# numpy
import numpy as np
# pandas
import pandas as pd
# matplotlib
import matplotlib.pyplot as plt

deg2rad = np.radians
sin = np.sin
cos = np.cos

__all__=['footPrintFilter']

def footPrintFilter(observations, survey, detectors,
                         ra_name="AstRA(deg)", dec_name="AstDec(deg)", field_name="FieldID", field_name_survey="observationId",
                         ra_name_field='fieldRA', dec_name_field="fieldDec", rot_name_field="rotSkyPos"):
    """Applies camera footpint to remove observations that do not fall on
    detector chips.

    Input
    -----
    observations        ... pandas dataframe containing ra, dec, and fieldID.
    survey              ... pandas dataframe containing fieldID, field center ra
                            and dec, and field rotation.
    detectors           ... list of lists containing detectors corners as angles
                            from x and y axes.
    Output
    ------
    detectedObs         ... mask for observations that will return detected observations.
    """

    #convert ra, dec to xyz on the unit sphere
    ra=deg2rad(observations[ra_name])
    dec=deg2rad(observations[dec_name])

    field_df = pd.merge(
        observations[[field_name]],
        survey[[field_name_survey, ra_name_field, dec_name_field, rot_name_field]],
        left_on=field_name,
        right_on=field_name_survey
    )

    fieldra   = deg2rad(field_df[ra_name_field])
    fielddec  = deg2rad(field_df[dec_name_field])
    rotSkyPos = deg2rad(field_df[rot_name_field])

    #get coords on focal plane
    x, y, z = RADEC2fovXYZ(ra, dec, fieldra, fielddec, rotSkyPos) # y,z in 3d -> x, y in focal plane
    y *= 2. / (1.+x)
    z *= 2. / (1.+x)

    #check if obs fall in detectors
    detectedObs=[]
    for detector in detectors:
        corners = sortCorners(detector)
        #project corners to plane
        xd = np.cos(corners[:,0]) * np.cos(corners[:,1])
        yd = np.sin(corners[:,0]) * np.cos(corners[:,1])
        zd = np.sin(corners[:,1])

        yd *= 2. / (1.+xd)
        zd *= 2. / (1.+xd)
        corners = np.array((yd, zd)).T

        r, detector_center=detectorCircle(corners)
        obsSelIndex=np.where((y-detector_center[0])**2 + (z-detector_center[1])**2 < r**2 )[0]

        ySel=y[obsSelIndex]
        zSel=z[obsSelIndex]

        points=np.array((ySel, zSel)).T
        detected=isinPolygon(points, corners)
        #print(detected)

        detectedObs.append(pd.Series(obsSelIndex[detected]))

    return pd.concat(detectedObs).reset_index(drop=True)

def detectors2fovXY(detectors):

    detectors_out = []
    for detector in detectors:
        xd=cos(detector[:,1])*cos(detector[:,0])
        yd=cos(detector[:,1])*sin(detector[:,0])
        zd=sin(detector[:,1])
        #print(xd)
        #yd/=xd
        #zd/=xd
        #xd/=xd
        detectors_out += [np.array([yd, zd]).T]

    return np.array(detectors_out)

def xyz_xrot(x, y, z, theta):
    #xf =
    yf = y*cos(theta) - z*sin(theta)
    zf = y*sin(theta) + z*cos(theta)
    return x, yf, zf

def xyz_yrot(x, y, z, theta):
    xf =  x*cos(theta) + z*sin(theta)
    #yf =
    zf = -x*sin(theta) + z*cos(theta)
    return xf, y, zf

def xyz_zrot(x, y, z, theta):
    xf = x*cos(theta) - y*sin(theta)
    yf = x*sin(theta) + y*cos(theta)
    #zf =
    return xf, yf, z

def RADEC2fovXYZ(RA, Dec, fieldRA, fieldDec, rotSkyPos):
    x=cos(Dec)*cos(RA)
    y=cos(Dec)*sin(RA)
    z=sin(Dec)

    fieldx = cos(fieldDec) * cos(fieldRA)
    fieldy = cos(fieldDec) * sin(fieldRA)
    fieldz = sin(fieldDec)

    phi = np.arctan2(fieldz, fieldx)
    x, y, z = xyz_yrot(x, y, z, phi)
    fieldx, fieldy, fieldz = xyz_yrot(fieldx, fieldy, fieldz, phi)

    phi = np.arctan2(fieldy, fieldx)
    x, y, z = xyz_zrot(x, y, z, -phi)

    x, y, z = xyz_xrot(x, y, z, -rotSkyPos)

    #project y, z onto distant plane
    #x*=()
    #y*= 2 / (1+x)
    #z*= 2 / (1+x)

    return x, y, z

def polygonArea(corners):
    """Calculates the area of a convex polygon.
    Input
    -----
    corners         ... list containing [x, y] pairs for each corner.
    """
    cornersRolled=np.roll(corners, 1, axis=0)
    return .5*np.sum(np.sum(corners[:,0]*cornersRolled[:,1] - corners[:,1]*cornersRolled[:,0]))

def isinPolygon(point, corners, error=10**-10):
    """Determines whether a point is inside a polygon by comparing the area of
    the polygon to the sum of the areas of the triangles formed by the point and
    each pair of adjacent corners.

    Input
    -----
    point           ... [x, y] pair
    corners         ... list containing [x, y] pairs for each corner.
    error           ... sensitivity of the area difference

    """
    cornersRolled=np.roll(corners, -1, axis=0)
    trueArea=polygonArea(corners)
    if point.shape==(2,):
        areas=0.5*np.abs(point[0]*corners[:,1] - corners[:,0]*point[1]
                   + corners[:,0]*cornersRolled[:,1] - cornersRolled[:,0]*corners[:,1]
                   + cornersRolled[:,0]*point[1] - point[0]*cornersRolled[:,1]
                     )
        return (np.abs(np.sum(areas) - trueArea) <= error)
    else:
        n=len(point)
        areas=np.zeros(n)
        for i in range(len(corners)):
            term1=point[:,0]*corners[i,1] - point[:,1]*corners[i,0]
            term2=(corners[i,0]*cornersRolled[i,1] - corners[i,1]*cornersRolled[i,0])*(np.zeros(n)+1.)
            term3=point[:,1]*cornersRolled[i,0] - point[:,0]*cornersRolled[i,1]
            areas+=np.abs(term1+term2+term3)

        return ((.5*areas - trueArea)/trueArea <= error)

def detectorCircle(detector):
    """
    calculates a radius for a circle containing the detector
    assumes the detector is a convex quadrilateral
    """
    centroidx=np.sum(detector[:,0])/4
    centroidy=np.sum(detector[:,1])/4

    distancesx = detector[:,0] - centroidx
    distancesy = detector[:,1] - centroidy
    distances = distancesx**2 + distancesy**2

    return (np.sqrt(max(distances)), [centroidx, centroidy])

def sortCorners(points):
    """sorts points into order to plot as a convex polygon"""
    points=np.array(points)
    centroid=np.array([np.sum(points[:,0]), np.sum(points[:,1])])/4
    corner_rays=points-centroid
    #print(corner_rays[:,0], corner_rays[:,1])
    angles=np.arctan2(corner_rays[:,0], corner_rays[:,1])
    return np.array([x for x, y in sorted(zip(points, angles), key=lambda pair: pair[1])])
