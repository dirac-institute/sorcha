Inputs
==========

.. note::
  The user must specify the properties of each synthetic planetesimal individually: an orbit, other physical parameters (like color, asbolute magnitude, phase curve parameters, etc), and, if needed, cometarty activity properties.



There is a set of input files that are required to run the survey simulator post processing codes, which describe the orbital
and physical parameters for synthetic planetesimals that are being simulated. These files are: an orbit file, a physical paramerer file,
an optional cometary parameter file, ephemeris file (Objects in Field output) and the LSST pointing database. Each of these files are described within this section and example files
are shown.


.. image:: images/OIF.png
  :width: 800
  :alt: An overview of the inputs and outputs of the survey simulator post processing code.

.. tip::
  Each synthetic planetesimal has its own unique object identifier set by the user and must have entries in the orbits and physical parameters files, as well as the cometary activity file, if used. 

.. warning::
  OIF and SurveySimPP are not checking whether or not a planetesimal ID has been repeated in another row of the input files. **It is up to the user to ensure their input files include only unique IDs**. 

Orbit File
-----------------

.. note::
  The orbit file is used by  **Objects in Field** and **surveySimPP**.

This is a file which contains the orbital information of a set of synthetic objects. The orbital parameters must be **heliolcentric**, and orbits can be define in **Cometary(COM)  or Keplerian (KEP)** formats. Each simulated planetesimals within the synthetic population must be be given it's own unique object ID (ObjID). The file can be **white space separated**  or **comma value separated (CSV)** format. The first line of the orbit file is a header line starting with !! that specifies what each of the columns are.

.. tip::
  *  The orbit file must have a consistent format (i.e. cometary or Keplerian) throughout
  *  The ordering of the columns does not matter as long as the required columns exist and have entries.
  *  The first row in the orbit file must be a header started with '!!' to denote it as the header row
  *  Objects in Field does take other input formats, but surveySimPP is only designed to handle cometary and keplerian orbits

.. warning::
  OIF and SurveySimPP assume **heliocentric** orbits are provided as input!

Cometary Orbit Format
~~~~~~~~~~~~~~~~~~~~~
An example of an orbit file in cometary format, with each object ID represented by a unique string::

   !!ObjID FORMAT q e i node argperi t_p H t_0
   S1000000a COM 3.01822 0.05208 22.56035 211.00286 335.42134 51575.94061 14.20 54800.00000
   S1000001a COM 2.10974 0.07518 4.91571 209.40298 322.66447 54205.77161 20.57 54800.00000
   S1000002a COM 2.80523 0.07777 1.24945 112.52284 139.86858 54468.71747 14.65 54800.00000
   S1000003a COM 2.10917 0.13219 1.46615 266.54621 232.24412 54212.16304 19.58 54800.00000 
   S1000004a COM 2.17676 0.19949 12.92422 162.14580 192.22312 51895.46586 10.56 54800.00000

+-------------+----------------------------------------------------------------------------------+
| Keyword     | Description                                                                      |
+=============+==================================================================================+
| ObjID       | Object identifier for each synthetic planetesimal simulated (string)             |
+-------------+----------------------------------------------------------------------------------+
| FORMAT      | Orbit format string (COM)  						         |
+-------------+----------------------------------------------------------------------------------+
| q           | Perihelion (au)									 |
+-------------+----------------------------------------------------------------------------------+
| e           | Eccentricity                                                                     |
+-------------+----------------------------------------------------------------------------------+
| inc         | Inclination (degrees)                                                            |
+-------------+----------------------------------------------------------------------------------+
| node        | Longitude of the ascending node (degrees)                                        |
+-------------+----------------------------------------------------------------------------------+
| argPeri     | Argument of perihelion (degrees)                                                 |
+-------------+----------------------------------------------------------------------------------+
| t_P         | Time of periapsis (degrees)                                                      |
+-------------+----------------------------------------------------------------------------------+
| t_0         | Epoch (MJD)                                                                      |
+-------------+----------------------------------------------------------------------------------+

**Header line**
The first row in the orbit file must be a header started with ‘!!’ to denote it as the header row::

   !!ObjID FORMAT q e i node argperi t_p t_0


.. tip::
  The orbit file can be either white space separated or comma value separated (CSV). For readability we show examples with white space in the online documentation. 


