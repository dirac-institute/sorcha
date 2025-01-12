sorcha.utilities.sorcha_copy_configs
====================================

.. py:module:: sorcha.utilities.sorcha_copy_configs


Functions
---------

.. autoapisummary::

   sorcha.utilities.sorcha_copy_configs.copy_demo_configs


Module Contents
---------------

.. py:function:: copy_demo_configs(copy_location, which_configs, force_overwrite)

   Copies the example Sorcha configuration files to a user-specified location.

   :param copy_location: String containing the filepath of the location to which the configuration files should be copied.
   :type copy_location: string
   :param which_configs: String indicating which configuration files to retrieve. Should be "rubin", "demo" or "all".
   :type which_configs: string
   :param force_overwrite: Flag for determining whether existing files should be overwritten.
   :type force_overwrite: boolean

   :rtype: None


