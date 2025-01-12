sorcha.modules.PPMiniDifi
=========================

.. py:module:: sorcha.modules.PPMiniDifi


Functions
---------

.. autoapisummary::

   sorcha.modules.PPMiniDifi.haversine_np
   sorcha.modules.PPMiniDifi.hasTracklet
   sorcha.modules.PPMiniDifi.trackletsInNights
   sorcha.modules.PPMiniDifi.discoveryOpportunities
   sorcha.modules.PPMiniDifi.linkObject
   sorcha.modules.PPMiniDifi.linkObservations


Module Contents
---------------

.. py:function:: haversine_np(lon1, lat1, lon2, lat2)

   Calculate the great circle distance between two points
   on the earth (specified in decimal degrees)

   :param lon1: longitude of point 1
   :type lon1: float or array of floats
   :param lat1: latitude of point 1
   :type lat1: float or array of floats
   :param lon2: longitude of point 2
   :type lon2: float or array of floats
   :param lat1: latitude of point 1
   :type lat1: float or array of floats

   :returns: * *float or array of floats*
             * **Great distance between the two points [Units** (*Decimal degrees]*)

   .. rubric:: Notes

   All args must be of equal length.

   Because SkyCoord is slow AF.


.. py:function:: hasTracklet(mjd, ra, dec, maxdt_minutes, minlen_arcsec)

   Given a set of observations in one night, calculate it has
   at least onedetectable tracklet.

   :param mjd: Modified Julian date time
   :type mjd: float or array of floats
   :param ra: Object's RA at given mjd  [Units: degrees]
   :type ra: float or array of floats
   :param dec: Object's dec at given mjd  [Units: degrees]
   :type dec: float or array of floats
   :param maxdt_minutes: Maximum allowable time between observations [Units: minutes]
   :type maxdt_minutes: float
   :param minlen_arcsec: Minimum allowable distance separation between observations [Units: arcsec]
   :type minlen_arcsec: float

   :returns: * *boolean*
             * *True if tracklet can be made else False*


.. py:function:: trackletsInNights(night, mjd, ra, dec, maxdt_minutes, minlen_arcsec)

   Calculate, for a given set of observations sorted by observation time,
   whether or not it has at least one discoverable tracklet in each night.

   :param night: Array of the integer night corresponding to each observation
   :type night: float or array of floats
   :param mjd: Modified Julian date time
   :type mjd: float or array of floats
   :param ra: Object's RA at given mjd  [Units: degrees]
   :type ra: float or array of floats
   :param dec: Object's dec at given mjd  [Units: degrees]
   :type dec: float or array of floats
   :param maxdt_minutes: Maximum allowable time between observations [Units: minutes]
   :type maxdt_minutes: float
   :param minlen_arcsec: Minimum allowable distance separation between observations [Units: arcsec]
   :type minlen_arcsec: float

   :returns: * **nights** (*float or array of floats*) -- Numpy array of the unique nights in the set of observations
             * **hasTrk** (*boolean or array of booleans*) -- Array denoting if each night has a discoverable tracklet


.. py:function:: discoveryOpportunities(nights, nightHasTracklets, window, nlink, p, rng)

   Find all nights where a trailing window of <window> nights (including the
   current night) has at least <nlink> tracklets to constitute a discovery.

   :param nights: Array of the integer night corresponding to each observation
   :type nights: float or array of floats
   :param nightHasTracklets: List of nights that have tracklets within them
   :type nightHasTracklets: list of booleans
   :param window: Number of tracklets required with <= this window to complete a detection
   :type window: float
   :param nlink: Number of tracklets required to form detection
   :type nlink: float
   :param p: SSP detection efficiency, or what fraction of objects are successfuly linked
   :type p: float
   :param rng: PGC64 generator object to determine which objects to drop
   :type rng: numpy RNG generator object

   :returns: * **discIdx** (*float*) -- The index of where in the observation array the object is reported as discovered
             * **disc** (*list of floats*) -- List of MJD dates where the object is discoverable


.. py:function:: linkObject(obsv, seed, maxdt_minutes, minlen_arcsec, window, nlink, p, night_start_utc_days)

   For a set of observations of a single object, calculate if there are any tracklets,
   if there are enough tracklets to form a discovery window, and then report back all of
   those successful discoveries.

   :param obsv: Array of observations for one object, of the format:
                ssObjectId : str
                    Unique ID for the Solar System object
                diaSourceId : float
                    Unique ID for the observation
                midPointTai : float
                    Time for the observation midpoint (MJD)
                ra : float
                    RA of the object (J2000)
                decl : float
                    Declination of the object (J2000)
   :type obsv: numpy array
   :param seed: Initial seed per object to keep observations deterministic for multithreading
   :type seed: float
   :param maxdt_minutes: Maximum allowable time between observations [Units: minutes]
   :type maxdt_minutes: float
   :param minlen_arcsec: Minimum allowable distance separation between observations [Units: arcsec]
   :type minlen_arcsec: float
   :param window: Number of tracklets required with <= this window to complete a detection
   :type window: float
   :param nlink: Number of tracklets required to form detection
   :type nlink: float
   :param p: SSP detection efficiency, or what fraction of objects are successfuly linked
   :type p: float
   :param night_start_utc_days: The UTC time of local noon at the observatory
   :type night_start_utc_days: float

   :returns: * **discoveryObservationId** (*float*) -- The ID of the observation that triggered the successful linking
             * **discoverySubmissionDate** (*float*) -- The night at which the discovery is first submitted
             * **discoveryChances** (*float*) -- The number of chances for discovery of the object


.. py:function:: linkObservations(obsv, seed, objectId='ssObjectId', sourceId='diaSourceId', mjdTime='midPointTai', ra='ra', dec='decl', **config)

   Ingesting a set of observations for one or more objects, determine if each object
   would be discovered by the SSP pipeline based on tracklet forming and linking.

   :param obsv: Array of observations for each object, of the format:
                ssObjectId : str
                    Unique ID for the Solar System object
                diaSourceId : float
                    Unique ID for the observation
                midPointTai : float
                    Time for the observation midpoint (MJD)
                ra : float
                    RA of the object (J2000)
                decl : float
                    Declination of the object (J2000)
   :type obsv: numpy array
   :param seed: Initial seed per object to keep observations deterministic for multithreading
   :type seed: float
   :param objectId: Column name for object ID's in observations dataframe
   :type objectId: string
   :param sourceId: Column name for observation ID's in observations dataframe
   :type sourceId: string
   :param mjdTime: Column name for MJD's in observations dataframe
   :type mjdTime: string
   :param ra: Column name for object RA's in observations dataframe
   :type ra: string
   :param dec: Column name for object Dec's in observations dataframe
   :type dec: string
   :param \*\*config: Dictionary containing configuration file variables

   :returns: **obj** --

             Array with one row per detected object, of the format:
                 ssObjectId : str
                     Unique ID for the Solar System object
                 discoveryObservationId : float
                     Unique ID for the observation
                 discoverySubmissionDate : float
                     The night at which the discovery is first submitted
                 discoveryChances : float
                     The number of chances for discovery of the object
   :rtype: numpy array


