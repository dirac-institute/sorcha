Incorporating Rotational Light Curves and Active Objects 
==========================================================
Sorcha has the ability user provided functions though python classes that augmnent/change the apparent brightness calculations for the synthetic Solar System objects. Any values required as input for these calculations, must be provided in the separate :ref:`CPP` file as input. 

We have base example classes that the user can take and modify to whatever your need is. Within the Sorcha :ref:`configs`, the user would then specify when class would use and provide the required complex physical parameters file on the command line.  We also have 2 pre-made example classes that can augment the calculated apparent magnitude of each synthetic object, One for handling cometary activity as a function of heliocentric distance and one that applies rotational light curves to the synthetic objects. 

Cometary Activity or Simulating Other Active Objects
--------------------------------------------------------

Rotational Light Curve Effects
-----------------------------------
