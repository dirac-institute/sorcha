.. _ephemeris_gen:

Ephemeris Generator
==========================================================

Sorcha's ephemeris generator is powered by `ASSIST  <https://github.com/matthewholman/assist>`_, a software package for ephemeris-quality integrations of test particles, and the `REBOUND <https://rebound.readthedocs.io/en/latest/>`_ N-body integrator. If the user prefers to use a different generator or provide the ephemeris output from a previous Sorcha run,  they have the ability to point Sorcha to an external file to ingest instead.

.. tip::
  We recommend using Sorcha's ephemeris generator for all your survey simulations. 

How It Works
--------------------------------------------------------

Because ASSIST uses REBOUND's `IAS15 integrator <https://ui.adsabs.harvard.edu/abs/2015MNRAS.446.1424R/abstract>`_, which has an adaptive time step, Sorcha's ephemeris generator instantiates a REBOUND n-body simulation for each individual massless synethetic object including the effects of the Sun, planets, Moon, and 16 asteroids (see the :ref:`MAP` section). It also includes the J2, J3, and J4 gravitational harmonics of the Earth, the J2 gravitational harmonic of the Sun, and general relativistic correction terms for the Sun, using the Parameterized Post-Newtonian (PPN) formulation. The positions of the massive bodies come from the latest `DE441 <https://iopscience.iop.org/article/10.3847/1538-3881/abd414>`_ ephemeris, provided by NASA's `Navigation and Ancillary Information Facility (NAIF) <https://naif.jpl.nasa.gov/naif/credit.html>`_. We note that the coordinate frame for ASSIST+REBOUND  is the equatorial International Celestial Reference Frame (ICRF). We note that this is barycentric, rather than heliocentric. The ephemeris generator translates the input barycentric or heliocentric orbits into x,y, z and velocities in the ICRF to be read into ASSIST. 


The ephemeris generator runs through the survey visits and does on-the-fly checks of where every synthetic object is near the center of each night for which there are visits (like planting the pickets (vetical planks of wood) along a picket fence. Given that information, it then steps through the visits for that night, doing precise calculations for just those objects that are near the camera FOV (field-of-view) of each survey on-sky visit.

For each survey visit, the generator calculates the location of the observatory and the  topocentric unit vector to the field RA/Dec. Then it finds the  set of `HEALPix (Hierarchical Equal Area isoLatitude Pixelation of a sphere) <https://healpix.sourceforge.io/>`_ tiles that are overlapped by the survey vist's camera FOV (nside=64). The ephemeris generator then collects the IDs for the particles in the HEALPix tiles overlapped by the given survey visit FOV, and do light time corrected ephemeris calculations for just those, outputting the right ascenion, declination, rates, and relevant distances, and phase angle values for each of the particles. 

.. tip::
  If using Sorcha's internal ephemeris generation mode (which is the default mode), **we recommend calculating/creating your input orbits with epochs close in time to the start of the first survey observation**. This will minimize the REBOUND n-body integrations required to set up the ephemeris generation.

.. _MAP:
Massive Asteroid Perturbers
--------------------------------------------------------
Here's the list of asteroid pertubers that are included in the ASSIST+REBOUND integrations.

- *(107) Camilla = A868 WA = 1886 WA**
- **(1) Ceres = A801 AA** 
- **(65) Cybele = A861 EB** 
- **(511) Davida = A903 KB**
- **(15) Eunomia = A851 OA**
- **(31) Euphrosyne = A854 RA**
- **(52) Europa = A858 CA** 
- **(10) Hygiea = A849 GA**
- **(704) Interamnia = A910 TC**
- **(7) Iris = A847 PA**
- **(3) Juno = A804 RA**
- **(2) Pallas = A802 FA**
- **(16) Psyche = A852 FA** 
- **(87) Sylvia = A866 KA**
- **(88) Thisbe = A866 LA**
- **(4) Vesta = A807 FA** 

.. warning::
  If you simulate the orbits of these select asteroids you will get *POOR results* with the internal Sorcha epehmeris generator because of how the n-body integration is setup. We recommend getting the positions of these asteroids from some other source and inputting them as an external ephemeris file. 

Tuning the Ephemeris Generator
-----------------------------------
