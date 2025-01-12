sorcha_cmdline.init
===================

.. py:module:: sorcha_cmdline.init


Functions
---------

.. autoapisummary::

   sorcha_cmdline.init.parse_file_selection
   sorcha_cmdline.init.execute
   sorcha_cmdline.init.main


Module Contents
---------------

.. py:function:: parse_file_selection(file_select)

   Turns the number entered by the user at the command line into a string
   prompt. Also performs error handling.

   :param file_select: Integer entered by the user at command line.
   :type file_select: int

   :returns: **which_configs** -- String indicating which configuration files to retrieve. Should be "rubin", "demo" or "all".
   :rtype: string


.. py:function:: execute(args)

.. py:function:: main()

