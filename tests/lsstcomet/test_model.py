import numpy as np
import astropy.units as u
from sbpy.activity import Afrho
import synphot
from sorcha.lsstcomet.model import Comet

from sorcha.utilities.dataUtilitiesForTests import get_test_filepath


class TestComet:
    def test_afrho(self):
        comet = Comet(R=1, afrho1=100, k=-2)
        g = {"rh": 2.0, "delta": 1.0, "phase": 0}
        assert np.isclose(comet.afrho(g), 100 * 2**-2)

    def test_mag(self):
        # compare to sbpy
        g = {"rh": 2.0 * u.au, "delta": 1.0 * u.au, "phase": 0 * u.deg}
        afrho = Afrho(100 * 2**-2, "cm")
        tab = np.loadtxt(get_test_filepath("lsst-total-r.dat")).T
        r = synphot.SpectralElement(synphot.Empirical1D, points=tab[0] * u.nm, lookup_table=tab[1])
        rap = 1 * u.arcsec
        m0 = afrho.to_fluxd(r, rap, g, unit=u.ABmag).value

        comet = Comet(R=1, afrho1=100, k=-2)
        m = comet.mag(g, "r", rap=rap.value, nucleus=False)

        assert np.isclose(m, m0, atol=0.05)

    def test_init_R(self):
        comet = Comet(R=0.835, afrho1=100, k=-2)
        assert np.isclose(comet.Hv, 18, atol=0.002)

    def test_init_H(self):
        comet = Comet(Hv=18, afrho1=100, k=-2)
        assert np.isclose(comet.R, 0.835, atol=0.001)
