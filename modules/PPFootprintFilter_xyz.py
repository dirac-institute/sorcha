
# numpy
import numpy as np
# pandas
import pandas as pd
# matplotlib
import matplotlib.pyplot as plt


__all__=['footprintFilter','plotFootprintFiltering']

def footprintFilter(observations, survey, detectors,
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
    #fieldra=deg2rad(field[ra_name_field])
    fieldra=deg2rad(survey.set_index(field_name_survey).lookup(observations[field_name], [ra_name_field]*len(observations.index)))
    fielddec=deg2rad(survey.set_index(field_name_survey).lookup(observations[field_name], [dec_name_field]*len(observations.index)))
    rotSkyPos=deg2rad(survey.set_index(field_name_survey).lookup(observations[field_name], [rot_name_field]*len(observations.index)))

    z=sin(dec)
    z_2=cos(dec)

    x=z_2*cos(ra)
    y=z_2*sin(ra)
    del(z_2)

    z_field=sin(fielddec)
    z_field_2=cos(fielddec)

    x_field=z_field_2*sin(fieldra)
    y_field=z_field_2*cos(fieldra)
    del(z_field_2)

    #align field rotations
    #do this before projecting onto detector plane
    #rotate every point onto the same great circle, (i.e. along the x axis)

    cos_ra = cos(ra)
    sin_ra = sin(ra)

    x2 =  x*cos_ra + y*sin_ra
    y2 = -x*sin_ra + y*cos_ra
    z2 = z

    #rotate around the y axis
    cos_dec_f = cos(fielddec)
    sin_dec_f = sin(fielddec)

    x3 =  x2*cos_dec_f + z2*sin_dec_f
    y3 =  y2
    z3 = -x2*sin_dec_f + z2*cos_dec_f

    #rotate back to original ra
    x4 =  x3*cos_ra - y3*sin_ra
    y4 =  x3*sin_ra + y3*cos_ra
    z4 =  z3

    #rotate to ra for focal plane
    cos_ra_f = cos(fieldra)
    sin_ra_f = sin(fieldra)

    x5 =  x4*cos_ra_f + y4*sin_ra_f
    y5 = -x4*sin_ra_f + y4*cos_ra_f
    z5 = z4

    #align rotSkyPos
    cos_rot = cos(-rotSkyPos)
    sin_rot = sin(-rotSkyPos)

    y6 = y5*cos_rot - z5*sin_rot
    z6 = y5*sin_rot + z5*cos_rot

    x=x6
    y=y6
    z=z6

    #get vector from field center to obs in plane
    x/=x
    y/=x
    z/=x

    #check if obs fall in detectors
    detectedObs=[]
    for detector in detectors:
        xd=cos(detector[:,1])*cos(detector[:,0])
        yd=cos(detector[:,1])*sin(detector[:,0])
        zd=sin(detector[:,1])

        xd/=xd
        yd/=xd
        zd/=xd

        r, detector_center=detectorCircle(np.array((yd, zd)).T)
        obsSelIndex=np.where((y-detector_center[0])**2 + (z-detector_center[1])**2 < r**2 )[0]

        ySel=y[obsSelIndex]
        zSel=z[obsSelIndex]

        points=np.array((ySel, zSel)).T
        detected=isinPolygon(points, sortCorners(detector))

        detectedObs.append(pd.Series(obsSelIndex[detected]))

    return pd.concat(detectedObs).reset_index(drop=True)

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
