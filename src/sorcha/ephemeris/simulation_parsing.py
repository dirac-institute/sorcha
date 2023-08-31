import json
import numpy as np
import spiceypy as spice

from sorcha.ephemeris.simulation_constants import GMSUN, RADIUS_EARTH_KM
from sorcha.ephemeris.simulation_geometry import ecliptic_to_equatorial
from sorcha.ephemeris.simulation_data_files import OBSERVATORY_CODES, make_retriever
from sorcha.ephemeris.orbit_conversion_utilities import universal_cartesian
from . import kepcart as kc


def convert_mpc_epoch(epoch):
    """
    Converts MPC [packed dates](https://www.minorplanetcenter.net/iau/info/PackedDates.html)
    into Year, Month, Day integer values.

    Parameters:
    -----------
    epoch (string): The 5 character MPC packed date.

    Returns:
    -----------
    Tuple of ints (Year, Month, Day)

    """
    if len(epoch) != 5:
        raise ValueError("invalid MPC epoch provided (length).")

    century_char = epoch[0]
    if century_char == "I":
        century = 1800
    elif century_char == "J":
        century = 1900
    elif century_char == "K":
        century = 2000
    else:
        raise ValueError("invalid MPC epoch provided (century).")
    year = century + int(epoch[1:3])

    month = epoch[3]
    if month.isdigit():
        month = int(month)
        if month < 1 or month > 9:
            raise ValueError("invalid MPC epoch provided (month).")
    elif month == "A":
        month = 10
    elif month == "B":
        month = 11
    elif month == "C":
        month = 12
    else:
        raise ValueError("invalid MPC epoch provided (month).")

    day = epoch[4]
    if not day.isdigit():
        day = 10 + ord(day) - ord("A")

    day = int(day)
    if day < 1 or day > 31:
        raise ValueError("invalid MPC epoch provided (day).")

    return year, month, day


# TODO: Remove unused parts due to input refactor (CombinedDataReader)
def convert_mpc_orbit(line, ephem, sun_dict=None):
    desig = line[0:7]
    try:
        H = float(line[8:13])
    except ValueError:
        H = "-----"
    try:
        G = float(line[14:19])
    except ValueError:
        G = "-----"

    epoch_tuple = convert_mpc_epoch(line[20:25])
    epoch = "%d-%02d-%02d TDB" % epoch_tuple
    epoch = spice.j2000() + spice.str2et(epoch) / (24 * 60 * 60)

    desig = desig.strip()
    meananom = float(line[26:35])
    argperi = float(line[37:46])
    longnode = float(line[48:57])
    inclination = float(line[59:68])
    eccentricity = float(line[70:79])
    daily_motion = float(line[80:91])
    a = float(line[92:103])

    if epoch not in sun_dict:
        sun_dict[epoch] = ephem.get_particle("Sun", epoch - ephem.jd_ref)

    # Convert to equatorial barycentric cartesian
    if True:
        xx, yy, zz, xd, yd, zd = universal_cartesian(
            GMSUN,
            a * (1 - eccentricity),
            eccentricity,
            inclination * np.pi / 180,
            longnode * np.pi / 180,
            argperi * np.pi / 180,
            epoch - (meananom * np.pi / 180) * np.sqrt(a**3 / GMSUN),
            epoch,
        )
        pos = ecliptic_to_equatorial([xx, yy, zz])
        vel = ecliptic_to_equatorial([xd, yd, zd])
    else:
        state = kc.cartesian(
            GMSUN,
            a,
            eccentricity,
            inclination * np.pi / 180,
            longnode * np.pi / 180,
            argperi * np.pi / 180,
            meananom * np.pi / 180,
        )
        st = np.array((state.x, state.y, state.z, state.xd, state.yd, state.zd))
        pos = ecliptic_to_equatorial(st[0:3])
        vel = ecliptic_to_equatorial(st[3:6])
    sun = sun_dict[epoch]
    pos += np.array((sun.x, sun.y, sun.z))
    vel += np.array((sun.vx, sun.vy, sun.vz))

    return desig, H, G, epoch, pos, vel


# TODO: Remove this (CombinedDataReader)
def convertS3morbit(line):
    (
        desig,
        FORMAT,
        q,
        e,
        incl,
        longnode,
        argperi,
        t_p,
        H,
        Epoch_MJD,
        INDEX,
        N_PAR,
        MOID,
        COMPCODE,
    ) = line.rstrip().split()

    q = float(q)
    e = float(e)
    incl = float(incl)
    longnode = float(longnode)
    argperi = float(argperi)
    t_p = float(t_p)
    H = float(H)

    return desig, q, e, incl, longnode, argperi, t_p, H, Epoch_MJD


