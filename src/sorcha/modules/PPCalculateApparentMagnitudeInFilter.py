import sys
import numpy as np
import astropy.units as u
from sbpy.photometry import HG, HG1G2, HG12_Pen16, LinearPhaseFunc
import logging

from sorcha.lightcurves.lightcurve_registration import LC_METHODS


def PPCalculateApparentMagnitudeInFilter(
    padain, function, colname="TrailedSourceMag", lightcurve_choice=None
):
    """
    This task calculates the apparent brightness of an object at a given pointing
    according to one of the following photometric phase function models:
        - HG:                Bowell et al. (1989) Asteroids II book.
        - HG1G2:             Muinonen et al. (2010) Icarus 209 542.
        - HG12:              Penttilä et al. (2016) PSS 123 117.
        - linear:             (as implemented in sbpy)

    The apparent magnitude is calculated in the filter for which the H and
    phase function variables are given. PPApplyColourOffsets should be
    run beforehand to apply any needed colour offset to H and ensure correct
    variables are present.

    The function makes use of implementations in the sbpy library.

    Parameters:
    -----------
    padain (Pandas dataframe): dataframe of observations.

    function (string): desired phase function model. Options are HG, HG12, HG1G2, linear, none.

    colname (string): column name in which to store calculated magnitude.

    lightcurve_choice (string): choice of lightcurve model. Default None


    Returns:
    ----------
    padain (Pandas dataframe): dataframe of observations with calculated magnitude column.

    """

    pplogger = logging.getLogger(__name__)

    H_col = "H_filter"

    # first, get H, r, delta and alpha as ndarrays
    # r, delta and alpha are converted to au from kilometres
    r = padain["AstRange(km)"].values / 1.495978707e8

    try:
        delta = padain["Ast-Sun(km)"] / 1.495978707e8
    except KeyError:
        delta = (
            np.sqrt(
                padain["Ast-Sun(J2000x)(km)"].values ** 2
                + padain["Ast-Sun(J2000y)(km)"].values ** 2
                + padain["Ast-Sun(J2000z)(km)"].values ** 2
            )
            / 1.495978707e8
        )

    alpha = padain["Sun-Ast-Obs(deg)"].values
    H = padain[H_col].values

    # calculating light curve offset
    if lightcurve_choice and LC_METHODS.get(lightcurve_choice, False):
        lc_model = LC_METHODS[lightcurve_choice]()
        lc_shift = lc_model.compute(padain)
        padain["Delta_m"] = lc_shift
        Heff = H + lc_shift
    else:
        Heff = H

    # calculate reduced magnitude and contribution from phase function
    # reduced magnitude = H + 2.5log10(f(phi))
    if function == "HG1G2":
        G1 = padain["G1"].values
        G2 = padain["G2"].values
        HGm = HG1G2(H=Heff * u.mag, G1=G1, G2=G2)
        reduced_mag = HGm(alpha * u.deg).value

    elif function == "HG":
        G = padain["GS"].values
        HGm = HG(H=Heff * u.mag, G=G)
        reduced_mag = HGm(alpha * u.deg).value

    elif function == "HG12":
        G12 = padain["G12"].values
        HGm = HG12_Pen16(H=Heff * u.mag, G12=G12)
        reduced_mag = HGm(alpha * u.deg).value

    elif function == "linear":
        S = padain["S"].values
        HGm = LinearPhaseFunc(H=Heff * u.mag, S=S * u.mag / u.deg)
        reduced_mag = HGm(alpha * u.deg).value

    elif function == "none":
        reduced_mag = Heff.copy()

    else:
        pplogger.error(
            "ERROR: PPCalculateApparentMagnitudeInFilter: unknown phase function. Should be HG1G2, HG, HG12 or linear."
        )
        sys.exit(
            "ERROR: PPCalculateApparentMagnitudeInFilter: unknown phase function. Should be HG1G2, HG, HG12 or linear."
        )

    # apparent magnitude equation: see equation 1 in Schwamb et al. 2023
    padain[colname] = 5.0 * np.log10(delta) + 5.0 * np.log10(r) + reduced_mag

    padain = padain.reset_index(drop=True)

    return padain
