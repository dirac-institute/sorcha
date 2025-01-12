sorcha.modules.PPFootprintFilter
================================

.. py:module:: sorcha.modules.PPFootprintFilter


Attributes
----------

.. autoapisummary::

   sorcha.modules.PPFootprintFilter.deg2rad
   sorcha.modules.PPFootprintFilter.sin
   sorcha.modules.PPFootprintFilter.cos
   sorcha.modules.PPFootprintFilter.logger


Classes
-------

.. autoapisummary::

   sorcha.modules.PPFootprintFilter.Detector
   sorcha.modules.PPFootprintFilter.Footprint


Functions
---------

.. autoapisummary::

   sorcha.modules.PPFootprintFilter.distToSegment
   sorcha.modules.PPFootprintFilter.radec_to_tangent_plane
   sorcha.modules.PPFootprintFilter.radec_to_focal_plane


Module Contents
---------------

.. py:data:: deg2rad

.. py:data:: sin

.. py:data:: cos

.. py:data:: logger

.. py:function:: distToSegment(points, x0, y0, x1, y1)

   Compute the distance from each point to the line segment defined by
   the points (x0, y0) and (x1, y1).  Returns the distance in the same
   units as the points are specified in (radians, degrees, etc.). Uses planar
   geometry for the calculations (assuming small angular distances).

   :param points: Array of shape (2, n) describing the corners of the sensor.
   :type points: array
   :param x0: The x coordinate of the first end of the segment.
   :type x0: float
   :param y0: The y coordinate of the first end of the segment.
   :type y0: float
   :param x1: The x coordinate of the second end of the segment.
   :type x1: float
   :param y1: The y coordinate of the second end of the segment.
   :type y1: float

   :returns: **dist** -- Array of length n storing the distances.
   :rtype: array


.. py:function:: radec_to_tangent_plane(ra, dec, field_ra, field_dec)

   Converts ra and dec to xy on the plane tangent to image center, in the 2-d coordinate system where y is aligned with the meridian.

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



.. py:function:: radec_to_focal_plane(ra, dec, field_ra, field_dec, field_rot)

.. py:class:: Detector(points, ID=0, units='radians')

   Detector class


   .. py:attribute:: ID
      :value: 0



   .. py:attribute:: ra


   .. py:attribute:: dec


   .. py:attribute:: units
      :value: 'radians'



   .. py:attribute:: x


   .. py:attribute:: y


   .. py:attribute:: centerx


   .. py:attribute:: centery


   .. py:method:: ison(point, ε=10.0**(-11), edge_thresh=None, plot=False)

      Determines whether a point (or array of points) falls on the
      detector.

      :param point: Array of shape (2, n) for n points.
      :type point: array
      :param ϵ: Threshold for whether point is on detector. Default: 10.0 ** (-11)
      :type ϵ: float, optional
      :param edge_thresh: The focal plane distance (in arcseconds) from the detector's edge
                          for a point to be counted. Removes points that are too
                          close to the edge for source detection. Default = None
      :type edge_thresh: float, optional
      :param plot: Flag for whether to plot the detector and the point. Default = False
      :type plot: Boolean, optional

      :returns: **selectedidx** -- Indices of points in point array that fall on the sensor.
      :rtype: array



   .. py:method:: trueArea()

      Returns the area of the detector. Uses the same method as
      segmentedArea, but the test point is the mean of the corner coordinates.
      Will probably fail if the sensor is not convex.

      :param None.:

      :returns: **area** -- The area of the detector.
      :rtype: float



   .. py:method:: segmentedArea(point)

      Returns the area of the detector by calculating the area of each
      triangle segment defined by each pair of adjacent corners and a point
      inside the sensor.
      Fails if the point is not inside the sensor or if the sensor is not
      convex.

      :param point: Array of shape (2, n) for n points.
      :type point: array

      :returns: **area** -- The area of the detector.
      :rtype: float



   .. py:method:: sortCorners()

      Sorts the corners to be counterclockwise by angle from center of
      the detector. Modifies self.

      :param None.:

      :rtype: None.



   .. py:method:: rotateDetector(theta)

      Rotates a sensor around the origin of the coordinate system its
      corner locations are provided in.

      :param theta: Angle to rotate by, in radians.
      :type theta: float

      :returns: **Detector** -- New Detector instance.
      :rtype: Detector



   .. py:method:: rad2deg()

      Converts corners from radians to degrees.

      :param None.:

      :rtype: None.



   .. py:method:: deg2rad()

      Converts corners from degrees to radians.

      :param None.:

      :rtype: None.



   .. py:method:: plot(theta=0.0, color='gray', units='rad', annotate=False)

      Plots the footprint for an individual sensor. Currently not on the
      focal plane, just the sky coordinates. Relatively minor difference
      (width of footprint for LSST is <2.1 degrees), so should be fine for
      internal demonstration purposes, but not for confirming algorithms or
      for offical plots.

      :param theta: Aangle to rotate footprint by, radians or degrees. Default =0.0
      :type theta: float, optional
      :param color: Line color. Default = "gray"
      :type color: string, optional
      :param units: Units. Units is provided in ("deg" or "rad"). Default = 'rad'.
      :type units: string, optional
      :param annotate: Flag whether to annotate each sensor with its index in self.detectors.
                       Default = False
      :type annotate: Boolean

      :rtype: None.



