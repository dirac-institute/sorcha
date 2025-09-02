.. _reporting:

Reporting Issues, Proposing Changes, and Contributing
======================================================

.. tip::
   Is something not working? Have you checked the :ref:`troubleshooting` page to see if your problem is covered there?

.. tip::
   To keep up with the latest ``Sorcha`` updates and annoucements, we recommend signing up for our `google group <https://groups.google.com/g/sorcha>`_.


Contributions are very welcome. If there is a feature or functionality not yet available in ``Sorcha``, we encourage you to propose the feature or share your code with the new enhancements. 

Submitting a GitHub Issue
---------------------------
The best way to get in touch about a bug, suggest enhancements to ``Sorcha``, or recommend changes to the documentation is raise an issue through the `project's GitHub repository <https://github.com/dirac-institute/sorcha/issues>`__. We have a small team working on the project, so please be patient while we get back to you.

Contributing Code
-----------------------------------

We welcome upgrades/bug fixes to the code. This can be done by opening a pull request in the main ``Sorcha`` `GitHub repository <https://github.com/dirac-institute/sorcha>`__. If you have new classes that provide enhanced light curve or activity estimations, we welcome pull requests to the ``Sorcha Add-ons`` `GitHub repository <https://github.com/dirac-institute/sorcha-addons>`__.

You will need to install ``Sorcha`` from the source code via pip in editable development mode as described in the :ref:`dev_mode` page. If you are making a contributio to the ``Sorcha Add-ons`` package,  you will also need to install that in editable development mode via `these instructions <https://sorcha-addons.readthedocs.io/en/latest/installation.html>`__.

.. note::
   If you are planning to submit a pull request with enhancements, please raise a `GitHub issue in the main sorcha repository <https://github.com/dirac-institute/sorcha/issues>`__ first to discuss further with the ``Sorcha`` team.

Running the Unit Tests
~~~~~~~~~~~~~~~~~~~~~~~~~~~

You will need to install ``Sorcha`` from the source code via pip in editable development mode as described in the :ref:`dev_mode` page.

Then in the terminal running::

   pytest

or:: 

   python -m pytest

Modifying the End-to-End Unit Test Comparison Files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you have made significant changes to what ``Sorcha`` outputs by default, then our end-to-end unit tests will need the output files (which we refer to as *the goldens*) updated. We have a script to regenerate these in the correct directory within the sorcha repo. You will need to clone the repo and in the /src/sorcha/utilities/ directory run the ``generateGoldens.py`` script on the command line::

   python generateGoldens.py 

.. danger::
   For most updates to ``Sorcha`` you should **not** have to change the goldens. Change these files with care as they are used to check that sorcha is outputting what they think it should be. 

Contributing to the  Documentation
--------------------------------------

We are very happy to receive feedback on the online documentation through the `project's GitHub repository <https://github.com/dirac-institute/sorcha/issues>`_. Beyond pointing out typos and small changes through issues, we welcome pull requests on the `sphinx <https://www.sphinx-doc.org/en/master/#user-guides>`_ documentation used here on the readthedocs.

You will need to install the development version of ``Sorcha`` from a clone of the ``Sorcha`` repository and other associated packages for documentation.  See the our  :ref:`dev_mode` instructions for further details. 


If you move to the docs directory (cd sorcha/docs/), edit the .rst files, and run::

   make html

You will find the generated index.html file in  ../_readthedocs/html/ 
