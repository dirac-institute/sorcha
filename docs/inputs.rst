.. _inputs:

Inputs
==========

``Sorcha`` requires two input files describing the synthetic solar system objects to simulate -- one for the orbital parameters and one for the physical parameters -- as well as a survey pointing database. Optionally, the user can provide a pre-generated ephemeris file with the positions of each object and a complex physical parameter file for rotational light curves and cometary activity. Each of these files are described within this section and example files are shown.


.. image:: images/survey_simulator_flow_chart.png
  :width: 800
  :alt: An overview of the inputs and outputs of the Sorcha code.
  :align: center

.. tip::
  Each synthetic planetesimal has its own unique object identifier set by the user and must have entries in the orbits and physical parameters files, as well as the cometary activity file, if used.

.. warning::
  ``Sorcha`` does not check whether or not a planetesimal ID has been repeated in another row of the input files. **It is up to the user to ensure their input files include only unique IDs**.

.. _orbits:


Orbit File
-----------------

This is a file which contains the orbital information of a set of synthetic objects.

.. tip::
  *  ``Sorcha`` is designed to handle heliocentric **Cometary (COM), Keplerian (KEP), and Cartesian (CART)** orbits, as well as their barycentric equivalents: **Barycentric Cometary (BCOM), Keplerian (BKEP) and Cartesian (BCART)**
  *  The orbit file **must** have a consistent format (i.e. Cometary or Keplerian or Cartesian) throughout
  *  The first column must be ObjID, but the ordering of the remaining columns does not matter as long as the required columns exist and have entries
  *  The first row in the orbit file **must** be a header listing the column names
  *  The **correct capitalization of column names** is required
  *  The orbit file can be either **whitespace-separated** or **comma-separated values (CSV)**
  *  Each simulated particle **must** have a unique string identifier
  *  The orbit file **must only** have 9 columns (object identifier, format column, 6 orbital parameters, and a time epoch)

.. warning::
  The orbit epoch is expected to be given in **TDB (Barycentric Dynamical Time)**

.. tip::
  If using ``Sorcha``'s internal :ref:`ephemeris generator<ephemeris_gen>` (which is the default mode), **we recommend calculating/creating your input orbits with epochs close in time to the start of the first survey observation**. This will minimize the n-body integrations required to set up the ephemeris generation.

.. tip::
  Be careful about the way your input elements are defined! Using heliocentric elements as barycentric (or vice-versa) will lead to wrong outputs. Similarly, if using Cartesian elements, be careful about the orientation of the coordinate system! ``Sorcha`` assumes that Cartesian elements are Ecliptic-oriented.

.. attention::
   Use the **--ob (--orbits)** flag with the **sorcha run** command on the terminal to specify the orbit file  that ``Sorcha`` should use.

.. note::
  For readability we show examples of whitespace-separated files below. We show only the heliocentric versions of these inputs, as the barycentric column requirements are identical, changing only the `FORMAT` designation


Cometary Orbit Format
~~~~~~~~~~~~~~~~~~~~~~~

Example Orbit File in Cometary Format
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block::

   ObjID FORMAT q e inc node argPeri t_p_MJD_TDB epochMJD_TDB
   S1000000a COM 3.01822 0.05208 22.56035 211.00286 335.42134 51575.94061 54800.00000
   S1000001a COM 2.10974 0.07518 4.91571 209.40298 322.66447 54205.77161 54800.00000
   S1000002a COM 2.80523 0.07777 1.24945 112.52284 139.86858 54468.71747 54800.00000
   S1000003a COM 2.10917 0.13219 1.46615 266.54621 232.24412 54212.16304 54800.00000 
   S1000004a COM 2.17676 0.19949 12.92422 162.14580 192.22312 51895.46586 54800.00000

