.. _advanced:

Advanced User Features
==========================

.. warning::
   **If you're new to sorcha, turn away from this section NOW! (we're only partially kidding)** This section provides information about features for advanced users of ``Sorcha``. Changing or adjusting the parameters described in this section may produce unintended results. **With great power comes great responsibility. Be very careful in applying the knowledge below.** Most users will not need to touch these parameters within ``Sorcha``.

Setting the Random Number Generator Seed
---------------------------------------------

.. warning::
   For most science cases, you **DO NOT** want to set the same seed for each ``Sorcha`` run, but if you need reproducability then you do want to see the seed as an environment variable before running ``Sorcha`` 

The value used to seed the random number generator can be specified via the **SORCHA_SEED** environmental variable. This allows for ``Sorcha``  to be fully reproducibly run with (if using a bash shell or Z-shell)::

   export SORCHA_SEED=52

.. tip::
   If you're trying to reproduce a crash or a certain behavior in ``Sorcha``, you can find the value that you need to set the random seed to in the log file.  
  

Expert User Filters and Config File Options
-----------------------------------------------

The following options can be optionally added to an expert section ([EXPERT]) of the :ref:`configs`. 

 
Turning Vignetting Off 
~~~~~~~~~~~~~~~~~~~~~~~~~~~

By default, :ref:`vignetting<vignetting>` using LSSTCam parameters is applied. To turn vignetting off, add to the :ref:`configs`::

   [EXPERT]
   vignetting_on = False

.. note::
   If vigentting is turned off, then the 5σ Limiting Magnitude at the Source Location will be the limiting magnitude at the cetner of the FOV from the :ref:`pointing`.
 
.. tip::
   Vignetting is a small effect for the LSSTCam, so you will see only a modest change in results if you turn this off for LSST simulations


Turning Off the Randomization of the Magnitude and Astrometry Values
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There may be a reason that you want to turn off the :ref:`randomization<randomization>` of the trailed source magnitude and PSF magnitude as well as the RA and Dec values::

   [EXPERT]
   randomization_on = False


Turning Off Trailing Losses
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Applying :ref:`trailing losses<trailing>` is on by default, but it can be turned off by including the option in the :ref:`configs`::

    [EXPERT]
    trailing_losses_on = False

.. warning::
    We **very strongly recommend** that the user never turn this off, but we provide
    this option for debugging or for speed increases when the user is absolutely sure
    they are only supplying slow-moving objects.

Turning off Detection Efficiency/Applying the Fading Function
----------------------------------------------------------------

Applying the :ref:`survey detection efficiency<fading>` is on by default, but it can be turned off by including the option in the :ref:`configs`::

    [FADINGFUNCTION]
    fading_function_on = False

Turning Off the Camera Footprint Filter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In rare instances you may need to skip the  :ref:`camera footprint filter<footprint>` and turn it off. This can be done by setting the camera model to none in the field-of-view (FOV) section of the :ref:`configs`::

    [FOV]
    camera_model = none

.. note::
    If you're using ``Sorcha``'s bult-in :ref:`ephemeris generator<ephemeris_gen>`, the generator will apply a circular search region around each filed pointing when associating potential input population detections with the survey observations. 


SNR/Apparent Magnitude Filters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. warning::
    These filters are for the advanced user. If you only want to know what the survey will discover, you **DO NOT** need these filters on.

These two mutually-exclusive filters serve to cut observations of faint objects.
The user may either implement the SNR limit, to remove all observations of objects
below a user-defined SNR threshold; or the magnitude limit, to remove all observations
of objects above a user-defined **trailed source magniitude** magnitude. 
**These filters are applied before the detection efficiency (fading function) is applied in** ``Sorcha``. 

The SNR filter which will remove syntheitc observations that are less than a user-supplied  SNR limit, To implelment the SNR limit (in this example to keep synthetic observations of input objects with a SNR > =2) include the following in the config file::

    [EXPERT]
    SNR_limit = 2.0

To implement the magnitude limit (remove detections of objects fainter than 22 mag in all survey observing bands), include the following in the :ref:`configs`::
    
    [EXPERT]
    magnitude_limit = 22.0
    
.. attention::
    Only one of these filters may be implemented at once.

.. seealso::
  We have an `example Jupyter notebook <notebooks/demo_MagnitudeAndSNRCuts.ipynb>`_  demonstrating how these filters work within ``Sorcha``.

