import numpy as np

__all__ = ["H2R", "R2H"]


def H2R(Hv, mv_sun, Ap=0.04):
    return 10 ** (0.2 * (mv_sun - Hv)) / np.sqrt(Ap) * 149597870.7


def R2H(R, mv_sun, Ap=0.04):
    return mv_sun - 5 * np.log10(R * np.sqrt(Ap) / 149597870.7)
