sorcha.utilities.sorchaConfigs
==============================

.. py:module:: sorcha.utilities.sorchaConfigs


Classes
-------

.. autoapisummary::

   sorcha.utilities.sorchaConfigs.inputConfigs
   sorcha.utilities.sorchaConfigs.simulationConfigs
   sorcha.utilities.sorchaConfigs.filtersConfigs
   sorcha.utilities.sorchaConfigs.saturationConfigs
   sorcha.utilities.sorchaConfigs.phasecurvesConfigs
   sorcha.utilities.sorchaConfigs.fovConfigs
   sorcha.utilities.sorchaConfigs.fadingfunctionConfigs
   sorcha.utilities.sorchaConfigs.linkingfilterConfigs
   sorcha.utilities.sorchaConfigs.outputConfigs
   sorcha.utilities.sorchaConfigs.lightcurveConfigs
   sorcha.utilities.sorchaConfigs.activityConfigs
   sorcha.utilities.sorchaConfigs.expertConfigs
   sorcha.utilities.sorchaConfigs.auxiliaryConfigs
   sorcha.utilities.sorchaConfigs.sorchaConfigs


Functions
---------

.. autoapisummary::

   sorcha.utilities.sorchaConfigs.check_key_exists
   sorcha.utilities.sorchaConfigs.check_key_doesnt_exist
   sorcha.utilities.sorchaConfigs.cast_as_int
   sorcha.utilities.sorchaConfigs.cast_as_float
   sorcha.utilities.sorchaConfigs.cast_as_bool
   sorcha.utilities.sorchaConfigs.check_value_in_list
   sorcha.utilities.sorchaConfigs.PPFindFileOrExit
   sorcha.utilities.sorchaConfigs.cast_as_bool_or_set_default
   sorcha.utilities.sorchaConfigs.PrintConfigsToLog


Module Contents
---------------

.. py:class:: inputConfigs

   Data class for holding INPUTS section configuration file keys and validating them.


   .. py:attribute:: ephemerides_type
      :type:  str
      :value: None


      Simulation used for ephemeris input.


   .. py:attribute:: eph_format
      :type:  str
      :value: None


      Format for ephemeris simulation input file.


   .. py:attribute:: size_serial_chunk
      :type:  int
      :value: None


      Sorcha chunk size.


   .. py:attribute:: aux_format
      :type:  str
      :value: None


      Format for the auxiliary input files.


   .. py:attribute:: pointing_sql_query
      :type:  str
      :value: None


      SQL query for extracting data from pointing database.


   .. py:method:: __post_init__()

      Automagically validates the input configs after initialisation.



   .. py:method:: _validate_input_configs()

      Validates the input config attributes after initialisation.

      :param None.:

      :rtype: None



.. py:class:: simulationConfigs

   Data class for holding SIMULATION section configuration file keys and validating them


   .. py:attribute:: ar_ang_fov
      :type:  float
      :value: None


      the field of view of our search field, in degrees


   .. py:attribute:: ar_fov_buffer
      :type:  float
      :value: None


      the buffer zone around the field of view we want to include, in degrees


   .. py:attribute:: ar_picket
      :type:  float
      :value: None


      imprecise discretization of time that allows us to move progress our simulations forward without getting too granular when we don't have to. the unit is number of days.


   .. py:attribute:: ar_obs_code
      :type:  str
      :value: None


      the obscode is the MPC observatory code for the provided telescope.


   .. py:attribute:: ar_healpix_order
      :type:  int
      :value: None


      the order of healpix which we will use for the healpy portions of the code.


   .. py:attribute:: _ephemerides_type
      :type:  str
      :value: None


      Simulation used for ephemeris input.


   .. py:method:: __post_init__()

      Automagically validates the simulation configs after initialisation.



   .. py:method:: _validate_simulation_configs()

      Validates the simulation config attributes after initialisation.

      :param None.:

      :rtype: None



