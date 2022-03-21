Inputs
==========

There are a set of utilities that are installed alongside the survey simulator. These are configuration
file generators, which generate a set of config files for use with both OIF and the survey simulator.
An overview of the possible inputs for these config file generators is given below::

Objects in Field Configuration File
------------------------------------
The first config file generator works alongside OIF. By typing in the command::

   makeConfigOIF --help

It returns the following::

  usage: makeConfigOIF [-h] [-no NO] [-ndays NDAYS] [-day1 DAY1] [-prefix PREFIX] [-camerafov CAMERAFOV] [-inputformat INPUTFORMAT] [-cache CACHE] [-mpcfile MPCFILE][-spkstep SPKSTEP] [-telescope TELESCOPE] o pointing

This gives an overview of the arguments accepted by makeCConfigOIF. The two arguments that are required to generate an OIF config file are the name of a file containing 
the orbits and the name of the pointing database being used. Each of the other parameters are optional, 
but we will describe them here:



+--------------------------+----------------------------------------------------------------------------------------------------+
| Argument                 | Description                                                                                        |
+==========================+====================================================================================================+
| o                        | Orbits file                                                                                        |
+--------------------------+----------------------------------------------------------------------------------------------------+
| pointing                 | pointing database                                                                                  |
+--------------------------+----------------------------------------------------------------------------------------------------+
| -no NO                   | Number of orbits per config file, -1 runs all the orbits in one config file. Default value = 300   | 
+--------------------------+----------------------------------------------------------------------------------------------------+
| -ndays NDAYS             | Number of days in survey to run, -1 runs entire survey. Default value = -1                         | 
+--------------------------+----------------------------------------------------------------------------------------------------+
| -day1 DAY1               | First day in survey to run. Default value = 1                                                      | 
+--------------------------+----------------------------------------------------------------------------------------------------+
| -prefix PREFIX           | Config file name prefix, Default value is an empty string                                          | 
+--------------------------+----------------------------------------------------------------------------------------------------+
| -camerafov CAMERAFOV     | Path and file name of the camera fov. Default value = instrument_polygon.dat                       | 
+--------------------------+----------------------------------------------------------------------------------------------------+
| -inputformat INPUTFORMAT | Input format (CSV or whitespace). Default value = whitespace                                       | 
+--------------------------+----------------------------------------------------------------------------------------------------+
| -cache CACHE             | Base cache directory name. Default value = _cache                                                  | 
+--------------------------+----------------------------------------------------------------------------------------------------+
| -mpcfile MPCFILE         | Name of the file containing the MPC observatory codes. Default value = obslist.dat                 | 
+--------------------------+----------------------------------------------------------------------------------------------------+
| -spkstep SPKSTEP         | Integration step in days. Default value = 30                                                       | 
+--------------------------+----------------------------------------------------------------------------------------------------+
| -telescope TELESCOPE     | Observatory MPC Code. Default value = I11 (Gemini South to be changed to Rubin Observatory)        |
+--------------------------+----------------------------------------------------------------------------------------------------+


The most basic way to use the OIF config file generator is to run::

  makeConfigOIF ./data/test/testorb.des ./data/test/baseline_10yrs_10klines.db

Where testorb.des is the orbit file and baseline_10yrs_10klines.db is the pointing database. This will generate 
a basic config file, filled mostly with default values. These values can be tweaked by running something like::

  makeConfigOIF ./data/test/testorb.des ./data/test/baseline_10yrs_10klines.db -ndays 10
  
Which will generate a config file with the number of days in the survey set to 10.




Survey Simulator Configuration File 
-------------------------------------
Typing in the command::

   makeConfigPP --help

Returns the following::

  usage: makeConfigPP [-h] [--objecttype OBJECTTYPE] [-pointingdatabase POINTINGDATABASE] [--footprintpath FOOTPRINTPATH] [--pointingformat POINTINGFORMAT]
  [--auxformat AUXFORMAT] [--mainfilter MAINFILTER] [--othercolours OTHERCOLOURS] [--resfilter RESFILTER] [--phasefunction PHASEFUNCTION]
  [--trailinglosseson] [--cameramodel CAMERAMODEL] [--detectionefficiency DETECTIONEFFICIENCY] [--fillfactor FILLFACTOR] [--mintracklet MINTRACKLET]
  [--notracklets NOTRACKLETS] [--trackletinterval TRACKLETINTERVAL] [--brightlimit BRIGHTLIMIT] [--insepthreshold INSEPTHRESHOLD] [--outpath OUTPATH]
  [--outfilestem OUTFILESTEM] [--outputformat OUTPUTFORMAT] [--separatelycsv] [--sizeserialchunk SIZESERIALCHUNK]
  filename

The only required argument is the filename, which is the location in which you want to store the config file. Each other argument is optional.
They are described as follows:

