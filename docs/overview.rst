Overview
========
The SSSC Science Roadmap (Schwamb et al. 2018) highlights probing the orbital distributions, size/brightness distributions, 
and surface colors as the top LSST science priorities in each of the Solar System small body populations. In order to do detailed 
population studies on the orbital properties and physical characteristics of the various Solar System small body reservoirs, one
requires being able to account for all the survey biases (the complex and often intertwined detection biases – brightness limits,
pointing, cadence, on-sky motion limits, software detection efficiencies) in one’s discovery survey (see Lawler et al. 2018 for 
a more detailed discussion). A survey simulator takes an input model small body population and outputs (biases the population to)
what Rubin Observatory should have detected by utilizing the LSST pointing history, observation metadata, and Rubin Observatory 
Solar System Processing pipeline’s detection efficiency.


The Survey Simulator Post Processing code is designed to compliment LSST observations, as a way to study
solar system object population statistics. The user is able to create synthetic population statistics and 
run them through the survey simulator, which applies the specific observational biases from the LSST. In 
this way, predicted models can be compared more accurately to what LSST observes. The survey simulator code 
takes a series of object parameter inputs and applies a range of filters, which affect the observed LSST data.
An overview of the inputs and filters are given in this section. 

While this survey simulator has been built with LSST in mind, it has been written in a way which allows
for customisation and can be applied in a general manner. The filters which can be applied can be switched
on or off depending on the population in question and users can easily write and insert their own filters 
for their specific needs.

The basic pipeline overview can be seen below. The user generates a population with a set of orbits. This
orbital parameter file is processed by Objects in Field (or any other orbital code) with respect to the LSST 
pointing database, before being passed into the survey simulator. Here the user can alter the configuration
file to apply relevant filters, which account for the observational biases in LSST. An optional cometary 
parameter file can also be added here.

.. image:: images/OIF.png
  :width: 800
  :alt: Alternative text
  
  