Cometary Orbit Format Required Columns
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+-------------+--------------------------------------------------------------------------------------------+
| Keyword     | Description                                                                                |
+=============+============================================================================================+
| ObjID       | Object identifier for each synthetic planetesimal simulated (string)                       |
+-------------+--------------------------------------------------------------------------------------------+
| FORMAT      | Orbit format string (COM for heliocentric or BCOM for barycentric)                         |
+-------------+--------------------------------------------------------------------------------------------+
| q           | Perihelion distance (au)	                                                           |
+-------------+--------------------------------------------------------------------------------------------+
| e           | Eccentricity                                                                               |
+-------------+--------------------------------------------------------------------------------------------+
| inc         | Inclination (degrees)                                                                      |
+-------------+--------------------------------------------------------------------------------------------+
| node        | Longitude of the ascending node (degrees)                                                  |
+-------------+--------------------------------------------------------------------------------------------+
| argPeri     | Argument of perihelion (degrees)                                                           |
+-------------+--------------------------------------------------------------------------------------------+
| t_p_MJD_TDB | Time of periapsis specified as Mean Julian Date (MJD) in TDB (Barycentric Dynamical Time)  |
+-------------+--------------------------------------------------------------------------------------------+
| epochMJD_TDB| Epoch specified as Mean Julian Date (MJD) in TDB (Barycentric Dynamical Time)              |
+-------------+--------------------------------------------------------------------------------------------+

Keplerian Orbit Format
~~~~~~~~~~~~~~~~~~~~~~~~

Example Orbit File in Keplerian Format
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block::

   ObjID FORMAT a e inc node argPeri ma epochMJD_TDB 
   t1 KEP 47.9877 0.0585 11.3584 148.4661 140.4756 308.3244 53157.00 
   t2 KEP 47.7468 0.0552 7.1829 171.9226 55.3728 158.9403 53157.00
   t3 KEP 47.9300 0.3805 3.4292 72.9463 7.0754 84.7860 53157.00 
   t4 KEP 47.6833 0.1973 14.0872 344.2142 167.0238 220.2356 53157.00  
   t5 KEP 47.9356 0.2912 4.3621 306.0908 217.8116 18.7043 53157.00  
   t6 KEP 47.9786 0.2730 2.2425 147.9340 166.6578 327.8996 53157.00  

Keplerian Orbit Format Required Columns
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
+-------------+----------------------------------------------------------------------------------+
| Keyword     | Description                                                                      |
+=============+==================================================================================+
| ObjID       | Object identifier for each synthetic planetesimal simulated (string)             |
+-------------+----------------------------------------------------------------------------------+
| FORMAT      | Orbit format string (KEP for heliocentric or BKEP for barycentric)               |
+-------------+----------------------------------------------------------------------------------+
| a           | Semimajor axis (au)                                                              |
+-------------+----------------------------------------------------------------------------------+
| e           | Eccentricity                                                                     |
+-------------+----------------------------------------------------------------------------------+
| inc         | Inclination (degree)                                                             |
+-------------+----------------------------------------------------------------------------------+
| node        | Longitude of the ascending node (degrees)                                        |
+-------------+----------------------------------------------------------------------------------+
| argPeri     | Argument of perihelion (degrees)                                                 |
+-------------+----------------------------------------------------------------------------------+
| ma          | Mean Anomaly (degrees)                                                           |           
+-------------+----------------------------------------------------------------------------------+
| epochMJD_TDB| Epoch specified as Mean Julian Date (MJD) in TDB (Barycentric Dynamical Time)    |
+-------------+----------------------------------------------------------------------------------+

Cartesian Orbit Format
~~~~~~~~~~~~~~~~~~~~~~~

Example Orbit File in Cartesian format
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block::

   ObjID FORMAT x y z xdot ydot zdot epochMJD_TDB
   STC001TFa CART  36.701800449281706  -8.770729364470023 -0.6261488665458296  0.0007155581026554  0.0026593939322716  7.344098975957749e-06   54466.0  36.54594860110992   0.04317
   STC001TG  CART -21.58733368378989   43.39783041151296   1.56699314137673   -0.0022005866864537 -0.0008717014384454 -4.735561770155727e-05   54466.0  44.842379308393234  0.11655
   STC001THa CART -37.814635799443394 -15.408895634838116 -5.805017616166551   0.0013198883808779 -0.0023982304849102  0.0001541826365505      54466.0  43.31324469003626,  0.13135
   STC001TI  CART  41.24248251296191   -5.652356017018537  2.248705059605729   0.0002800360644183  0.0027490608404251 -2.751096337281987e-05   54466.0  45.1101872463009    0.08356
   STC001TJa CART  17.40239702643279   34.77710957157372   0.0084291177638708 -0.0026387164932318  0.0010268353976719 -0.0001037528579236      54466.0  41.15242897966045   0.10765
   STC001TKa CART -15.182212553033564  31.98846596524726   0.179545295303334  -0.0026490933334786 -0.0013306706378324  0.0001110412982125      54466.0  37.39443807826161   0.05752
   STC001TLa CART  33.603411395500856  18.87464811210368  -0.6359802780512743 -0.0012855812467388  0.0025081701870071 -2.1885697562103903e-05  54466.0  39.93776165518987   0.05171
   STC001TMa CART -35.205151144286006 -21.59643017634877  -6.399036148167812   0.0012861312376887 -0.0023168284708868 -0.0001863582741122      54466.0  41.6549967769547    0.05369
   STC001TNa CART -33.79882997522472  -16.266135214977684 -5.221001391031022   0.0013485808895118 -0.0024033901851641 -0.0001051222283375      54466.0  36.890329257623286  0.06274