def mjd_tai_to_epoch(mjd_tai):
    jd = mjd_tai + 2400000.5 + 32.184 / (24 * 60 * 60)
    epoch_str = "JD %lf TDT" % jd
    epoch = spice.j2000() + spice.str2et(epoch_str) / (24 * 60 * 60)
    return epoch


def parse_orbit_row(row, epoch, ephem, sun_dict):
    orbit_format = row["FORMAT"]

    if orbit_format != "CART":
        if orbit_format == "COM":
            # TODO: I don't think this right, ask Pedro about it lol
            ecx, ecy, ecz, dx, dy, dz = universal_cartesian(
                GMSUN,
                row["q"],
                row["e"],
                row["inc"] * np.pi / 180.0,
                row["node"] * np.pi / 180.0,
                row["argPeri"] * np.pi / 180.0,
                row["t_p"],
            )
        elif orbit_format == "KEP":
            ecx, ecy, ecz, dx, dy, dz = universal_cartesian(
                GMSUN,
                row["a"] * (1 - row["e"]),
                row["e"],
                row["inc"] * np.pi / 180.0,
                row["node"] * np.pi / 180.0,
                row["argPeri"] * np.pi / 180.0,
                epoch - (row["ma"] * np.pi / 180.0) * np.sqrt(row["a"] ** 3 / GMSUN),
            )
        else:
            raise ValueError("Provided orbit format not supported.")
    else:
        ecx, ecy, ecz = row["x"], row["y"], row["z"]
        dx, dy, dz = row["xdot"], row["ydot"], row["zdot"]

    if epoch not in sun_dict:
        sun_dict[epoch] = ephem.get_particle("Sun", epoch - ephem.jd_ref)

    sun = sun_dict[epoch]

    equatorial_coords = np.array(ecliptic_to_equatorial([ecx, ecy, ecz]))
    equatorial_velocities = np.array(ecliptic_to_equatorial([dx, dy, dz]))

    equatorial_coords += np.array((sun.x, sun.y, sun.z))
    equatorial_velocities += np.array((sun.vx, sun.vy, sun.vz))

    return tuple(np.concatenate([equatorial_coords, equatorial_velocities]))


class Observatory:
    def __init__(self, oc_file=OBSERVATORY_CODES):
        self.observatoryPositionCache = {}  # previously calculated positions to speed up the process

        retriever = make_retriever()
        obs_file_path = retriever.fetch(oc_file)

        # Convert ObsCodes.json lines to geocentric x,y,z positions and
        # store them in a dictionary.  The keys are the observatory
        # code strings, and the values are (x,y,z) tuples.
        # Spacecraft and other moving observatories have (None,None,None)
        # as position.
        self.ObservatoryXYZ = {}
        with open(obs_file_path) as file_object:
            obs = json.load(file_object)

        for obs_name, obs_location in obs.items():
            self.ObservatoryXYZ[obs_name] = self.convert_to_geocentric(obs_location)

    def convert_to_geocentric(self, obs_location: dict) -> tuple:
        returned_tuple = (None, None, None)
        if (
            obs_location.get("Longitude", False)
            and obs_location.get("cos", False)
            and obs_location.get("sin", False)
        ):
            longitude = obs_location["Longitude"] * np.pi / 180.0
            x = obs_location["cos"] * np.cos(longitude)
            y = obs_location["cos"] * np.sin(longitude)
            z = obs_location["sin"]
            returned_tuple = (x, y, z)

        return returned_tuple

    def barycentricObservatory(
        self, et, obsCode, Rearth=RADIUS_EARTH_KM
    ):  # This JPL's quoted Earth radius (km)
        # et is JPL's internal time

        # Get the barycentric position of Earth
        pos, _ = spice.spkpos("EARTH", et, "J2000", "NONE", "SSB")

        # Get the matrix that rotates from the Earth's equatorial body fixed frame to the J2000 equatorial frame.
        m = spice.pxform("ITRF93", "J2000", et)

        # Get the MPC's unit vector from the geocenter to
        # the observatory
        # obsVec = Observatories.ObservatoryXYZ[obsCode]
        obsVec = self.ObservatoryXYZ[obsCode]
        obsVec = np.array(obsVec)

        # Carry out the rotation and scale
        mVec = np.dot(m, obsVec) * Rearth

        return pos + mVec