Keplerian Orbit Format
~~~~~~~~~~~~~~~~~~~~~~
An example of an orbit file, in Keplarian format, with the object ID represented by a unique set of numbers::

   !!ObjID FORMAT  a e inc node peri ma epoch H
   t1 KEP 47.9877 0.0585 11.3584 148.4661 140.4756 308.3244 53157.00 7.0 
   t2 KEP 47.7468 0.0552 7.1829 171.9226 55.3728 158.9403 53157.00 7.0 
   t3 KEP 47.9300 0.3805 3.4292 72.9463 7.0754 84.7860 53157.00 7.0 
   t4 KEP 47.6833 0.1973 14.0872 344.2142 167.0238 220.2356 53157.00 7.0 
   t5 KEP 47.9356 0.2912 4.3621 306.0908 217.8116 18.7043 53157.00 7.0 
   t6 KEP 47.9786 0.2730 2.2425 147.9340 166.6578 327.8996 53157.00 7.0 

+-------------+----------------------------------------------------------------------------------+
| Keyword     | Description                                                                      |
+=============+==================================================================================+
| ObjID       | Object identifier for each synthetic planetesimal simulated (string)             |
+-------------+----------------------------------------------------------------------------------+
| FORMAT      | Orbit format string (KEP)                                                        |
+-------------+----------------------------------------------------------------------------------+
| a           | Semimajor axis (au)                                                              |
+-------------+----------------------------------------------------------------------------------+
| e           | Eccentricity                                                                     |
+-------------+----------------------------------------------------------------------------------+
| inc         | Inclination (degree)                                                             |
+-------------+----------------------------------------------------------------------------------+
| node        | Longitude of the ascending node (degrees)                                        |
+-------------+----------------------------------------------------------------------------------+
| peri        | Argument of perihelion (degrees)                                                 |
+-------------+----------------------------------------------------------------------------------+
| ma          | Mean Anomaly (degrees)                                                           |           
+-------------+----------------------------------------------------------------------------------+
| epoch       | Epoch (MJD)                                                                      |
+-------------+----------------------------------------------------------------------------------+

**Header line**
The first row in the orbit file must be a header started with ‘!!’ to denote it as the header row::

   !!ObjID FORMAT q e i node argperi t_p H t_0

.. tip::
  The orbit file can be either white space separated or comma value separated (CSV). For readability we show examples with white space in the online documentation.

.. tip::
  Objects in Field does have the capability take a V-band absolute magnitude and other parameters to calculate a V-band apparent magnitude. surveySimPP allows for more complicated modifications to the apparent magnitude such as cometary activity (a simple cometary brightening model is included) or the ability to possibly add light curve effects if a module is developed. Therefore, we recommend not including any V-band H value in the orbits input file. Instead, we recommend providing the H  of the synthetic planetesimals in the physical paramters file used by surveySimPP (see the next section). 

Physical Parameters File
-------------------------------------------
.. note::
  The physical parameters file is used by **surveySimPP**.

The input file for the physical parameters includes information about the objects optical colors, phase curve, and absolute magnitude. 

An example of the physical parameter file can be seen here::


   ObjID H u-r g-r i-r z-r y-r GS 
   St500000a 5.63 0.0 0.0 0.0 0.0 0.0 0.15
   St500001a 6.25 0.0 0.0 0.0 0.0 0.0 0.15
   St500002a 6.36 0.0 0.0 0.0 0.0 0.0 0.15
   St500003a 6.61 0.0 0.0 0.0 0.0 0.0 0.15
   St500004a 6.92 0.0 0.0 0.0 0.0 0.0 0.15

Rubin Observatory will survey the sky in six broadband (optical filters),**u, g, r, i, z, and y**. In the physical parameters file
you can set a main filter which all other colours are compared to.

- **other colours = g-r, i-r, z-r**
- **res filters = r, g, i, z**

The brightness of an atmosphereless body is a function of its phase angle (a).
Several empirical models exist to predict the brightness, including the HG system (where H is approximately
the brightness at d = 0 and G represents the slope)
For this input, the options are: HG, HG1G2, HG12, linear, none

+-------------+----------------------------------------------------------------------------------+
| Keyword     | Description                                                                      |
+=============+==================================================================================+
| ObjID       | Object identifier for each synthetic planetesimal simulated (string)             |
+-------------+----------------------------------------------------------------------------------+
| H           | Absolute Magnitude (magnitudes)                                                  |
+-------------+----------------------------------------------------------------------------------+
| GS          | Phase Curve Parameter (either G12 or β)                                          |
+-------------+----------------------------------------------------------------------------------+