.. py:class:: filtersConfigs

   Data class for holding FILTERS section configuration file keys and validating them


   .. py:attribute:: observing_filters
      :type:  str
      :value: None


      Filters of the observations you are interested in, comma-separated.


   .. py:attribute:: survey_name
      :type:  str
      :value: None


      survey name to be used for checking filters are correct


   .. py:attribute:: mainfilter
      :type:  str
      :value: None


      main filter chosen in physical parameter file


   .. py:attribute:: othercolours
      :type:  str
      :value: None


      other filters given alongside main filter


   .. py:method:: __post_init__()

      Automagically validates the filters configs after initialisation.



   .. py:method:: _validate_filters_configs()

      Validates the filters config attributes after initialisation.

      :param None.:

      :rtype: None



   .. py:method:: _check_for_correct_filters()

      Checks the filters selected are used by the chosen survey.

      :param None.:

      :rtype: None



.. py:class:: saturationConfigs

   Data class for holding SATURATION section configuration file keys and validating them


   .. py:attribute:: bright_limit_on
      :type:  bool
      :value: None



   .. py:attribute:: bright_limit
      :type:  float
      :value: None


      Upper magnitude limit on sources that will overfill the detector pixels/have counts above the non-linearity regime of the pixels where one can’t do photometry. Objects brighter than this limit (in magnitude) will be cut.


   .. py:attribute:: _observing_filters
      :type:  list
      :value: None


      Filters of the observations you are interested in, comma-separated.


   .. py:method:: __post_init__()

      Automagically validates the saturation configs after initialisation.



   .. py:method:: _validate_saturation_configs()

      Validates the saturation config attributes after initialisation.

      :param None.:

      :rtype: None



.. py:class:: phasecurvesConfigs

   Data class for holding PHASECURVES section configuration file keys and validating them


   .. py:attribute:: phase_function
      :type:  str
      :value: None


      The phase function used to calculate apparent magnitude. The physical parameters input


   .. py:method:: __post_init__()

      Automagically validates the phasecurve configs after initialisation.



   .. py:method:: _validate_phasecurve_configs()

      Validates the phasecurve config attributes after initialisation.

      :param None.:

      :rtype: None



.. py:class:: fovConfigs

   Data class for holding FOV section configuration file keys and validating them


   .. py:attribute:: camera_model
      :type:  str
      :value: None


      Choose between circular or actual camera footprint, including chip gaps.


   .. py:attribute:: footprint_path
      :type:  str
      :value: None


      Path to camera footprint file. Uncomment to provide a path to the desired camera detector configuration file if not using the default built-in LSSTCam detector configuration for the actual camera footprint.


   .. py:attribute:: fill_factor
      :type:  str
      :value: None


      Fraction of detector surface area which contains CCD -- simulates chip gaps for OIF output. Comment out if using camera footprint.


   .. py:attribute:: circle_radius
      :type:  float
      :value: None


      Radius of the circle for a circular footprint (in degrees). Float. Comment out or do not include if using footprint camera model.


   .. py:attribute:: footprint_edge_threshold
      :type:  float
      :value: None


      The distance from the edge of a detector (in arcseconds on the focal plane) at which we will not correctly extract an object. By default this is 10px or 2 arcseconds. Comment out or do not include if not using footprint camera model.


   .. py:attribute:: survey_name
      :type:  str
      :value: None


      name of survey


   .. py:method:: __post_init__()

      Automagically validates the fov configs after initialisation.



   .. py:method:: _validate_fov_configs()

      Validates the fov config attributes after initialisation.

      :param None.:

      :rtype: None



   .. py:method:: _camera_footprint()

      Validates the fov config attributes for a footprint camera model.

      :param None.:

      :rtype: None



   .. py:method:: _camera_circle()

      Validates the fov config attributes for a circle camera model.

      :param None.:

      :rtype: None



