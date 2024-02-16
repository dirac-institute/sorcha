import numpy as np


def test_orbit_conversion_relationships():
    # this uses a very similar idea to the demo notebook - this is a case where we *know* the answer
    from sorcha.ephemeris.orbit_conversion_utilities import universal_cartesian, universal_keplerian

    # define orbits (no e)
    q = 10
    i = 0
    Omega = 0
    omega = 0
    Tp = 0
    # define constants
    epochMJD_TDB = 0
    mu = 1
    # the answer is: (10,0,0) for all tested orbits. They're at perihelion in a well chosen set of units
    # this also means the vx = 0, and, since i = 0, vz = 0. vy > 0 is the final constraint from this setup

    for e in [0, 0.1, 0.9999, 1.0, 1.0001, 6.0]:
        x, y, z, vx, vy, vz = universal_cartesian(mu, q, e, i, Omega, omega, Tp, epochMJD_TDB)
        assert np.isclose(x, 10.0)
        assert np.isclose(y, 0.0)
        assert np.isclose(z, 0.0)
        assert np.isclose(vx, 0.0)
        assert vy > 0
        assert np.isclose(vz, 0.0)

    # we also know that we are invariant under 2 pi rotations in Omega and omega
    for e in [0, 0.1, 0.9999, 1.0, 1.0001, 6.0]:
        x, y, z, vx, vy, vz = universal_cartesian(
            mu, q, e, i, Omega + 2 * np.pi, omega + 2 * np.pi, Tp, epochMJD_TDB
        )
        assert np.isclose(x, 10.0)
        assert np.isclose(y, 0.0)
        assert np.isclose(z, 0.0)
        assert np.isclose(vx, 0.0)
        assert vy > 0
        assert np.isclose(vz, 0.0)
        x, y, z, vx, vy, vz = universal_cartesian(
            mu, q, e, i, Omega - 2 * np.pi, omega - 2 * np.pi, Tp, epochMJD_TDB
        )
        assert np.isclose(x, 10.0)
        assert np.isclose(y, 0.0)
        assert np.isclose(z, 0.0)
        assert np.isclose(vx, 0.0)
        assert vy > 0
        assert np.isclose(vz, 0.0)

    # finally, if we rotate inclination to 90 deg, we should flip vz and vy
    for e in [0, 0.1, 0.9999, 1.0, 1.0001, 6.0]:
        x_0, y_0, z_0, vx_0, vy_0, vz_0 = universal_cartesian(mu, q, e, 0.0, Omega, omega, Tp, epochMJD_TDB)
        x_90, y_90, z_90, vx_90, vy_90, vz_90 = universal_cartesian(
            mu, q, e, np.pi / 2, Omega, omega, Tp, epochMJD_TDB
        )
        assert np.isclose(x_0, x_90)
        assert np.isclose(y_0, y_90)
        assert np.isclose(z_0, z_90)
        assert np.isclose(vx_0, vx_90)
        # note these are different now!
        assert np.isclose(vy_0, vz_90)
        assert np.isclose(vz_0, vy_90)


def test_orbit_conversion_edgecases():
    from sorcha.ephemeris.orbit_conversion_utilities import universal_cartesian, universal_keplerian

    # this will test weird edge cases that require additional work to converge to a solution
    # fow now, this only has the Centaur from one of our larger test populations
    # additional weirdos should be added as needed
    gm_sun = 2.9591220828559115e-04

    a = 23.38
    e = 0.4839
    inc = 31.58
    node = 294.2
    argPeri = 303.4
    ma = 158.4
    epochMJD_TDB = 60676.0

    q = a * (1 - e)
    Tp = epochMJD_TDB - (ma * np.pi / 180.0) * np.sqrt(a**3 / gm_sun)

    x, y, z, vx, vy, vz = universal_cartesian(
        gm_sun, q, e, inc * np.pi / 180, node * np.pi / 180, argPeri * np.pi / 180, Tp, epochMJD_TDB
    )

    # independently computed state vector from destnosim
    x_p = 18.33081872
    y_p = 23.99734358
    z_p = 16.3251825
    vx_p = -0.00132138
    vy_p = 0.00165302
    vz_p = -0.00032436

    assert np.isclose(x, x_p)
    assert np.isclose(y, y_p)
    assert np.isclose(z, z_p)
    assert np.isclose(vx, vx_p)
    assert np.isclose(vy, vy_p)
    assert np.isclose(vz, vz_p)