Phase Functions
~~~~~~~~~~~~~~~~~~~~~
This is done using the linear phase slope utilities in using `sbpy <https://sbpy.readthedocs.io/en/latest/api/sbpy.photometry.LinearPhaseFunc.html#sbpy.photometry.LinearPhaseFunc>`_.


Cometary Activity Parameters File (Optional)
-----------------------------------------------

.. note::
  The cometary activity file is used by  **surveySimPP**.

This is an optional input file which describes how the object apparent magnitude will be augmented from 
a standard non-active, atmosphereless body as it moves inwards and outwards towards the Sun.


An example of a cometary activity parameter file::

   ObjID                       afrho1 k
   67P/Churyumov-Gerasimenko   1552  -3.35


.. warning::

   **When running an instance of surveySimPP, either every synthetic planetesimal experiences cometary activity, or none do.** When running simulations of synthetic planetesimals exhibiting cometary activity, **every** object in that simulation must have an entry in the  associated cometary activity file.

+-------------+-----------------------------------------------------------------------------------+
| Keyword     | Description                                                                       |
+=============+===================================================================================+
| ObjID       | Object identifier for each synthetic planetesimal simulated (string)              |
+-------------+-----------------------------------------------------------------------------------+
| afrho1      | Afρ, quantity of                                                                  |
|             | `A'Hearn et al. (1984) <https://ui.adsabs.harvard.edu/abs/1984AJ.....89..579A>`_. |
|             | at perihelion (cm). The product of                                                |
|             | albedo, filling factor of grains within the observer field of view, and the       |
|             | linear radius of the field of view at the comet                                   |
+-------------+-----------------------------------------------------------------------------------+
| k           | Dust falling exponential value (dust falling at rh^k)                             |
+-------------+-----------------------------------------------------------------------------------+

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
-----------------------------------------

.. note::
  The ephemeris file is used by **surveySimPP**.

.. tip::
  We reccomend using **Objects in Field** to generate this file.