.. py:class:: fadingfunctionConfigs

   Data class for holding FADINGFUNCTION section configuration file keys and validating them


   .. py:attribute:: fading_function_on
      :type:  bool
      :value: None


      Detection efficiency fading function on or off.


   .. py:attribute:: fading_function_width
      :type:  float
      :value: None


      Width parameter for fading function. Should be greater than zero and less than 0.5.


   .. py:attribute:: fading_function_peak_efficiency
      :type:  float
      :value: None


      Peak efficiency for the fading function, called the 'fill factor' in Chesley and Veres (2017).


   .. py:method:: __post_init__()

      Automagically validates the fading function configs after initialisation.



   .. py:method:: _validate_fadingfunction_configs()

      Validates the fadindfunction config attributes after initialisation.

      :param None.:

      :rtype: None



.. py:class:: linkingfilterConfigs

   Data class for holding LINKINGFILTER section configuration file keys and validating them.


   .. py:attribute:: ssp_linking_on
      :type:  bool
      :value: None


      flag to see if model should run ssp linking filter


   .. py:attribute:: drop_unlinked
      :type:  bool
      :value: None


      Decides if unlinked objects will be dropped.


   .. py:attribute:: ssp_detection_efficiency
      :type:  float
      :value: None


      ssp detection efficiency. Which fraction of the observations of an object will the automated solar system processing pipeline successfully link? Float.


   .. py:attribute:: ssp_number_observations
      :type:  int
      :value: None


      Length of tracklets. How many observations of an object during one night are required to produce a valid tracklet?


   .. py:attribute:: ssp_separation_threshold
      :type:  float
      :value: None


      Minimum separation (in arcsec) between two observations of an object required for the linking software to distinguish them as separate and therefore as a valid tracklet.


   .. py:attribute:: ssp_maximum_time
      :type:  float
      :value: None


      Maximum time separation (in days) between subsequent observations in a tracklet. Default is 0.0625 days (90mins).


   .. py:attribute:: ssp_number_tracklets
      :type:  int
      :value: None


      Number of tracklets for detection. How many tracklets are required to classify an object as detected?


   .. py:attribute:: ssp_track_window
      :type:  int
      :value: None


      The number of tracklets defined above must occur in <= this number of days to constitute a complete track/detection.


   .. py:attribute:: ssp_night_start_utc
      :type:  float
      :value: None


      The time in UTC at which it is noon at the observatory location (in standard time). For the LSST, 12pm Chile Standard Time is 4pm UTC.


   .. py:method:: __post_init__()

      Automagically validates the linking filter configs after initialisation.



   .. py:method:: _validate_linkingfilter_configs()

      Validates the linkingfilter config attributes after initialisation.

      :param None.:

      :rtype: None



.. py:class:: outputConfigs

   Data class for holding OUTPUT section configuration file keys and validating them.


   .. py:attribute:: output_format
      :type:  str
      :value: None


      Output format of the output file[s]


   .. py:attribute:: output_columns
      :type:  str
      :value: None


      Controls which columns are in the output files.


   .. py:attribute:: position_decimals
      :type:  float
      :value: None


      position decimal places


   .. py:attribute:: magnitude_decimals
      :type:  float
      :value: None


      magnitude decimal places


   .. py:method:: __post_init__()

      Automagically validates the output configs after initialisation.



   .. py:method:: _validate_output_configs()

      Validates the output config attributes after initialisation.

      :param None.:

      :rtype: None



   .. py:method:: _validate_decimals()

      Validates the decimal output config attributes after initialisation.

      :param None.:

      :rtype: None



.. py:class:: lightcurveConfigs

   Data class for holding LIGHTCURVE section configuration file keys and validating them.


   .. py:attribute:: lc_model
      :type:  str
      :value: None


      The unique name of the lightcurve model to use. Defined in the ``name_id`` method of the subclasses of AbstractLightCurve. If not none, the complex physical parameters file must be specified at the command line.lc_model = none


   .. py:method:: __post_init__()

      Automagically validates the lightcurve configs after initialisation.



   .. py:method:: _validate_lightcurve_configs()

      Validates the lightcurve config attributes after initialisation.

      :param None.:

      :rtype: None