Modifying the Ephemeris Generator Interpolation
--------------------------------------------------

A user can update the number of sub-intervals for the Lagrange ephemerides interpolation used within ``Sorcha``'s internal ephemeris generator. By default this value is set to **101**, but the user can update it to a different value. 101 works for most orbits, but it may be worth exploring using a different value if you're modeling Earth impactors and very close Near-Earth Objects (NEOs). To change the number of sub-intervals, **n_sub_intervals** variable is  added to the ([SIMULATION]) section::

    [SIMULATION]
    n_sub_intervals = 122

Specifying Alernative Versions of the Auxiliary Files Used in the Ephemeris Generator 
-----------------------------------------------------------------------------------------

For backwards compability and to enable new version of the files to be run as well, users can override the default filenames and download locations of the :ref:`auxiliary files<auxfiles>` used by ``Sorcha``'s bult-in :ref:`ephemeris generator<ephemeris_gen>`.  These :ref:`configs`:: variables are added to a new auxiliary ([AUXILIARY]) section::


    [AUXILIARY]
    de440s = de440s.bsp
    de440s_url = https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/de440s.bsp

    earth_predict = earth_200101_990827_predict.bpc
    earth_predict_url = https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/earth_200101_990827_predict.bpc

    earth_historical = earth_620120_240827.bpc
    earth_historical_url = https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/earth_620120_240827.bpc

    earth_high_precision = earth_latest_high_prec.bpc
    earth_high_precision_url = https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/earth_latest_high_prec.bpc

    jpl_planets = linux_p1550p2650.440
    jpl_planets_url = https://ssd.jpl.nasa.gov/ftp/eph/planets/Linux/de440/linux_p1550p2650.440

    jpl_small_bodies = sb441-n16.bsp
    jpl_small_bodies_url = https://ssd.jpl.nasa.gov/ftp/eph/small_bodies/asteroids_de441/sb441-n16.bsp 

    leap_seconds = naif0012.tls
    leap_seconds_url = https://naif.jpl.nasa.gov/pub/naif/generic_kernels/lsk/naif0012.tls

    meta_kernel = meta_kernel.txt
    
    observatory_codes = ObsCodes.json
    observatory_codes_compressed = ObsCodes.json.gz
    observatory_codes_compressed_url = https://minorplanetcenter.net/Extended_Files/obscodes_extended.json.gz

    orientation_constants = pck00010.pck
    orientation_constants_url = https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/pck00010.tpc


.. note::
   You can specify one or any number of the filenames or URLs. 
 
.. note::
   If you make changes to the filenames or the download urls, you'll likely need to first remove meta_kernel.txt  from the auxiliary cache (the directory these files are stored in) or specify a different filename name for meta_kernel file in the config file so that it can be rebuilt with the appropriate names.  

.. note:: 
   ``Sorcha`` checks if the :ref:`auxiliary files<auxfiles>` exist in the cache directory first before attempting to download any missing files and copies them over into the default filenames. 
   
Advanced Output Options
-----------------------------------

Custom Outputs 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

By setting the value of the output_columns configuration file keyword to a comma-separated list of column names, you may
specify your own custom output, using this page as a reference for potential column names.

For example, you could state this in your configuration file to get the object ID, position and magnitude only::

    [OUTPUT]
    output_columns = ObjID,RA_deg,Dec_deg,trailedSourceMag

.. warning::
   If you are choosing to specify the column names in this way, please perform a quick test-run first to ensure your column names are correct before
   embarking on any long runs. As we allow for user-written code and add-ons to add new column names, we do not error-handle the column names until
   late in the code, upon output.


Specifying the Decimal Precision for the Photometric and Astromeitc Values 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

By default, no rounding is performed on any of the output values. We recommend that you do not change the decimal place precision  and instead leave ``Sorcha`` to output the full value to machine precision, but there may be reasons why you need to reduce the size of the output.

In the [OUTPUT] section of the :ref:`configs`, you can set the decimal precision for the astrometry outputs::

    [OUTPUT]
    # Decimal places to which RA and Dec should be rounded to in output.
    position_decimals = 7


In the [OUTPUT] section of the :ref:`configs`, you can set the decimal precision for the magnitude outputs::

    [OUTPUT]
    # Decimal places to which all magnitudes should be rounded to in output.
    magnitude_decimals = 3


