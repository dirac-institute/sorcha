import numpy as np
import numba
from collections import namedtuple

halley_result = namedtuple(
    "halley_result",
    "root iterations function_calls converged flag f fp fpp",
    defaults=(np.nan, 0, 0, False, np.nan, np.nan, np.nan),
)


@numba.njit(fastmath=True)
def stumpff(x):
    n = 0
    xm = 0.1

    while np.abs(x) > xm:
        n += 1
        x /= 4

    d2 = (
        1 - x * (1 - x * (1 - x * (1 - x * (1 - x * (1 - x / 182.0) / 132.0) / 90.0) / 56.0) / 30.0) / 12.0
    ) / 2.0
    d3 = (
        1 - x * (1 - x * (1 - x * (1 - x * (1 - x * (1 - x / 210.0) / 156.0) / 110.0) / 72.0) / 42.0) / 20.0
    ) / 6.0

    d1 = 1.0 - x * d3
    d0 = 1.0 - x * d2

    while n > 0:
        n -= 1
        d3 = (d2 + d0 * d3) / 4.0
        d2 = d1 * d1 / 2.0
        d1 = d0 * d1
        d0 = 2.0 * d0 * d0 - 1.0

    return d0, d1, d2, d3


@numba.njit(fastmath=True)
def root_function(s, mu, alpha, r0, r0dot, t):
    c0, c1, c2, c3 = stumpff(alpha * s * s)
    zeta = mu - alpha * r0
    f = r0 * s * c1 + r0 * r0dot * s * s * c2 + mu * s * s * s * c3 - t
    fp = r0 * c0 + r0 * r0dot * s * c1 + mu * s * s * c2  # This is equivalent to r.
    fpp = zeta * s * c1 + r0 * r0dot * c0
    fppp = zeta * c0 - r0 * r0dot * alpha * s * c1
    return f, fp, fpp, fppp


@numba.njit
def halley_safe(x1, x2, mu, alpha, r0, r0dot, t, xacc=1e-14, maxit=100):
    # verify the bracket
    # Use these values later
    fl, fpl, fppl = root_function(x1, mu, alpha, r0, r0dot, t)[0:3]
    fh, fph, fpph = root_function(x2, mu, alpha, r0, r0dot, t)[0:3]
    if (fl > 0.0 and fh > 0.0) or (fl < 0.0 and fh < 0.0):
        return False, np.nan, fl
    if fl == 0:
        return True, x1, fpl
    if fh == 0:
        return True, x2, fph

    # Orient the search so that f(xl) < 0 and f(xh)>0
    if fl < 0.0:
        xl = x1
        xh = x2
    else:
        xh = x1
        xl = x2

    if np.abs(fl) < np.abs(fh):
        rts, f, fp, fpp = xl, fl, fpl, fppl
    else:
        rts, f, fp, fpp = xh, fh, fph, fpph

    rts = 0.5 * (x1 + x2)  # Initialize the guess for root,
    dxold = np.abs(x2 - x1)  # the “stepsize before last,”
    dx = dxold  # and the last step.
    f, fp, fpp = root_function(rts, mu, alpha, r0, r0dot, t)[0:3]
    for j in range(maxit):  # Loop over allowed iterations.
        if (((rts - xh) * fp - f) * ((rts - xl) * fp - f) > 0.0) or (np.abs(2.0 * f) > np.abs(dxold * fp)):
            # Check the criteria.
            dxold = dx
            dx = 0.5 * (xh - xl)
            rts = xl + dx
            if np.abs(dx / rts) < xacc:
                return True, rts, fp
        else:
            dxold = dx
            dx = f / fp
            dx = 2 * f * fp / (2 * fp * fp - f * fpp)  # halley
            temp = rts
            rts -= dx
            if np.abs(dx / rts) < xacc:
                return True, rts, fp
        if np.abs(dx / rts) < xacc:
            return True, rts, fp
        f, fp, fpp = root_function(rts, mu, alpha, r0, r0dot, t)[0:3]
        # Maintain the bracket on the root.
        if f < 0.0:
            xl = rts
            fl = f
        else:
            xh = rts
            fh = f

    return False, np.nan, fp


