# Developed for the Vera C. Rubin Observatory/LSST Data Management System.
# This product includes software developed by the
# Vera C. Rubin Observatory/LSST Project (https://www.lsst.org).
#
# Copyright 2020 University of Washington
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


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

class Detector:

    def __init__(self, points, ID=0, units='radians'):
        """ initiates a detector object.

        INPUT
        -----
        points      ... array of shape (2, n) describing the corners of the sensor
        ID          ... An integer ID for the sensor
        units       ... units that points is provided in, radians or degrees from 
                        center of the focal plane.

        RETURNS
        -------
        detector    ...a detector instance
        """
    #points  --->   should be shape dims, n points
        self.ID = ID
        self.ra = points[0]
        self.dec = points[1]
        self.units = units
        
        if units == 'degrees' or units == 'deg':
            self.deg2rad()
        
        # generate focal plane coordinates
        # convert to xyz on unit sphere
        z = np.cos(self.ra)*np.cos(self.dec) #x
        self.x = sin(self.ra)*np.cos(self.dec) #y
        self.y = sin(self.dec)
        
        # project to focal plane
        self.x /= z
        self.y /= z
        
        # calculate centroid
        self.centerx = np.sum(self.x) / len(self.x)
        self.centery = np.sum(self.y) / len(self.y)
        
    def ison(self, point, ϵ=10.**(-11), plot=False):
        """ Determines whether a point (or array of points) falls on the 
        detector.

        INPUT
        -----
        point   ... array of shape (2, n) for n points
        plot    ... whether to plot the detector and the point

        RETURNS
        -------
        ison    ... indices of points in point array that fall on the sensor.
        """
        #points needs to be shape 2,n
        #if single point, needs to be an array of single element arrays
        
        #check whether point is in circle bounding the detector
        r2 = np.max((self.x - self.centerx)**2 + (self.y - self.centery)**2)
        selectedidx = np.where((point[0] - self.centerx)**2 + (point[1] - self.centery)**2 <= r2)[0]

        selected = point[:, selectedidx]
        xselected = point[0][selectedidx]
        yselected = point[1][selectedidx]
        
        #check whether selected fall on the detector
        #compare true area to the segmented area
        
        detectedidx = np.where(
            np.abs(self.segmentedArea(selected) - self.trueArea()) <= ϵ
        )[0]
        
        if plot:
            x = xselected[detectedidx]
            y = yselected[detectedidx]
        
            plt.scatter(x, y, color='red', s=3.)
        
        return selectedidx[detectedidx]
        
    def trueArea(self):
        """ Uses the same method as segmented area, but the test point is the
        mean of the corner coordinates. Will probably fail if the sensor is 
        not convex.
        """        
        x = self.x - self.centerx
        y = self.y - self.centery
        
        xrolled = np.roll(x, 1)
        yrolled = np.roll(y, 1)
        
        area = 0.5*np.sum(
            np.abs(x*yrolled - y*xrolled)
        )
                
        return area
        
    def segmentedArea(self, point):
        """ Returns the area of the detector by calculating the area of each
        triangle segment defined by each pair of adjacent corners and a point
        inside the sensor.
        Fails if the point is not inside the sensor or if the sensor is not 
        convex.

        INPUT
        -----
        point       ... a point inside the sensor

        RETURNS
        area        ... area of the sensor
        """
        #so that poth a single and many points work
        ncorners = self.x.shape[0]
        
        if len(point.shape) == 1:
            x = self.x - point[0]
            y = self.y - point[1]
            
        else:
            x = ((np.zeros((ncorners, point.shape[1])).T + self.x).T - point[0])
            y = ((np.zeros((ncorners, point.shape[1])).T + self.y).T - point[1]) #copy over an array to make broadcasting work
        
        xrolled = np.roll(x, 1, axis=0)
        yrolled = np.roll(y, 1, axis=0)
        area = []
        
        for i in range(len(self.x)):
            area.append(
                np.abs(x[i] * yrolled[i] - y[i]*xrolled[i])
            )
        
        return 0.5*(np.sum(area, axis=0))
        
    def sortCorners(self):
        """ Sorts the corners to be counterclockwise by angle from center of 
        the detector. Modifies self.
        """        
        #convert corners to angles (radians)
        θ = np.arctan2(self.y - self.centery / self.x - self.centerx)
        
        neworder = np.argsort(θ)
        self.x = self.x[neworder]
        self.y = self.y[neworder]
        
    def rotateDetector(self, θ):
        """ Rotates a sensor around the origin of the coordinate system its
        corner locations are provided in.

        INPUT
        -----
        θ   ... Angle to rotate by, in radians.

        RETURNS
        -------
        Detector    ... New Detector instance
        """
        #convert rotation angle to complex number
        q = cos(θ) + sin(θ)*1.0j
        
        #convert points to complex numbers
        coords = self.x + self.y*1.0j
        
        #rotate
        newcoords = coords * q
        return Detector(np.array((np.real(newcoords), np.imag(newcoords))), self.ID)
    
    def rad2deg(self):
        """ Converts corners from radians to degrees.
        """
        if self.units == 'radians':
            self.x = np.degrees(self.x)
            self.y = np.degrees(self.y)
            self.centerx = np.degrees(self.centerx)
            self.centery = np.degrees(self.centery)
            self.units = 'degrees'
        else:
            print("Units are already degrees")
        
    def deg2rad(self):
        """ Converts corners from degrees to radians.
        """
        if self.units == "degrees":
            self.x = np.radians(self.x)
            self.y = np.radians(self.y)
            self.centerx = np.radians(self.centerx)
            self.centery = np.radians(self.centery)
            self.units = "radians"
        else:
            print("Units are already radians")
            
    def plot(self, θ=0.0, color='gray', units='rad', annotate=False):
        """ Plots the footprint for an individual sensor. Currently not on the 
        focal plane, just the sky coordinates. Relatively minor difference 
        (width of footprint for LSST is <2.1 degrees), so should be fine for
        internal demonstration purposes, but not for confirming algorithms or 
        for offical plots.

        INPUT
        -----
        θ           ... Angle to rotate footprint by, radians or degrees
        color       ... line color
        units       ... units θ is provided in
        annote      ... whether to annotate each sensor with its index in 
                        self.detectors
        """    
        detector = self.rotateDetector(θ)
        if units=='deg':
            detector.rad2deg()
        nd = len(self.x)
        x = np.zeros(nd+1)
        x[0:nd] = detector.x
        x[-1] = x[0]
        y = np.zeros(nd+1)
        y[0:nd] = detector.y
        y[-1] = y[0]
        plt.plot(x, y, color=color)
        
        if annotate == True:
            plt.annotate(str(detector.ID), (detector.centerx, detector.centery))
        
                
