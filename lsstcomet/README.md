# lsstcomet
Template comet models for LSST.

# Examples
## Photometric Model

The model is based on the Afρ quantity of A'Hearn et al. (1984) and
the nucleus radius.

Example: Comet 67P/Churyumov-Gerasimenko, radius = 2 km, Afρ at
perihelion = 1500 cm at 1.29 au, falling with rh**-3.35.  Observe at
rh = 1.5 au, delta = 1.0 au, phase = 30 deg, LSST r-band, 1" radius
aperture:

``` python
>>> from lsstcomet import Comet
>>> comet_cg = Comet(R=2, afrho_q=1500, q=1.29, k=-3.35)
>>> g = {'rh': 1.5, 'delta': 1.0, 'phase': 30}
>>> print(comet_cg.mag(g, 'r', rap=1))
15.163185893463375
```

Use `sbpy`'s ephemeris object:

``` python
>>> from sbpy.data import Ephem
>>> epochs = {'start': '2015-08-15', 'stop': '2017-08-15', 'step': '10d'}
>>> eph = Ephem.from_horizons('67P', id_type='designation',
...                           epochs=epochs, closest_apparition=True)
>>> print(comet_cg.mag(eph, 'r', rap=1))
[14.818066   14.85643785 14.95028233 15.09272597 15.27433532 15.48484197
 15.71394234 15.9522569  16.19193125 16.4262542  16.64974682 16.8580641
 17.04731069 17.21386977 17.35478671 17.46640137 17.54661195 17.59482436
 17.61375638 17.61296238 17.61493974 17.69987652 17.99285274 18.34850299
 18.69129768 19.00780463 19.29598928 19.5566426  19.7911343  20.00159282
 20.18983971 20.35734131 20.50555693 20.63578619 20.74886857 20.84603981
 20.92787266 20.99519172 21.0490891  21.09001448 21.11908424 21.13754192
 21.14889865 21.20636921 21.34159093 21.47161989 21.58936816 21.69375911
 21.78394749 21.8592057  21.91927098 21.96333794 21.99107909 22.00222784
 21.99659594 21.97454092 21.93679473 21.88476892 21.82122182 21.74948331
 21.67438385 21.60181067 21.55347769 21.68579448 21.83933983 21.99235815
 22.13998723 22.2785389  22.40573971 22.5198483  22.62001806 22.70600969
 22.77775974 22.83560086]
```

## Template comets for LSST MAF (Metric Analysis Framework).
These templates need more consideration!

``` python
>>> from lsstcomet import Comet
>>> jfc = Comet.from_Hv(18, 'short')  # short period
>>> occ = Comet.from_Hv(18, 'oort')   # Oort cloud comet
>>> mbc = Comet.from_Hv(18, 'short')  # main-belt comet
>>> g = {'rh': 1.5, 'delta': 1.0, 'phase': 30}
>>> print(jfc.mag(g, 'r'))
19.094821264028777
```
