sorcha.modules.PPRandomizeMeasurements
======================================

.. py:module:: sorcha.modules.PPRandomizeMeasurements


Attributes
----------

.. autoapisummary::

   sorcha.modules.PPRandomizeMeasurements.logger


Functions
---------

.. autoapisummary::

   sorcha.modules.PPRandomizeMeasurements.randomizeAstrometryAndPhotometry
   sorcha.modules.PPRandomizeMeasurements.randomizeAstrometry
   sorcha.modules.PPRandomizeMeasurements.sampleNormalFOV
   sorcha.modules.PPRandomizeMeasurements.randomizePhotometry
   sorcha.modules.PPRandomizeMeasurements.flux2mag
   sorcha.modules.PPRandomizeMeasurements.mag2flux
   sorcha.modules.PPRandomizeMeasurements.icrf2radec
   sorcha.modules.PPRandomizeMeasurements.radec2icrf


Module Contents
---------------

.. py:data:: logger

.. py:function:: randomizeAstrometryAndPhotometry(observations, sconfigs, module_rngs, verbose=False)

   Wrapper function to perform randomisation of astrometry and photometry around
   their uncertainties. Calls randomizePhotometry() and randomizeAstrometry().

   Adds the following columns to the dataframe:
   - trailedSourceMag
   - PSFMag
   - AstRATrue(deg)
   - AstDecTrue(deg)

   :param observations: Dataframe containing observations.
   :type observations: pandas dataframe
   :param sconfigs: Dataclass of configuration file arguments.
   :type sconfigs: dataclass
   :param module_rngs: A collection of random number generators (per module).
   :type module_rngs: PerModuleRNG
   :param verbose: Verbosity on or off. Default False.
   :type verbose: bool

   :returns: **observations** -- Original input dataframe with RA and Dec columns and trailedSourceMag and PSFMag
             columns randomized around astrometric and photometric sigma. Original RA and Dec/magnitudes
             stored in separate columns.
   :rtype: pandas dataframe


.. py:function:: randomizeAstrometry(df, module_rngs, raName='RA_deg', decName='Dec_deg', raOrigName='RATrue_deg', decOrigName='DecTrue_deg', sigName='AstSig(deg)', radecUnits='deg', sigUnits='mas')

   Randomize astrometry with a normal distribution around the actual RADEC pointing.
   The randomized values replace the original astrometry, with the original values
   stored in separate columns.

   Adds the following columns to the observations dataframe:

   - AstRATrue(deg)
   - AstDecTrue(deg)

   :param df: Dataframe containing astrometry and sigma.
   :type df: pandas dataframe
   :param module_rngs: A collection of random number generators (per module).
   :type module_rngs: PerModuleRNG
   :param ra_Name: "df" dataframe column name for the right ascension.
                   Default = "RA_deg"
   :type ra_Name: string, optional
   :param dec_Name: "df" dataframe column name for the declination. Default = "Dec_deg"
   :type dec_Name: string, optional
   :param raOrigName: "df" dataframe column name for where to store original right
                      ascension. Default = "RATrue_deg"
   :type raOrigName: string, optional
   :param decOrigName: "df" dataframe column name for where to store original declination.
                       Default = "DecTrue_deg"
   :type decOrigName: string, optional
   :param sigName: "df" dataframe column name for the standard deviation, uncertainty in the
                   astrometric position.
                   Default = "AstSig(deg)"
   :type sigName: string, optional
   :param radecUnits: Units for RA and Dec ('deg'/'rad'/'mas'). Default = "deg"
   :type radecUnits: string
   :param sigUnits: Units for standard deviation ('deg'/'rad'/'mas'). Default = "mas"
   :type sigUnits: string

   :returns: **df** -- original input dataframe with RA and Dec columns randomized around
             astrometric sigma and original RA and Dec stored in separate columns
   :rtype: pandas dataframe

   .. rubric:: Notes

   Covariances in RADEC are currently not supported. The routine calculates
   a normal distribution on the unit sphere, so as to allow for a correct modeling of
   the poles. Distributions close to the poles may look odd in RADEC.