def test_orbit_conversion_realdata():
    from sorcha.ephemeris.simulation_parsing import parse_orbit_row
    from collections import namedtuple

    # constants

    # values from the spice kernel - dec 13 2023
    gm_sun = 2.9591220828559115e-04
    gm_total = 2.9630927487993194e-04

    # this is a hack where we are hardcoding the Sun positions at the time (computed using JPL)
    # note that this needs to be a namedtuple due to the way `parse_orbit_row` expects the input
    Sun = namedtuple("Sun", "x y z vx vy vz")

    # this is similar to the notebook - values come from JPL and are for asteroid Holman
    # let's start with Holman
    epochJD_TDB = 2457545.5
    # note these are equatorially aligned\
    sun_epoch = Sun(
        x=3.743893517879733e-03,
        y=2.355922092887896e-03,
        z=8.440770737482685e-04,
        vx=-7.096646739414067e-07,
        vy=6.421467712437571e-06,
        vz=2.788964122162865e-06,
    )
    # sun_epoch = Sun(x = 0, y = 0, z = 0, vx = 0, vy = 0, vz = 0)
    sun_dict = {epochJD_TDB: sun_epoch}
    # heliocentric keplerian and cometary - note angles are in degrees!
    e_helio = 1.273098035049758e-01
    q_helio = 2.719440725596252e00
    inc_helio = 2.363582123773087e00
    lan_helio = 1.203869311659506e02
    aop_helio = 5.506308037812056e01
    Tp_helio = 2457934.552658705506
    M_helio = 2.902919054404318e02
    a_helio = 3.116158215731438e00
    # heliocentric cartesian (ecliptic)
    X_helio = -7.569545429706993e-02
    Y_helio = 3.024083648650882e00
    Z_helio = -6.044399403284755e-02
    VX_helio = -9.914117209213893e-03
    VY_helio = -1.485136186100886e-03
    VZ_helio = 3.840061650310168e-04
    # barycentric keplerian and cometary
    e_bary = 1.277080918842867e-01
    q_bary = 2.718601009368714e00
    inc_bary = 2.364051308275402e00
    lan_bary = 1.203686955102486e02
    aop_bary = 5.537099088407054e01
    Tp_bary = 2457936.050825081766
    M_bary = 2.899920485236385e02
    a_bary = 3.116618398124679e00
    # barycentric cartesian (ecliptic!)
    X_bary = -7.195156074800051e-02
    Y_bary = 3.026580919478138e00
    Z_bary = -6.060670045129734e-02
    VX_bary = -9.914826873812788e-03
    VY_bary = -1.478135218486216e-03
    VZ_bary = 3.840106764287660e-04

    # barycentric cartesian (equatorial) - these are the reference values for comparison
    x_bary_eq = -7.195156074800051e-02
    y_bary_eq = 2.800941663957977e00
    z_bary_eq = 1.148299189842545e00
    vx_bary_eq = -9.914826873812788e-03
    vy_bary_eq = -1.508913222991139e-03
    vz_bary_eq = -2.356455160257992e-04
    vec_bary = np.array([x_bary_eq, y_bary_eq, z_bary_eq, vx_bary_eq, vy_bary_eq, vz_bary_eq])
    # let's not import pandas - we can use simple dictionaries here

    # COM - note Tp needs to be in MJD for input
    COM_elements = {
        "q": q_helio,
        "e": e_helio,
        "inc": inc_helio,
        "node": lan_helio,
        "argPeri": aop_helio,
        "t_p_MJD_TDB": Tp_helio - 2400000.5,
        "FORMAT": "COM",
    }
    KEP_elements = {
        "a": a_helio,
        "e": e_helio,
        "inc": inc_helio,
        "node": lan_helio,
        "argPeri": aop_helio,
        "ma": M_helio,
        "FORMAT": "KEP",
    }
    CART_elements = {
        "x": X_helio,
        "y": Y_helio,
        "z": Z_helio,
        "xdot": VX_helio,
        "ydot": VY_helio,
        "zdot": VZ_helio,
        "FORMAT": "CART",
    }

    BCOM_elements = {
        "q": q_bary,
        "e": e_bary,
        "inc": inc_bary,
        "node": lan_bary,
        "argPeri": aop_bary,
        "t_p_MJD_TDB": Tp_bary - 2400000.5,
        "FORMAT": "BCOM",
    }
    BKEP_elements = {
        "a": a_bary,
        "e": e_bary,
        "inc": inc_bary,
        "node": lan_bary,
        "argPeri": aop_bary,
        "ma": M_bary,
        "FORMAT": "BKEP",
    }
    BCART_elements = {
        "x": X_bary,
        "y": Y_bary,
        "z": Z_bary,
        "xdot": VX_bary,
        "ydot": VY_bary,
        "zdot": VZ_bary,
        "FORMAT": "BCART",
    }

    orbit_types = {
        "COM": COM_elements,
        "KEP": KEP_elements,
        "CART": CART_elements,
        "BCOM": BCOM_elements,
        "BKEP": BKEP_elements,
        "BCART": BCART_elements,
    }
    for i in orbit_types:
        converted = np.array(parse_orbit_row(orbit_types[i], epochJD_TDB, None, sun_dict, gm_sun, gm_total))
        for j in range(6):
            assert np.isclose(converted[j], vec_bary[j])