class Footprint:

    def __init__(self, path, detectorName="detector"):
        """ Initiates a Footprint object.

        INPUT
        -----
        path            ... path to a .csv file containing detector corners
        detectorName    ... name of column in detector file inidicating to 
                            which sensor a corner belongs.

        RETURNS
        -------
        Footprint       ... Footprint object for the provided sensors.
        """
        #file should be a .csv (and should be actually comma seperated)
        #the center of the camera should be the origin
        allcornersdf = pd.read_csv(path)
        
        self.detectors = [Detector( np.array( (
            allcornersdf.loc[allcornersdf[detectorName]==i, 'x'], 
            allcornersdf.loc[allcornersdf[detectorName]==i, 'y']) ), i ) 
            for i in range(len(allcornersdf[detectorName].unique())) ]
        
        self.N = len(self.detectors)
        
        #sort the corners of each detector
        for i in range(self.N):
            self.detectors[i].sortCorners            
        
    def plot(self, θ=0., color='gray', units='rad', annotate=False):    
        """ Plots the footprint. Currently not on the focal plane, just the sky
        coordinates. Relatively minor difference (width of footprint for LSST
        is <2.1 degrees), so should be fine for internal demonstration 
        purposes, but not for confirming algorithms or for offical plots.

        INPUT
        -----
        θ           ... Angle to rotate footprint by, radians or degrees
        color       ... line color
        units       ... units θ is provided in
        annote      ... whether to annotate each sensor with its index in 
                        self.detectors
        """    
        for i in range(self.N):
            self.detectors[i].plot(θ=θ, color=color, units=units, annotate=annotate)
            
    
    def applyFootprint(
        self, oifDF, pointings,
        ra_name="AstRA(deg)", 
        dec_name="AstDec(deg)", 
        field_name="FieldID", 
        field_name_survey="FieldID",
        ra_name_field='fieldRA', 
        dec_name_field="fieldDec", 
        rot_name_field="rotSkyPos",
        method="direct projection",
        ):
        """ Determine whether detections fall on the sensors defined by the 
        footprint. Also returns the an ID for the sensor a detection is made 
        on.

        Includes option to use old algorithm, for testing purposes.

        INPUT
        -----
        oifDF           ... Pandas DataFrame containing detection information
        pointings       ... Pandas DataFrame containing field pointing information
        *_name          ... column names for oifDF
        *_name_field    ... column names for pointings
        method          ... which algorthim to use to convert on sky location
                            to focal plane coordinates

        RETURNS
        -------
        detected        ... Indices of rows in oifDF which fall on the sensor(s)
        detecorID       ... Index corresponding to a detector in 
                            self.detectors for each entry in detected
        """
        # TODO: only grab pointings that have detections in oifDF
        
        # convert detections to xyz on unit sphere
        ra=deg2rad(oifDF[ra_name])
        dec=deg2rad(oifDF[dec_name])
        
        #
        field_df = pd.merge(
            oifDF[[field_name]],
            pointings[[field_name_survey, ra_name_field, dec_name_field, rot_name_field]],
            left_on=field_name,
            right_on=field_name_survey,
            how="left"
        )
        
        # convert field pointings to xyz on unit sphere
        fieldra   = deg2rad(field_df[ra_name_field])
        fielddec  = deg2rad(field_df[dec_name_field])
        rotSkyPos = deg2rad(field_df[rot_name_field])
        
        # convert detections to x, y in focal plane
        if method == "Quaternion" or method == "quaternion": #rotation on 3d unit sphere
            x, y, z = RADEC2fovXYZ(ra, dec, fieldra, fielddec, np.zeros(rotSkyPos.shape))#rotSkyPos) # y,z in 3d -> x, y in focal plane
            y /= x #*= 2. / (1.+x)
            z /= x #*= 2. / (1.+x)
            
            #x = y
            #y = z
            #del(z)
            plt.scatter(y, z, s=3.0)
            points = np.array((y, z))
            
        else: # use direct projection method (no rotation on 3d unit sphere)
            x, y = radec2focalplane(ra, dec, fieldra, fielddec)
        
        # apply field rotation
        # first convert to complex numbers
        # maybe do this in the focal plane function?
        observations_complex = x + y*1.0j
        rotation = np.exp(-rotSkyPos*1.0j)

        observations_complex *= rotation
        x = np.real(observations_complex)
        y = np.imag(observations_complex)
        
        plt.scatter(x, y, s=3.0)
        points = np.array((x, y))
        
        #check whether they land on any of the detectors
        i = 0
        detected = []
        detectorId = []
        for detector in self.detectors:
            if True:
                stuff = detector.ison(points)
                detected.append(stuff)
                detectorId.append([i]*len(stuff))
                i+=1
            
        return np.concatenate(detected), np.concatenate(detectorId)
        
    
