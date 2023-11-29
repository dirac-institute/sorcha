from dataclasses import dataclass
from collections import defaultdict
from csv import writer
from io import StringIO

import numpy as np
import pandas as pd
import spiceypy as spice

from sorcha.ephemeris.simulation_setup import (
    create_assist_ephemeris,
    furnish_spiceypy,
    generate_simulations,
)
from sorcha.ephemeris.simulation_constants import *
from sorcha.ephemeris.simulation_geometry import *
from sorcha.ephemeris.simulation_parsing import *
from sorcha.utilities.dataUtilitiesForTests import get_data_out_filepath

out_csv_path = get_data_out_filepath("ephemeris_output.csv")


@dataclass
class EphemerisGeometryParameters:
    obj_id: str = None
    mjd_tai: float = None
    rho: float = None
    rho_hat: float = None
    rho_mag: float = None
    r_ast: float = None
    v_ast: float = None


def create_ephemeris(orbits_df, pointings_df, args, configs):
    """Generate a set of observations given a collection of orbits
    and set of pointings.

    This works by calculating and regularly updating the sky-plane
    locations (unit vectors) of all the objects in the collection
    of orbits.  The HEALPix index for each of the locations is calculated.
    A dictionary with pixel indices as keys and lists of ObjIDs for
    those objects in each HEALPix tile as values.  One of these
    calculations is called a 'picket', as one element of a long picket
    fence.  At present,

    Given a specific pointing, the set of HEALPix tiles that are overlapped
    by the pointing (and a buffer region) is computed.  These the precise
    locations of just those objects within that set of HEALPix tiles are
    computed.  Details for those that actually do land within the field
    of view are passed along.

    Parameters
    ----------
    orbits_df : pd.DataFrame
        The dataframe containing the collection of orbits.
    pointings_df : pd.DataFrame
        The dataframe containing the collection of telescope/camera pointings.
    args :
        Various arguments necessary for the calculation
    configs : dict
        Various configuration parameters necessary for the calculation
        ang_fov : float
            The angular size (deg) of the field of view
        buffer : float
            The angular size (deg) of the buffer around the field of view.
            A buffer is required to allow for some motion between the time
            of the observation and the time of the picket (t_picket)
        picket_interval : float
            The interval (days) between picket calculations.  This is 1 day
            by default.  Current there is only one such interval, used for
            all objects.  It is currently possible for extremely fast-moving
            objects to be missed.  This will be remedied in future releases.
        obsCode : string
            The MPC code for the observatory.  (This is current a configuration
            parameter, but these should be included in the visit information,
            to allow for multiple observatories.
        nside : int
            The nside value used for the HEALPIx calculations.  Must be a
            power of 2 (1, 2, 4, ...)  nside=64 is current default.

    Returns
    -------
    pd.DataFrame
        The dataframe of observations needed for Sorcha to continue
    """
    verboselog = args.pplogger.info if args.verbose else lambda *a, **k: None

    ang_fov = configs["ar_ang_fov"]
    buffer = configs["ar_fov_buffer"]
    picket_interval = configs["ar_picket"]
    obsCode = configs["ar_obs_code"]
    nside = 2 ** configs["ar_healpix_order"]
    first = 1  # Try to get away from this

    ephemeris_csv_filename = None
    if args.output_ephemeris_file and args.outpath:
        ephemeris_csv_filename = os.path.join(args.outpath, args.output_ephemeris_file)

    verboselog("Building ASSIST ephemeris object.")
    ephem, gm_sun, gm_total = create_assist_ephemeris(args)
    verboselog("Furnishing SPICE kernels.")
    furnish_spiceypy(args)
    verboselog("Generating ASSIST+REBOUND simulations.")
    sim_dict = generate_simulations(ephem, gm_sun, gm_total, orbits_df, args)
    pixel_dict = defaultdict(list)
    observatories = Observatory(args)

    output = StringIO()
    in_memory_csv = writer(output)

    column_names = (
        "ObjID",
        "FieldID",
        "FieldMJD_TAI",
        "JD_TDB",
        "AstRange(km)",
        "AstRangeRate(km/s)",
        "AstRA(deg)",
        "AstRARate(deg/day)",
        "AstDec(deg)",
        "AstDecRate(deg/day)",
        "Ast-Sun(J2000x)(km)",
        "Ast-Sun(J2000y)(km)",
        "Ast-Sun(J2000z)(km)",
        "Ast-Sun(J2000vx)(km/s)",
        "Ast-Sun(J2000vy)(km/s)",
        "Ast-Sun(J2000vz)(km/s)",
        "Obs-Sun(J2000x)(km)",
        "Obs-Sun(J2000y)(km)",
        "Obs-Sun(J2000z)(km)",
        "Obs-Sun(J2000vx)(km/s)",
        "Obs-Sun(J2000vy)(km/s)",
        "Obs-Sun(J2000vz)(km/s)",
        "Sun-Ast-Obs(deg)",
    )
    column_types = defaultdict(ObjID=str, FieldID=str).setdefault(float)
    in_memory_csv.writerow(column_names)

    # t_picket is the last time at which the sky positions of all the objects
    # were calculated and placed into a healpix dictionary, i.e. the
    # update_pixel_dict() function is called.  That calculation is redone at
    # regular (tunable) intervals.
    # Setting t_picket to 0 ensures that the function is called on the
    # first run.

    t_picket = 0.0

    verboselog("Generating ephemeris...")

    for _, pointing in pointings_df.iterrows():
        mjd_tai = float(pointing["observationMidpointMJD_TAI"])

        # If the observation time is too far from the
        # time of the last set of ballpark sky position,
        # compute a new set
        while (
            abs(pointing["JD_TDB"] - t_picket) > 0.5 * picket_interval or first == 1
        ):  # right now this assumes time ordering
            t_picket, pixel_dict, _ = update_pixel_dict(
                pointing["JD_TDB"], t_picket, picket_interval, sim_dict, ephem, obsCode, observatories, nside
            )
            first = 0

        # This loop builds a python set containing ids for objects in the pixels
        # around the current pointing. The function `update_pixel_dict` does
        # the majority of the computation to build out `pixel_dict`.
        desigs = set()
        for pix in pointing["pixels"]:
            desigs.update(pixel_dict[pix])

        for obj_id in sorted(desigs):
            ephem_geom_params = EphemerisGeometryParameters()
            ephem_geom_params.obj_id = obj_id
            ephem_geom_params.mjd_tai = mjd_tai

            v = sim_dict[obj_id]
            sim, ex, rho_hat_rough = v["sim"], v["ex"], v["rho_hat"]
            ang = np.arccos(np.dot(rho_hat_rough, pointing["visit_vector"])) * 180 / np.pi
            if ang < ang_fov + buffer:
                (
                    ephem_geom_params.rho,
                    ephem_geom_params.rho_mag,
                    _,
                    ephem_geom_params.r_ast,
                    ephem_geom_params.v_ast,
                ) = integrate_light_time(
                    sim, ex, pointing["JD_TDB"] - ephem.jd_ref, pointing["r_obs"], lt0=0.01
                )
                ephem_geom_params.rho_hat = ephem_geom_params.rho / ephem_geom_params.rho_mag

                ang_from_center = (
                    180 / np.pi * np.arccos(np.dot(ephem_geom_params.rho_hat, pointing["visit_vector"]))
                )
                if ang_from_center < ang_fov:
                    out_tuple = calculate_rates_and_geometry(pointing, ephem_geom_params)
                    in_memory_csv.writerow(out_tuple)

    verboselog("Ephemeris generated.")
    # reset to the beginning of the in-memory CSV
    output.seek(0)
    ephemeris_df = pd.read_csv(output, dtype=column_types)

    # if the user has defined an output file name for the ephemeris results, write out to that file
    if ephemeris_csv_filename:
        verboselog("Writing out ephemeris results to file.")
        write_header = True
        # due to chunking, if the file already exists and it has contents, then we won't include the header information
        if os.path.exists(ephemeris_csv_filename) and os.stat(ephemeris_csv_filename).st_size != 0:
            write_header = False
        ephemeris_df.to_csv(ephemeris_csv_filename, mode="a", index=False, header=write_header)

    # join the ephemeris and input orbits dataframe, take special care to make
    # sure the 'ObjID' column types match.
    verboselog("Joining ephemeris to orbits dataframe.")
    ephemeris_df["ObjID"] = ephemeris_df["ObjID"].astype("string")
    orbits_df["ObjID"] = orbits_df["ObjID"].astype("string")
    observations = ephemeris_df.join(orbits_df.set_index("ObjID"), on="ObjID")

    spice.kclear()

    # Return the dataframe needed for Sorcha to continue
    return observations


