from collections import defaultdict
from csv import writer
from dataclasses import dataclass
from io import StringIO

import numpy as np
import pandas as pd
import spiceypy as spice

from sorcha.ephemeris.pixel_dict import PixelDict
from sorcha.ephemeris.simulation_constants import *
from sorcha.ephemeris.simulation_geometry import *
from sorcha.ephemeris.simulation_parsing import *
from sorcha.ephemeris.simulation_setup import (create_assist_ephemeris,
                                               furnish_spiceypy,
                                               generate_simulations)
from sorcha.modules.PPOutput import (PPOutWriteCSV, PPOutWriteHDF5,
                                     PPOutWriteSqlite3)
from sorcha.utilities.dataUtilitiesForTests import get_data_out_filepath


@dataclass
class EphemerisGeometryParameters:
    """Data class for holding parameters related to ephemeris geometry"""

    obj_id: str = None
    mjd_tai: float = None
    rho: float = None
    rho_hat: float = None
    rho_mag: float = None
    r_ast: float = None
    v_ast: float = None


def get_vec(row, vecname):
    """
    Extracts a vector from a Pandas dataframe row
    Parameters
    ----------
    row : row from the dataframe
    vecname : name of the vector
    Returns
    -------
    : 3D numpy array
    """
    return np.asarray([row[f"{vecname}_x"], row[f"{vecname}_y"], row[f"{vecname}_z"]])


