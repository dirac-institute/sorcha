.. _output:

Outputs
==================

``Sorcha`` outputs:
  * :ref:`Detections File <detections>` (list of all the detections of the input popuation made by the simulated survey
  * (Optional) :ref:`Statistics (Tally) File <statsf>`  that provides a summary overview for the objects from the input population that were ''found'' in the simulated survey
  * (Optional) :ref:`Ephemeris Output <ephem_output>` that provides the output from the :ref:`Ephemeris Generation<ephemeris_gen>`  

.. image:: images/survey_simulator_flow_chart.png
  :width: 800
  :alt: An overview of the inputs and outputs of the Sorcha code.
  :align: center


.. attention::
   Use the **-o (--outfile)** flag with the **sorcha run** command to specify where ``Sorcha`` should be  saving any output and log files (the file path).

.. tip::
   By default ``Sorcha`` will complain if a user attempts to overwrite existing files in the output directory. Users can apply the **-f (--force)** flag to force deletion/overwrite of existing the output file(s).

Output File Formats
----------------------------
The :ref:`configuration file<configs>` keyword output_format in the OUTPUT section allows ``Sorcha`` to output files in CSV, SQLite3 or HDF5 formats.  For example::

   [OUTPUT]
   # The options: csv, sqlite3, hdf5
    output_format = csv
 
.. note::
   If you are outputting to a SQLite3 database, the data will be saved in a table named 'sorcha_results'.

.. warning::
   If you are writing to a HDF5 file that you plan to access using the PyTables library, note that your object IDs cannot begin
   with a number (due to a limitation in PyTables).

.. attention::
   Use the **-t (--stem)** flag on the command line to specify the filename stem for all the ``Sorcha`` output files and logs.

.. _detections:

Detections File
----------------------

``Sorcha`` produces a detections file describing each predicted survey detection of the input small body populations, 
with a row for each predicted detection and a column for each parameter  calculated.


Additionally, the output columns of the detections file  can be set to either "basic" or "all" settings (described below) using the output_columns :ref:`configuration file<configs>` keyword. 

.. _basic:

Basic Output
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The "basic" output includes the columns most relevant to general photometry and detection purposes. This is declared
in the :ref:`configuration file<configs>` like so::

    [OUTPUT]
    output_columns = basic

Detections File: Basic Output Column Names, Formats, and Descriptions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   
+------------------------------------+--------------+----------------------------------------------------------------------------------+
| Keyword                            | Format       | Description                                                                      |
+====================================+==============+==================================================================================+
| ObjID                              | String       | Unique string identifier                                                         |
+------------------------------------+--------------+----------------------------------------------------------------------------------+
| fieldMJD_TAI                       | Float        | MJD (International Atomic Time Modified Julian Date) of the observation          |
+------------------------------------+--------------+----------------------------------------------------------------------------------+
| fieldRA_deg                        | Float        | Right ascension (RA) of the center of the observation pointing (degrees)         | 
+------------------------------------+--------------+----------------------------------------------------------------------------------+
| fieldDec_deg                       | Float        | Declination (Dec) of the center of the observation pointing (degrees)            |
+------------------------------------+--------------+----------------------------------------------------------------------------------+
| RA_deg                             | Float        | Object Right Ascension (RA) (degrees)                                            |
+------------------------------------+--------------+----------------------------------------------------------------------------------+
| Dec_deg                            | Float        | Object Declination (Dec) (degrees)                                               |
+------------------------------------+--------------+----------------------------------------------------------------------------------+
| astrometricSigma_deg               | Float        | Astrometric uncertainty in object (ra, dec) position (degrees)                   |
+------------------------------------+--------------+----------------------------------------------------------------------------------+
| optFilter                          | String       | Filter (band) for this observation (ugrizy)                                      |
+------------------------------------+--------------+----------------------------------------------------------------------------------+
| trailedSourceMag                   | Float        | Observed apparent magnitude, fit as a trailed source                             |
+------------------------------------+--------------+----------------------------------------------------------------------------------+
| trailedSourceMagSigma              | Float        | 1-:math:`{\sigma}` uncertainty on trailed source magnitude                       |
+------------------------------------+--------------+----------------------------------------------------------------------------------+
| fiveSigmaDepth_mag                 | Float        | Depth required for a 5-:math:`{\sigma}` detection at this source's location      |
+------------------------------------+--------------+----------------------------------------------------------------------------------+
| phase_deg                          | Float        | The sun-object-observer angle (degrees)                                          |
+------------------------------------+--------------+----------------------------------------------------------------------------------+
| Range_LTC_km                       | Float        | Light-time-corrected object-observer distance (km)                               |
+------------------------------------+--------------+----------------------------------------------------------------------------------+
| RangeRate_LTC_km_s                 | Float        | Light-time-corrected rate of change of the object-observer distance (km/s)       |
+------------------------------------+--------------+----------------------------------------------------------------------------------+
| Obj_Sun_LTC_km                     | Float        | Object-sun light-time-corrected distance (km)                                    |
+------------------------------------+--------------+----------------------------------------------------------------------------------+

.. note::
   All positions and velocities are in respect to J2000.
   
.. note::
   The **date_linked_MJD** only appears if :ref:`linking filter<linking>` is turned on. The **object_linked** column only appears if the :ref:`linking filter<linking>` is on and **drop_unlinked = False** in the :ref:`configuration file<configs> (the user has requested that detections of unlinked objects not be dropped in the output).


.. warning::
   If you are writing to a HDF5 file that you plan to access using the PyTables library, note that your object IDs cannot begin
   with a number (due to a limitation in PyTables).


Example Detections File in Basic Format
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block::

   ObjID,fieldMJD_TAI,fieldRA_deg,fieldDec_deg,RA_deg,Dec_deg,astrometricSigma_deg,optFilter,trailedSourceMag,trailedSourceMagSigma,fiveSigmaDepth_mag,phase_deg,Range_LTC_km,RangeRate_LTC_km_s,Obj_Sun_LTC_km
   2011_OB60,60225.247167832895,2.8340797698367206,-12.194064864430457,1.9825620351227258,-11.895484307981585,7.4867112566597e-06,i,22.397430358313322,0.06355310419224419,23.811384411034403,0.5514796131072949,5381400132.572322,8.91189502816155,5521397111.153749
   2011_OB60,60225.27094733885,2.8340797698367206,-12.194064864430457,1.9820733099821837,-11.895712910186568,1.970228013144157e-05,z,22.460227240263052,0.13963007732177396,22.882545620891758,0.5519774373107185,5381418504.312244,8.970786995836564,5521396245.784194
   2011_OB60,60225.28270233429,2.8340797698367206,-12.194064864430457,1.9818659905929508,-11.895814828402601,1.3684499193740731e-05,z,22.53660697139078,0.11795137669248643,23.08084637194619,0.5522233482014428,5381427629.198054,8.997821199753972,5521395818.016169
   2011_OB60,60227.24471872862,1.830365601304555,-10.653419743409385,1.9444189752160241,-11.911537564591345,1.2466492192790164e-05,r,22.51906829448326,0.07307916451539384,23.764317867665323,0.5935019031565647,5382985829.82119,9.8900048055957,5521324456.507859
   2011_OB60,60227.26843110208,1.830365601304555,-10.653419743409385,1.9439540758655767,-11.911714297468937,1.0506087754733871e-05,i,22.46544565090926,0.07951187390559222,23.55633186666243,0.5940086408462589,5383006152.782514,9.947927989901528,5521323594.47957
   2011_OB60,60229.23294578834,1.7408953022743148,-11.367447303472217,1.9068694316324013,-11.926897607683264,6.448960302837116e-06,g,23.140501955036218,0.050129668307068526,24.689706821972628,0.6359862246231764,5384729639.820431,10.83405865998129,5521252216.560329
   2011_OB60,60229.25681096732,1.7408953022743148,-11.367447303472217,1.9064220778352592,-11.927086784963755,1.1882851203406536e-05,r,22.612408442214235,0.07164675338559678,23.793181284412043,0.6365024755814216,5384752041.250169,10.893584442112983,5521251349.911665
   2011_OB60,60230.18746404967,2.7692539237126224,-11.336818754683701,1.889048916261686,-11.934078257963817,5.321102892399358e-06,r,22.65756207818313,0.043887401062701954,24.36853846041664,0.656511920586929,5385624478.812803,11.19259941049343,5521217562.0051365
   2010_TU149,60230.2013547434,15.887030292262942,2.610528423589063,16.290872685024397,3.366320258497593,3.317636137485369e-06,r,21.073976986836836,0.0175955975012035,24.304131138512204,2.7059212412059983,95234455.08950086,-19.59908790043077,244356465.5755924
   2011_OB60,60230.21124082722,2.7692539237126224,-11.336818754683701,1.8885945451311272,-11.93423196825781,7.4281493616584545e-06,i,22.38771848485939,0.06317500696644751,23.83261335450819,0.6570289187575631,5385647540.167239,11.25923211162477,5521216699.0213375
   2010_TU149,60230.22511697796,15.887030292262942,2.610528423589063,16.273200569421988,3.358882710303584,3.93383422696979e-06,i,20.849349008832156,0.023711054681634577,23.68081053978629,2.723994416598135,95194288.60276434,-19.527216320319525,244312929.4142877


.. _full:

Full Output
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The 'all' output option includes all columns from the basic output, as well as those relevant to ephemeris generation for each 
predicted detection, and some of the input orbital and physical parameters of each simulated object. All columns within the pandas databframe at the end of the ``Sorcha`` run are written out.  This is declared in the :ref:`configuration file<configs>` like so::

    [OUTPUT]
    output_columns = all

Detections File: Full Output Column Names, Formats, and Descriptions 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| Keyword                            | Format       | Description                                                                                              |
+====================================+==============+==========================================================================================================+
| ObjID                              | String       | Unique string identifier                                                                                 |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| fieldId                            | Int          | Integer identifier of the observation                                                                    |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| fieldMJD_TAI                       | Float        | MJD (International Atomic Time Modified Julian Date) of the observation                                  |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| fieldJD_TDB                        | Float        | JD (Barycentric Julian Date) of the observation                                                          |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| Range_LTC_km                       | Float        | Light-time-corrected object-observer distance (km)                                                       |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| RangeRate_LTC_km_s                 | Float        | Light-time-corrected rate of change of the object-observer distance (km/s)                               |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| RA_true_deg                        | Float        | Calculated value of object right ascension unadjusted for astrometric uncertainty (degrees)              |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| RARateCosDec_deg_day               | Float        | Object right ascension rate of motion (deg/day)                                                          |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| Dec_true_deg                       | Float        | Calculated value of object declination unadjusted for astrometric uncertainty  (degrees)                 |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| DecRate_deg_day                    | Float        | Object declination rate of motion (deg/day)                                                              |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| Obj_Sun_x_LTC_km                   | Float        | Heliocentric object-sun light-time-corrected Cartesian x distance (km)                                   |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| Obj_Sun_y_LTC_km                   | Float        | Heliocentric object-sun light-time-corrected Cartesian y distance (km)                                   |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| Obj_Sun_x_LTC_km                   | Float        | Heliocentric object-sun light-time-corrected Cartesian z distance (km)                                   |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| Obj_Sun_vx_LTC_km_s                | Float        | Heliocentric object-sun light-time-corrected Cartesian x velocity (km/s)                                 |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| Obj_Sun_vy_LTC_km_s                | Float        | Heliocentric object-sun light-time-corrected Cartesian y velocity (km/s)                                 |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| Obj_Sun_vz_LTC_km_s                | Float        | Heliocentric object-sun light-time-corrected Cartesian z velocity (km/s)                                 |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| Obj_Sun_x_km                       | Float        | Heliocentric object-sun Cartesian x distance (km)                                                        |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| Obj_Sun_y_km                       | Float        | Heliocentric object-sun Cartesian y distance (km)                                                        |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| Obj_Sun_x_km                       | Float        | Heliocentric object-sun Cartesian z distance (km)                                                        |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| Obj_Sun_vx_km_s                    | Float        | Heliocentric object-sun Cartesian x velocity (km/s)                                                      |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| Obj_Sun_vy_km_s                    | Float        | Heliocentric object-sun Cartesian y velocity (km/s)                                                      |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| Obj_Sun_vz_km_s                    | Float        | Heliocentric object-sun Cartesian z velocity (km/s)                                                      |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| phase_deg                          | Float        | The sun-object-observer angle (degrees)                                                                  |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| *Orbital parameters*               | Float        | Specified input orbits in provided format (KEP, COM, CART, etc.)                                         |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| epochMJD_TDB                       | Float        | Epoch of orbit (MJD) in Barycentric Dynamical Time                                                       |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| FORMAT                             | Float        | Orbit format string (COM for heliocentric, BCOM for barycentric, KEP for Keplerian, CART for Cartesian)  |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| H_filter                           | Float        | Predicted measurement of absolute magnitude in the corresponding filter                                  |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| *Phase parameters*                 | Float        | (If specified) Phase curve parameter(s) for all filters (G12, G1 & G2, or :math:`{\beta}`)               |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| visitTime                          | Float        | Total length of time for a visit (seconds)                                                               |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| visitExposureTime                  | Float        | Total exposure time for a visit (seconds)                                                                |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| optFilter                          | String       | Filter (band) for this observation (ugrizy)                                                              |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| seeingFwhmGeom_arcsec              | Float        | Geometric full-width half-maximum for the field (arcsec)                                                 |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| seeingFwhmEff_arcsec               | Float        | Effective full-width half-maximum for the field (arcsec)                                                 |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| fieldFiveSigmaDepth_mag            | Float        | 5-:math:`{\sigma}` limiting magnitude at the centre of the field of view                                 |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| fieldRA_deg                        | Float        | Right ascension (RA) of the center of the observation pointing (degrees)                                 | 
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| fieldDec_deg                       | Float        | Declination (Dec) of the center of the observation pointing (degrees)                                    |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| fieldRotSkyPos_deg                 | Float        | Angle of the field y-axis and celestial north, oriented towards increasing right ascension               |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| H_{main filter}                    | Float        | Absolute magnitude in the specified main filter                                                          |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| trailedSourceMagTrue               | Float        | Observed apparent magnitude, fit as a trailed source, not adjusted for photometric uncertainty           |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| PSFMagTrue                         | Float        | Observed PSF magnitude, fit as a trailed source, not adjusted for photometric uncertainty                |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| fiveSigmaDepth_mag                 | Float        | 5-:math:`{\sigma}` limting magnitude at the location of the object on the focal plane                    |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| astrometricSigma_deg               | Float        | Astrometric uncertainty in object (ra, dec) position (degrees)                                           |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| trailedSourceMagSigma              | Float        | 1-:math:`{\sigma}` uncertainty on trailed source magnitude                                               |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| SNR                                | Float        | Predicted signal-to-noise ratio of detection                                                             |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| PSFMagSigma                        | Float        | 1-:math:`{\sigma}` uncertainty on PSF magnitude                                                          |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| trailedSourceMag                   | Float        | Observed apparent magnitude, fit as a trailed source                                                     |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| PSFMag                             | Float        | Observed apparent magnitude, fit with a point spread function                                            |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| RA_deg                             | Float        | Measured object Right Ascension (RA) (degrees)                                                           |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| Dec_deg                            | Float        | Measured object Declination (Dec) (degrees)                                                              |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| detectorID                         | Float        | Identifier of the detector covering the observation                                                      |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| Obj_Sun_LTC_km                     | Float        | Object-sun light-time-corrected distance (km)                                                            |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| object_linked                      | Boolean      | True/False whether the object passed the linking filter. See note below                                  |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| date_linked_MJD                    | Float        | MJD (TAI) Date the object was linked (if it was linked) See note below                                   |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+

.. note::
   If the user has specified **drop_unlinked = False** in the :ref:`configuration file<configs>`, the object_linked column will only contain TRUE. To see outputs for unlinked objects set **drop_unlinked = False**.

.. note::
   All positions, positions, and velocities are in respect to J2000.

.. note::
   All columns in the complete physical parameters file will also be included in the full output. 


.. warning::
   If you are writing to a HDF5 file that you plan to access using the PyTables library, note that your object IDs cannot begin
   with a number (due to a limitation in PyTables).

Optional  Outputs
----------------------

.. _statsf:
   
Statistics (Tally) File
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
``Sorcha`` can also output a statistics or "tally" file (if specified uisng the **--st flag)  which contains an overview of the ``Sorcha`` output for each object and filter. Minimally, this
file lists the number of observations for each object in each filter, along with the minimum, maximum and median apparent magnitude and the minimum and maximum
phase angle. If the :ref:`linking filter<linking>` is on, this file also contains information on when the object was linked by SSP.


.. attention::
   Use the **-st** flag on the command line to initialize ``Sorcha`` to generate the statistics file and specify the file stem for the resulting file.


Statistics (Tally) File Column Names, Formats, and Descriptions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| Keyword                            | Format       | Description                                                                                              |
+====================================+==============+==========================================================================================================+
| ObjID                              | String       | Unique string identifier                                                                                 |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| optFilter                          | String       | Filter (band) (ugrizy)                                                                                   |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| number_obs                         | Integer      | Number of observations for this object in this filter                                                    |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| min_apparent_mag                   | Float        | Minimum calculated apparent magnitude for this object in this filter                                     |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| max_apparent_mag                   | Float        | Maximum calculated apparent magnitude for this object in this filter                                     |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| median_apparent_mag                | Float        | Median calculated apparent magnitude for this object in this filter                                      |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| min_phase                          | Float        | Minimum calculated phase angle for this object in this filter (degrees)                                  |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| min_phase                          | Float        | Maximum calculated phase angle for this object in this filter (degrees)                                  |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| object_linked                      | Boolean      | True/False whether the object was linked by SSP (only included if linking is on)                         |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| date_linked_MJD                    | Float        | Date the object was linked (if it was linked) in MJD (only included if linking is on)                    |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+

.. _ephem_output:
  
Ephemeris Output
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Optionally (with the **--ew (--ephem-write)** flag set at the command line), an ephemeris file of all detections near the
field can be generated to a separate file, which can then be provided back to ``Sorcha`` as an optional external ephemeris file with the **--er (--ephem-read)** flag.
More information can be found on this functionality in the :ref:`Ephemeris Generation<ephemeris_gen>` section of the documentation.

The format of the outputted ephemeris file is controlled by the **eph_format** configuration keyword in the Inputs section of the :ref:`configuration file<configs>` ::

   [INPUT]
   ephemerides_type = external
   eph_format = csv

Detections File: Full Output Column Names, Formats, and Descriptions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ObjID,FieldID,fieldMJD_TAI,fieldJD_TDB,Range_LTC_km,RangeRate_LTC_km_s,RA_deg,RARateCosDec_deg_day,Dec_deg,DecRate_deg_day,Obj_Sun_x_LTC_km,Obj_Sun_y_LTC_km,Obj_Sun_z_LTC_km,Obj_Sun_vx_LTC_km_s,Obj_Sun_vy_LTC_km_s,Obj_Sun_vz_LTC_km_s,Obs_Sun_x_km,Obs_Sun_y_km,Obs_Sun_z_km,Obs_Sun_vx_km_s,Obs_Sun_vy_km_s,Obs_Sun_vz_km_s,phase_deg

+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| Keyword                            | Format       | Description                                                                                              |
+====================================+==============+==========================================================================================================+
| ObjID                              | String       | Unique string identifier                                                                                 |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| fieldId                            | Int          | Integer identifier of the observation                                                                    |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| fieldMJD_TAI                       | Float        | MJD (International Atomic Time Modified Julian Date) of the observation                                  |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| fieldJD_TDB                        | Float        | JD (Barycentric Julian Date) of the observation                                                          |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| Range_LTC_km                       | Float        | Light-time-corrected object-observer distance (km)                                                       |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| RangeRate_LTC_km_s                 | Float        | Light-time-corrected rate of change of the object-observer distance (km/s)                               |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| RA_deg                             | Float        | Calculated value of object right ascension unadjusted for astrometric uncertainty (degrees)              |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| RARateCosDec_deg_day               | Float        | Object right ascension rate of motion (deg/day)                                                          |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| Dec_deg                            | Float        | Calculated value of object declination unadjusted for astrometric uncertainty  (degrees)                 |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| DecRate_deg_day                    | Float        | Object declination rate of motion (deg/day)                                                              |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| Obj_Sun_x_LTC_km                   | Float        | Heliocentric object-sun light-time-corrected Cartesian x distance (km)                                   |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| Obj_Sun_y_LTC_km                   | Float        | Heliocentric object-sun light-time-corrected Cartesian y distance (km)                                   |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| Obj_Sun_x_LTC_km                   | Float        | Heliocentric object-sun light-time-corrected Cartesian z distance (km)                                   |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| Obj_Sun_vx_LTC_km_s                | Float        | Heliocentric object-sun light-time-corrected Cartesian x velocity (km/s)                                 |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| Obj_Sun_vy_LTC_km_s                | Float        | Heliocentric object-sun light-time-corrected Cartesian y velocity (km/s)                                 |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| Obj_Sun_vz_LTC_km_s                | Float        | Heliocentric object-sun light-time-corrected Cartesian z velocity (km/s)                                 |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| Obj_Sun_x_km                       | Float        | Heliocentric object-sun Cartesian x distance (km)                                                        |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| Obj_Sun_y_km                       | Float        | Heliocentric object-sun Cartesian y distance (km)                                                        |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| Obj_Sun_x_km                       | Float        | Heliocentric object-sun Cartesian z distance (km)                                                        |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| Obj_Sun_vx_km_s                    | Float        | Heliocentric object-sun Cartesian x velocity (km/s)                                                      |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| Obj_Sun_vy_km_s                    | Float        | Heliocentric object-sun Cartesian y velocity (km/s)                                                      |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| Obj_Sun_vz_km_s                    | Float        | Heliocentric object-sun Cartesian z velocity (km/s)                                                      |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+
| phase_deg                          | Float        | The sun-object-observer angle (degrees)                                                                  |
+------------------------------------+--------------+----------------------------------------------------------------------------------------------------------+

.. note::
   All positions, positions, and velocities are in respect to J2000.

.. note::
   All columns in the comple physical parameters file will also be included in the full output.

.. attention::
   Users should note that output produced by reading in a previously generated ephemeris file will be in a different order than the output produced when running the ephemeris generator within ``Sorcha``. This is simply a side-effect of how  ``Sorcha`` reads in ephemeris files and does not affect the actual content of the output.

.. tip::
   If instead you want to know which of the input small body population lands in the survey observations with an estimate of their apparent magnitude wihtout applying any other cuts or filters on the detections (not including discovery efficiency and linking effects), you can use/adapt the :ref:`known_config` example :ref:`configs`.

