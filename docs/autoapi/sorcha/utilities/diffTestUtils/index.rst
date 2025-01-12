sorcha.utilities.diffTestUtils
==============================

.. py:module:: sorcha.utilities.diffTestUtils


Attributes
----------

.. autoapisummary::

   sorcha.utilities.diffTestUtils.BASELINE_ARGS
   sorcha.utilities.diffTestUtils.WITH_EPHEMERIS_ARGS
   sorcha.utilities.diffTestUtils.CHUNKED_ARGS
   sorcha.utilities.diffTestUtils.UNCHUNKED_ARGS
   sorcha.utilities.diffTestUtils.VERIFICATION_TRUTH


Functions
---------

.. autoapisummary::

   sorcha.utilities.diffTestUtils.compare_result_files
   sorcha.utilities.diffTestUtils.override_seed_and_run


Module Contents
---------------

.. py:function:: compare_result_files(test_output, golden_output)

   Compare the results in test_output to those in golden_output.

   :param test_output: The path and file name of the test results.
   :type test_output: string
   :param golden_output: The path and file name of the golden set results.
   :type golden_output: string

   :returns: Indicates whether the results are the same.
   :rtype: bool


.. py:data:: BASELINE_ARGS

.. py:data:: WITH_EPHEMERIS_ARGS

.. py:data:: CHUNKED_ARGS

.. py:data:: UNCHUNKED_ARGS

.. py:data:: VERIFICATION_TRUTH

.. py:function:: override_seed_and_run(outpath, arg_set='baseline')

   Run the full Rubin sim on the demo data and a fixed seed.

   WARNING: Never use a fixed seed for scientific analysis. This is
   for testing purposes only.

   :param outpath: The path for the output files.
   :type outpath: string
   :param arg_set: set of arguments for setting up the run. Options: "baseline" or "with_ephemeris".
                   "baseline"" run does not ephemeris generation. "with_ephemeeris" is a full end to end run
                   of all main components of sorcha.
                   Default = "baseline"
   :type arg_set: string, optional


