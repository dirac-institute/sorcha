What Sorcha Does Not Handle
=================================

Here we note the effects that are not currently captured within this survey simulator. With the 
modular nature of the package, it should be straightforward to develop functions to handle these 
in the future. If you want to add any of these features into ``Sorcha``, please check out our 
:ref:`reporting` page.

Here is a short summary of the key effects not accounted for in ``Sorcha``:

- Properly simulating the locations of the 16 massive asteroid perturbers in the main belt. Further details can be found :ref:`here<MAP>`.  
- Changing phase curves due to changing viewing angles (impacts some inner Solar System objects)
- Stellar crowding as a function of galactic latitude
- Non-gravitational forces including cometary outgassing or Yarkovsky or YORP (Yarkovsky–O'Keefe–Radzievskii–Paddack) effect. Although not directly handled, you can input your own ephemeris files that account for these effects if required.  
- Properly handling collisions between the planets and the simulated objects 
- Removing simulated objects due to small body collisions and breakup events
- Handling or including false detections/linkages
- Using space-based or moving observatory locations. We currently require an observatory code for a stationary observatory on the Earth with a location that is reported to the Minor Planet Center. 


.. seealso::
   We do have methods for  users to easily develop their own functions for adjusting the apparent 
   magnitude of the simulated objects  due to cometary activity, rotational light curves, cometary 
   outbursts, etc. We have some basic functionality already built for simple sinusoidal rotational 
   light curves and cometary activity. Further details can be found  :ref:`here<addons>`.

.. warning::
  If you simulate the orbits of 16 massive asteroid perturbers listed  :ref:`here<MAP>`, you will get **POOR results** with the internal ``Sorcha`` ephemeris generator because of how the n-body integration is set up. We recommend getting the positions of these asteroids from some other source and inputting them as an external ephemeris file.


