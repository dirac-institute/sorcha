Inputs
==========
There are a set of input files that are required to run the survey simulator post processing code, which describe the orbital
and physical parameters of the series of objects that are being simulated. These files are: an orbit file, a physical paramerer file,
an optional cometary parameter file and the LSST pointing database. Each of these files are describe within this section and example files
are shown.

Orbit File
-----------------
This is a file which contains the orbital information of a set of synthetic objects. The orbital parameters should be heliolcentric
and can be given in **Cometary, Keplerian or Cartesian** formats. Each object within the synthetic population should be given it's own unique
object ID (OID). 

The orbit file is used when running both **Objects in Field** and **Post Processing**.

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

   Remember that all orbits used should be **heliocentric**.

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
| x           |                                                                                  |
+-------------+----------------------------------------------------------------------------------+
| y           |                                                                                  |
+-------------+----------------------------------------------------------------------------------+
| z           |                                                                                  |
+-------------+----------------------------------------------------------------------------------+
| xdot        | Inclination                                                                      |
+-------------+----------------------------------------------------------------------------------+
| ydot        | Longitude of the ascending node                                                  |
+-------------+----------------------------------------------------------------------------------+
| zdot        | Longitude of the ascending node                                                  |
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
| g           |                                                                                  |
+-------------+----------------------------------------------------------------------------------+


.. attention::
   When using the Survey Simulator Post Processing code the format of the orbits (i.e. Cometary, Keplerian, Cartesian) should remain consistent throughout
   each simulation, i.e. only use one type of coordinate format per run.


Physical Parameters File
-------------------------------------------
The input file for the physical parameters includes information about the objects colour and brightness.

This file is used when running **Post Processing**

The LSST will survey the sky in six bandpasses. These are **u, g, r, i, z and y**. In the colour file
you can set a main filter which all other colours are compared to.

- **main filter = r**
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

This is an optional input file which describes how the object apparent magnitude will be augmented from 
a standard non-active, atmosphere-less body as it moves inwards towards the Sun. This is dependent on
calculations done using `sbpy <https://sbpy.readthedocs.io/en/latest/api/sbpy.photometry.LinearPhaseFunc.html#sbpy.photometry.LinearPhaseFunc>`_.


.. warning::

   When running simulations of objects exhibiting cometary activity, **every** object in that simulation must have an associated cometary activety.
   When running a single simulation either every object experiences cometary activity, or none do.

An example of a cometary activity parameter file can be seen here::

   ObjID                       afrho1 k
   67P/Churyumov-Gerasimenko   1552  -3.35


LSST Pointing Database
------------------------

This is a file containing the pointing data for the LSST survey. Prior to the start of the survey, this 
data is estimated from up-to-date observation planning and environmental data. This is generated through
the Rubin Observatory scheduler (known as rubin_sim). A description of an early version of this python software can be found in
Delgado et al. (2014) and the open source repository is found at https://github.com/lsst/rubin_sim. 
The output of rubin_sim is a sqlite database containing the pointing history and associated metadata 
of the simulated observation history of LSST. This will be updated with real-life pointing data as 
observations take place.


.. raw:: html

    <iframe width="700" height="360" src="https://epyc.astro.washington.edu/~lynnej/opsim_downloads/baseline_v2.0_10yrs.mp4" frameborder="0" allowfullscreen></iframe>