Cartesian Orbit Format Required Columns
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+-------------+----------------------------------------------------------------------------------+
| Keyword     | Description                                                                      |
+=============+==================================================================================+
| ObjID       | Object identifier for each synthetic planetesimal simulated (string)             |
+-------------+----------------------------------------------------------------------------------+
| FORMAT      | Orbit format string (CART for heliocentric or BCART for barycentric)             |
+-------------+----------------------------------------------------------------------------------+
| x           | heliocentric or barycentric position on the ecliptic x axis (au)                 |
+-------------+----------------------------------------------------------------------------------+
| y           | heliocentric or barycentric position on the ecliptic y axis (au)                 |
+-------------+----------------------------------------------------------------------------------+
| z           | heliocentric or barycentric position on the ecliptic z axis (au)                 |
+-------------+----------------------------------------------------------------------------------+
| xdot        | heliocentric or barycentric velocity on the ecliptic x axis (au/day)             |
+-------------+----------------------------------------------------------------------------------+
| ydot        | heliocentric or barycentric velocity on the ecliptic y axis (au/day)             |
+-------------+----------------------------------------------------------------------------------+
| zdot        | heliocentric or barycentric velocity on the ecliptic z axis (au/day)             |
+-------------+----------------------------------------------------------------------------------+
| epochMJD_TDB| Epoch specified as Mean Julian Date (MJD) in TDB (Barycentric Dynamical Time)    |
+-------------+----------------------------------------------------------------------------------+

.. note::
   All positions and velocities are in respect to J2000

Orbit File Configuration Parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``Sorcha`` is initialized for the format of the input orbit file through the :ref:`configuration file<configs>` INPUT sections:

.. code-block::

   [INPUT]

   # Sorcha chunk size: how many objects should be processed at once?

   size_serial_chunk = 20000

   # Format for the orbit, physical parameters, and complex physical parameters input files.
   # Options: csv or whitespace

   aux_format = csv


.. _physical:

Physical Parameters File
-------------------------------------------

The input file for the physical parameters includes information about the objects' optical colors, phase curve parameters, and absolute magnitude. The contents of this file are the bare minimum needed to simulate survey detections. For more advanced handling of the apparent magnitude of the synthetic objects, including light curve effects and cometary activity, you would also specify values in the complex physical parameters file.

.. tip::
  *  The first column must be ObjID, but the ordering of the remaining columns does not matter as long as the required columns exist and have entries
  *  The first row in the physical parameters file **must** be a header listing the column names
  *  The **correct capitalization of column names** is required
  *  The physical parameters file can be either **whitespace-separated** or **comma-separated values (CSV)**
  *  Each simulated object **must** have a unique string identifier
  *  You  **must use the same phase curve prescription for all simulated objects**. If you want to use different phase curve prescriptions for different synthetic populations, you will need to run them in separate input files to ``Sorcha``
  *  If the  phase curve function is set to NONE in the configuration value then no phase curve parameter values are required in the physical parameters files.
  *  In the :ref:`configuration file<configs>` you can decide which observing filters (e.g *r*-band,*g*-band,etc) you want have ``Sorcha`` run on and specify which observing filter is the main filter that the absolute magnitude is defined for. You only need to provide colors for those filters specified in the :ref:`configuration file<configs>`.