+------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Argument                                                                     | Description                                                                                                                                                                                                                                                          |
+==============================================================================+======================================================================================================================================================================================================================================================================+
| filename                                                                     | The pathway where you want to store the configuration file                                                                                                                                                                                                           |
+------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| --objecttype OBJECTTYPE, -obj OBJECTTYPE                                     | Type of object: asteroid or comet. Default is "asteroid".                                                                                                                                                                                                            |
+------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| --pointingdatabase POINTINGDATABASE, -inpt POINTINGDATABASE                  | Path to pointing database. Default is "./data/test/baseline_10yrs_10klines.db".                                                                                                                                                                                      |
+------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| --footprintpath FOOTPRINTPATH, -infoot FOOTPRINTPATH                         | Path to camera footprint file. Default is "./data/detectors_corners.csv".                                                                                                                                                                                            | 
+------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| --pointingformat POINTINGFORMAT, -inptf POINTINGFORMAT                       |  Separator in pointing database: csv, whitespace, hdf5. Default is "whitespace".                                                                                                                                                                                     | 
+------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| --auxformat AUXFORMAT, -inauxf AUXFORMAT                                     | Separator in orbit/colour/brightness/cometary data files: comma or whitespace. Default is "whitespace".                                                                                                                                                              | 
+------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| --mainfilter MAINFILTER, -mfilt MAINFILTER                                   | The main filter in the colour file to which all other colours are compared. Default is "r".                                                                                                                                                                          | 
+------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| --othercolours OTHERCOLOURS, -ofilt OTHERCOLOURS                             | Other colours with respect to the main filter, e.g g-r. Should be given separated by comma. Default is "g-r,i-r,z-r".                                                                                                                                                | 
+------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| --resfilter RESFILTER, -rfilt RESFILTER                                      | resulting filters; main filter, followed by resolved colours, such as, e.g. 'r'+'g-r'='g'. Should be given in the following order: main filter, resolved filters in the same order as respective other colours. Should be separated by comma. Default is "r,g,i,z"   | 
+------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| --phasefunction PHASEFUNCTION, -phfunc PHASEFUNCTION                         | Define the used input phase function. Options: HG, HG1G2, HG12, linear, none. Default is "HG".                                                                                                                                                                       | 
+------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| --trailinglosseson, -tloss                                                   |Switch on trailing losses. Revelant for close-approaching NEOs. Default False.                                                                                                                                                                                        | 
+------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| --cameramodel CAMERAMODEL, -cammod CAMERAMODEL                               | Choose between surface area equivalent or actual camera footprint, including chip gaps. Options: circle, footprint. Default is "footprint".                                                                                                                          | 
+------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| --detectionefficiency DETECTIONEFFICIENCY, -deteff DETECTIONEFFICIENCY       | Which fraction of the detections will the automated solar system processing pipeline recognise? Expects a float. Default is 0.95.                                                                                                                                    |
+------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| --fillfactor FILLFACTOR, -ff FILLFACTOR                                      |  Fraction of detector surface area which contains CCD -- simulates chip gaps. Expects a float. Default is 0.9.                                                                                                                                                       | 
+------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| --mintracklet MINTRACKLET, -mintrk MINTRACKLET                               | How many observations during one night are required to produce a valid tracklet? Expects an int. Default 2.                                                                                                                                                          | 
+------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| --notracklets NOTRACKLETS, -ntrk NOTRACKLETS                                 | How many tracklets are required to classify as a detection? Expects an int. Default 3.                                                                                                                                                                               | 
+------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|  --trackletinterval TRACKLETINTERVAL, -inttrk TRACKLETINTERVAL               | In what amount of time does the aforementioned number of tracklets needs to be discovered to constitute a complete detection? In days. Expects a float. Default 15.0.                                                                                                | 
+------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| --brightlimit BRIGHTLIMIT, -brtlim BRIGHTLIMIT                               | Limit of brightness: detections brighter than this are omitted assuming saturation. Expects a float. Default is 16.0.                                                                                                                                                | 
+------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| --outpath OUTPATH, -out OUTPATH                                              |  Path to output. Default is "./data/out".                                                                                                                                                                                                                            |                                                                                                                                            
+------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| --outfilestem OUTFILESTEM, -outstem OUTFILESTEM                              |  Output file name stem. Default is "hundredcomets"                                                                                                                                                                                                                   | 
+------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| --outputformat OUTPUTFORMAT, -outf OUTPUTFORMAT                              | Output format. Options: csv, sqlite3, hdf5. Default is csv.                                                                                                                                                                                                          |
+------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| --separatelycsv, -sepcsv                                                     | Toggle to write out the CSV file for each object separately. Default is False.                                                                                                                                                                                       | 
+------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| --sizeserialchunk SIZESERIALCHUNK, -chunk SIZESERIALCHUNK                    |  Size of chunk of objects to be processed serially. Default is 10.                                                                                                                                                                                                   | 
+------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

  



Objects in Field
-----------------

**Inputs: Orbits**

The orbital parameter file is used with both Objects in Field and the Survey Simulator Post Processing
code. The orbital parameters can take three formats: **Cometary, Keplarian** and **Cartesian**


- **'COM'** = objID, q, e, inc, Omega, argPeri, tPeri, epoch, H, g, sed_filename


