sorcha_cmdline.sorchaargumentparser
===================================

.. py:module:: sorcha_cmdline.sorchaargumentparser


Classes
-------

.. autoapisummary::

   sorcha_cmdline.sorchaargumentparser.SorchaArgumentParser


Module Contents
---------------

.. py:class:: SorchaArgumentParser(*args, **kwargs)

   Bases: :py:obj:`argparse.ArgumentParser`


   A subclass of the argparse.ArgumentParser that adds in a print statement
   to make it clearer how to get detailed help for new users who may not be
   as familiar with linux/unix


   .. py:method:: print_usage(file=None)

      Print a brief description of how the ArgumentParser should be invoked
      on the command line. If file is None, sys.stdout is assumed.


      :param file: Variable length argument list.
      :type file: str or None

      :rtype: None.