def radec2focalplane(ra, dec, fieldra, fielddec, fieldID=None):
    """ Converts ra and dec to xy on the focal plane. Projects all pointings to
    the same focal plane, but does not account for field rotation. Maintains 
    alignment with the meridian passing through the field center.

    INPUT
    -----
    ra          ... Observation Right Ascension, radians
    dec         ... Observation Declination, radians
    fieldra     ... Field Pointing Right Ascension, radians
    fielddec    ... Field Pointing Declination, radians
    fieldID     ... Field ID, Integer, optional.

    RETURNS
    -------
    x, y        ... Coordinates on the focal plane, radians projected
                    to the plane tangent to the unit sphere.
    """

    # convert to cartesian coordiantes on unit sphere
    observation_vectors = np.array(
        [cos(ra)*np.cos(dec), #x
         sin(ra)*np.cos(dec), #y
         sin(dec)])           #z
        
    field_vectors = np.array(
        [cos(fieldra)*np.cos(fielddec), #x
         sin(fieldra)*np.cos(fielddec), #y
         sin(fielddec)])                #z
    
    # make the basis vectors for the fields of view
    # the "x" basis is easy, 90 d rotation of the x, y components
    focalx = np.zeros(field_vectors.shape)
    focalx[0] = -field_vectors[1]
    focalx[1] = field_vectors[0]

    # "y" by taking cross product of field vector and "x"
    focaly = np.cross(field_vectors, focalx, axis=0)

    # normalize
    focalx /= np.linalg.norm(focalx, axis=0)
    focaly /= np.linalg.norm(focaly, axis=0)
    
    # TODO: if fieldIDs are provided, match detections to field pointings
    # may or may not add, benefits are likely negligible

    # extend observation vectors to plane tangent to field pointings
    k = 1. / np.sum(field_vectors * observation_vectors, axis=0)
    #np.sum(field_vectors * field_vectors, axis=0) / np.sum(field_vectors * observation_vectors, axis=0)
    observation_vectors *= k
    
    observation_vectors -= field_vectors #

    # get observation vectors as combinations of focal vectors
    x = np.sum(observation_vectors * focalx, axis=0)
    y = np.sum(observation_vectors * focaly, axis=0)
            
    return x, y

#------------------------------------------------------------------------------
# DEPRECATED: will be removed in future update. 

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

    
    fieldra   = deg2rad(observations[ra_name_field])
    fielddec  = deg2rad(observations[dec_name_field])
    rotSkyPos = deg2rad(observations[rot_name_field])
    

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

        detectedObs.append(pd.Series(obsSelIndex[detected]))

    return detectedObs
    
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

        detectors_out += [np.array([yd, zd]).T]

    return np.array(detectors_out)

def xrot(p, θ):
    #rotation of a 3d vector around the x-axis
    p_out = np.zeros(p.shape)
    cosθ = cos(θ)
    sinθ = sin(θ)

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

    angles=np.arctan2(corner_rays[:,0], corner_rays[:,1])
    return np.array([x for x, y in sorted(zip(points, angles), key=lambda pair: pair[1])])

def HamiltonProduct(q1, q2):
    """where q1 and q2 are arrays of length 4 representing quaternions
    Not commutative."""

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
    #do rotation
    P_out = HamiltonProduct(Q, HamiltonProduct(P, Qinv))
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
    ϕ = -np.arctan2(zh2[2], zh2[1]) + 0.5 * np.pi
    
    return xrot(p2, ϕ)
