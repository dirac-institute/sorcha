.. _filters:

Sorcha's Filter Options
========================================

Brightness Limit
-----------------

The saturation limit of the LSST is magnitude 16.0. Anything that is brighter than this cannot be correctly
measured, and so typically it is omitted. 

- **brightLimit = 16.0**

Detection Efficiency
-----------------------


The LSST automatic pipeline is not expected to identify all objects. This will lower the
number of objects detected by a given amount. The number of objects that are not identified is 
set to 5%. 

 - **SSPDetectionEfficiency = 0.95**


Trailing Loss
-----------------


If the object we are observing is fast moving, the signal will be smeared over several pixels. This 
reduces the signal to noise of each pixel. For the LSST this is mostly relevant to NEOs.
Options: True, False

- **trailingLossesOn = False**

.. image:: images/Trail.png
  :width: 400
  :alt: Alternative text
  

Faint Detections
-----------------


Towards fainter magnitudes, the likelihood of detecting an object decreases. This filter determines if a 
faint object is detected depending on the (simulated) seeing and the limiting magnitude given in the pointing
database.



Camera Footprint
-----------------


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


Vignetting
-----------------


Objects that are on the edges of the field of view are dimmer due to vignetting. This filter applies
a model of this from a built-in function.


Linking 
---------------------------
