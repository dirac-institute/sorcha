Complex Physical Parameters
=============================

Cometary Activity
------------------------


.. note::
  The cometary activity file is used by  **Sorcha**.

This is an optional input file which describes how the object apparent magnitude will be augmented from
a standard non-active, atmosphereless body as it moves inwards and outwards towards the Sun. The file can be **white space separated**  or **comma value separated (CSV)** format.


An example of a cometary activity parameter file::

   ObjID afrho1 k
   67P 1552 -3.35


.. warning::

   **When running an instance of Sorcha, either every synthetic planetesimal experiences cometary activity, or none do.** When running simulations of synthetic planetesimals exhibiting cometary activity, **every** object in that simulation must have an entry in the associated cometary activity file.

+-------------+-----------------------------------------------------------------------------------+
| Keyword     | Description                                                                       |
+=============+===================================================================================+
| ObjID       | Object identifier for each synthetic planetesimal simulated (string)              |
+-------------+-----------------------------------------------------------------------------------+
| afrho1      | Afρ, quantity of                                                                  |
|             | `A'Hearn et al. (1984) <https://ui.adsabs.harvard.edu/abs/1984AJ.....89..579A>`_. |
|             | at perihelion (cm). The product of                                                |
|             | albedo, filling factor of grains within the observer field of view, and the       |
|             | linear radius of the field of view at the comet                                   |
+-------------+-----------------------------------------------------------------------------------+
| k           | Dust falling exponential value (dust falling at rh^k)                             |
+-------------+-----------------------------------------------------------------------------------+

.. attention::

   These parameters are only used to adjust the apparent brightness of the synthetic planetesimal. We do not account for non-gravitational effects on the ephemeris.


Rotational Light Curve Effects
-----------------------------------
