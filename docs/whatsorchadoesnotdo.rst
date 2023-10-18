What Sorcha Does Not Handle
=================================

Here we note the effects that are not currently captured within this survey simulator. With the 
modular nature of the package, it should be straight forward to develop functions to handle these 
in the future. If you want to add any of these features into Sorcha, please check out our 
:ref:`reporting` page.

Here is a short summary of the key effects not accounted for in Sorcha:

- Changing phase curves due to changing viewing angles (impacts some inner Solar System objects)
- Stellar crowding as a function of galactic latitude
- Non-gravitational forces including cometary outgassing or YORP (Yarkovsky–O'Keefe–Radzievskii–Paddack) effect. Although not directly handled,you can input your own ephemeris files that account for these effects if required.  
- Removing simulated objects due to small body collisions and breakup events
- Handling or including false detections/linkages. 


.. seealso::
   We do have methods for  users to easily develop their own functions for adjusting the apparent 
   magnitude of the simulated objects  due to cometary activity, rotational light curves, cometary 
   outbursts, etc. We have some basic functionality already built for simple sinusoidal rotational 
   light curves and cometary activity. Further details can be found  in the
   `sorcha addons <https://sorcha-addons.readthedocs.io/en/latest/?badge=latest>`_.  
