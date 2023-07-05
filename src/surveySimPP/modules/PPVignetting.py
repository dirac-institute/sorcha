import numpy as np

deg2rad = np.radians
rad2deg = np.degrees
sin = np.sin
cos = np.cos


def vignettingEffects(
    oifdf,
    raNameOIF="AstRA(deg)",
    decNameOIF="AstDec(deg)",
    fieldNameOIF="FieldID",
    raNameSurvey="fieldRA",
    decNameSurvey="fieldDec",
):
    """
    Calculates effective limiting magnitude at source, taking vignetting into account.
    Wrapper for calcVignettingLosses.

    Parameters:
    -----------
    oif_df (Pandas dataframe): dataframe of observations.

    *NameOIF (strings): column names of object RA, object Dec, field ID, field RA and field Dec respectively.

    Returns:
    -----------
    Pandas series: five sigma depth at object location, adjusted for vignetting.

    """

    dmagVignet = calcVignettingLosses(
        oifdf[raNameOIF], oifdf[decNameOIF], oifdf[raNameSurvey], oifdf[decNameSurvey]
    )

    return oifdf["fiveSigmaDepth"] - dmagVignet


def calcVignettingLosses(ra, dec, fieldra, fielddec):
    """
    Calculates magnitude loss due to vignetting for a point with the telescope
    centered on fieldra, fielddec.

    Parameters:
    -----------
    ra (float/array of floats): RA of object(s).

    dec (float/array of floats): Dec of object(s).

    fieldra (float/array of floats): RA of field(s).

    fielddec (float/array of floats): Dec of field(s).

    Returns:
    -----------
    Magnitude loss due to vignetting at object position (float/array of floats).

    """

    RA = deg2rad(ra)
    Dec = deg2rad(dec)
    fieldRA = deg2rad(fieldra)
    fieldDec = deg2rad(fielddec)

    theta = rad2deg(haversine(RA, Dec, fieldRA, fieldDec))

    return vignetFunc(theta)


def haversine(ra1, dec1, ra2, dec2):
    """
    Calculates angular distance between two points. Can produce floating point
    errors for antipodal points, which are not intended to be encountered within
    the scope of this module.

    Parameters:
    -----------
    ra1 (float/array of floats): RA of first point.

    dec1 (float/array of floats): Dec of first point.

    ra2 (float/array of floats): RA of second point.

    dec2 (float/array of floats): Dec of second point.

    Returns:
    -----------
    Angular distance between two points (float/array of floats).

    """

    return 2.0 * np.arcsin(
        np.sqrt(sin((dec2 - dec1) / 2.0) ** 2 + cos(dec1) * cos(dec2) * sin((ra2 - ra1) / 2.0) ** 2)
    )


def vignetFunc(x):
    """
    Grabbed from sims_selfcal. From VignettingFunc_v3.3.TXT. r is in degrees,
    frac is fraction of rays which were not vignetted. Returns the magnitudes
    of dimming caused by the vignetting relative to the center of the field.

    Parameters:
    -----------
    x (float/array of floats): angular separation of point from field centre.

    Returns:
    -----------
    Magnitude of dimming due to vignetting at object position (float/array of floats).

    """

    if not hasattr(vignetFunc, "r"):
        vignetFunc.r = np.array(
            [
                0.000000,
                0.020000,
                0.040000,
                0.060000,
                0.080000,
                0.100000,
                0.120000,
                0.140000,
                0.160000,
                0.180000,
                0.200000,
                0.220000,
                0.240000,
                0.260000,
                0.280000,
                0.300000,
                0.320000,
                0.340000,
                0.360000,
                0.380000,
                0.400000,
                0.420000,
                0.440000,
                0.460000,
                0.480000,
                0.500000,
                0.520000,
                0.540000,
                0.560000,
                0.580000,
                0.600000,
                0.620000,
                0.640000,
                0.660000,
                0.680000,
                0.700000,
                0.720000,
                0.740000,
                0.760000,
                0.780000,
                0.800000,
                0.820000,
                0.840000,
                0.860000,
                0.880000,
                0.900000,
                0.920000,
                0.940000,
                0.960000,
                0.980000,
                1.000000,
                1.020000,
                1.040000,
                1.060000,
                1.080000,
                1.100000,
                1.120000,
                1.140000,
                1.160000,
                1.180000,
                1.200000,
                1.220000,
                1.240000,
                1.260000,
                1.280000,
                1.300000,
                1.320000,
                1.340000,
                1.360000,
                1.380000,
                1.400000,
                1.420000,
                1.440000,
                1.460000,
                1.480000,
                1.500000,
                1.520000,
                1.540000,
                1.560000,
                1.580000,
                1.600000,
                1.620000,
                1.640000,
                1.660000,
                1.680000,
                1.700000,
                1.720000,
                1.740000,
                1.760000,
                1.780000,
                1.800000,
                1.820000,
                1.840000,
                1.860000,
                1.880000,
                1.900000,
                1.920000,
                1.940000,
                1.960000,
                1.980000,
                2.000000,
            ]
        )
        vignetFunc.frac = np.array(
            [
                0.623885,
                0.623885,
                0.623885,
                0.623885,
                0.623885,
                0.623885,
                0.623885,
                0.623885,
                0.623885,
                0.623885,
                0.623885,
                0.623885,
                0.623885,
                0.623885,
                0.623885,
                0.623885,
                0.623885,
                0.623885,
                0.623885,
                0.623885,
                0.623885,
                0.623885,
                0.623885,
                0.623885,
                0.623885,
                0.623885,
                0.623885,
                0.623885,
                0.623885,
                0.623885,
                0.623885,
                0.623885,
                0.623885,
                0.623822,
                0.623759,
                0.623632,
                0.623442,
                0.623316,
                0.623000,
                0.622494,
                0.622367,
                0.621861,
                0.621671,
                0.621292,
                0.621039,
                0.620659,
                0.620216,
                0.619963,
                0.619394,
                0.619204,
                0.618635,
                0.618319,
                0.618066,
                0.617496,
                0.617117,
                0.616737,
                0.616168,
                0.615535,
                0.614840,
                0.614207,
                0.613385,
                0.612436,
                0.611614,
                0.610602,
                0.609716,
                0.608957,
                0.608071,
                0.606996,
                0.605668,
                0.604972,
                0.603770,
                0.602758,
                0.601177,
                0.599595,
                0.598140,
                0.595673,
                0.594282,
                0.592447,
                0.590613,
                0.588526,
                0.586312,
                0.584287,
                0.582137,
                0.580113,
                0.578025,
                0.576064,
                0.573344,
                0.570561,
                0.563730,
                0.545322,
                0.521412,
                0.492757,
                0.460624,
                0.429565,
                0.404959,
                0.383073,
                0.356190,
                0.317161,
                0.279777,
                0.241824,
                0.201974,
            ]
        )
        vignetFunc.frac = vignetFunc.frac / vignetFunc.frac[0]

    result = -2.5 * np.log10(np.interp(x, vignetFunc.r, vignetFunc.frac))

    return result
