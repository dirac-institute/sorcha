import pytest
import numpy as np
import pandas as pd
from sorcha.ephemeris.simulation_driver import calculate_rates_and_geometry, EphemerisGeometryParameters


def test_calculate_rates_and_geometry():
    ephem_geom_params = EphemerisGeometryParameters()
    ephem_geom_params.obj_id = "S100cuR2a"
    ephem_geom_params.mjd_tai = 60218.98462644687
    ephem_geom_params.rho = np.asarray([1.23883859, -1.59558594, -0.94141702])
    ephem_geom_params.rho_mag = 2.2286501594614134
    ephem_geom_params.rho_hat = np.asarray([0.55586947, -0.71594276, -0.42241579])
    ephem_geom_params.r_ast = np.asarray([2.22134111, -1.4666382, -0.88530195])
    ephem_geom_params.v_ast = np.asarray([0.00608846, 0.00585226, 0.00487886])

    pointing_df = pd.DataFrame(
        {
            "FieldID": 848,
            "observationStartMJD_TAI": 60218.984626,
            "optFilter": "i",
            "seeingFwhmGeom": 1.1027086372149535,
            "seeingFwhmEff": 1.2782343518430093,
            "fiveSigmaDepth": 22.951091131134614,
            "fieldRA": 307.3355402760053,
            "fieldDec": -23.54289743479277,
            "rotSkyPos": 112.25651472435484,
            "observationId_": 848,
            "visit_vector": [[0.555998946329719, -0.7289145382156643, -0.399435561333849]],
            "JD_TDB": 2460219.484998981,
            "pixels": None,
            "r_obs": [[0.9825025212987633, 0.12894773431445178, 0.056115072741286603]],
            "v_obs": [[-0.002514846222194574, 0.015645226468919866, 0.006740310710189443]],
            "r_sun": [[-0.008375571318557293, -0.0021278397223137443, -0.0006896179222345509]],
            "v_sun": [[4.014508061373484e-06, -7.199434717117629e-06, -3.1502131721138966e-06]],
        }
    )

    single_pointing = pointing_df.iloc[0]

    output_tuple = calculate_rates_and_geometry(single_pointing, ephem_geom_params)

    expected_tuple = (
        "S100cuR2a",
        848,
        60218.98462644687,
        2460219.484998981,
        333401318.3906429,
        21.781422998045304,
        307.8263396305563,
        0.020288816433054996,
        -24.987200752790443,
        0.09791651860940978,
        333560867.6659607,
        -219087631.65531665,
        -132336121.193526,
        10.534961069620792,
        10.145404535726742,
        8.452994256388143,
        148233252.77882853,
        19608626.776680324,
        8497860.769034933,
        -4.361298632362694,
        27.101499843444632,
        11.676011519485472,
        18.73383934462223,
    )

    assert np.allclose(output_tuple[1:], expected_tuple[1:])
