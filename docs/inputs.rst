Inputs
==========

.. note::
  The user must specify the properties of each synthetic planetesimal individually: an orbit, other physical parameters (like color, asbolute magnitude, phase curve parameters, etc), and, if needed, cometarty activity properties.



There is a set of input files that are required to run the survey simulator post processing codes, which describe the orbital
and physical parameters for synetheric planetesimals that are being simulated. These files are: an orbit file, a physical paramerer file,
an optional cometary parameter file, ephemeris file (Objects in Field output) and the LSST pointing database. Each of these files are described within this section and example files
are shown.


.. image:: images/OIF.png
  :width: 800
  :alt: An overview of the inputs and outputs of the survey simulator post processing code.

.. tip::
  * Each synthetic planetesimal has its own unique object identifier set by the user and must have entries in the orbits and physical parameters files, as well as the cometary activity file, if used. 

Orbit File
-----------------

.. note::
  The orbit file is used by  **Objects in Field** and **surveySimPP**.

This is a file which contains the orbital information of a set of synthetic objects. The orbital parameters should be **heliolcentric**
and can be given in **Cometary orKeplerian** formats. Each object within the synthetic population must be be given it's own unique
object ID (OID). 

An example of an orbit file in cometary format, with each object ID represented by a unique string can be seen here::

   !!OID FORMAT q e i node argperi t_p H t_0
   S1000000a COM 3.01822 0.05208 22.56035 211.00286 335.42134 51575.94061 14.20 54800.00000
   S1000001a COM 2.10974 0.07518 4.91571 209.40298 322.66447 54205.77161 20.57 54800.00000
   S1000002a COM 2.80523 0.07777 1.24945 112.52284 139.86858 54468.71747 14.65 54800.00000
   S1000003a COM 2.10917 0.13219 1.46615 266.54621 232.24412 54212.16304 19.58 54800.00000 
   S1000004a COM 2.17676 0.19949 12.92422 162.14580 192.22312 51895.46586 10.56 54800.00000

While another example of an orbit file, in Keplarian format, with the object ID represented by a unique set of numbers can be seen here::

   !!OID FORMAT q e i node argperi t_p H t_0 
   242880 KEP 1.81032181 0.457012266 8.52469063 321.309082 218.878296 194.936127 24.9029942 59853.0 
   175331 KEP 1.39049709 0.458397567 43.3037987 232.109802 241.479919 91.1170349 24.4742165 59853.0 
   647396 KEP 1.65742993 0.493258268 5.16465139 302.836609 266.81219500000003 161.882599 23.124664300000006 59853.0  
   492747 KEP 2.07343841 0.55492866 10.4931965 185.436066 139.102676 261.443756 24.706829100000004 59853.0 
   546031 KEP 1.33862102 0.133786723 39.04102329999999 341.855743 186.264435 40.9884872 24.6075134 59853.0  

.. warning::

   OIF and SurveySimPP assume **heliocentric** orbits are provided as input!


The orbital parameter file is used with both Objects in Field and the Survey Simulator Post Processing
code. The orbital parameters can take three formats: **Cometary, Keplarian** and **Cartesian**


- **'COM'** = objID, q, e, inc, Omega, argPeri, tPeri, epoch, H, g


- **'KEP'** = objID, a, e, inc, Omega, argPeri, meanAnomaly, epoch, H, g


- **'CART'** = objID, x, y, z, xdot, ydot, zdot, epoch, H, g



+-------------+----------------------------------------------------------------------------------+
| Keyword     | Description                                                                      |
+=============+==================================================================================+
| objID       | Object identifier. Unique identifier for each object withtin the population      |
+-------------+----------------------------------------------------------------------------------+
| q           | Perihelion distance  = a*(1-e)                                                   |
+-------------+----------------------------------------------------------------------------------+
| e           | Eccentricity                                                                     | 
+-------------+----------------------------------------------------------------------------------+
| a           | Semimajor axis                                                                   |
+-------------+----------------------------------------------------------------------------------+
| inc         | Inclination                                                                      |
+-------------+----------------------------------------------------------------------------------+
| Omega       | Longitude of the ascending node                                                  |
+-------------+----------------------------------------------------------------------------------+
| argPeri     | Argument of periapsis                                                            |
+-------------+----------------------------------------------------------------------------------+
| meanAnomaly |                                                                                  |
+-------------+----------------------------------------------------------------------------------+
| tPeri       | Time of periapsis                                                                |
+-------------+----------------------------------------------------------------------------------+
| epoch       |                                                                                  |
+-------------+----------------------------------------------------------------------------------+
| H           |                                                                                  |
+-------------+----------------------------------------------------------------------------------+

