import json
import os
import numpy as np
import spiceypy as spice
from pooch import Decompress

from sorcha.ephemeris.simulation_constants import RADIUS_EARTH_KM
from sorcha.ephemeris.simulation_geometry import ecliptic_to_equatorial
from sorcha.ephemeris.simulation_data_files import (
    OBSERVATORY_CODES,
    OBSERVATORY_CODES_COMPRESSED,
    make_retriever,
)
from sorcha.ephemeris.orbit_conversion_utilities import universal_cartesian


def mjd_tai_to_epoch(mjd_tai):
    jd = mjd_tai + 2400000.5 + 32.184 / (24 * 60 * 60)
    epoch_str = "JD %lf TDT" % jd
    epoch = spice.j2000() + spice.str2et(epoch_str) / (24 * 60 * 60)
    return epoch


def parse_orbit_row(row, epochJD_TDB, ephem, sun_dict, gm_sun, gm_total):
    orbit_format = row["FORMAT"]

    if orbit_format not in ["CART", "BCART"]:
        if orbit_format == "COM":
            t_p_JD_TDB = row["t_p_MJD_TDB"] + 2400000.5
            ecx, ecy, ecz, dx, dy, dz = universal_cartesian(
                gm_sun,
                row["q"],
                row["e"],
                row["inc"] * np.pi / 180.0,
                row["node"] * np.pi / 180.0,
                row["argPeri"] * np.pi / 180.0,
                t_p_JD_TDB,
                epochJD_TDB,
            )
        elif orbit_format == "BCOM":
            t_p_JD_TDB = row["t_p_MJD_TDB"] + 2400000.5
            ecx, ecy, ecz, dx, dy, dz = universal_cartesian(
                gm_total,
                row["q"],
                row["e"],
                row["inc"] * np.pi / 180.0,
                row["node"] * np.pi / 180.0,
                row["argPeri"] * np.pi / 180.0,
                t_p_JD_TDB,
                epochJD_TDB,
            )
        elif orbit_format == "KEP":
            ecx, ecy, ecz, dx, dy, dz = universal_cartesian(
                gm_sun,
                row["a"] * (1 - row["e"]),
                row["e"],
                row["inc"] * np.pi / 180.0,
                row["node"] * np.pi / 180.0,
                row["argPeri"] * np.pi / 180.0,
                epochJD_TDB - (row["ma"] * np.pi / 180.0) * np.sqrt(row["a"] ** 3 / gm_sun),
                epochJD_TDB,
            )
        elif orbit_format == "BKEP":
            ecx, ecy, ecz, dx, dy, dz = universal_cartesian(
                gm_total,
                row["a"] * (1 - row["e"]),
                row["e"],
                row["inc"] * np.pi / 180.0,
                row["node"] * np.pi / 180.0,
                row["argPeri"] * np.pi / 180.0,
                epochJD_TDB - (row["ma"] * np.pi / 180.0) * np.sqrt(row["a"] ** 3 / gm_total),
                epochJD_TDB,
            )
        else:
            raise ValueError("Provided orbit format not supported.")
    else:
        ecx, ecy, ecz = row["x"], row["y"], row["z"]
        dx, dy, dz = row["xdot"], row["ydot"], row["zdot"]

    if epochJD_TDB not in sun_dict:
        sun_dict[epochJD_TDB] = ephem.get_particle("Sun", epochJD_TDB - ephem.jd_ref)

    sun = sun_dict[epochJD_TDB]

    equatorial_coords = np.array(ecliptic_to_equatorial([ecx, ecy, ecz]))
    equatorial_velocities = np.array(ecliptic_to_equatorial([dx, dy, dz]))

    if orbit_format in ["KEP", "COM", "CART"]:
        equatorial_coords += np.array((sun.x, sun.y, sun.z))
        equatorial_velocities += np.array((sun.vx, sun.vy, sun.vz))

    return tuple(np.concatenate([equatorial_coords, equatorial_velocities]))


class Observatory:
    def __init__(self, args, oc_file=OBSERVATORY_CODES):
        self.observatoryPositionCache = {}  # previously calculated positions to speed up the process

        if oc_file == OBSERVATORY_CODES:
            retriever = make_retriever(args.ar_data_file_path)

            # is the file available locally, if so, return the full path
            if os.path.isfile(os.path.join(retriever.abspath, OBSERVATORY_CODES)):
                obs_file_path = retriever.fetch(OBSERVATORY_CODES)

            # if the file is not local, download, and decompress it, then return the path.
            else:
                obs_file_path = retriever.fetch(
                    OBSERVATORY_CODES_COMPRESSED, processor=Decompress(name=OBSERVATORY_CODES)
                )

        else:
            obs_file_path = oc_file

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
