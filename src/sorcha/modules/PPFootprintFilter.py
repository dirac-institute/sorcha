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


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

deg2rad = np.radians
sin = np.sin
cos = np.cos


class Detector:
    def __init__(self, points, ID=0, units="radians"):
        """
        Initiates a detector object.

        Parameters:
        -----------
        points (array): array of shape (2, n) describing the corners of the sensor.

        ID (int): an integer ID for the sensor.

        units (string): units that points is provided in, "radians" or "degrees" from
                        center of the focal plane.

        Returns:
        ----------
        detector (Detector): a detector instance.

        """

        # points  --->   should be shape dims, n points
        self.ID = ID
        self.ra = points[0]
        self.dec = points[1]
        self.units = units

        if units == "degrees" or units == "deg":
            self.deg2rad()

        # generate focal plane coordinates
        # convert to xyz on unit sphere
        z = np.cos(self.ra) * np.cos(self.dec)  # x
        self.x = sin(self.ra) * np.cos(self.dec)  # y
        self.y = sin(self.dec)

        # project to focal plane
        self.x /= z
        self.y /= z

        # calculate centroid
        self.centerx = np.sum(self.x) / len(self.x)
        self.centery = np.sum(self.y) / len(self.y)

    def ison(self, point, ϵ=10.0 ** (-11), plot=False):
        """
        Determines whether a point (or array of points) falls on the
        detector.

        Parameters:
        -----------
        point (array): array of shape (2, n) for n points.

        ϵ (float): threshold for whether point is on detector.

        plot (Boolean): whether to plot the detector and the point.

        Returns:
        ----------
        ison (array): indices of points in point array that fall on the sensor.
        """

        # points needs to be shape 2,n
        # if single point, needs to be an array of single element arrays

        # check whether point is in circle bounding the detector
        r2 = np.max((self.x - self.centerx) ** 2 + (self.y - self.centery) ** 2)
        selectedidx = np.where((point[0] - self.centerx) ** 2 + (point[1] - self.centery) ** 2 <= r2)[0]

        selected = point[:, selectedidx]
        xselected = point[0][selectedidx]
        yselected = point[1][selectedidx]

        # check whether selected fall on the detector
        # compare true area to the segmented area

        detectedidx = np.where(np.abs(self.segmentedArea(selected) - self.trueArea()) <= ϵ)[0]

        if plot:
            x = xselected[detectedidx]
            y = yselected[detectedidx]

            plt.scatter(x, y, color="red", s=3.0)

        return selectedidx[detectedidx]

    def trueArea(self):
        """
        Returns the area of the detector. Uses the same method as
        segmentedArea, but the test point is the mean of the corner coordinates.
        Will probably fail if the sensor is not convex.

        Parameters:
        -----------
        None.

        Returns:
        ----------
        area (float): the area of the detector.

        """
        x = self.x - self.centerx
        y = self.y - self.centery

        xrolled = np.roll(x, 1)
        yrolled = np.roll(y, 1)

        area = 0.5 * np.sum(np.abs(x * yrolled - y * xrolled))

        return area

    def segmentedArea(self, point):
        """
        Returns the area of the detector by calculating the area of each
        triangle segment defined by each pair of adjacent corners and a point
        inside the sensor.
        Fails if the point is not inside the sensor or if the sensor is not
        convex.

        Parameters:
        -----------
        None.

        Returns:
        ----------
        area (float): the area of the detector.

        """

        # so that both a single and many points work
        ncorners = self.x.shape[0]

        if len(point.shape) == 1:
            x = self.x - point[0]
            y = self.y - point[1]

        else:
            x = (np.zeros((ncorners, point.shape[1])).T + self.x).T - point[0]
            y = (np.zeros((ncorners, point.shape[1])).T + self.y).T - point[
                1
            ]  # copy over an array to make broadcasting work

        xrolled = np.roll(x, 1, axis=0)
        yrolled = np.roll(y, 1, axis=0)
        area = []

        for i in range(len(self.x)):
            area.append(np.abs(x[i] * yrolled[i] - y[i] * xrolled[i]))

        return 0.5 * (np.sum(area, axis=0))

    def sortCorners(self):
        """
        Sorts the corners to be counterclockwise by angle from center of
        the detector. Modifies self.

        Parameters:
        -----------
        None.

        Returns:
        ----------
        None.

        """

        # convert corners to angles (radians)
        θ = np.arctan2(self.y - self.centery, self.x - self.centerx)

        neworder = np.argsort(θ)
        self.x = self.x[neworder]
        self.y = self.y[neworder]

    def rotateDetector(self, θ):
        """
        Rotates a sensor around the origin of the coordinate system its
        corner locations are provided in.

        Parameters:
        -----------
        θ (float): angle to rotate by, in radians.

        Returns:
        ----------
        Detector: new Detector instance.

        """

        # convert rotation angle to complex number
        q = cos(θ) + sin(θ) * 1.0j

        # convert points to complex numbers
        coords = self.x + self.y * 1.0j

        # rotate
        newcoords = coords * q
        return Detector(np.array((np.real(newcoords), np.imag(newcoords))), self.ID)

    def rad2deg(self):
        """
        Converts corners from radians to degrees.

        Parameters:
        -----------
        None.

        Returns:
        ----------
        None.

        """

        if self.units == "radians":
            self.x = np.degrees(self.x)
            self.y = np.degrees(self.y)
            self.centerx = np.degrees(self.centerx)
            self.centery = np.degrees(self.centery)
            self.units = "degrees"
        else:
            print("Units are already degrees")

    def deg2rad(self):
        """
        Converts corners from degrees to radians.

        Parameters:
        -----------
        None.

        Returns:
        ----------
        None.

        """

        if self.units == "degrees":
            self.x = np.radians(self.x)
            self.y = np.radians(self.y)
            self.centerx = np.radians(self.centerx)
            self.centery = np.radians(self.centery)
            self.units = "radians"
        else:
            print("Units are already radians")

    def plot(self, θ=0.0, color="gray", units="rad", annotate=False):
        """
        Plots the footprint for an individual sensor. Currently not on the
        focal plane, just the sky coordinates. Relatively minor difference
        (width of footprint for LSST is <2.1 degrees), so should be fine for
        internal demonstration purposes, but not for confirming algorithms or
        for offical plots.

        Parameters:
        -----------
        θ (float): angle to rotate footprint by, radians or degrees.

        color  (string): line color.

        units (string): units θ is provided in ("deg" or "rad").

        annotate (Boolean): whether to annotate each sensor with its index in
        self.detectors.

        Returns:
        ----------
        None.

        """

        detector = self.rotateDetector(θ)
        if units == "deg":
            detector.rad2deg()
        nd = len(self.x)
        x = np.zeros(nd + 1)
        x[0:nd] = detector.x
        x[-1] = x[0]
        y = np.zeros(nd + 1)
        y[0:nd] = detector.y
        y[-1] = y[0]
        plt.plot(x, y, color=color)

        if annotate is True:
            plt.annotate(str(detector.ID), (detector.centerx, detector.centery))


