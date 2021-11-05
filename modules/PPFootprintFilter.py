
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
                         ra_name="AstRA(deg)", dec_name="AstDec(deg)", field_name="FieldID", 
                         ra_name_field='fieldRA', dec_name_field="fieldDec", rot_name_field="rotSkyPos"):
                         # field_name_survey="observationId",
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

    #field_df = pd.merge(
    #    observations[[field_name]],
    #    survey[[field_name_survey, ra_name_field, dec_name_field, rot_name_field]],
    #    left_on=field_name,
    #    right_on=field_name_survey,
    #    how="left"
    #)
    #
    #fieldra   = deg2rad(field_df[ra_name_field])
    #fielddec  = deg2rad(field_df[dec_name_field])
    #rotSkyPos = deg2rad(field_df[rot_name_field])
    #
    fieldra   = deg2rad(observations[ra_name_field])
    fielddec  = deg2rad(observations[dec_name_field])
    rotSkyPos = deg2rad(observations[rot_name_field])
    

    #get coords on focal plane
    x, y, z = RADEC2fovXYZ(ra, dec, fieldra, fielddec, rotSkyPos) # y,z in 3d -> x, y in focal plane
    y *= 2. / (1.+x)
    z *= 2. / (1.+x)
    
    print('y: ', y)
    print('z: ', z)
    
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
        
        #print(ySel)
        #print(zSel)
        #print('wait')
        print(obsSelIndex)
        print(np.array((ySel, zSel)))
        print(len(y), len(z))

        points=np.array((ySel, zSel)).T
        detected=isinPolygon(points, corners)
        #print(detected)

        detectedObs.append(pd.Series(obsSelIndex[detected]))

    return detectedObs#pd.concat(detectedObs).reset_index(drop=True)

def readFootPrintFile(path2file):
    #currently requires a specific header
    detectors_df=pd.read_csv(path2file)
    detectors=[]
    for i in range(len(detectors_df["detector"].unique())):
        detectors+=[ np.array([detectors_df.loc[detectors_df["detector"]==i]['x'], detectors_df.loc[detectors_df["detector"]==i]['y']]).T ]
    return np.array(detectors)


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

def xrot(p, θ):
    #rotation of a 3d vector around the x-axis
    p_out = np.zeros(p.shape)
    cosθ = cos(θ)
    sinθ = sin(θ)
    #m = np.array([[cosθ, -sinθ], [sinθ, cosθ]])
    p_out[0] = p[0] 
    p_out[1] = cosθ * p[1] - sinθ * p[2]
    p_out[2] = sinθ * p[1] + cosθ * p[2]
    return p_out

def RADEC2fovXYZ(RA, Dec, fieldRA, fieldDec, rotSkyPos):
    x=cos(Dec)*cos(RA)
    y=cos(Dec)*sin(RA)
    z=sin(Dec)
    p = np.array([x, y, z])

    fieldx = cos(fieldDec) * cos(fieldRA)
    fieldy = cos(fieldDec) * sin(fieldRA)
    fieldz = sin(fieldDec)
    pf = np.array([fieldx, fieldy, fieldz])
    
    p_out = rotateField2XAxis(p, pf)
    p_out = xrot(p_out, -rotSkyPos)

    return p_out

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

def HamiltonProduct(q1, q2):
    """where q1 and q2 are arrays of length 4 representing quaternions
    Not commutative."""
    #assert (q1.size[2] == 4) and (q2.size[2] == 4)
    assert (q1.shape == q2.shape), "q1 and q2 must be the same length"
    
    a1, b1, c1, d1 = q1
    a2, b2, c2, d2 = q2
    
    return np.array([
        a1*a2 - b1*b2 - c1*c2 - d1*d2,
        a1*b2 + b1*a2 + c1*d2 - d1*c2,
        a1*c2 - b1*d2 + c1*a2 + d1*b2,
        a1*d2 + b1*c2 - c1*b2 + d1*a2
    ]).reshape(q1.shape)

def quatRotate2XAxis(p, pf):
    """Rotates a 3d vector p such that the vector pf is aligned with the x-axis"""
    #where p is the point and pf is the center of the field
    #assert p.shape[0] == 3
    #print(p)
    
    #get rotation angle
    yzf = np.sqrt(pf[1]*pf[1] + pf[2]*pf[2])
    ρ = -np.arctan2(yzf, pf[0]) * 0.5
    
    #convert p to a quaternion
    P = np.zeros((4, p.shape[1]))
    P[1:4] = p
    
    #get rotation quaternion  
    # since this is a special case we can disregard the i component for some operations
    Q = np.zeros(P.shape)
    Q[0] = np.cos(ρ)
    Q[2] = -pf[2] 
    Q[3] = pf[1] 
    Q[2:4] *= (np.sin(ρ) / yzf)
    Qinv = Q.copy()
    Qinv[2:4] *= -1.
    #print(HamiltonProduct(Q, Qinv))
    #do rotation
    P_out = HamiltonProduct(Q, HamiltonProduct(P, Qinv))
    #P_out = HamiltonProduct(HamiltonProduct(Q, P), Qinv)
    return P_out[1:4]

def quatRotate(p, u, θ):
    """Rotate a point p around u by θ ."""
    #convert p to a quaternion
    P = np.zeros((4, p.shape[1]))
    P[1:4] = p
    
    #Construct rotation vector
    Q = np.zeros(P.shape)
    Q[0] = np.cos(0.5*θ)
    Q[1:4] = np.sin(0.5*θ) * u
    
    #construct conjugate quaternion
    Qc = Q.copy()
    Qc[1:4] *= -1.
    
    #do quaternion multiplication
    return HamiltonProduct(Q, HamiltonProduct(P, Qc))[1:4]

def rotateField2XAxis(p, pf):
    u = np.cross(np.array([1., 0., 0.]), pf,  axisa=0, axisb=0).T
    u /= np.linalg.norm(u, axis=0)
    θ = -np.arctan2(np.sqrt(1. - pf[0]*pf[0]), pf[0])
    p2 = quatRotate(p, u, θ)
    #calculate angle to undo precession
    zh = np.zeros(p.shape)
    zh[2] += 1.
    zh2 = quatRotate(zh, u, θ)
    ϕ = -np.arctan2(zh2[2], zh2[1])
    
    return xrot(p2, ϕ)