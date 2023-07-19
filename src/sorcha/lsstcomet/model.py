__all__ = ["Comet", "ChuryumovGerasimenko"]

import numpy as np

try:
    import astropy.units as u
except ImportError:
    u = None

from .phase import phase_HalleyMarcus, make_phase_LogLinear
from .util import H2R, R2H


class Comet:
    """LSST comet model.

    The goal of this model is to make a template comet based on ``H``
    magnitude, which is the main brightness parameter in the LSST
    Metrics Analysis Framework.  Using this value enables easy object
    cloning.


    Parameters
    ----------
    Hv or R : float
        Absolute magnitude or radius (km) of the nucleus.

    afrho1 or afrho_q: float
        Comet coma quantity Afρ at 1 au (``afrho1``) or at perihelion
        (``afrho_q``), in units of cm.  The latter requires ``q``.

    k : float
        Activity power-law slope with heliocentric distance: ``rh^k``.

    q : float, required if ``afrho_q`` is provided
        Perihelion distance for Afρ normalization.

    Phi_c : function, optional
        One-parameter function that takes phase angle in degrees and
        returns the phase function for comae.  It is assumed that
        Phi(0) = 1.0.  Default is to use the Halley-Marcus phase
        function of Schleicher & Bair 2011.

    Phi_n : function, optional
        Same as ``Phi_c`` but for nuclei.  Default is 0.04 mag/deg.

    """

    # Willmer 2018, ApJS 236, 47
    mv_sun = -26.76  # Vega mag
    m_sun = {"u": -25.30, "g": -26.52, "r": -26.93, "i": -27.05, "z": -27.07, "y": -27.07}  # AB mag

    def __init__(self, **kwargs):
        self.Hv = kwargs.get("Hv", R2H(kwargs.get("R", 1.0), self.mv_sun))

        self.R = kwargs.get("R", H2R(kwargs.get("Hv", self.Hv), self.mv_sun))

        self.k = kwargs.get("k", -2)

        self.afrho1 = kwargs.get("afrho1")
        if self.afrho1 is None:
            self.afrho1 = kwargs.get("afrho_q") * kwargs.get("q") ** -self.k

        self.Phi_c = kwargs.get("Phi_c", phase_HalleyMarcus)
        self.Phi_n = kwargs.get("Phi_n", make_phase_LogLinear(0.04))

        # self.activity = kwargs.get('Afrho2A', 100 / 4 / np.pi)
        # self.nu_range = kwargs.get('nu_range', [-180, 180])
        # self.nu_range = (np.array(self.nu_range) + 360) % 360

    @classmethod
    def from_Hv(cls, Hv, comet_class):
        """Initialize from H magnitude.

        Parameters
        ----------
        Hv : float
            Absolute magnitude of the nucleus in V-band (Vega mag).

        comet_class : string
            Name of the parameter set to use.
                * 'short': Afrho1/R**2 = 100 cm/km2, k=-4
                * 'oort': Afrho1/R**2 = 1000 cm/km2, k=-2
                * 'mbc': Afrho1/R**2 = 4000 cm/km2, k=-6

        """

        R = H2R(Hv, cls.mv_sun)

        if comet_class.lower() == "short":
            k = -4
            afrho1 = 100 * R**2
        elif comet_class.lower() == "oort":
            k = -2
            afrho1 = 100 * R**2
        elif comet_class.lower() == "mbc":
            k = -6
            afrho1 = 100 * R**2
        else:
            raise ValueError("Invalid comet_class: {}".format(comet_class))

        return cls(R=R, afrho1=afrho1, k=k)

    def _get_value(self, d, keys, unit):
        v = None
        for k in keys[::-1]:
            try:
                # this works with sbpy Ephem objects
                v = d[k]
                break
            except KeyError:
                pass

        if v is None:
            raise IndexError
        if u:
            v = u.Quantity(v, unit).value
        return v

    def _normalize_geom(self, geom):
        # allows for sbpy Ephem objects, LSST MAF ssObs, and plain
        # dictionaries
        return {
            "rh": self._get_value(geom, ("rh", "helio_dist"), "au"),
            "delta": self._get_value(geom, ("delta", "geo_dist"), "au"),
            "phase": self._get_value(geom, ("phase", "alpha"), "deg"),
        }

    def afrho(self, geom):
        """Afρ quanitity given geometrical circumstances.

        Parameters
        ----------
        geom: dictionary-like
            'rh' or 'helio_dist', and 'phase' or 'alpha' angle in au
            and deg.

        Returns
        -------
        afrho: float
            Afρ parameter in cm.

        """
        g = self._normalize_geom(geom)
        afrho = self.afrho1 * g["rh"] ** self.k * self.Phi_c(g["phase"])
        return afrho

    def mag(self, geom, bandpass, rap=1, nucleus=True):
        """Apparent magnitude within aperture.

        Parameters
        ----------
        geom : dictionary-like
            'rh' or 'helio_dist', 'delta' or 'geo_dist', and 'phase'
            angle in au and deg.

        bandpass : string
            LSST bandpass.  One of u, g, r, i, z, y.

        rap : float, optional
            Aperture radius in arcsec.

        nucleus : bool, optional
            Flag to include nucleus.

        """
        g = self._normalize_geom(geom)
        delta = 14959787070000 * g["delta"]  # au to cm

        afrho = self.afrho(g)
        rho = 725e5 * g["delta"] * rap  # arcsec to projected cm
        dm = -2.5 * np.log10(afrho * rho / (2 * g["rh"] * delta) ** 2)
        coma = self.m_sun[bandpass] + dm

        if nucleus:
            color = self.m_sun[bandpass] - self.mv_sun
            H = self.Hv + color
            nucleus = (
                H + 5 * np.log10(g["rh"]) + 5 * np.log10(g["delta"]) - 2.5 * np.log10(self.Phi_n(g["phase"]))
            )

            m = -2.5 * np.log10(10 ** (-0.4 * coma) + 10 ** (-0.4 * nucleus))
        else:
            m = coma

        return m


class ChuryumovGerasimenko(Comet):
    """67P/C-G based on Snodgrass et al. 2013.

    Presently uses post-perihelion results.

    """

    def __init__(self):
        afrho1 = 1552  # cm
        R = 2.04  # km
        # k = -3.35
        return super().__init__(R=R, afrho1=afrho1, k=-3.35)