def get_residual_vectors(v1):
    x, y, z = v1
    cosd = np.sqrt(1 - z * z)
    A = np.array((-y, x, 0.0)) / cosd
    D = np.array((-z * x / cosd, -z * y / cosd, cosd))
    return A, D


# arguments: JD_TDB, t_picket, picket_interval, sim_dict, obsCode
# returns t_picket, pixel_dict, r_obs
def update_pixel_dict(JD_TDB, t_picket, picket_interval, sim_dict, ephem, obsCode, observatories, nside):
    n = round((JD_TDB - t_picket) / picket_interval)
    t_picket += n * picket_interval
    et = (t_picket - spice.j2000()) * 24 * 60 * 60
    r_obs = observatories.barycentricObservatory(et, obsCode) / AU_KM
    pixel_dict = defaultdict(list)
    for k, v in sim_dict.items():
        sim, ex = v["sim"], v["ex"]
        ex.integrate_or_interpolate(t_picket - ephem.jd_ref)
        rho = np.array(sim.particles[0].xyz) - r_obs
        rho_hat = rho / np.linalg.norm(rho)
        sim_dict[k]["rho_hat"] = rho_hat
        this_pix = hp.vec2pix(nside, rho_hat[0], rho_hat[1], rho_hat[2], nest=True)
        pixel_dict[this_pix].append(k)
    return t_picket, pixel_dict, r_obs


