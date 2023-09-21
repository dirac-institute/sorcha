from collections import defaultdict
from csv import writer
from io import StringIO
from os import path

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
from sorcha.modules.PPReadPointingDatabase import PPReadPointingDatabase

out_csv_path = get_data_out_filepath("ephemeris_output.csv")


def create_ephemeris(orbits_df, pointings_df, args, configs):
    ang_fov = configs["ar_ang_fov"]
    buffer = configs["ar_fov_buffer"]
    picket_interval = configs["ar_picket"]
    obsCode = configs["ar_obs_code"]
    nside = 2 ** configs["ar_healpix_order"]
    first = 1  # Try to get away from this

    if args.output_ephemeris_file and args.outpath:
        ephemeris_csv_filename = os.path.join(args.outpath, args.output_ephemeris_file)

    t_picket = 2460000.5

    ephem, gm_sun = create_assist_ephemeris(args)
    furnish_spiceypy(args)
    sim_dict = generate_simulations(ephem, gm_sun, orbits_df)
    pixel_dict = defaultdict(list)
    observatories = Observatory(args)

    output = StringIO()
    in_memory_csv = writer(output)

    # this header is broken up to match the string built at the end of this method
    column_names = (
        "ObjID",
        "FieldID",
        "FieldMJD",
        "jd_tdb",
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

    for _, pointing in pointings_df.iterrows():
        mjd_tai = float(pointing["observationStartMJD"])
        ra, dec = float(pointing["fieldRA"]), float(pointing["fieldDec"])

        # If the observation time is too far from the
        # time of the last set of ballpark sky position,
        # compute a new set
        while (
            abs(pointing["jd_tdb"] - t_picket) > 0.5 * picket_interval or first == 1
        ):  # right now this assumes time ordering
            t_picket, pixel_dict, _ = update_pixel_dict(
                pointing["jd_tdb"], t_picket, picket_interval, sim_dict, ephem, obsCode, observatories, nside
            )
            first = 0

        # This should be a separate function
        desigs = set()
        for pix in pointing["pixels"]:
            desigs.update(pixel_dict[pix])

        for obj_id in sorted(desigs):
            v = sim_dict[obj_id]
            sim, ex, rho_hat_rough = v["sim"], v["ex"], v["rho_hat"]
            ang = np.arccos(np.dot(rho_hat_rough, pointing["visit_vector"])) * 180 / np.pi
            if ang < ang_fov + buffer:
                rho, rho_mag, lt, r_ast, v_ast = integrate_light_time(
                    sim, ex, pointing["jd_tdb"] - ephem.jd_ref, pointing["r_obs"], lt0=0.01
                )
                rho_hat = rho / rho_mag

                ang_from_center = 180 / np.pi * np.arccos(np.dot(rho_hat, pointing["visit_vector"]))
                if ang_from_center < ang_fov:
                    # Only do rates and geometry if the object is within the FOV
                    ra0, dec0 = vec2ra_dec(rho_hat)
                    drhodt = v_ast - pointing["v_obs"]
                    drho_magdt = (1 / rho_mag) * np.dot(rho, drhodt)
                    ddeltatdt = drho_magdt / (SPEED_OF_LIGHT)
                    drhodt = v_ast * (1 - ddeltatdt) - pointing["v_obs"]
                    A, D = get_residual_vectors(rho_hat)
                    drho_hatdt = drhodt / rho_mag - drho_magdt * rho_hat / rho_mag
                    dradt = np.dot(A, drho_hatdt)
                    ddecdt = np.dot(D, drho_hatdt)
                    r_ast_sun = r_ast - pointing["r_sun"]
                    v_ast_sun = v_ast - pointing["v_sun"]
                    r_ast_obs = r_ast - pointing["r_obs"]
                    phase_angle = np.arccos(
                        np.dot(r_ast_sun, r_ast_obs) / (np.linalg.norm(r_ast_sun) * np.linalg.norm(r_ast_obs))
                    )
                    obs_sun = np.asarray(pointing["r_obs"]) - np.asarray(pointing["r_sun"])
                    dobs_sundt = np.asarray(pointing["v_obs"]) - np.asarray(pointing["v_sun"])

                    out_tuple = (
                        obj_id,
                        pointing["FieldID"],
                        mjd_tai,
                        pointing["jd_tdb"],
                        rho_mag * AU_KM,
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

                    in_memory_csv.writerow(out_tuple)

    # reset to the beginning of the in-memory CSV
    output.seek(0)
    ephemeris_df = pd.read_csv(output, dtype=column_types)

    # if the user has defined an output file name for the ephemeris results, write out to that file
    if ephemeris_csv_filename:
        write_header = True
        # due to chunking, if the file already exists and it has contents, then we won't include the header information
        if os.path.exists(ephemeris_csv_filename) and os.stat(ephemeris_csv_filename).st_size != 0:
            write_header = False
        ephemeris_df.to_csv(ephemeris_csv_filename, mode="a", index=False, header=write_header)

    # join the ephemeris and input orbits dataframe, take special care to make
    # sure the 'ObjID' column types match.
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


# arguments: jd_tdb, t_picket, picket_interval, sim_dict, obsCode
# returns t_picket, pixel_dict, r_obs
def update_pixel_dict(jd_tdb, t_picket, picket_interval, sim_dict, ephem, obsCode, observatories, nside):
    n = round((jd_tdb - t_picket) / picket_interval)
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