We have implemented several phase curve parameterizations that can be specified in the :ref:`configuration file<configs>` and then inputted through the physical parameters. **You can either specify one set of phase curve parameters for all observing filters or specify values for each filter examined by** ``Sorcha``. We are using the  `sbpy <https://sbpy.org/>`_  phase function utilities. The supported options are: `HG <https://sbpy.readthedocs.io/en/latest/api/sbpy.photometry.HG.html#sbpy.photometry.HG>`_, `HG1G2 <https://sbpy.readthedocs.io/en/latest/api/sbpy.photometry.HG1G2.html#sbpy.photometry.HG1G2>`_, `HG12 <https://sbpy.readthedocs.io/en/latest/api/sbpy.photometry.HG12.html#sbpy.photometry.HG12>`_, `linear <https://sbpy.readthedocs.io/en/latest/api/sbpy.photometry.LinearPhaseFunc.html#sbpy.photometry.LinearPhaseFunc>`_ (specified by S in the header of the physical parameters file), and none (if no columns for phase curve are included in the physical parameters file then the synthetic object is considered to have a flat phase curve). Note that the HG12 model is the `Penttilä et al. (2016) <https://www.sciencedirect.com/science/article/abs/pii/S0032063315002408>`_ modified model, and not the original (IAU adopted) `Muinonen et al. (2010) <https://www.sciencedirect.com/science/article/abs/pii/S001910351000151X>`_ model.



Example Physical Parameters File (single linear slope phase curve parameter for all observing filters)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. note::
  For readability we show examples of whitespace-separated files below.

.. code-block::

   ObjID H u-r g-r i-r z-r y-r GS 
   St500000a 5.63 2.55 0.92 -0.38 -0.59 -0.70 0.15
   St500001a 6.25 2.55 0.92 -0.38 -0.59 -0.70 0.15
   St500002a 6.36 1.72 0.48 -0.11 -0.12 -0.12 0.15
   St500003a 6.67 1.72 0.48 -0.11 -0.12 -0.12 0.15
   St500004a 10.2 1.90 0.58 -0.21 -0.30 -0.39 0.15


Example Physical Parameters File (a HG value is specified for each observing filter)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. note::
  For readability we show examples of whitespace-separated files below.

.. code-block::

   ObjID H u-r g-r i-r z-r y-r Gr Gu Gg Gi Gz Gy
   St500000a 5.63 2.55 0.92 -0.38 -0.59 -0.70 0.15 0.17 0.14 0.19 0.18 0.20
   St500001a 6.25 2.55 0.92 -0.38 -0.59 -0.70 0.15 0.17 0.14 0.17 0.19 0.17
   St500002a 6.36 1.72 0.48 -0.11 -0.12 -0.12 0.15 0.17 0.13 0.17 0.16 0.18
   St500003a 6.67 1.72 0.48 -0.11 -0.12 -0.12 0.15 0.16 0.12 0.20 0.15 0.19
   St500004a 10.2 1.90 0.58 -0.21 -0.30 -0.39 0.15 0.15 0.16 0.15 0.14 0.16

Rubin Observatory will survey the sky in six broadband (optical filters), *u, g, r, i, z,* and *y* . In the physical parameters file, you will specify the object's absolute magnitude in the main filter as specified in the :ref:`configuration file<configs>` (usually this is g or r band) and then provide the synthetic planetesimal's color in other filters relative to the main filter.


Required Physical Parameters File Columns and Format
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

+------------------+----------------------------------------------------------------------------------+
| Keyword          | Description                                                                      |
+==================+==================================================================================+
| ObjID            | Object identifier for each synthetic planetesimal simulated (string)             |
+------------------+----------------------------------------------------------------------------------+
| H                | Absolute magnitude in the main filter                                            |
+------------------+----------------------------------------------------------------------------------+
| u-r,g-r,etc      | Photometric colors in the relevant survey filters                                |
+------------------+----------------------------------------------------------------------------------+
| G, G1&G2, G12, S | Phase curve parameter(s) for all filters (either G12, G1 & G2, or β) (optional)  |
+------------------+----------------------------------------------------------------------------------+

.. note::
  The Phase curve parameters(s) column will not be present if the phase curve function/calculation is set to None in the :ref:`configuration file<configs>`.

.. note::
  In the :ref:`configuration file<configs>` you can decide which filters you want to have ``Sorcha`` run on and specify which filter is the main filter that the absolute magnitude is defined for. You only need to provide colors for those filters specified in the :ref:`configuration file<configs>`.


.. attention::
   Use the **-p (--physical-parameters)** flag with the **sorcha run** command on the terminal to specify the pointing database that ``Sorcha`` should use.

