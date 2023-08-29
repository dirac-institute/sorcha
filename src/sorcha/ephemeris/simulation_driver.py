import spiceypy as spice
from sorcha.ephemeris.simulation_setup import *
from sorcha.ephemeris.simulation_constants import *
from collections import defaultdict
from os import path
import csv
from sorcha.ephemeris.simulation_geometry import *
from sorcha.ephemeris.simulation_parsing import *
import numpy as np
from sorcha.utilities.dataUtilitiesForTests import get_data_out_filepath
from sorcha.modules.PPReadPointingDatabase import PPReadPointingDatabase

# TODO: this should be handled by the `simulation_data_files` module
dir_path = "/Users/maxwest/notebooks/assist_plus_rebound/input_for_mpchecker"

out_path = get_data_out_filepath("checker.txt")


def create_ephemeris(args, configs):
    ang_fov = configs["ar_ang_fov"]
    buffer = configs["ar_fov_buffer"]
    picket_interval = configs["ar_picket"]
    obsCode = configs["ar_obs_code"]
    nside = 2 ** configs["ar_healpix_order"]
    first = 1  # Try to get away from this

    t_picket = 2460000.5

    ephem = create_assist_ephemeris()
    furnish_spiceypy()
    sim_dict = generate_simulations(ephem)
    pixel_dict = defaultdict(list)
    observatories = Observatory()

    outfile = open(out_path, "w", encoding="utf-8")

    pointings_df = PPReadPointingDatabase(
        args.pointing_database, configs["observing_filters"], configs["pointing_sql_query"]
    )
    for _, pointing in pointings_df.iterrows():
        mjd_tai = float(pointing["observationStartMJD"])
        ra, dec = float(pointing["fieldRA"]), float(pointing["fieldDec"])
        visit_vec = ra_dec2vec(ra, dec)
        pixels = get_hp_neighbors(ra, dec, ang_fov + buffer, nside=nside, nested=True)
        jd_tdb = mjd_tai_to_epoch(mjd_tai)
        et = (jd_tdb - spice.j2000()) * 24 * 60 * 60
        utc_str = spice.et2utc(et, "J", 7)
        r_obs = observatories.barycentricObservatory(et, obsCode) / AU_KM

        # If the observation time is too far from the
        # time of the last set of ballpark sky position,
        # compute a new set
        while (
            abs(jd_tdb - t_picket) > 0.5 * picket_interval or first == 1
        ):  # right now this assumes a direction
            # This section should be a separate function
            # print('picket', jd_tdb, t_picket)
            n = round((jd_tdb - t_picket) / picket_interval)
            t_picket += n * picket_interval
            first = 0
            et = (t_picket - spice.j2000()) * 24 * 60 * 60
            r_obs = observatories.barycentricObservatory(et, obsCode) / AU_KM
            pixel_dict.clear()
            for k, v in sim_dict.items():
                sim, ex = v["sim"], v["ex"]
                ex.integrate_or_interpolate(t_picket - ephem.jd_ref)
                rho = np.array(sim.particles[0].xyz) - r_obs
                rho_hat = rho / np.linalg.norm(rho)
                sim_dict[k]["rho_hat"] = rho_hat
                this_pix = hp.vec2pix(nside, rho_hat[0], rho_hat[1], rho_hat[2], nest=True)
                pixel_dict[this_pix].append(k)

        # This should be a separate function
        desigs = set()
        for pix in pixels:
            desigs.update(pixel_dict[pix])

        for k in desigs:
            v = sim_dict[k]
            sim, ex, rho_hat_rough = v["sim"], v["ex"], v["rho_hat"]
            ang = np.arccos(np.dot(rho_hat_rough, visit_vec)) * 180 / np.pi
            if ang < ang_fov + buffer:
                rho, rho_mag, lt = integrate_light_time(sim, ex, jd_tdb - ephem.jd_ref, r_obs, lt0=0.01)
                rho_hat = rho / rho_mag
                ra0, dec0 = vec2ra_dec(rho_hat)

                ang_from_center = 180 / np.pi * np.arccos(np.dot(rho_hat, visit_vec))
                if ang_from_center < ang_fov:
                    outstring = "%lf %lf %s %s %f %f %lf\n" % (
                        jd_tdb,
                        mjd_tai,
                        utc_str,
                        k,
                        ra0,
                        dec0,
                        ang_from_center,
                    )
                    outfile.write(outstring)

    outfile.close()
    spice.kclear()
