sorcha.modules.PPModuleRNG
==========================

.. py:module:: sorcha.modules.PPModuleRNG


Classes
-------

.. autoapisummary::

   sorcha.modules.PPModuleRNG.PerModuleRNG


Module Contents
---------------

.. py:class:: PerModuleRNG(base_seed, pplogger=None)

   A collection of per-module random number generators.


   .. py:attribute:: _base_seed


   .. py:attribute:: _rngs


   .. py:attribute:: pplogger
      :value: None



   .. py:method:: getModuleRNG(module_name)

      Return a random number generator that is based on a base seed
      and the current module name.

      :param module_name: The name of the module
      :type module_name: string

      :returns: **rng** -- The random number generator.
      :rtype: numpy Generator