.. seealso::
  We have an `example Jupyter notebook <notebooks/demo_CalculateLSSTColours.ipynb>`_  demonstrating how to take a representative optical/NIR spectra of your input population and using the `rubin_sim <https://github.com/lsst/rubin_sim>`_  package to estimate the expected colors in the LSST filter bandpasses.  


Physical Parameters  File Configuration Parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``Sorcha`` is initialized for the format of the input physical parameters file through the :ref:`configuration file<configs>` INPUT, FILTERS, and PHASECURVES sections:

.. code-block::

   [INPUT]

   # Sorcha chunk size: how many objects should be processed at once?

   size_serial_chunk = 20000

   # Format for the orbit, physical parameters, and complex physical parameters input files.
   # Options: csv or whitespace

   aux_format = csv

   [FILTERS]

   # Filters of the observations you are interested in, comma-separated.
   # Your physical parameters file must have H calculated in one of these filters
   # and colour offset columns defined relative to that filter.

   observing_filters = r,g,i,z,u,y

   [PHASECURVES]   

   # The phase function used to calculate apparent magnitude. The physical parameters input
   # file must contain the columns needed to calculate the phase function.
   # Options: HG, HG1G2, HG12, linear, none.

   phase_function = linear

.. note::
  In the :ref:`configuration file<configs>` you can decide which filters you want to have ``Sorcha`` run on and specify which filter is the main filter that the absolute magnitude is defined for. You only need to provide colors for those filters specified in the :ref:`configuration file<configs>`.


.. _CPP:

Complex Physical Parameters File (Optional)
---------------------------------------------------

The complex physical parameters file is only needed if you're going to include your own rotational light curve class or cometary activity class to augment the calculated apparent magnitudes. ``Sorcha`` is set up such that any values required for this such as (light curve amplitude and period per simulated object) are included in a file, separate from the physical parameters file, that we refer to as the complex physical parameters file.  What columns are required in the complex physical parameters file depends on the classes you are using.

.. tip::
  *  The first column must be ObjID, but the ordering of the remaining columns does not matter as long as the required columns exist and have entries
  *  The first row in the complex  physical parameters file **must** list  the column names
  *  The **correct capitalization of column names** is required
  *  The complex physical parameters file can be either **whitespace-separated** or **comma-separated values (CSV)**
  *  Each simulated object **must** have a unique string identifier

.. seealso::
   Further details about how to use ``Sorcha add-ons`` to apply cometary activity and lightcurve effects can be found :ref:`here<addons>`.


.. attention::
   Use the **--cp (--complex-physical-parameters)** flag with the **sorcha run**  command on the terminal to specify the pointing database that ``Sorcha`` should use.

Complex Parameters File Configuration Parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``Sorcha`` is initialized for the format of the complex physical parameters file through the :ref:`configuration file<configs>` INPUT sections:

.. code-block::

   [INPUT]

   # Sorcha chunk size: how many objects should be processed at once?

   size_serial_chunk = 20000

   # Format for the orbit, physical parameters, and complex physical parameters input files.
   # Options: csv or whitespace

   aux_format = csv


.. _pointing:

Survey Pointing Database
------------------------

.. note::
  Currently ``Sorcha`` is set up to run with the LSST cadence simulations pointing databases.

This database contains information about the LSST pointing history and observing conditions.  We use observation mid-point time, right ascension, declination, rotation angle of the camera, 5-sigma limiting magnitude, filter, and seeing information in ``Sorcha`` to determine if a synthetic Solar System object is observable.

What we call the LSST pointing database (currently simulated since Rubin Observatory hasn’t started operations) is generated through the Rubin Observatory scheduler (since 2021 referred to as `rubin_sim <https://github.com/lsst/rubin_sim>`_ and previously known as OpSim). This software is currently under active development and is being used to run many simulated iterations of LSST scenarios, showing what the cadence would look like with differing survey strategies. A description of an early version of this Python software can be found in `Delgado et al.(2014) <https://ui.adsabs.harvard.edu/abs/2014SPIE.9150E..15D>`_. The output of rubin_sim is a SQLlite database containing the pointing history and associated metadata of the simulated observation history of LSST.

.. tip::
   The contents of the observations table in the SQLite LSST pointing database can be found `here <https://rubin-sim.lsst.io/rs_scheduler/output_schema.html>`_

.. warning::
  The pointing databases times are expected to be TAI (Temps Atomique International; French for International Atomic Time),