.. attention::
   When using the Survey Simulator Post Processing code the format of the orbits (i.e. Cometary, Keplerian, Cartesian) should remain consistent throughout
   each simulation, i.e. only use one type of coordinate format per run.


Physical Parameters File
-------------------------------------------
.. note::
  The physical parameters file is used by **surveySimPP**.


The input file for the physical parameters includes information about the objects color and brightness.

Rubin Observatory will survey the sky in six broadband (optical filters),**u, g, r, i, z, and y**. In the physical parameters file
you can set a main filter which all other colours are compared to.

- **other colours = g-r, i-r, z-r**
- **res filters = r, g, i, z**

The brightness of an atmosphereless body is a function of its phase angle (a). 
Several empirical models exist to predict the brightness, including the HG system (where H is approximately
the brightness at d = 0 and G represents the slope)
For this input, the options are: HG, HG1G2, HG12, linear, none


The physical parameter file must contain an associated value for each of the objects within the orbit file above. If there 
is a  mis-match between these files, the survey simulator code will throw an error.

An example of the physical parameter file can be seen here::


   ObjID r u-r g-r i-r z-r y-r GS
   St500000a 5.63 0.0 0.0 0.0 0.0 0.0 0.15
   St500001a 6.25 0.0 0.0 0.0 0.0 0.0 0.15
   St500002a 6.36 0.0 0.0 0.0 0.0 0.0 0.15
   St500003a 6.61 0.0 0.0 0.0 0.0 0.0 0.15
   St500004a 6.92 0.0 0.0 0.0 0.0 0.0 0.15



Cometary Activity Parameters File (Optional)
-----------------------------------------------

.. note::
  The cometary activity file is used by  **surveySimPP**.

This is an optional input file which describes how the object apparent magnitude will be augmented from 
a standard non-active, atmosphere-less body as it moves inwards towards the Sun. This is dependent on
calculations done using `sbpy <https://sbpy.readthedocs.io/en/latest/api/sbpy.photometry.LinearPhaseFunc.html#sbpy.photometry.LinearPhaseFunc>`_.


An example of a cometary activity parameter file::

   ObjID                       afrho1 k
   67P/Churyumov-Gerasimenko   1552  -3.35


.. warning::

   **When running an instance of surveySimPP, either every synthetic planetesimal experiences cometary activity, or none do.** When running simulations of synthetic planetesimals exhibiting cometary activity, **every** object in that simulation must have an entry in the  associated cometary activety file.


LSST Pointing Database
------------------------


.. note::
  The LSST pointing database is used by  **Objects in Field** and **surveySimPP**.

This database contains information about the LSST pointing history and observing conditions.  We use observation mid-point time, right ascension, declination, rotation angle of the camera, 5-sigma limiting magnitude, filter, and seeing information in Objects in Field and surveySimPP to determine if a synthetic Solar System object is observable.  
What we call the LSST pointing database (currently simulated since Rubin Observatory hasn’t started operations) is generated through the Rubin Observatory scheduler (since 2021 referred to as `rubin_sim <https://github.com/lsst/rubin_sim>`_ and previously known as OpSim). This software is currently under active development and is being used to run many simulated iterations of LSST scenarios showing what the cadence would look like with differing survey strategies. A description of an early version of this python software can be found in `Delgado et al.(2014) <https://ui.adsabs.harvard.edu/abs/2014SPIE.9150E..15D>`_.The output of rubin_sim is a sqlite database containing the pointing history and associated metadata 
of the simulated observation history of LSST.

.. tip::
   The contents of the observations table in the sqlite LSST pointing database can be found `here <https://rubin-sim.lsst.io/rs_scheduler/output_schema.html>`_

The latest version of rubin_sim cadence simulations can be found at https://lsst.ncsa.illinois.edu/sim-data/sims_featureScheduler_runs2.0/. An example rubin_sim simulation visualized on sky is shown below: 

.. raw:: html

    <iframe width="700" height="360" src="https://epyc.astro.washington.edu/~lynnej/opsim_downloads/baseline_v2.0_10yrs.mp4" frameborder="0" allowfullscreen></iframe>


.. attention::
   There may be changes to how this information is read in when the Rubin Observatory science operations begin in approximately mid-2024.

Ephemeris file (Objects in Field Output)
------------------------

.. note::
  The ephemeris file is used by  **surveySimPP**. We recommend using **Objects in Fields** to generate it.