.. py:class:: Footprint(path=None, detectorName='detector')

   Camera footprint class


   .. py:attribute:: detectors


   .. py:attribute:: N


   .. py:method:: plot(theta=0.0, color='gray', units='rad', annotate=False)

      Plots the footprint. Currently not on the focal plane, just the sky
      coordinates. Relatively minor difference (width of footprint for LSST
      is <2.1 degrees), so should be fine for internal demonstration
      purposes, but not for confirming algorithms or for offical plots.

      :param theta: Angle to rotate footprint by, radians or degrees. Default = 0.0
      :type theta: float, optional
      :param color: Line color. Default = "gray"
      :type color: string, optional
      :param units: Units theta is provided in ("deg" or "rad"). Default = "rad"
      :type units: string, optional
      :param annotate: Whether to annotate each sensor with its index in
                       self.detectors. Default = False
      :type annotate: boolean, optional

      :rtype: None.



   .. py:method:: applyFootprint(field_df, ra_name='RA_deg', dec_name='Dec_deg', field_name='FieldID', ra_name_field='fieldRA_deg', dec_name_field='fieldDec_deg', rot_name_field='fieldRotSkyPos_deg', edge_thresh=None)

      Determine whether detections fall on the sensors defined by the
      footprint. Also returns the an ID for the sensor a detection is made
      on.

      :param field_df: Dataframe containing detection information with pointings.
      :type field_df: Pandas dataframe
      :param ra_name:
                      "field_df" dataframe's column name for object's RA
                       for the given observation. Default = "RA_deg" [units: degrees]
      :type ra_name: string, optional
      :param dec_name:
                       "field_df" dataframe's column name for object's declination
                        for the given observation. Default = "Dec_deg" [units: dgrees]
      :type dec_name: string, optional
      :param ra_name_field:
                            "field_df" dataframe's column name for the observation field's RA
                             Default = "fieldRA_deg" [units: degrees]
      :type ra_name_field: string, optional
      :param dec_name_field:
                             "field_df" dataframe's column name for the observation field's declination
                              Default = "fieldDec_deg" [Units: degrees]
      :type dec_name_field: string, optional
      :param rot_name_field: "field_df" dataframe's column name for the observation field's rotation angle
                             Default = "fieldRotSkyPos_deg" [Units: degrees]
      :type rot_name_field: string, optional
      :param edge_thresh: An angular threshold in arcseconds for dropping pixels too close to the edge.
                          Default  = None
      :type edge_thresh: float, optional

      :returns: * **detected** (*array*) -- Indices of rows in field_df which fall on the sensor(s).
                * **detectorID** (*array*) -- Index corresponding to a detector in self.detectors for each entry in detected.