.. py:class:: activityConfigs

   Data class for holding Activity section configuration file keys and validating them.


   .. py:attribute:: comet_activity
      :type:  str
      :value: None


      The unique name of the actvity model to use. Defined in the ``name_id`` method of the subclasses of AbstractCometaryActivity.  If not none, a complex physical parameters file must be specified at the command line.


   .. py:method:: __post_init__()

      Automagically validates the activity configs after initialisation.



   .. py:method:: _validate_activity_configs()

      Validates the activity config attributes after initialisation.

      :param None.:

      :rtype: None



.. py:class:: expertConfigs

   Data class for holding expert section configuration file keys and validating them.


   .. py:attribute:: SNR_limit
      :type:  float
      :value: None


      Drops observations with signal to noise ratio less than limit given


   .. py:attribute:: SNR_limit_on
      :type:  bool
      :value: None


      flag for when an SNR limit is given


   .. py:attribute:: mag_limit
      :type:  float
      :value: None


      Drops observations with magnitude less than limit given


   .. py:attribute:: mag_limit_on
      :type:  bool
      :value: None


      flag for when a magnitude limit is given


   .. py:attribute:: trailing_losses_on
      :type:  bool
      :value: None


      flag for trailing losses


   .. py:attribute:: default_SNR_cut
      :type:  bool
      :value: None


      flag for default SNR


   .. py:attribute:: randomization_on
      :type:  bool
      :value: None


      flag for randomizing astrometry and photometry


   .. py:attribute:: vignetting_on
      :type:  bool
      :value: None


      flag for calculating effects of vignetting on limiting magnitude


   .. py:method:: __post_init__()

      Automagically validates the expert configs after initialisation.



   .. py:method:: _validate_expert_configs()

      Validates the expert config attributes after initialisation.

      :param None.:

      :rtype: None