def calculate_rates_and_geometry(pointing: pd.DataFrame, ephem_geom_params: EphemerisGeometryParameters):
    """Calculate rates and geometry for objects within the field of view

    Parameters
    ----------
    pointing : pd.DataFrame
        The dataframe containing the pointing database.
    ephem_geom_params : EphemerisGeometryParameters
        Various parameters necessary to calculate the ephemeris

    Returns
    -------
    tuple
        Tuple containing the ephemeris parameters needed for Sorcha post processing.
    """
    ra0, dec0 = vec2ra_dec(ephem_geom_params.rho_hat)
    drhodt = ephem_geom_params.v_ast - pointing["v_obs"]
    drho_magdt = (1 / ephem_geom_params.rho_mag) * np.dot(ephem_geom_params.rho, drhodt)
    ddeltatdt = drho_magdt / (SPEED_OF_LIGHT)
    drhodt = ephem_geom_params.v_ast * (1 - ddeltatdt) - pointing["v_obs"]
    A, D = get_residual_vectors(ephem_geom_params.rho_hat)
    drho_hatdt = (
        drhodt / ephem_geom_params.rho_mag
        - drho_magdt * ephem_geom_params.rho_hat / ephem_geom_params.rho_mag
    )
    dradt = np.dot(A, drho_hatdt)
    ddecdt = np.dot(D, drho_hatdt)
    r_ast_sun = ephem_geom_params.r_ast - pointing["r_sun"]
    v_ast_sun = ephem_geom_params.v_ast - pointing["v_sun"]
    r_ast_obs = ephem_geom_params.r_ast - pointing["r_obs"]
    phase_angle = np.arccos(
        np.dot(r_ast_sun, r_ast_obs) / (np.linalg.norm(r_ast_sun) * np.linalg.norm(r_ast_obs))
    )
    obs_sun = np.asarray(pointing["r_obs"]) - np.asarray(pointing["r_sun"])
    dobs_sundt = np.asarray(pointing["v_obs"]) - np.asarray(pointing["v_sun"])

    return (
        ephem_geom_params.obj_id,
        pointing["FieldID"],
        ephem_geom_params.mjd_tai,
        pointing["JD_TDB"],
        ephem_geom_params.rho_mag * AU_KM,
        drho_magdt * AU_KM / (24 * 60 * 60),
        ra0,
        dradt * 180 / np.pi,
        dec0,
        ddecdt * 180 / np.pi,
        r_ast_sun[0] * AU_KM,
        r_ast_sun[1] * AU_KM,
        r_ast_sun[2] * AU_KM,
        v_ast_sun[0] * AU_KM / (24 * 60 * 60),
        v_ast_sun[1] * AU_KM / (24 * 60 * 60),
        v_ast_sun[2] * AU_KM / (24 * 60 * 60),
        obs_sun[0] * AU_KM,
        obs_sun[1] * AU_KM,
        obs_sun[2] * AU_KM,
        dobs_sundt[0] * AU_KM / (24 * 60 * 60),
        dobs_sundt[1] * AU_KM / (24 * 60 * 60),
        dobs_sundt[2] * AU_KM / (24 * 60 * 60),
        phase_angle * 180 / np.pi,
    )
