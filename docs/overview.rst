How Sorcha Works
=================

To do detailed population studies on the orbital properties and physical characteristics of the various Solar System small body reservoirs, one must account for all the survey biases (the complex and often intertwined detection biases – brightness limits,
pointing, cadence, on-sky motion limits, software detection efficiencies) in one’s discovery survey (`see Lawler et al. 2018 <https://ui.adsabs.harvard.edu/abs/2018FrASS...5...14L/abstract>`_ for a more detailed discussion). Sorhca is a Solar System survey simulator designed for the `Vera C. Rubin Observatory Legacy Survey of Space and Time (LSST) <https://www.lsst.org/>`_. Sorcha takes an input model small body population and outputs (biases the population to) what Rubin Observatory should have detected by utilizing the LSST pointing history, observation metadata, and the Rubin Solar System Processing (SSP) pipeline’s detection efficiency. 

Overview 
-------------------------------

Sorcha takes a series of inputs as shown in the figure below. 

.. image:: images/survey_simulator_flow_chart.png
  :width: 800
  :alt: An overview of the inputs and outputs for Sorcha


Sorcha works by the user inputting a synthetic Solar System small body population, speecifyigh Sorcha.applies the specific observational biases relevant for ths specific survey. In this way, a synthetic population can be compared to the real survey's discoveries. Sorcha by default uses its own hephemeris generator to take the orbits and propogate them on sky. Sorcha's ephemeris generator is based on ASSIST+REBOUND. If the user prefers ot use a different the user can use any relevant ephemerides generator, using what we have called :ref:`filters<Filters>`.  it has been written in a way which allows
for customisation and can be applied in a general manner. The filters which can be applied can be switched
on or off via a configuration file  depending on the population in question and users can easily write and insert their own filters
for their specific needs.


.. warning::
   We have validated Sorcha with its internal ephemeris generator. If the user chooses to use a different emphemeris engine's calculations as input for Sorcha, the user has the responsibiilty to check the accuracy of this input.
   

Design Philosophy 
----------------------
While Sorcha has been built with LSST in mind, it has been written in a way which allows
for customisation that with some effort could expand to other Solar System discovery surveys. Sorcha is open source and written in a modular way, where each filter has been written as its
own function. We have developed a suite of filters which should cover the majority
of use cases for the LSST, but there is a possibility to adapt the code for the users own goals. This
may come in the form of adding additional filters or by adapting the software for use with another wide-field survey.

.. warning::
  For a wide variety of use cases, the user should be able to use Sorcha straight out of the box. We have designed the software in a modular way to make it easier to adapt and modify Sorcha if needed. As with any open source package, **once the user has made modifications to the code, it is the responsibility of the user to confirm these changes provide an accurate result**. 
   
   
.. note::
   Contributions are very welcome. If there is a feature or functionality not yet available in Sorcha, we encourage you to propose the feature as an issue in the `main Sorcha repository <https://github.com/dirac-institute/survey_simulator_post_processing/issues>`_ or share your code with the new enhancements. Further details can be found on our :ref:`reporting` page.
      