.. py:class:: auxiliaryConfigs

   .. py:attribute:: de440s
      :type:  str
      :value: 'de440s.bsp'


      filename of de440s


   .. py:attribute:: de440s_url
      :type:  str
      :value: 'https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/de440s.bsp'


      url for de4440s


   .. py:attribute:: earth_predict
      :type:  str
      :value: 'earth_200101_990827_predict.bpc'


      filename of earth_predict


   .. py:attribute:: earth_predict_url
      :type:  str
      :value: 'https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/earth_200101_990827_predict.bpc'


      url for earth_predict


   .. py:attribute:: earth_historical
      :type:  str
      :value: 'earth_620120_240827.bpc'


      filename of earth_histoical


   .. py:attribute:: earth_historical_url
      :type:  str
      :value: 'https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/earth_620120_240827.bpc'


      url for earth_historical


   .. py:attribute:: earth_high_precision
      :type:  str
      :value: 'earth_latest_high_prec.bpc'


      filename of earth_high_precision


   .. py:attribute:: earth_high_precision_url
      :type:  str
      :value: 'https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/earth_latest_high_prec.bpc'


      url of earth_high_precision


   .. py:attribute:: jpl_planets
      :type:  str
      :value: 'linux_p1550p2650.440'


      filename of jpl_planets


   .. py:attribute:: jpl_planets_url
      :type:  str
      :value: 'https://ssd.jpl.nasa.gov/ftp/eph/planets/Linux/de440/linux_p1550p2650.440'


      url of jpl_planets


   .. py:attribute:: jpl_small_bodies
      :type:  str
      :value: 'sb441-n16.bsp'


      filename of jpl_small_bodies


   .. py:attribute:: jpl_small_bodies_url
      :type:  str
      :value: 'https://ssd.jpl.nasa.gov/ftp/eph/small_bodies/asteroids_de441/sb441-n16.bsp'


      url of jpl_small_bodies


   .. py:attribute:: leap_seconds
      :type:  str
      :value: 'naif0012.tls'


      filename of leap_seconds


   .. py:attribute:: leap_seconds_url
      :type:  str
      :value: 'https://naif.jpl.nasa.gov/pub/naif/generic_kernels/lsk/naif0012.tls'


      url of leap_seconds


   .. py:attribute:: meta_kernel
      :type:  str
      :value: 'meta_kernel.txt'


      filename of meta_kernal


   .. py:attribute:: observatory_codes
      :type:  str
      :value: 'ObsCodes.json'


      filename of observatory_codes


   .. py:attribute:: observatory_codes_compressed
      :type:  str
      :value: 'ObsCodes.json.gz'


      filename of observatory_codes_compressed


   .. py:attribute:: observatory_codes_compressed_url
      :type:  str
      :value: 'https://minorplanetcenter.net/Extended_Files/obscodes_extended.json.gz'


      url of observatory_codes_compressed


   .. py:attribute:: orientation_constants
      :type:  str
      :value: 'pck00010.pck'


      filename of observatory_constants


   .. py:attribute:: orientation_constants_url
      :type:  str
      :value: 'https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/pck00010.tpc'


      url of observatory_constants


   .. py:attribute:: data_file_list
      :type:  list
      :value: None


      convenience list of all the file names


   .. py:attribute:: urls
      :type:  dict
      :value: None


      url

      :type: dictionary of filename


   .. py:attribute:: data_files_to_download
      :type:  list
      :value: None


      list of files that need to be downloaded


   .. py:attribute:: ordered_kernel_files
      :type:  list
      :value: None


      list of kernels ordered from least to most precise - used to assemble meta_kernel file


   .. py:attribute:: registry
      :type:  list
      :value: None


      Default Pooch registry to define which files will be tracked and retrievable


   .. py:property:: default_url

      returns a dictionary of the default urls used in this version of sorcha


   .. py:property:: default_filenames

      returns a dictionary of the default filenames used in this version


   .. py:method:: __post_init__()

      Automagically validates the auxiliary configs after initialisation.



   .. py:method:: _validate_auxiliary_configs()

      validates the auxililary config attributes after initialisation.



   .. py:method:: _create_lists_auxiliary_configs()

      creates lists of the auxililary config attributes after initialisation.

      :param None.:

      :rtype: None



.. py:class:: sorchaConfigs(config_file_location=None, survey_name=None)

   Dataclass which stores configuration file keywords in dataclasses.


   .. py:attribute:: input
      :type:  inputConfigs
      :value: None


      inputConfigs dataclass which stores the keywords from the INPUT section of the config file.


   .. py:attribute:: simulation
      :type:  simulationConfigs
      :value: None


      simulationConfigs dataclass which stores the keywords from the SIMULATION section of the config file.


   .. py:attribute:: filters
      :type:  filtersConfigs
      :value: None


      filtersConfigs dataclass which stores the keywords from the FILTERS section of the config file.


   .. py:attribute:: saturation
      :type:  saturationConfigs
      :value: None


      saturationConfigs dataclass which stores the keywords from the SATURATION section of the config file.


   .. py:attribute:: phasecurves
      :type:  phasecurvesConfigs
      :value: None


      phasecurveConfigs dataclass which stores the keywords from the PHASECURVES section of the config file.


   .. py:attribute:: fov
      :type:  fovConfigs
      :value: None


      fovConfigs dataclass which stores the keywords from the FOV section of the config file.


   .. py:attribute:: fadingfunction
      :type:  fadingfunctionConfigs
      :value: None


      fadingfunctionConfigs dataclass which stores the keywords from the FADINGFUNCTION section of the config file.


   .. py:attribute:: linkingfilter
      :type:  linkingfilterConfigs
      :value: None


      linkingfilterConfigs dataclass which stores the keywords from the LINKINGFILTER section of the config file.


   .. py:attribute:: output
      :type:  outputConfigs
      :value: None


      outputConfigs dataclass which stores the keywords from the OUTPUT section of the config file.


   .. py:attribute:: lightcurve
      :type:  lightcurveConfigs
      :value: None


      lightcurveConfigs dataclass which stores the keywords from the LIGHTCURVE section of the config file.


   .. py:attribute:: activity
      :type:  activityConfigs
      :value: None


      activityConfigs dataclass which stores the keywords from the ACTIVITY section of the config file.


   .. py:attribute:: expert
      :type:  expertConfigs
      :value: None


      expertConfigs dataclass which stores the keywords from the EXPERT section of the config file.


   .. py:attribute:: auxiliary
      :type:  auxiliaryConfigs
      :value: None


      auxiliaryConfigs dataclass which stores the keywords from the AUXILIARY section of the config file.


   .. py:attribute:: pplogger
      :type:  None
      :value: None


      The Python logger instance


   .. py:attribute:: survey_name
      :type:  str
      :value: ''


      The name of the survey.


   .. py:method:: _read_configs_from_object(config_object)

      function that populates the class attributes

      :param config_object: ConfigParser object that has the config file read into it
      :type config_object: ConfigParser object

      :rtype: None



