
Advanced User Features
==========================

.. warning::
   **If you're new to sorcha, turn away from this section NOW! (we're only partially kidding)** This section provides information about features for advanced users of ``sorcha``. Changing or adjusting the parameters described in this section may produce unintended results. **With great power comes great responsibility. Be very careful in applying the knowledge below.** Most users will not need to touch these parameters within ``sorcha``.

Setting the Random Number Generator Seed
---------------------------------------------

.. warning::
   For most science cases, you **DO NOT** want to set the same seed for each ``sorcha`` run, but if you need reproducability then you do want to see the seed as an environment variable before running ``sorcha`` 

The value used to seed the random number generator can be specified via the **SORCHA_SEED** environmental variable. This allows for ``sorcha``  to be fully reproducibly run with (if using a bash shell or Z-shell)::

   export SORCHA_SEED=42

.. tip::
   If you're trying to reproduce a crash or a certain behavior in ``sorcha``, you can find the value that you need to set the random seed to in the log file.  
  

Expert User Config File Options
-----------------------------------

The following options can be optionally added to an expert section of the :ref:`configs`. The section will start with::

   [EXPERT]

 
Turning Vignetting Off 
~~~~~~~~~~~~~~~~~~~~~~~~~~~

By default, vignetting using LSSTCam parameters is applied. To turn vignetting off, add to the configuratuion file::

   [EXPERT]
   vignetting_on = False

.. tip::
   Vignetting is a small effect for the LSSTCam, so you will see only a modest change in results if you turn this off for LSST simulations


Turning Off the Randomization of the Magnitude and Astrometry Values
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
There may be a reason that you want to turn off the randomization of the trailed source magnitude and PSF magnitude as well as the RA and Dec values::

   [EXPERT]
   randomization_on = False


Turning Off Trailing Losses
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The trailing losses filter is on by default, but it can be turned off by including the option in the configuration file::

    [EXPERT]
    trailing_losses_on = False

.. warning::
    We **very strongly recommend** that the user never turn this off, but we provide
    this option for debugging or for speed increases when the user is absolutely sure
    they are only supplying slow-moving objects.

SNR/Apparent Magnitude Filters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. warning::
    These filters are for the advanced user. If you only want to know what the survey will discover, you **DO NOT** need these filters on.

These two mutually-exclusive filters serve to cut observations of faint objects.
The user may either implement the SNR limit, to remove all observations of objects
below a user-defined SNR threshold; or the magnitude limit, to remove all observations
of objects above a user-defined magnitude.

To implement the SNR limit, include the following in the config file::

    [EXPERT]
    SNR_limit = 2.0

To implement the magnitude limit, include the following in the config file::
    
    [EXPERT]
    magnitude_limit = 22.0
    
.. attention::
    Only one of these filters may be implemented at once.



