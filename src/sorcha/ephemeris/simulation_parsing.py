import numpy as np
import spiceypy as spice

from sorcha.ephemeris.simulation_constants import GMSUN
from sorcha.ephemeris.simulation_geometry import ecliptic_to_equatorial


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


def convertMPCorbit(line, ephem, sun_dict):
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
    incl = float(line[59:68])
    e = float(line[70:79])
    n = float(line[80:91])
    a = float(line[92:103])

    if epoch not in sun_dict:
        sun_dict[epoch] = ephem.get_particle("Sun", epoch - ephem.jd_ref)

    # Convert to equatorial barycentric cartesian
    state = kc.cartesian(
        GMSUN, a, e, incl * np.pi / 180, longnode * np.pi / 180, argperi * np.pi / 180, meananom * np.pi / 180
    )
    st = np.array((state.x, state.y, state.z, state.xd, state.yd, state.zd))
    pos = ecliptic_to_equatorial(st[0:3])
    vel = ecliptic_to_equatorial(st[3:6])
    sun = sun_dict[epoch]
    pos += np.array((sun.x, sun.y, sun.z))
    vel += np.array((sun.vx, sun.vy, sun.vz))

    return desig, H, G, epoch, pos, vel


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


class Observatory:
    def __init__(self, oc_file="ObsCodes.txt"):
        self.observatoryPositionCache = {}  # previously calculated positions to speed up the process

        # Convert ObsCodes.txt lines to geocentric x,y,z positions and
        # store them in a dictionary.  The keys are the observatory
        # code strings, and the values are (x,y,z) tuples.
        # Spacecraft and other moving observatories have (None,None,None)
        # as position.
        ObservatoryXYZ = {}
        with open(oc_file, "r") as f:
            next(f)
            for line in f:
                code, longitude, rhocos, rhosin, Obsname = self.parseObsCode(line)
                if longitude and rhocos and rhosin:
                    rhocos, rhosin, longitude = float(rhocos), float(rhosin), float(longitude)
                    longitude *= np.pi / 180.0
                    x = rhocos * np.cos(longitude)
                    y = rhocos * np.sin(longitude)
                    z = rhosin
                    ObservatoryXYZ[code] = (x, y, z)
                else:
                    ObservatoryXYZ[code] = (None, None, None)
        self.ObservatoryXYZ = ObservatoryXYZ

    # Parses a line from the MPC's ObsCode.txt file
    def parseObsCode(self, line):
        code, longitude, rhocos, rhosin, ObsName = (
            line[0:3],
            line[4:13],
            line[13:21],
            line[21:30],
            line[30:].rstrip("\n"),
        )
        if longitude.isspace():
            longitude = None
        if rhocos.isspace():
            rhocos = None
        if rhosin.isspace():
            rhosin = None
        return code, longitude, rhocos, rhosin, ObsName

    # This routine parses the section of the second line that encodes the geocentric satellite position.
    def parseXYZ(xyz):
        try:
            xs = xyz[0]
            x = float(xyz[1:11])
            if xs == "-":
                x = -x
            ys = xyz[12]
            y = float(xyz[13:23])
            if ys == "-":
                y = -y
            zs = xyz[24]
            z = float(xyz[25:])
            if zs == "-":
                z = -z
        except:
            print("error parseXYZ")
            print(xyz)
        return x, y, z
