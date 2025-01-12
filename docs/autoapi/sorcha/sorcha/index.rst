sorcha.sorcha
=============

.. py:module:: sorcha.sorcha


Functions
---------

.. autoapisummary::

   sorcha.sorcha.cite
   sorcha.sorcha.mem
   sorcha.sorcha.runLSSTSimulation


Module Contents
---------------

.. py:function:: cite()

   Providing the bibtex, AAS Journals software latex command, and acknowledgement
   statements for Sorcha and the associated packages that power it.

   :param None:

   :rtype: None


.. py:function:: mem(df)

   Memory utility function that returns back how much memory the inputted pandas dataframe is using
   :param df:
   :type df: pandas dataframe

   :returns: **usage**
   :rtype: int


.. py:function:: runLSSTSimulation(args, sconfigs)

   Runs the post processing survey simulator functions that apply a series of
   filters to bias a model Solar System small body population to what the
   Vera C. Rubin Observatory Legacy Survey of Space and Time would observe.

   :param args: dictionary of command-line arguments.
   :type args: dictionary or `sorchaArguments` object
   :param pplogger: The logger to use in this function. If None creates a new one.
                    Default = None
   :type pplogger: logging.Logger, optional
   :param sconfigs: Dataclass of configuration file arguments.
   :type sconfigs: dataclass

   :rtype: None.


