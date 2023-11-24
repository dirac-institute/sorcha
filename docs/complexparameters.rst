Incorporating Rotational Light Curves and Active Objects 
==========================================================
Sorcha has the ability user provided functions though python classes that augment/change the apparent brightness calculations for the synthetic Solar System objects. Any values required as input for these calculations, must be provided in the separate :ref:`CPP` file as input. 

We have base example classes that the user can take and modify to whatever your need is. Within the Sorcha :ref:`configs`, the user would then specify when class would use and provide the required :ref:`CPP` file on the command line.  We also have 2 pre-made example classes that can augment the calculated apparent magnitude of each synthetic object, One for handling cometary activity as a function of heliocentric distance and one that applies rotational light curves to the synthetic objects. In both cases, any derived class must inherit from the corresponding base class and follow its API, to ensure that sorcha knows how to find and use your class.

Cometary Activity or Simulating Other Active Objects
--------------------------------------------------------

.. literalinclude:: ../src/sorcha/activity/base_activity.py
   :language: python


Rotational Light Curve Effects
-----------------------------------

The base lightcurve class is `AbstractLightCurve <https://github.com/dirac-institute/sorcha/blob/04baa79a7d67e1647b839a2d3880d8bfd9ce4624/src/sorcha/lightcurves/base_lightcurve.py#L10>`_ (see below). Inside the `sorcha addons  GitHub repository <https://github.com/dirac-institute/sorcha-addons>`_, we provide a simple example implementation where the apparent magnitude of the object (that is, the magnitude after all geometric effects have been taken into account), has a sinusoidal term added to it. To use this function, in the :ref:`CPP` file, the user must provide a light curve amplitude (`LCA`), corresponding to half the peak-to-peak amplitude for the magnitude changes, a period `Period`, and a reference time `Time0` where the light curve is at 0 - if these are not provided, the software will produce an error message. Despite being simple, that implementation shows all the class methods that need to be implemented for a custom light curve function.

.. literalinclude:: ../src/sorcha/lightcurves/base_lightcurve.py
   :language: python

