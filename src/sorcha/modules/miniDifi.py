#!/usr/bin/env python

import numpy as np
from numba import njit


@njit(cache=True)
def haversine_np(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)

    All args must be of equal length.

    Because SkyCoord is slow AF.

    """
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = np.sin(dlat / 2.0) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2.0) ** 2
    c = 2 * np.arcsin(np.sqrt(a))
    return np.degrees(c)


# Construct a list of nights that have detectable tracklets
@njit(cache=True)
def hasTracklet(mjd, ra, dec, maxdt_minutes, minlen_arcsec):
    """
    Given a set of observations in one night, calculate it has at least one
    detectable tracklet.

    Inputs: numpy arrays of mjd (time, days), ra (degrees), dec(degrees).

    Output: True or False
    """
    ## a tracklet must be longer than some minimum separation (1arcsec)
    ## and shorter than some maximum time (90 minutes). We find
    ## tracklets by taking all observations in a night and computing
    ## all of theirs pairwise distances, then selecting on that.
    nobs = len(ra)
    if nobs < 2:
        return False

    maxdt = maxdt_minutes / (60 * 24)
    minlen = minlen_arcsec / 3600

    for i in range(nobs):
        for j in range(nobs):
            diff = mjd[i] - mjd[j]
            if diff > 0 and diff < maxdt:
                sep = haversine_np(ra[i], dec[i], ra[j], dec[j])
                if sep > minlen:
                    return True

    return False


@njit(cache=True)
def trackletsInNights(night, mjd, ra, dec, maxdt_minutes, minlen_arcsec):
    # given a table of observations SORTED BY OBSERVATION TIME (!)
    # of a single object, compute for each night whether it has
    # at least one discoverable tracklet.
    #
    # Returns: (nights, hasTrk), two ndarrays where the first is a
    #          list of unique nights, and hasTrk is a bool array
    #          denoting if it has or has not a discoverable tracklet.

    nights = np.unique(night)
    hasTrk = np.zeros(len(nights), dtype="bool")

    i = np.searchsorted(night, nights, side="right")

    # for each night, test if it has a tracklet
    b = 0
    for k, e in enumerate(i):
        hasTrk[k] = hasTracklet(mjd[b:e], ra[b:e], dec[b:e], maxdt_minutes, minlen_arcsec)
        b = e

    return nights, hasTrk


@njit(cache=True)
def discoveryOpportunities(nights, nightHasTracklets, window, nlink, p, rng):
    # Find all nights where a trailing window of <window> nights
    # (including the current night) has at least <nlink> tracklets.
    #
    # algorithm: create an array of length [0 ... num_nights],
    #    representing the nights where there are tracklets.
    #    populate it with the tracklets (1 for each night where)
    #    there's a detectable tracklet. Then convolve it with a
    #    <window>-length window (we do this with .cumsum() and
    #    then subtracting the shifted array -- basic integration)
    #    And then find nights where the # of tracklets >= nlink
    #
    n0, n1 = nights.min(), nights.max()
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
    arr2[nights - n0] = rng.uniform(size=len(nights))
    arr2 = arr2.cumsum()
    arr[window:] -= arr[:-window].copy()
    arr2 = arr2[disc - n0]
    arr2[1:] -= arr2[:-1].copy()
    disc = disc[arr2.nonzero()]

    # finally, at every discovery opportunity we have a probability <p>
    # to discover the object. Figure out when we'll discover it.
    discN = (rng.uniform(size=len(disc)) < p).nonzero()[0]
    discIdx = discN[0] if len(discN) else -1

    return discIdx, disc


def linkObject(obsv, seed, maxdt_minutes, minlen_arcsec, window, nlink, p, night_start_utc_days):
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

        nights, hasTrk = trackletsInNights(night, mjd, ra, dec, maxdt_minutes, minlen_arcsec)
        discIdx, discNights = discoveryOpportunities(nights, hasTrk, window, nlink, p, rng)
        if discIdx != -1:
            discoveryChances = len(discNights)
            discoverySubmissionDate = discNights[discIdx]

            # find the first observation on the discovery date
            i, j = np.searchsorted(night, [discoverySubmissionDate, discoverySubmissionDate + 1])
            k = i + np.argmin(mjd[i:j])
            discoveryObservationId = diaSourceId[k]

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
    # expects a ndarray of observations, with the following columns:
    #
    #  - objectId: a unique ID of the solar system object
    #  - sourceId: a unique ID of the observation
    #  - mjdTime:  time of the observation (midpoint), MJD, UTC
    #  - ra:       R.A. of the observation (J2000)
    #  - dec:      Declination of the observation (J2000)
    #
    # The names of these columns can be overridden with optional arguments
    #
    # output: an ndarray with one row per /detected/ object, containing the
    #         following columns:
    #
    #  - ssObjectId:              the objectId of this object
    #  - discoveryObservationId:  the sourceId of the observation that triggered a succesful linkage
    #  - discoverySubmissionDate: the submission date of the
    #  - discoveryChances:        the number of discovery chances for this objects
    #

    # update the default configuration
    _cfg, config = config, default_config.copy()
    config.update(_cfg)

    # group-by
    import time

    start = time.perf_counter()
    # create the "group by" splits for individual objects
    # See https://stackoverflow.com/a/43094244 for inspiration for this code
    i = np.argsort(obsv[objectId], kind="stable")
    ssObjects, idx = np.unique(obsv[objectId][i], return_index=True)
    splits = np.split(i, idx[1:])
    ##    print(f"{len(ssObjects)=}")

    end = time.perf_counter()
    ##    print(f"Group-by time: {end-start:.3f} seconds")

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

    ##    print(obj["discoveryObservationId"])

    end = time.perf_counter()
    ##    print(f"Total linking time: {end-start:.3f} seconds")

    return obj


###########################################################

default_config = dict(
    night_start_utc_days=17.0 / 24.0,  # this corresponds to 5pm UTC, or 2pm Chile time.
    maxdt_minutes=90,
    minlen_arcsec=1.0,
    window=14,
    nlink=3,
    p=0.95,
)

if __name__ == "__main__":
    import pandas as pd

    def load_test_dataset(fn="test_obsv.csv", ncopies=1):
        df = pd.read_csv(fn)

        # replicate
        dfs = []
        for i in range(ncopies):
            df2 = df.copy()
            if i != 0:
                df2["_name"] += f"_{i}"
            dfs += [df2]
        df = pd.concat(dfs)
        return df

    ncopies = 100
    df = load_test_dataset(ncopies=ncopies)

    # convert to (an efficiently packed) ndarray that linkObservations expects
    print(df[-10:])
    nameLen = df["_name"].str.len().max()
    obsv = np.asarray(
        df.to_records(
            index=False,
            column_dtypes=dict(_name=f"a{nameLen}", diaSourceId="u8", midPointTai="f8", ra="f8", decl="f8"),
        )
    )
    del df
    print(f"{obsv.dtype=}\n{len(obsv)=}")

    # go!
    obj = linkObservations(obsv, seed=0, objectId="_name")

    # print some nice results
    print("Found:", (~np.isnan(obj["discoverySubmissionDate"])).sum())
    objsample = pd.DataFrame(obj[::ncopies][:10])
    print(objsample)

    # filter out the observations of objects that weren't found
    import time

    start = time.perf_counter()
    found = obj["ssObjectId"][~np.isnan(obj["discoverySubmissionDate"])]
    obsv_found = obsv[np.isin(obsv["_name"], found)]
    end = time.perf_counter()
    print(f"Observation filtering time: {end-start:.3f} seconds")
    print(
        pd.DataFrame(obsv_found[np.isin(obsv_found["_name"], objsample["ssObjectId"])])
        .groupby("_name")
        .count()
    )

    # basic sanity checks
    obsv_missed = obsv[~np.isin(obsv["_name"], found)]
    print(f"{len(obsv_found)=}")
    print(f"{len(obsv_missed)=}")
    assert len(obsv_found) + len(obsv_missed) == len(obsv)

    # done
    print("done.")