class Footprint:
    def __init__(self, path, detectorName="detector"):
        """
        Initiates a Footprint object.

        Parameters:
        -----------
        path (string): path to a .csv file containing detector corners.

        detectorName (string): name of column in detector file indicating to
        which sensor a corner belongs.

        Returns:
        ----------
        Footprint: Footprint object for the provided sensors.

        """

        # file should be a .csv (and should be actually comma seperated)
        # the center of the camera should be the origin
        allcornersdf = pd.read_csv(path)

        self.detectors = [
            Detector(
                np.array(
                    (
                        allcornersdf.loc[allcornersdf[detectorName] == i, "x"],
                        allcornersdf.loc[allcornersdf[detectorName] == i, "y"],
                    )
                ),
                i,
            )
            for i in range(len(allcornersdf[detectorName].unique()))
        ]

        self.N = len(self.detectors)

        # sort the corners of each detector
        for i in range(self.N):
            self.detectors[i].sortCorners()

    def plot(self, θ=0.0, color="gray", units="rad", annotate=False):
        """
        Plots the footprint. Currently not on the focal plane, just the sky
        coordinates. Relatively minor difference (width of footprint for LSST
        is <2.1 degrees), so should be fine for internal demonstration
        purposes, but not for confirming algorithms or for offical plots.

        Parameters:
        -----------
        θ (float): angle to rotate footprint by, radians or degrees.

        color  (string): line color.

        units (string): units θ is provided in ("deg" or "rad").

        annotate (Boolean): whether to annotate each sensor with its index in
        self.detectors.

        Returns:
        ----------
        None.

        """

        for i in range(self.N):
            self.detectors[i].plot(θ=θ, color=color, units=units, annotate=annotate)

    def applyFootprint(
        self,
        field_df,
        ra_name="AstRA(deg)",
        dec_name="AstDec(deg)",
        field_name="FieldID",
        ra_name_field="fieldRA",
        dec_name_field="fieldDec",
        rot_name_field="rotSkyPos",
    ):
        """
        Determine whether detections fall on the sensors defined by the
        footprint. Also returns the an ID for the sensor a detection is made
        on.

        Parameters:
        -----------
        field_df (Pandas dataframe): dataframe containing detection information with pointings.

        *_name (string): column names for object RA and Dec and field name.

        *_name_field (string): column names for field RA and Dec and rotation.

        Returns:
        ----------
        detected (array): indices of rows in oifDF which fall on the sensor(s).

        detectorID  (array): index corresponding to a detector in
        self.detectors for each entry in detected.

        """

        # convert detections to xyz on unit sphere
        ra = deg2rad(field_df[ra_name])
        dec = deg2rad(field_df[dec_name])

        # convert field pointings to xyz on unit sphere
        fieldra = deg2rad(field_df[ra_name_field])
        fielddec = deg2rad(field_df[dec_name_field])
        rotSkyPos = deg2rad(field_df[rot_name_field])

        # quaternion method has been removed. uses direct projection method
        # (no rotation on 3d unit sphere):
        x, y = radec2focalplane(ra, dec, fieldra, fielddec)

        # apply field rotation
        # first convert to complex numbers
        # maybe do this in the focal plane function?
        observations_complex = x + y * 1.0j
        rotation = np.exp(-rotSkyPos * 1.0j)

        observations_complex *= rotation
        x = np.real(observations_complex)
        y = np.imag(observations_complex)

        plt.scatter(x, y, s=3.0)
        points = np.array((x, y))

        # check whether they land on any of the detectors
        i = 0
        detected = []
        detectorId = []
        for detector in self.detectors:
            if True:
                stuff = detector.ison(points)
                detected.append(stuff)
                detectorId.append([i] * len(stuff))
                i += 1

        return np.concatenate(detected), np.concatenate(detectorId)