.. py:function:: sampleNormalFOV(center, sigma, module_rngs, ndim=3)

   Sample n points randomly (normal distribution) on a region on the unit (hyper-)sphere.

   :param center: Center of hpyer-sphere: can be an [n, ndim] dimensional array,
                  but only if n == npoints.
   :type center: float
   :param sigma: 1 sigma distance on unit sphere [radians]x
   :type sigma: n-dimensional array
   :param module_rngs: A collection of random number generators (per module).
   :type module_rngs: PerModuleRNG
   :param ndim: Dimension of hyper-sphere. Default = 3
   :type ndim: integer, optional

   :returns: **vec** -- Size [npoints, ndim]
   :rtype: numpy array


.. py:function:: randomizePhotometry(df, module_rngs, magName='Filtermag', magRndName='FiltermagRnd', sigName='FiltermagSig')

   Randomize photometry with normal distribution around magName value.

   :param df: Dataframe containing astrometry and sigma.
   :type df: pandas dataframe
   :param module_rngs: A collection of random number generators (per module).
   :type module_rngs: PerModuleRNG
   :param magName: 'df' column name of apparent magnitude. Default = "Filtermag"
   :type magName: string, optional
   :param magRndName: 'df' column name for storing randomized apparent magnitude, Default = "FiltermagRnd"
   :type magRndName: string, optional
   :param sigName: 'df' column name for magnitude standard deviation. Default = "FiltermagSig"
   :type sigName: float, optional

   :returns: randomized magnitudes for each row in 'df'
   :rtype: array of floats

   .. rubric:: Notes

   The normal distribution here is in magnitudes while it should be in flux. This will fail for large sigmas.
   Should be fixed at some point.

   We assume that apparent magnitudes are stored within 'df' and that 'magName'
   corresponds to the corresponding column within 'df'

    'df' is also modified with added column magRndNam to store the randomize apparent magnitude


.. py:function:: flux2mag(f, f0=3631)

   AB ugriz system (f0 = 3631 Jy) to magnitude conversion.

   :param f: flux. [Units : Jy].
   :type f: float or array of floats
   :param f0: Zero point flux. Default = 3631
   :type f0: float, optional

   :returns: **mag** -- pogson magnitude. [Units: mag]
   :rtype: float or array of floats


.. py:function:: mag2flux(mag, f0=3631)

   AB ugriz system (f0 = 3631 Jy) magnitude to flux conversion.

   :param mag: Pogson magnitude. [Units: mag]
   :type mag: float or rray of floats
   :param f0: Zero point flux. Default = 3631
   :type f0: float, optional

   :returns: **f (float/array of floats)**
   :rtype: flux [Units: Jy].


.. py:function:: icrf2radec(x, y, z, deg=True)

   Convert ICRF xyz to Right Ascension and Declination.
   Geometric states on unit sphere, no light travel time/aberration correction.

   :param x: 3D vector of unit length (ICRF)
   :type x: floats/arrays of floats
   :param y: 3D vector of unit length (ICRF)
   :type y: floats/arrays of floats
   :param z: 3D vector of unit length (ICRF)
   :type z: floats/arrays of floats
   :param de: True for angles in degrees, False for angles in radians. Default = True
   :type de: boolean, optional

   :returns: * **ra** (*float or array of floats*) -- Right Ascension. [Units: deg]
             * **dec** (*float or array of floats*) -- Declination. [Units: deg]


.. py:function:: radec2icrf(ra, dec, deg=True)

   Convert Right Ascension and Declination to ICRF xyz unit vector.
   Geometric states on unit sphere, no light travel time/aberration correction.

   :param ra: Right Ascension. [Units: deg]
   :type ra: float or array of floats
   :param dec: Declination. [Units deg]
   :type dec: float or array of floats
   :param deg: True for angles in degrees, False for angles in radians. Default = True
   :type deg: boolean, optional

   :returns: **array([x, y, z])** -- 3D vector of unit length (ICRF)
   :rtype: arrays/matrix of floats