.. attention::
   Use the **--pd** flag on the command line to specify the pointing database that ``Sorcha`` should use.



The latest version of `rubin_sim <https://github.com/lsst/rubin_sim>`_ cadence simulations can be found at https://survey-strategy.lsst.io/baseline/index.html or  https://s3df.slac.stanford.edu/data/rubin/sim-data/. An example rubin_sim simulation visualized on sky is shown in the plot below of the number of on-sky visits over the 10-year simulated baseline v3.2 survey (image credit: Lynne Jones):

.. image:: images/Rubin_v3.2_baseline_visits.png
  :width: 410
  :alt: Sorcha logo
  :align: center

.. attention::
   There may be changes to how this information is read in when the Rubin Observatory operations begin in late 2025.


.. _database_query:


Setting Up the Correct LSST Pointing Database Query
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``Sorcha``'s **ppsqldbquery** :ref:`configuration file<configs>` parameter contains the SQL query for obtaining this information from the pointing database.

From `rubin_sim <https://github.com/lsst/rubin_sim>`_ v2.0 cadence simulations onward use the query::

  SELECT observationId, observationStartMJD as observationStartMJD_TAI, visitTime, visitExposureTime, filter, seeingFwhmGeom as seeingFwhmGeom_arcsec, seeingFwhmEff as seeingFwhmEff_arcsec, fiveSigmaDepth as fieldFiveSigmaDepth_mag , fieldRA as fieldRA_deg, fieldDec as fieldDec_deg, rotSkyPos as fieldRotSkyPos_deg FROM observations order by observationId

For past `rubin_sim <https://github.com/lsst/rubin_sim>`_ LSST cadence simulations pre-v2.0 use the query::

  SELECT observationId, observationStartMJD as observationStartMJD_TAI, visitTime, visitExposureTime, filter, seeingFwhmGeom as seeingFwhmGeom_arcsec, seeingFwhmEff as seeingFwhmEff_arcsec, fiveSigmaDepth  fieldFiveSigmaDepth_mag, fieldRA as fieldRA_deg, fieldDec as fieldDec_deg, rotSkyPos as fieldRotSkyPos_deg  FROM SummaryAllProps order by observationId



Survey Pointing Database Configuration Parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The survey pointing database query is set in the :ref:`configuration file<configs>` INPUT section:


.. code-block::

   [INPUT]

   # SQL query for extracting data from the pointing database.

   pointing_sql_query = SELECT observationId, observationStartMJD as observationStartMJD_TAI, visitTime, visitExposureTime, filter, seeingFwhmGeom as seeingFwhmGeom_arcsec, seeingFwhmEff as seeingFwhmEff_arcsec, fiveSigmaDepth as fieldFiveSigmaDepth_mag , fieldRA as fieldRA_deg, fieldDec as fieldDec_deg, rotSkyPos as fieldRotSkyPos_deg FROM observations order by observationId



Camera Footprint File (Optional)
-----------------------------------------

.. attention::
    The camera footprint file is only required if you are using the camera footprint 

If you are going to simulate the full camera architecture including CCD locations and chip gaps in the camera focal plane, you will need to provide a file that describes the layout of detectors on the camera focal plane. 

The camera footprint file is a comma-separated values (CSV) file with three columns describing the detector shapes, with the header “detector,x,y”. The first column indicates which detector a point belongs to, and should be an integer. Second and third columns specify where on the focal plane the corners are. Values are unitless, equal to tan( ra ), tan( dec ), where ra and dec are the vertical and horizontal angles of the points from the center of the sphere tangent to origin in the focal plane. Ordering does not matter, as the constructor sorts the points automatically.

.. tip::
    ``Sorcha`` comes with a representation of the LSSTCam architecture already installed. Further details of how to use this built-in default file can be found in the description of the :ref:`Full Camera Footprint Filter<full_camera_footprint>`.

Example Camera Footprint File
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../src/sorcha/modules/data/LSST_detector_corners_100123.csv 
    :language: text
    :lines: 1-20

Required Camera Footprints File Columns and Format
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

