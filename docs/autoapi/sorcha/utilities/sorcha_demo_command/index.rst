sorcha.utilities.sorcha_demo_command
====================================

.. py:module:: sorcha.utilities.sorcha_demo_command


Functions
---------

.. autoapisummary::

   sorcha.utilities.sorcha_demo_command.get_demo_command
   sorcha.utilities.sorcha_demo_command.print_demo_command


Module Contents
---------------

.. py:function:: get_demo_command()

   Returns the current working version of the Sorcha demo command as a string.
   If the Sorcha run command changes, updating this function will ensure
   associated unit tests pass.

   :param None.:

   :returns: working sorcha demo command
   :rtype: string


.. py:function:: print_demo_command(printall=True)

   Prints the current working version of the Sorcha demo command to the terminal, with
   optional functionality to also tell the user how to copy the demo files.

   :param printall: When True, prints the demo command plus the instructions for copying the demo files.
                    When False, prints the demo command only.
   :type printall: boolean

   :rtype: None.


