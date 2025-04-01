import numpy as np
from numba import njit


@njit(cache=True)
def haversine_np(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)

    Parameters
    -----------
    lon1 : float or array of floats
        longitude of point 1

    lat1 : float or array of floats
        latitude of point 1

    lon2 : float or array of floats
        longitude of point 2

    lat1 : float or array of floats
        latitude of point 1

    Returns
    --------
        : float or array of floats
        Great distance between the two points [Units: Decimal degrees]

    Notes
    ------
    All args must be of equal length.

    Because SkyCoord is slow AF.

    """
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = np.sin(dlat / 2.0) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2.0) ** 2
    c = 2 * np.arcsin(np.sqrt(a))
    return np.degrees(c)


@njit(cache=True)
def hasTracklet(mjd, ra, dec, maxdt_minutes, minlen_arcsec, min_observations):
    """
    Given a set of observations in one night, calculate it has
    at least onedetectable tracklet.

    Parameters
    -----------
    mjd : float or array of floats
        Modified Julian date time

    ra : float or array of floats
        Object's RA at given mjd  [Units: degrees]

    dec : float or array of floats
        Object's dec at given mjd  [Units: degrees]

    maxdt_minutes: float
        Maximum allowable time between observations [Units: minutes]

    minlen_arcsec : float
        Minimum allowable distance separation between observations [Units: arcsec]

    min_observations (int):
        the minimum number of observations in a night required to form a tracklet.

    Returns
    --------
        : boolean
        True if tracklet can be made else False

    """
    ## a tracklet must be longer than some minimum separation (0.5arcsec)
    ## and shorter than some maximum time (90 minutes). We find
    ## tracklets by taking all observations in a night and computing
    ## all of theirs pairwise distances, then selecting on that.
    nobs = len(ra)
    if nobs >= 1 and min_observations == 1:  # edge case when 1 observation is needed for a tracklet
        return True
    if nobs < 2:
        return False

    maxdt = maxdt_minutes / (60 * 24)
    minlen = minlen_arcsec / 3600
    detection_pair_count = 0  # counting number of detection pairs

    for i in range(nobs):
        for j in range(nobs):
            diff = mjd[i] - mjd[j]
            if diff > 0 and diff < maxdt:
                sep = haversine_np(ra[i], dec[i], ra[j], dec[j])
                if sep > minlen:
                    detection_pair_count += 1
    if detection_pair_count >= (min_observations - 1):
        return True
    else:
        return False


@njit(cache=True)
def trackletsInNights(night, mjd, ra, dec, maxdt_minutes, minlen_arcsec, min_observations):
    """
    Calculate, for a given set of observations sorted by observation time,
    whether or not it has at least one discoverable tracklet in each night.

    Parameters
    -----------
    night : float or array of floats
        Array of the integer night corresponding to each observation

    mjd : float or array of floats
        Modified Julian date time

    ra : float or array of floats
        Object's RA at given mjd  [Units: degrees]

    dec : float or array of floats
        Object's dec at given mjd  [Units: degrees]

    maxdt_minutes: float
        Maximum allowable time between observations [Units: minutes]

    minlen_arcsec : float
        Minimum allowable distance separation between observations [Units: arcsec]

    min_observations (int):
        the minimum number of observations in a night required to form a tracklet.

    Returns
    --------
    nights : float or array of floats
        Numpy array of the unique nights in the set of observations

    hasTrk : boolean or array of booleans
        Array denoting if each night has a discoverable tracklet

    """

    nights = np.unique(night)
    hasTrk = np.zeros(len(nights), dtype="bool")

    i = np.searchsorted(night, nights, side="right")

    # for each night, test if it has a tracklet
    b = 0
    for k, e in enumerate(i):
        hasTrk[k] = hasTracklet(mjd[b:e], ra[b:e], dec[b:e], maxdt_minutes, minlen_arcsec, min_observations)
        b = e

    return nights, hasTrk


@njit(cache=True)
def discoveryOpportunities(nights, nightHasTracklets, window, nlink, p, rng):
    """
    Find all nights where a trailing window of <window> nights (including the
    current night) has at least <nlink> tracklets to constitute a discovery.

    Parameters
    -----------
    nights : float or array of floats
        Array of the integer night corresponding to each observation

    nightHasTracklets : list of booleans
        List of nights that have tracklets within them

    window : float
        Number of tracklets required with <= this window to complete a detection

    nlink : float
        Number of tracklets required to form detection

    p : float
        SSP detection efficiency, or what fraction of objects are successfuly linked

    rng : numpy RNG generator object
        PGC64 generator object to determine which objects to drop

    Returns
    --------
    discIdx : float
        The index of where in the observation array the object is reported as discovered

    disc : list of floats
        List of MJD dates where the object is discoverable

    """

    if nlink > 1:
        # algorithm: create an array of length [0 ... num_nights],
        #    representing the nights where there are tracklets.
        #    populate it with the tracklets (1 for each night where)
        #    there's a detectable tracklet. Then convolve it with a
        #    <window>-length window (we do this with .cumsum() and
        #    then subtracting the shifted array -- basic integration)
        #    And then find nights where the # of tracklets >= nlink
        #
        n0, n1 = nights.min(), nights.max() + window
        nlen = n1 - n0 + 1
        arr = np.zeros(nlen, dtype="i8")
        arr[nights - n0] = nightHasTracklets
        arr = arr.cumsum()
        arr[window:] -= arr[:-window].copy()
        disc = (arr >= nlink).nonzero()[0] + n0

        # we're not done yet. the above gives us a list of nights when
        #    the object is discoverable, but this involves many duplicates
        #    (e.g., if there are tracklets on nights 3, 4, and 5, the object)
        #    will be discoverable on nights 5 through 17. What we really
        #    need is a list of nights with unique discovery opportunities.
        # algorithm: we essentially do the same as above, but instead of
        #    filling an array with "1", for each night with a tracklet, we
        #    fill it with a random number. The idea is that when we do the
        #    convolution, these random numbers will sum up to unique sums
        #    every time the same three (or more) tracklets make up for a
        #    discovery opportunity. We then find unique discovery
        #    opportunities by filtering on when the sums change.
        arr2 = np.zeros(nlen)
        arr2[nights - n0] = nightHasTracklets
        arr2[arr2 != 0] = np.random.rand(np.count_nonzero(nightHasTracklets))
        arr2 = arr2.cumsum()
        arr2[window:] -= arr2[:-window].copy()
        arr2 = arr2[disc - n0]
        arr2[1:] -= arr2[:-1].copy()
        disc = disc[arr2.nonzero()]
    else:
        # Special-case nlink=1 case: if there's no linking to perform,
        # then the window doesn't matter and each night with a tracklet
        # is considered a separate discovery opportunity
        disc = nights[nightHasTracklets]

    # finally, at every discovery opportunity we have a probability <p>
    # to discover the object. Figure out when we'll discover it.
    discN = (rng.uniform(size=len(disc)) < p).nonzero()[0]
    discIdx = discN[0] if len(discN) else -1

    return discIdx, disc


def linkObject(
    obsv, seed, maxdt_minutes, minlen_arcsec, min_observations, window, nlink, p, night_start_utc_days
):
    """
    For a set of observations of a single object, calculate if there are any tracklets,
    if there are enough tracklets to form a discovery window, and then report back all of
    those successful discoveries.

    Parameters
    -----------
    obsv : numpy array
        Array of observations for one object, of the format:
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

    seed : float
        Initial seed per object to keep observations deterministic for multithreading

    maxdt_minutes : float
        Maximum allowable time between observations [Units: minutes]

    minlen_arcsec : float
        Minimum allowable distance separation between observations [Units: arcsec]

    min_observations (int):
        the minimum number of observations in a night required to form a tracklet.

    window : float
        Number of tracklets required with <= this window to complete a detection

    nlink : float
        Number of tracklets required to form detection

    p : float
        SSP detection efficiency, or what fraction of objects are successfuly linked

    night_start_utc_days : float
        The UTC time of local noon at the observatory

    Returns
    --------
    discoveryObservationId : float
        The ID of the observation that triggered the successful linking

    discoverySubmissionDate : float
        The night at which the discovery is first submitted

    discoveryChances : float
        The number of chances for discovery of the object

    """
    discoveryObservationId = 0xFFFF_FFFF_FFFF_FFFF
    discoverySubmissionDate = np.nan
    discoveryChances = 0

    if len(obsv):
        i = np.argsort(obsv["midPointTai"])
        obsv = obsv[i]

        # compute the night of observation
        tshift = obsv["midPointTai"] - night_start_utc_days
        night = tshift.astype(int)
        phased = tshift - night
        assert np.all(
            (0.1 < phased) & (phased < 0.9)
        )  # quick check that we didn't screw up the night boundary
        mjd, ra, dec, diaSourceId = obsv["midPointTai"], obsv["ra"], obsv["decl"], obsv["diaSourceId"]

        # compute a random seed for this object, based on the hash of its (sorted) data
        # this keeps all outputs deterministics across the full catalog in multithreading
        # scenarios (where different objects are distributed to different threads)
        # note: becasue np.random.seed expects a uint32, we truncate the hash to 4 bytes.
        import hashlib

        seed += int.from_bytes(hashlib.sha256(ra.tobytes()).digest()[-4:], "little", signed=False)
        seed %= 0xFFFF_FFFF
        rng = np.random.default_rng(seed)

        nights, hasTrk = trackletsInNights(
            night, mjd, ra, dec, maxdt_minutes, minlen_arcsec, min_observations
        )
        discIdx, discNights = discoveryOpportunities(nights, hasTrk, window, nlink, p, rng)
        if discIdx != -1:
            discoveryChances = len(discNights)
            discoverySubmissionDate = discNights[discIdx]

            # find the first observation in the discovery window.
            # we'll (somewhat arbitrarily) define this as the "asterisk" observation.
            # in reality, we'll run precovery on linkages so the asterisk observation
            # will sometimes be (much) earlier.
            i, j = np.searchsorted(night, [discoverySubmissionDate - window + 1, discoverySubmissionDate + 1])
            k = i + np.argmin(obsv["midPointTai"][i:j])
            discoveryObservationId = obsv["diaSourceId"][k]
            # make sure our asterisk observation is within the trailing window.
            assert (
                night[k] + window > discoverySubmissionDate
            ), f"{obsv['night'][k]=}, {window=}, {discoverySubmissionDate=}"

    return discoveryObservationId, discoverySubmissionDate, discoveryChances


def linkObservations(
    obsv,
    seed,
    objectId="ssObjectId",
    sourceId="diaSourceId",
    mjdTime="midPointTai",
    ra="ra",
    dec="decl",
    **config,
):
    """
    Ingesting a set of observations for one or more objects, determine if each object
    would be discovered by the SSP pipeline based on tracklet forming and linking.

    Parameters
    -----------
    obsv : numpy array
        Array of observations for each object, of the format:
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

    seed : float
        Initial seed per object to keep observations deterministic for multithreading

    objectId : string
        Column name for object ID's in observations dataframe

    sourceId : string
        Column name for observation ID's in observations dataframe

    mjdTime : string
        Column name for MJD's in observations dataframe

    ra : string
        Column name for object RA's in observations dataframe

    dec : string
        Column name for object Dec's in observations dataframe

    **config
        Dictionary containing configuration file variables

    Returns
    --------
    obj : numpy array
        Array with one row per detected object, of the format:
            ssObjectId : str
                Unique ID for the Solar System object
            discoveryObservationId : float
                Unique ID for the observation
            discoverySubmissionDate : float
                The night at which the discovery is first submitted
            discoveryChances : float
                The number of chances for discovery of the object

    """

    # create the "group by" splits for individual objects
    # See https://stackoverflow.com/a/43094244 for inspiration for this code
    i = np.argsort(obsv[objectId], kind="stable")
    ssObjects, idx = np.unique(obsv[objectId][i], return_index=True)
    splits = np.split(i, idx[1:])

    # "link"
    # pre-initialize output columns
    obj = np.zeros(
        len(splits),
        dtype=np.dtype(
            [
                ("ssObjectId", obsv[objectId].dtype),
                ("discoveryObservationId", "u8"),
                ("discoverySubmissionDate", "f8"),
                ("discoveryChances", "i4"),
            ]
        ),
    )

    # linking test for each object
    for k, obsv_indices in enumerate(splits):
        # extract the observations of this object into a ndarray of expected
        # format and column names
        thisObsv = obsv[[sourceId, mjdTime, ra, dec]][obsv_indices]
        thisObsv.dtype.names = ["diaSourceId", "midPointTai", "ra", "decl"]

        obj[k] = (ssObjects[k], *linkObject(thisObsv, seed, **config))

    return obj