@numba.njit(fastmath=True)
def universal_cartesian(mu, q, e, incl, longnode, argperi, tp, epochMJD_TDB):
    # General constant
    p = q * (1 + e)
    t = epochMJD_TDB - tp  # tp - epochMJD_TDB

    if e < 1:
        a = q / (1 - e)
        per = 2 * np.pi / np.sqrt(mu / (a * a * a))
        t = t % per

    # Establish constants for Kepler's equation,
    # starting at pericenter:
    r0 = q
    r0dot = 0
    v2 = mu * (1 + e) / q
    alpha = 2 * mu / r0 - v2

    # print(alpha, np.sqrt(v2), mu/alpha)

    # bracket the root
    count = 0
    ds = (t - 0) / 4
    s_prev = 0
    f_prev = root_function(s_prev, mu, alpha, r0, r0dot, t)[0]
    s = s_prev + ds
    f = root_function(s, mu, alpha, r0, r0dot, t)[0]
    count += 1
    while f * f_prev > 0.0:
        s_prev = s
        f_prev = f
        s = s_prev + ds
        f = root_function(s, mu, alpha, r0, r0dot, t)[0]
        count += 1

    converged, ss, fp = halley_safe(s_prev, s, mu, alpha, r0, r0dot, t)
    if not converged:
        return np.nan, np.nan, np.nan, np.nan, np.nan, np.nan

    c0, c1, c2, c3 = stumpff(alpha * ss * ss)
    count += 1

    r = r0 * c0 + r0 * r0dot * ss * c1 + mu * ss * ss * c2  # This is equivalent to fp.

    g0 = c0
    g1 = c1 * ss
    g2 = c2 * ss * ss
    g3 = c3 * ss * ss * ss

    f = 1.0 - (mu / r0) * g2
    g = t - mu * g3
    fdot = -(mu / (r * r0)) * g1
    gdot = 1.0 - (mu / r) * g2

    # define position and velocity at pericenter
    x0 = np.array((q, 0.0, 0.0))
    v0 = np.array((0.0, np.sqrt(v2), 0.0))

    # compute position and velocity at time t (from pericenter)
    xt = f * x0 + g * v0
    vt = fdot * x0 + gdot * v0

    # Could probably make all these rotations separate routine

    # rotate by argument of perihelion in orbit plane
    cosw = np.cos(argperi)
    sinw = np.sin(argperi)

    omega_matrix = np.array(((cosw, -sinw, 0), (sinw, cosw, 0), (0, 0, 1)))

    xp = omega_matrix @ xt
    vp = omega_matrix @ vt

    # rotate by inclination about x axis
    cosi = np.cos(incl)
    sini = np.sin(incl)
    incl_matrix = np.array(((1, 0, 0), (0, cosi, -sini), (0, sini, cosi)))
    xpp = incl_matrix @ xp
    vpp = incl_matrix @ vp

    # rotate by longitude of node about z axis
    cosnode = np.cos(longnode)
    sinnode = np.sin(longnode)

    Omega_matrix = np.array(((cosnode, -sinnode, 0), (sinnode, cosnode, 0), (0, 0, 1)))

    xp = Omega_matrix @ xpp
    vp = Omega_matrix @ vpp

    return xp[0], xp[1], xp[2], vp[0], vp[1], vp[2]


@numba.njit
def principal_value(theta):
    if theta < 0:
        theta = theta - 2 * np.pi * np.ceil(theta / (2 * np.pi))
    else:
        theta = theta - 2 * np.pi * np.floor(theta / (2 * np.pi))
    return theta


@numba.njit(fastmath=True)
def universal_keplerian(mu, x, y, z, vx, vy, vz, epochMJD_TDB):
    pos = np.array([x, y, z])
    vel = np.array([vx, vy, vz])
    h_vec = np.cross(pos, vel)
    hs = np.dot(h_vec, h_vec)
    h = np.sqrt(hs)

    r = np.linalg.norm(pos)

    v2 = np.dot(vel, vel)

    rdotv = np.dot(pos, vel)
    rdot = rdotv / r

    p = hs / mu
    alpha = 2 * mu / r - v2

    incl = np.arccos(h_vec[2] / h)

    if h_vec[0] != 0.0 and h_vec[1] != 0.0:
        longnode = np.arctan2(h_vec[0], -h_vec[1])
    else:
        longnode = 0.0

    ecostrueanom = p / r - 1.0
    esintrueanom = rdot * h / mu
    e = np.sqrt(ecostrueanom * ecostrueanom + esintrueanom * esintrueanom)

    q = p / (1 + e)

    if esintrueanom != 0.0 and ecostrueanom != 0.0:
        trueanom = np.arctan2(esintrueanom, ecostrueanom)
    else:
        trueanom = 0.0

    cosnode = np.cos(longnode)
    sinnode = np.sin(longnode)

    # u is the argument of latitude
    rcosu = pos[0] * cosnode + pos[1] * sinnode
    rsinu = (pos[1] * cosnode - pos[0] * sinnode) / np.cos(incl)  # should check zero

    if rsinu != 0.0 and rcosu != 0.0:
        u = np.arctan2(rsinu, rcosu)
    else:
        u = 0.0

    argperi = u - trueanom

    # There should a better way to handle this.

    # Branch on e at this point, until there's a better solution
    # Be careful with the e=1 transition.
    if np.abs(e - 1) < 1e-15:
        e = 1
    if e < 1:
        # elliptical
        eccanom = 2.0 * np.arctan(np.sqrt((1.0 - e) / (1.0 + e)) * np.tan(trueanom / 2.0))
        meananom = eccanom - e * np.sin(eccanom)
        meananom = principal_value(meananom)
        a = mu / alpha
        mm = np.sqrt(mu / (a * a * a))
        tp = epochMJD_TDB - meananom / mm
    elif e == 1:
        # parabolic
        tf = np.tan(0.5 * trueanom)
        B = 0.5 * (tf * tf * tf + 3 * tf)
        mm = np.sqrt(mu / (p * p * p))
        tp = epochMJD_TDB - B / (3 * mm)
    else:
        # hyperbolic
        heccanom = 2.0 * np.arctanh(np.sqrt((e - 1.0) / (e + 1.0)) * np.tan(trueanom / 2.0))
        N = e * np.sinh(heccanom) - heccanom
        a = mu / alpha
        mm = np.sqrt(-mu / (a * a * a))
        tp = epochMJD_TDB - N / mm

    return q, e, incl, longnode, argperi, tp