The file can be **white space separated or comma value separated (CSV)** format. The first line after the header specifies what each of the columns are. An example of the ephemeris file expected is shown belowgn ascii format::

   START HEADER
   [configuration would be outputted here]
   END HEADER
   ObjID FieldID FieldMJD AstRange(km) AstRangeRate(km/s) AstRA(deg) AstRARate(deg/day) AstDec(deg) AstDecRate(deg/day) Ast-Sun(J2000x)(km) Ast-Sun(J2000y)(km) Ast-Sun(J2000z)(km) Ast-Sun(J2000vx)(km/s) Ast-Sun(J2000vy)(km/s) Ast-Sun(J2000vz)(km/s) Obs-Sun(J2000x)(km) Obs-Sun(J2000y)(km) Obs-Sun(J2000z)(km) Obs-Sun(J2000vx)(km/s) Obs-Sun(J2000vy)(km/s) Obs-Sun(J2000vz)(km/s) Sun-Ast-Obs(deg) V V(H=0
   S1000000a     144993 60425.402338    458272140.052  -21.379  302.104404  0.134147   3.473196  0.155803    120337437.532   -467360529.440     -6863861.395   15.814    3.135    3.395   -122770233.618    -79879875.157    -34626711.017   17.120  -22.269   -9.707   18.169656  20.115   5.915 
   S1000000a     145013 60425.411933    458254426.575  -21.355  302.105691  0.134050   3.474691  0.155787    120350548.117   -467357930.249     -6861046.878   15.813    3.135    3.395   -122756042.340    -79898326.109    -34634757.414   17.116  -22.244   -9.705   18.169632  20.115   5.915 
   S1000000a     180614 60503.206627    355295647.270   -4.213  299.360478 -0.185502  11.819392  0.002961    222559162.829   -434204364.757     15938036.863   14.472    6.666    3.359     52050159.823   -131110990.022    -56836222.957   27.873    9.424    4.014   10.189588  19.301   5.101 
   S1000000a     180664 60503.230597    355286994.232   -4.144  299.356031 -0.185547  11.819460  0.002695    222589133.907   -434190558.767     15944993.943   14.472    6.667    3.359     52107850.839   -131091407.626    -56827904.911   27.840    9.487    4.019   10.187081  19.301   5.101 
   S1000000a     183625 60507.194642    354133809.129   -2.598  298.635794 -0.188904  11.800365 -0.012248    227530687.962   -431878159.331     17094459.598   14.384    6.836    3.353     61402244.381   -127629446.799    -55326708.672   27.127   11.100    4.742    9.831253  19.281   5.081    

.. note::
  The ephemeris file is used by  **surveySimPP**. We recommend using **Objects in Fields** to generate it.

.. note::
  With our recommended setup you will have V magnitudes outputted by OIF into the ephemeris file which is generated from a default H assumed by OIF. SurveySimPP ignores these apparent magnitudes and computes its own based on the configuration inputs and additional input files.

+--------------------------+----------------------------------------------------------------------------------+
| Keyword                  | Description                                                                      |
+==========================+==================================================================================+
| ObjID                    | Object identifier for each synthetic planetesimal simulated (string)             |
+--------------------------+----------------------------------------------------------------------------------+
| FieldID                  | Observation pointing field identificator                                         |
+--------------------------+----------------------------------------------------------------------------------+
| FieldMJD                 | Observation Mean Julian Date                                                     |
+--------------------------+----------------------------------------------------------------------------------+
| AstRange(km)             | Topocentric distance to the synthetic planetesimal                               |
+--------------------------+----------------------------------------------------------------------------------+
| AstRangeRate(km/s)       | Radial component of the object’s topocentric velocity (km/s)                     |
+--------------------------+----------------------------------------------------------------------------------+
| AstRA(deg)               | Synthetic plantesimal's right ascension (degrees)                                |
+--------------------------+----------------------------------------------------------------------------------+
| AstRARate(deg/day)       | Synthetic plantesimal's right ascension rate of motion (deg/day)                 |
+--------------------------+----------------------------------------------------------------------------------+
| AstDec(deg)              | Synthetic plantesimal's declination (degrees)                                    |
+--------------------------+----------------------------------------------------------------------------------+
| AstDecRate(deg/day)      | Synthetic plantesimal's declination rate of motion (deg/day)                     |
+--------------------------+----------------------------------------------------------------------------------+
| Ast-Sun(J2000x)(km)      |  Cartesian X-component of the synthetic planetesimal's heliocentric distamce (km)|
+--------------------------+----------------------------------------------------------------------------------+
| Ast-Sun(J2000y)(km)      |  Cartesian Y-component of the synthetic planetesimal's heliocentric distance (km)|
+--------------------------+----------------------------------------------------------------------------------+
| Ast-Sun(J2000z)(km)      |  Cartesian Z-component of the synthetic planetesimal's heliocentric distance (km)|
+--------------------------+----------------------------------------------------------------------------------+
|Ast-Sun(J2000vx)(km/s)    |Cartesian X-component of the synthetic planetesimal's heliocentric velocity (km/s)|
+--------------------------+----------------------------------------------------------------------------------+
|Ast-Sun(J2000vy)(km/s)    |Cartesian Y-component of the synthetic planetesimal's heliocentric velocity (km/s)|
+--------------------------+----------------------------------------------------------------------------------+
| Ast-Sun(J2000vz)(km/s)   |Cartesian Z-component of the synthetic planetesimal's heliocentric velocity (km/s)|
+--------------------------+----------------------------------------------------------------------------------+
| Obs-Sun(J2000x)(km)      |  Cartesian X-component of observer's heliocentric distamce (km)                  |
+--------------------------+----------------------------------------------------------------------------------+
| Obs-Sun(J2000y)(km)      |  Cartesian Y-component of the observer's heliocentric distance (km)              |             
+--------------------------+----------------------------------------------------------------------------------+
| Obs-Sun(J2000z)(km)      |  Cartesian Z-component of the observer's heliocentric distance (km)              |
+--------------------------+----------------------------------------------------------------------------------+
|Obs-Sun(J2000vx)(km/s)    |  Cartesian X-component of the obsever's heliocentric velocity (km/s)             |
+--------------------------+----------------------------------------------------------------------------------+
|Obs-Sun(J2000vy)(km/s)    |  Cartesian Y-component of the observer's heliocentric velocity (km/s)            |
+--------------------------+----------------------------------------------------------------------------------+
| Obs-Sun(J2000vz)(km/s)   |Cartesian Z-component of the observer's heliocentric velocity (km/s)              |
+--------------------------+----------------------------------------------------------------------------------+
| Sun-Ast-Obs(deg)         | The phase angle between the Sun,synthetic plantesimal, & observer (deg)          |
+--------------------------+----------------------------------------------------------------------------------+
| V (optional)             | Calculated V-band magnitude (not read in)                                        |
+--------------------------+----------------------------------------------------------------------------------+
| V(H=0 (optional)         | Calculated V-band magnitude if H=0 (not read in)                                 |
+--------------------------+----------------------------------------------------------------------------------+

.. note::
   All positions and velocities are in respect to J2000 