def create_ephemeris(orbits_df, pointings_df, args, sconfigs):
    """Generate a set of observations given a collection of orbits
    and set of pointings.

    Parameters
    ----------
    orbits_df : pandas dataframe
        The dataframe containing the collection of orbits.
    pointings_df : pandas dataframe
        The dataframe containing the collection of telescope/camera pointings.
    args :
        Various arguments necessary for the calculation
    sconfigs:
        Dataclass of configuration file arguments.
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
        nside : integer
            The nside value used for the HEALPIx calculations.  Must be a
            power of 2 (1, 2, 4, ...)  nside=64 is current default.
        n_sub_intervals: int
            Number of sub-intervals for the Lagrange interpolation (default: 101)

    Returns
    -------
    observations: pandas dataframe
        The dataframe of observations needed for Sorcha to continue

    Notes
    -------
    This works by calculating and regularly updating the sky-plane
    locations (unit vectors) of all the objects in the collection
    of orbits.  The HEALPix index for each of the locations is calculated.
    A dictionary with pixel indices as keys and lists of ObjIDs for
    those objects in each HEALPix tile as values is generated.  An individual
    one of these calculations is called a 'picket', as one element of a long
    picket fence.  Typically, the interval between pickets is one day.

    Given a specific pointing, the set of HEALPix tiles that are overlapped
    by the pointing (and a buffer region) is computed.  Then the precise
    locations of just those objects within that set of HEALPix tiles are
    computed.  Details for those that actually do land within the field
    of view are passed along.
    """
    verboselog = args.pplogger.info if args.loglevel else lambda *a, **k: None

    ang_fov = sconfigs.simulation.ar_ang_fov
    buffer = sconfigs.simulation.ar_fov_buffer
    picket_interval = sconfigs.simulation.ar_picket
    obsCode = sconfigs.simulation.ar_obs_code
    nside = 2**sconfigs.simulation.ar_healpix_order
    n_sub_intervals = sconfigs.simulation.ar_n_sub_intervals

    ephemeris_csv_filename = None
    if args.output_ephemeris_file and args.outpath:
        ephemeris_csv_filename = os.path.join(args.outpath, args.output_ephemeris_file)

    verboselog("Building ASSIST ephemeris object.")
    ephem, gm_sun, gm_total = create_assist_ephemeris(args, sconfigs.auxiliary)
    verboselog("Furnishing SPICE kernels.")
    furnish_spiceypy(args, sconfigs.auxiliary)
    verboselog("Generating ASSIST+REBOUND simulations.")
    sim_dict = generate_simulations(ephem, gm_sun, gm_total, orbits_df, args)
    pixel_dict = defaultdict(list)
    observatories = Observatory(args, sconfigs.auxiliary)

    output = StringIO()
    in_memory_csv = writer(output)

    column_names = (
        "ObjID",
        "FieldID",
        "fieldMJD_TAI",
        "fieldJD_TDB",
        "Range_LTC_km",
        "RangeRate_LTC_km_s",
        "RA_deg",
        "RARateCosDec_deg_day",
        "Dec_deg",
        "DecRate_deg_day",
        "Obj_Sun_x_LTC_km",
        "Obj_Sun_y_LTC_km",
        "Obj_Sun_z_LTC_km",
        "Obj_Sun_vx_LTC_km_s",
        "Obj_Sun_vy_LTC_km_s",
        "Obj_Sun_vz_LTC_km_s",
        "Obs_Sun_x_km",
        "Obs_Sun_y_km",
        "Obs_Sun_z_km",
        "Obs_Sun_vx_km_s",
        "Obs_Sun_vy_km_s",
        "Obs_Sun_vz_km_s",
        "phase_deg",
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

    pixdict = PixelDict(
        pointings_df["fieldJD_TDB"].iloc[0],
        sim_dict,
        ephem,
        obsCode,
        observatories,
        picket_interval,
        nside,
        n_sub_intervals=n_sub_intervals,
        use_integrate=sconfigs.expert.ar_use_integrate,
    )
    for _, pointing in pointings_df.iterrows():
        mjd_tai = float(pointing["observationMidpointMJD_TAI"])

        # If the observation time is too far from the
        # time of the last set of ballpark sky position,
        # compute a new set

        desigs = pixdict.get_designations(
            pointing["fieldJD_TDB"], pointing["fieldRA_deg"], pointing["fieldDec_deg"], ang_fov
        )
        unit_vectors = pixdict.interpolate_unit_vectors(desigs, pointing["fieldJD_TDB"])
        visit_vector = get_vec(pointing, "visit_vector")
        r_obs = get_vec(pointing, "r_obs")

        for k, uv in unit_vectors.items():
            ephem_geom_params = EphemerisGeometryParameters()
            ephem_geom_params.obj_id = k
            ephem_geom_params.mjd_tai = mjd_tai

            v = sim_dict[k]
            sim, ex = v["sim"], v["ex"]
            uv /= np.linalg.norm(uv)
            ang = np.arccos(np.dot(uv, visit_vector)) * 180 / np.pi
            if ang < ang_fov + buffer:
                (
                    ephem_geom_params.rho,
                    ephem_geom_params.rho_mag,
                    _,
                    ephem_geom_params.r_ast,
                    ephem_geom_params.v_ast,
                ) = integrate_light_time(sim, ex, pointing["fieldJD_TDB"] - ephem.jd_ref, r_obs, lt0=0.01, use_integrate=sconfigs.expert.ar_use_integrate)
                ephem_geom_params.rho_hat = ephem_geom_params.rho / ephem_geom_params.rho_mag

                ang_from_center = 180 / np.pi * np.arccos(np.dot(ephem_geom_params.rho_hat, visit_vector))
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
        write_out_ephemeris_file(ephemeris_df, ephemeris_csv_filename, args, sconfigs)

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
    """
    Decomposes the vector into two unit vectors to facilitate computation of on-sky angles
    The decomposition is such that A  = (-sin (RA), cos(RA), 0) is in the direction of increasing RA,
    and D = (-sin(dec)cos (RA), -sin(dec) sin(RA), cos(dec)) is in the direction of increasing Dec
    The triplet (A,D,v1) forms an orthonormal basis of the 3D vector space
    Parameters
    -----------
        v1 : array, shape = (3,))
            The vector to be decomposed
    Returns
    ----------
        A :  array, shape = (3,))
            A  vector
        D : array, shape = (3,))
            D vector
    """
    x, y, z = v1
    cosd = np.sqrt(1 - z * z)
    A = np.array((-y, x, 0.0)) / cosd
    D = np.array((-z * x / cosd, -z * y / cosd, cosd))
    return A, D


def calculate_rates_and_geometry(pointing: pd.DataFrame, ephem_geom_params: EphemerisGeometryParameters):
    """Calculate rates and geometry for objects within the field of view

    Parameters
    ----------
    pointing : pandas dataframe
        The dataframe containing the pointing database.
    ephem_geom_params : EphemerisGeometryParameters
        Various parameters necessary to calculate the ephemeris

    Returns
    -------
    : tuple
        Tuple containing the ephemeris parameters needed for Sorcha post processing.
    """
    r_sun = get_vec(pointing, "r_sun")
    r_obs = get_vec(pointing, "r_obs")
    v_sun = get_vec(pointing, "v_sun")
    v_obs = get_vec(pointing, "v_obs")

    ra0, dec0 = vec2ra_dec(ephem_geom_params.rho_hat)
    drhodt = ephem_geom_params.v_ast - v_obs
    drho_magdt = (1 / ephem_geom_params.rho_mag) * np.dot(ephem_geom_params.rho, drhodt)
    ddeltatdt = drho_magdt / (SPEED_OF_LIGHT)
    drhodt = ephem_geom_params.v_ast * (1 - ddeltatdt) - v_obs
    A, D = get_residual_vectors(ephem_geom_params.rho_hat)
    drho_hatdt = (
        drhodt / ephem_geom_params.rho_mag
        - drho_magdt * ephem_geom_params.rho_hat / ephem_geom_params.rho_mag
    )
    dradt = np.dot(A, drho_hatdt)
    ddecdt = np.dot(D, drho_hatdt)
    r_ast_sun = ephem_geom_params.r_ast - r_sun
    v_ast_sun = ephem_geom_params.v_ast - v_sun
    r_ast_obs = ephem_geom_params.r_ast - r_obs
    phase_angle = np.arccos(
        np.dot(r_ast_sun, r_ast_obs) / (np.linalg.norm(r_ast_sun) * np.linalg.norm(r_ast_obs))
    )
    obs_sun = r_obs - r_sun
    dobs_sundt = v_obs - v_sun

    return (
        ephem_geom_params.obj_id,
        pointing["FieldID"],
        ephem_geom_params.mjd_tai,
        pointing["fieldJD_TDB"],
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


def write_out_ephemeris_file(ephemeris_df, ephemeris_csv_filename, args, sconfigs):
    """Writes the ephemeris out to an external file.

    Parameters
    ----------
    ephemeris_df : Pandas DataFrame
        The data frame of ephemeris information to be written out.

    ephemeris_csv_filename : string
        The filepath (without extension) to write the ephemeris file to.

    args: sorchaArguments object or similar
        Command-line arguments from Sorcha.

    sconfigs: dataclass
        Dataclass of configuration file arguments.

    Returns
    -------
    None.
    """

    verboselog = args.pplogger.info if args.loglevel else lambda *a, **k: None

    if sconfigs.input.eph_format == "csv":
        verboselog("Outputting ephemeris to CSV file...")
        PPOutWriteCSV(ephemeris_df, ephemeris_csv_filename + ".csv")
    elif sconfigs.input.eph_format == "whitespace":
        verboselog("Outputting ephemeris to whitespaced CSV file...")
        PPOutWriteCSV(ephemeris_df, ephemeris_csv_filename + ".csv", separator=" ")
    elif sconfigs.input.eph_format == "hdf5" or sconfigs.output.output_format == "h5":
        verboselog("Outputting ephemeris to HDF5 binary file...")
        PPOutWriteHDF5(ephemeris_df, ephemeris_csv_filename + ".h5", "sorcha_ephemeris")