+--------------------------+-----------------------------------------------------------------------------------------+
| Keyword                  | Description                                                                             |
+==========================+=========================================================================================+
| detector                 | Detector identifier (integer)                                                           |
+--------------------------+-----------------------------------------------------------------------------------------+
| x                        | x position of the detector corner on the focal plane (float)                            |
+--------------------------+-----------------------------------------------------------------------------------------+
| y                        | y position of the detector corner on the focal plane (float)                            |
+--------------------------+-----------------------------------------------------------------------------------------+


.. note::
   The x and y values are unitless and are respectively equal to
   tan(ra) and tan(dec) , where ra and dec are the vertical and horizontal
   angles of the points from the center of the sphere tangent to the origin
   in the focal plane. For each detector, all four corners must be specified
   in the camera footprint file.

Camera Footprint File Configuration Parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
You can set whether you're using a camera footprint file and the location of the file in the :ref:`configuration file<configs>` FOV section:

.. code-block::

   [FOV]

   # Choose between circular or actual camera footprint, including chip gaps.
   # Options: circle, footprint.
   
   camera_model = footprint


   # Path to camera footprint file. Uncomment to provide a path to the desired camera 
   # detector configuration file if not using the default built-in LSSTCam detector 
   # configuration for the actual camera footprint.

   footprint_path= ./data/detectors_corners.csv

.. note::
   If **camera_model** is set to footprint and **footprint_path** variable is not set, ``Sorcha`` will automatically read in its installed LSSTCam detector footprint file. 

.. tip::
   If using the cicle camera model, the **footprint_path** variable should not be present or commented out of the :ref:`configuration file<configs>` . 


.. _ephemf:

Ephemeris File (Optional)
-----------------------------------------

.. note::
  ``Sorcha`` has an :ref:`ephemeris_gen` that we recommend using by default, but as an alternative ``Sorcha`` can read in an external file containing calculated ephemeris values for each simulated object within a reasonable search radius of a given survey field pointing and observation times as specified in the survey pointing database. This could be the output from a previous ``Sorcha`` run or  provided from your own separate ephemeris generation method,


.. tip::
  *  The first column must be ObjID, but the ordering of the remaining columns does not matter as long as the required columns exist and have entries
  *  The first row in the physical parameters file **must** list  the column names
  *  The **correct capitalization of column names** is required
  *  The ephemeris file can be either **whitespace-separated** or **comma-separated values (CSV)**
  *  Each simulated object **must** have a unique string identifier

.. attention::
   Use the **--er (--ephem-read)** flag with the **sorcha run** command on then terminal to specify the external ephemeris file that ``Sorcha`` should use.


.. warning::
   We have validated ``Sorcha`` with its internal ephemeris generator. If the user chooses to use a different ephemeris engine's calculations as
   input for ``Sorcha``, the user has the responsibility to check the accuracy of this input.

Example Ephemeris File
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. note::
  For readability we show an example of a whitespace-separated file below.

.. literalinclude:: ../docs/example_files/assist_rebound.csv
    :language: text
    :lines: 1-20


Required Ephemeris File Columns and Format
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