def radec2focalplane(ra, dec, fieldra, fielddec, fieldID=None):
    """
    Converts ra and dec to xy on the focal plane. Projects all pointings to
    the same focal plane, but does not account for field rotation. Maintains
    alignment with the meridian passing through the field center.

    Parameters:
    -----------
    ra (float/array of floats): observation Right Ascension, radians.

    dec (float/array of floats): observation Declination, radians.

    fieldra (float/array of floats): field pointing Right Ascension, radians.

    fielddec (float/array of floats): field pointing Declination, radians.

    fieldID (float/array of floats): Field ID, optional.

    Returns:
    ----------
    x, y (float/array of floats): Coordinates on the focal plane, radians projected
    to the plane tangent to the unit sphere.

    """

    # convert to cartesian coordiantes on unit sphere
    observation_vectors = np.array([cos(ra) * np.cos(dec), sin(ra) * np.cos(dec), sin(dec)])  # x  # y  # z

    field_vectors = np.array(
        [cos(fieldra) * np.cos(fielddec), sin(fieldra) * np.cos(fielddec), sin(fielddec)]  # x  # y
    )  # z

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
    k = 1.0 / np.sum(field_vectors * observation_vectors, axis=0)
    # np.sum(field_vectors * field_vectors, axis=0) / np.sum(field_vectors * observation_vectors, axis=0)
    observation_vectors *= k

    observation_vectors -= field_vectors

    # get observation vectors as combinations of focal vectors
    x = np.sum(observation_vectors * focalx, axis=0)
    y = np.sum(observation_vectors * focaly, axis=0)

    return x, y
