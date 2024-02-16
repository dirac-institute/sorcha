.. _reporting:

Reporting Issues, Proposing Changes, and Contributing
======================================================

.. tip::
   Something not working? Have you checked the :ref:`troubleshooting` page to see if your problem is covered there?

Contributions are very welcome. If there is a feature or functionality not yet available in Sorcha, we encourage you to propose the feature or share your code with the new enhancements. 

Submitting a GitHub Issue
---------------------------
The best way to get in touch about a bug, suggest enhancements to Sorcha, or recommend changes to the documentation is raise an issue through the `project's GitHub repository <https://github.com/dirac-institute/sorcha/issues>`_. We have a small team working on the project, so please be patient, while we get back to you.

Contributing Code
-----------------------------------

We welcome upgrades/bug fixes to the code, This can be done by opening a pull request in the `main Sorcha GitHub repository <https://github.com/dirac-institute/sorcha>`_. If you have new classes that provide enhanced light curve or activity estimations, we welcome pull requests to the `Sorcha Community Utils GitHub repository <https://github.com/dirac-institute/sorcha_community_utils>`_.

You will need to install sorcha from the source code via pip in editable mode as described in the :ref:`installation` page.

.. note::
   We recommend that if you are planning to submit a pull request with enhancements to raise a `GitHub issue in the main sorcha repository <https://github.com/dirac-institute/sorcha/issues>`_ first to discuss further before submitting a pull request.


Contributing to the  Documentation
--------------------------------------

We are very happy to receive feedback on the online documentation through the `project's GitHub repository <https://github.com/dirac-institute/sorcha/issues>`_. Beyond pointing out typos and small changes through issues, we welcome pull requests on the `sphinx <https://www.sphinx-doc.org/en/master/#user-guides>`_ documentation used here on the readthedocs.

You will need to install the development version of Sorcha from a clone of the Sorcha repository. See the our  :ref:`dev_mode` instructions for further details. 


If you move to the docs directory (cd sorcha/docs/), edit the .rst files, and run::

   make html

You will find the generated index.html file in  ../_readthedocs/html/ 