+--------------------------+-----------------------------------------------------------------------------------------+
| Keyword                  | Description                                                                             |
+==========================+=========================================================================================+
| ObjID                    | Object identifier for each synthetic planetesimal simulated (string)                    |
+--------------------------+-----------------------------------------------------------------------------------------+
| FieldID                  | Observation pointing field identificator                                                |
+--------------------------+-----------------------------------------------------------------------------------------+
| fieldMJD_TAI             | Observation Mean Julian Date (MJD) in TAI (International Atomic Time)                   |
+--------------------------+-----------------------------------------------------------------------------------------+
| fieldJD_TDB              | Observation Julian Date in TDB (Barycentric Dynamical Time)                             |
+--------------------------+-----------------------------------------------------------------------------------------+
| Range_LTC_km             | Topocentric distance to the simulated object                                            |
+--------------------------+-----------------------------------------------------------------------------------------+
| RangeRate_LTC_km_s       | Radial component of the object’s topocentric velocity (km/s)                            |
+--------------------------+-----------------------------------------------------------------------------------------+
| RA_deg                   | Object right ascension (degrees)                                                        |
+--------------------------+-----------------------------------------------------------------------------------------+
| RARateCosDec_deg_day     | Object right ascension rate of motion multiplied by cos(Dec) (deg/day)                  |
+--------------------------+-----------------------------------------------------------------------------------------+
| Dec_deg                  | Object declination (degrees)                                                            |
+--------------------------+-----------------------------------------------------------------------------------------+
| DecRate_deg_day          | Object declination rate of motion (deg/day)                                             |
+--------------------------+-----------------------------------------------------------------------------------------+
| Obj_Sun_x_LTC_km         | Light-time-corrected Cartesian X-component of the object’s heliocentric distance (km)   |
+--------------------------+-----------------------------------------------------------------------------------------+
| Obj_Sun_y_LT_km          | Light-time-corrected Cartesian Y-component of the object’s heliocentric distance (km)   |
+--------------------------+-----------------------------------------------------------------------------------------+
| Obj_Sun_z_LTC_km         | Light-time-corrected Cartesian X-component of the object’s heliocentric distance (km)   |
+--------------------------+-----------------------------------------------------------------------------------------+
| Obj_Sun_vx_LTC_km_s      | Light-time-corrected Cartesian X-component of the object’s heliocentric velocity (km/s) |
+--------------------------+-----------------------------------------------------------------------------------------+
| Obj_Sun_vy_LTC_km_s      | Light-time-corrected Cartesian Y-component of the object’s heliocentric velocity (km/s) |
+--------------------------+-----------------------------------------------------------------------------------------+
| Obj_Sun_vz_LTC_km_s      | Light-time-corrected Cartesian Z-component of the object’s heliocentric velocity (km/s) |
+--------------------------+-----------------------------------------------------------------------------------------+
| Obs_Sun_x_km             |  Cartesian X-component of observer's heliocentric distance (km)                         |
+--------------------------+-----------------------------------------------------------------------------------------+
| Obs_Sun_y_km             |  Cartesian Y-component of the observer's heliocentric distance (km)                     |
+--------------------------+-----------------------------------------------------------------------------------------+
| Obs_Sun_z_km             |  Cartesian Z-component of the observer's heliocentric distance (km)                     |
+--------------------------+-----------------------------------------------------------------------------------------+
| Obs_Sun_vx_km_s          |  Cartesian X-component of the observer's heliocentric velocity (km/s)                   |
+--------------------------+-----------------------------------------------------------------------------------------+
| Obs_Sun_vy_km_s          |  Cartesian Y-component of the observer's heliocentric velocity (km/s)                   |
+--------------------------+-----------------------------------------------------------------------------------------+
| Obs_Sun_vz_km_s          | Cartesian Z-component of the observer’s heliocentric velocity (km/s)                    |
+--------------------------+-----------------------------------------------------------------------------------------+
| phase_deg                | Phase angle between the Sun, object, and observer (degrees)                             |
+--------------------------+-----------------------------------------------------------------------------------------+
.. note::
   All positions and velocities are in respect to J2000

.. tip::
   The format and columns contained in Sorcha's  :ref:`optional ephemeris output file<ephem_output>` are the same as the columns outlined above. 

Ephemeris File Configuration Parameters 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``Sorcha`` is initialized to use an external ephemeris file through the :ref:`configuration file<configs>` INPUT section:

.. code-block::

   [INPUT]


   # The simulation used for the ephemeris input. 
   # ar=ASSIST+REBOUND interal ephemeris generation 
   # external=providing an external input file from the command line
   # Options: "ar", "external"

   ephemerides_type = external


   # Format for ephemeris simulation input file if a file is specified at the command line. 
   # This is also the format to which ephemeris files will be written out, if specified.
   # Options: csv, whitespace, hdf5

   eph_format = csv


.. _installation_aux:

Downloading Auxiliary Files For the Ephemeris Generator
-----------------------------------------------------------

To run ``Sorcha``'s built in :ref:`ephemeris generator<ephemeris_gen>`, you will need to download the auxiliary files required for performing the N-body integrations. 

To install the necessary `SPICE (Spacecraft, Planet, Instrument, C-matrix, Events) <https://naif.jpl.nasa.gov/naif/spiceconcept.html>`_ auxiliary files and other required data files for ephemeris generation (774 MB total in size), run::

    sorcha bootstrap

.. note::
   This script will download and store the auxiliary files in your computer's local cache directory by default.

.. note::
   The optional --cache flag allows you to specify a specific location to download the auxiliary files. If the files have  already downloaded and want a fresh download, you need to use the -f flag.

.. warning:: These files can change/be updated with the revised positions of the planets every once in a while. So if you're running simulations for population statistics, we recommend downloading these files to a directory and having all Sorcha runs these files for consistency.
  