.. py:function:: check_key_exists(value, key_name)

   Checks to confirm that a mandatory config file value is present and has been read into the dataclass as truthy. Returns an error if value is falsy

   :param value: value of the config file attribute
   :type value: object attribute
   :param key_name: The key being checked.
   :type key_name: string

   :rtype: None.


.. py:function:: check_key_doesnt_exist(value, key_name, reason)

   Checks to confirm that a config file value is not present and has been read into the dataclass as falsy. Returns an error if value is truthy

   :param value: value of the config file attribute
   :type value: object attribute
   :param key_name: The key being checked.
   :type key_name: string
   :param reason: reason given in the error message on why this value shouldn't be in the config file
   :type reason: string

   :rtype: None.


.. py:function:: cast_as_int(value, key)

   Checks to see if value can be cast as an interger.

   :param value: value of the config file attribute
   :type value: object attribute
   :param key: The key being checked.
   :type key: string

   :rtype: value as an integer


.. py:function:: cast_as_float(value, key)

   Checks to see if value can be cast as a float.

   :param value: value of the config file attribute
   :type value: object attribute
   :param key: The key being checked.
   :type key: string

   :rtype: value as a float


.. py:function:: cast_as_bool(value, key)

   Checks to see if value can be cast as a boolen.

   :param value: value of the config file attribute
   :type value: object attribute
   :param key: The key being checked.
   :type key: string

   :rtype: value as a boolen


.. py:function:: check_value_in_list(value, valuelist, key)

   Checks to see if a config variable is in a list of permissible variables.

   :param value: value of the config file value
   :type value: object attribute
   :param valuelist: list of permissible values for attribute
   :type valuelist: list
   :param key: The key being checked.
   :type key: string

   :rtype: None.


.. py:function:: PPFindFileOrExit(arg_fn, argname)

   Checks to see if a file given by a filename exists. If it doesn't,
   this fails gracefully and exits to the command line.

   :param arg_fn: The filepath/name of the file to be checked.
   :type arg_fn: string
   :param argname: The name of the argument being checked. Used for error message.
   :type argname: string

   :returns: **arg_fn** -- The filepath/name of the file to be checked.
   :rtype: string


.. py:function:: cast_as_bool_or_set_default(value, key, default)

   Checks to see if value can be cast as a boolen and if not set (equals None) gives default bool.

   :param value: value of the config file attribute
   :type value: object attribute
   :param key: The key being checked.
   :type key: string
   :param default: default bool if value is None
   :type default: bool

   :rtype: value as a boolen


.. py:function:: PrintConfigsToLog(sconfigs, cmd_args)

   Prints all the values from the config file and command line to the log.

   :param sconfigs: Dataclass of config file variables.
   :type sconfigs: dataclass
   :param cmd_args: Dictionary of command line arguments.
   :type cmd_args: dictionary

   :rtype: None.