- **'KEP'** = objID, a, e, inc, Omega, argPeri, meanAnomaly, epoch, H, g, sed_filename


- **'CART'** = objID, x, y, z, xdot, ydot, zdot, epoch, H, g, sed_filename



+----------+----------------------------------------------------------------------------------+
| Keyword  | Description                                                                      |
+==========+==================================================================================+
| objID    | Object identifier. Unique identifier for each object withtin the population      |
+----------+----------------------------------------------------------------------------------+
| q        | Perihelion distance  = a*(1-e)                                                   |
+----------+----------------------------------------------------------------------------------+
| e        | Eccentricity                                                                     | 
+----------+----------------------------------------------------------------------------------+
| a        | Semimajor axis                                                                   |
+----------+----------------------------------------------------------------------------------+
| x        |                                                                                  |
+----------+----------------------------------------------------------------------------------+
| y        |                                                                                  |
+----------+----------------------------------------------------------------------------------+
| z        |                                                                                  |
+----------+----------------------------------------------------------------------------------+
| inc      | Inclination                                                                      |
+----------+----------------------------------------------------------------------------------+
| Omega    | Longitude of the ascending node                                                  |
+----------+----------------------------------------------------------------------------------+
| argPeri  | Argument of periapsis                                                            |
+----------+----------------------------------------------------------------------------------+
| tPeri    | Time of periapsis                                                                |
+----------+----------------------------------------------------------------------------------+

.. attention::
   All orbits used should be heliocentric. When using the Survey Simulator Post Processing code the 
   format of the orbits (i.e. Cometary, Keplerian, Cartesian) should remain consistent throughout
   each simulation, i.e. only use one type of coordinate format per run.


Survey Simulator Post Processing Inputs
-------------------------------------------

**Input: Physical Parameters**

The input file for the physical parameters includes information about the objects colour and brightness.

The LSST will survey the sky in six bandpasses. These are **u, g, r, i, z and y**. In the colour file
you can set a main filter which all other colours are compared to.

- **main filter = r**
- **other colours = g-r, i-r, z-r**
- **res filters = r, g, i, z**


The brightness of an atmosphereless body is a function of its phase angle (a). 
Several empirical models exist to predict the brightness, including the HG system (where H is approximately
the brightness at d = 0 and G represents the slope)
For this input, the options are: HG, HG1G2, HG12, linear, none

- **phasefunction = HG**


**Input: Cometary Properties (Optional)**

This is an input file which describes how the object brightness will be augmented from the normal r^4 
brightening as objects move inwards 


**Input: LSST Pointing Database**

This is a file containing the pointing data for the LSST survey. Prior to the start of the survey, this 
data is estimated from up-to-date observation planning and environmental data. This is generated through
the Rubin Observatory scheduler (known as rubin_sim). A description of an early version of this python software can be found in
Delgado et al. (2014) and the open source repository is found at https://github.com/lsst/rubin_sim. 
The output of rubin_sim is a sqlite database containing the pointing history and associated metadata 
of the simulated observation history of LSST. This will be updated with real-life pointing data as 
observations take place.




Filters
-----------------

**Filter: Brightness Limit**

The saturation limit of the LSST is magnitude 16.0. Anything that is brighter than this cannot be correctly
measured, and so typically it is omitted. 

- **brightLimit = 16.0**

**Filter: Detection Efficiency**

The LSST automatic pipeline is not expected to identify all objects. This will lower the
number of objects detected by a given amount. The number of objects that are not identified is 
set to 5%. 

 - **SSPDetectionEfficiency = 0.95**


**Filter: Trailing Loss**

If the object we are observing is fast moving, the signal will be smeared over several pixels. This 
reduces the signal to noise of each pixel. For the LSST this is mostly relevant to NEOs.
Options: True, False

- **trailingLossesOn = False**

.. image:: images/Trail.png
  :width: 400
  :alt: Alternative text
  

**Filter: Faint Detections**

Towards fainter magnitudes, the likelihood of detecting an object decreases. This filter determines if a 
faint object is detected depending on the (simulated) seeing and the limiting magnitude given in the pointing
database.



**Filter: Camera Footprint**

Due to footprint of the LSST detector (see figure below), it is possible that some objects may be lost in
gaps between the chips. This may not be an important factor in some cases, e.g. when observing very fast moving 
objects, so the calculation can be done in two ways.

Surface area: a simpler approach. The fraction of the surface area of a given pointing output (which is 
circular in objectsInField). **Use this if **

Camera footprint: using the LSST camera footprint, including chip gaps, with possibility to “remove” 
entire rafts. The Camera footprint given by a separate data file. **Use this to **

- **cameraModel = footprint**

.. image:: images/Footprint.png
  :width: 400
  :alt: Alternative text
  
.. attention::
   When using the surface area approach, remember to set the value of r to 1.75. When using the 
   camera footprint set r to 2.06. 


**Filter: Vignetting**

Objects that are on the edges of the field of view are dimmer due to vignetting. This filter applies
a model of this from a built-in function.


**Filter: Solar System Processing**
