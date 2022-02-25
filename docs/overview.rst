Overview
========

The Survey Simulator Post Processing code is 

.. image:: images/OIF.png
  :width: 800
  :alt: Alternative text
  
  
Inputs
-----------------

**Input: Orbits**

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
   each simulation.


**Input: Colours**

The LSST will survey the sky in six bandpasses. These are **u, g, r, i, z and y**. In the colour file
you can set a main filter which all other colours are compared to.

- **main filter = r**
- **other colours = g-r, i-r, z-r**
- **res filters = r, g, i, z**

**Input: Brightness**

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
data is estimated from up-to-date observation planning and environmental data. This file will be updated with
real-life pointing data as the observations take place.




Filters
-----------------

**Filter: Brightness Limit**

The saturation limit on the LSST is magnitude 16.0. Anything that is brighter than this cannot be correctly
measured, so typically it is omitted. 

- **brightLimit = 16.0**

**Filter: Detection Efficiency**

The LSST automatic pipeline is not expected to identify all relevant objects. This will lower the
number of objects detected by a given amount. 

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
