---
title: 'cogsworth: A Gala of COSMIC proportions combining binary stellar evolution and galactic dynamics'
tags:
  - Python
  - astronomy
  - binary stellar evolution
  - galactic dynamics
authors:
  - name: Tom Wagg
    orcid: 0000-0001-6147-5761
    affiliation: "1, 2"
  - name: Katelyn Breivik
    orcid: 0000-0001-5228-6598
    affiliation: "3"
  - name: Mathieu Renzo
    orcid: 0000-0002-6718-9472
    affiliation: "4"
  - name: Adrian M. Price-Whelan
    orcid: 0000-0003-0872-7098
    affiliation: "2"
affiliations:
 - name: Department of Astronomy, University of Washington, Seattle, WA, 98195, USA
   index: 1
 - name: Center for Computational Astrophysics, Flatiron Institute, 162 Fifth Ave, New York, NY, 10010, USA
   index: 2
 - name: McWilliams Center for Cosmology and Astrophysics, Department of Physics, Carnegie Mellon University, Pittsburgh, PA 15213, USA
   index: 3
 - name: University of Arizona, Department of Astronomy \& Steward Observatory, 933 N. Cherry Ave., Tucson, AZ 85721, USA
   index: 4
date: 06 September 2024
bibliography: paper.bib


# Summary

The upcoming Legacy Survey of Space and Time at the Vera C. Rubin Observatory is expected to revolutionize solar system astronomy. Unprecedented in scale, this ten-year wide-field survey will perform billions of observations and discover a predicted 5 million new solar system objects. This wealth of new information surpasses any solar system survey to date in its combination of depth, sky coverage and sheer number of observations, and this will allow us to probe the dynamics and formation history of the solar system on a scale never-before attempted. However, all astronomical surveys are affected by a complex set of intertwined observational biases caused by a number of factors, including observational strategy and cadence, limiting magnitude, instrumentation effects and poor weather/seeing. The detections from an astronomical survey therefore provide a biased and distorted view of the actual underlying population. To help address this, survey simulators have emerged as powerful tools for assessing the impact of observational biases and aiding in the study of the target population. Survey simulators have long been used in smaller population-specific surveys such as the Canada–France Ecliptic Plane Survey (CFEPS) [`@jones:2006’] and the Outer Solar System Origins Survey (OSSOS) `[@bannister:2016; @lawler:2018]` to forward-model the effects of biases on a given population, allowing for a direct comparison to real discoveries. However, the scale and tremendous scope of the LSST requires the development of a new tool capable of handling much larger data sets and all solar system small body populations.

# Statement of need

`sorcha` is a multipurpose, open-source solar system survey simulator for the LSST. Built in Python to be flexible, easy-to-use, and applicable to all solar system small body populations, ‘sorcha’ runs on the command-line via a sophisticated command-line interface, ingesting input files which describe the input population and survey. Its modular design and configuration file allows each simulation to be highly customizable by the user for their specific needs, and while `sorcha` was built with the LSST in mind, this inherent customizability also allows it to be easily adapted to other astronomical surveys. Additionally, `sorcha` was designed to work at the large scale demanded by the billions of upcoming LSST observations, and simulations can be run both locally and on high-performance computing clusters. 

To predict the position of potentially millions of solar system objects over ten years and over a billion observations in a reasonable timescale, `sorcha` makes use of an ephemeris generator powered by ASSIST `[@holman:2023]`, an open source `Python` and C99 software package for producing ephemeris-quality integrations of solar system test particles using the REBOUND N-body integrator `[@rein:2012]` to model the motion of the particles under the influence of gravity. `sorcha` also makes use of a per-module randomization approach that provides the ability to force deterministic behavior regardless of the order in which modules are executed, as described in ‘@schwamb:2024’. Additionally, in order to facilitate the use of customisable, community-built classes to describe cometary activity or light-curve modulation effects, `sorcha` provides abstract base classes from which custom implementations can inherit, allowing a high level of customisation of the code without requiring the user to modify the source code directly.

We have designed `sorcha` to be a key community tool for solar system science with the LSST. `sorcha` has already allowed for predictive work to be made ahead of the LSST’s launch, with predictions made of the overall yield of new solar system small body discoveries (`@Kurlander:2025`, in prep) and of centaurs, a class of small, icy bodies that orbit the Sun on giant planet-crossing paths (`@Murtagh:2025`, in prep), and upcoming work (`@Schwamb:2025`, in prep) plans to place limitations on the discoverability of Planet Nine with the LSST. 


# Acknowledgements

This work was supported by a LSST Discovery Alliance LINCC Frameworks Incubator grant [2023-SFF-LFI-01-Schwamb]. Support was provided by Schmidt Sciences. S.R.M. and M.E.S. acknowledge support in part from UK Science and Technology Facilities Council (STFC) grants ST/V000691/1 and ST/X001253/1. G.F. acknowledges support in part from STFC grant ST/P000304/1. This project has received funding from the European Union’s Horizon 2020 research and innovation program under the Marie Skłodowska-Curie grant agreement No. 101032479. M.J. and P.H.B. acknowledge the support from the University of Washington College of Arts and Sciences, Department of Astronomy, and the DiRAC (Data-intensive Research in Astrophysics and Cosmology) Institute. The DiRAC Institute is supported through generous gifts from the Charles and Lisa Simonyi Fund for Arts and Sciences and the Washington Research Foundation. M.J. wishes to acknowledge the support of the Washington Research Foundation Data Science Term Chair fund, and the University of Washington Provost's Initiative in Data-Intensive Discovery. J. Murtagh acknowledges support from the Department for the Economy (DfE) Northern Ireland postgraduate studentship scheme and travel support from the STFC for UK participation in LSST through grant ST/S006206/1. J.A.K. and J. Murtagh thank the LSST-DA Data Science Fellowship Program, which is funded by LSST-DA, the Brinson Foundation, and the Moore Foundation; their participation in the program has benefited this work. S.E. and S.C. acknowledge support from the National Science Foundation through the following awards: Collaborative Research: SWIFT-SAT: Minimizing Science Impact on LSST and Observatories Worldwide through Accurate Predictions of Satellite Position and Optical Brightness NSF Award Number: 2332736 and Collaborative Research: Rubin Rocks: Enabling near-Earth asteroid science with LSST NSF Award Number: 2307570. RRL was supported by the UK STFC grant ST/V506990/1. Any opinions, findings, and conclusions or recommendations expressed in this material are those of the authors and do not necessarily reflect the views of the National Science Foundation.
 
This work was also supported via the Preparing for Astrophysics with LSST Program, funded by the Heising Simons Foundation through grant 2021-2975, and administered by Las Cumbres Observatory. This work was supported in part by the LSST Discovery Alliance Enabling Science grants program, the B612 Foundation, the University of Washington's DiRAC Institute, the Planetary Society, Karman+, and Adler Planetarium through generous support of the LSST Solar System Readiness Sprints.

This research has made use of NASA’s Astrophysics Data System Bibliographic Services. This research has made use of data and/or services provided by the International Astronomical Union's Minor Planet Center. The SPICE Resource files used in this work are described in \citet{acton1996, acton2018}. Simulations in this paper made use of the REBOUND N-body code \citep{rein2012}. The simulations were integrated using IAS15, a 15th order Gauss-Radau integrator \citep{rein2015}. Some of the results in this paper have been derived using the healpy and HEALPix packages. This work made use of Astropy (http://www.astropy.org) a community-developed core \python package and an ecosystem of tools and resources for astronomy \citep{astropy2013,astropy2018,astropy2022}. We thank the Vera C. Rubin Observatory Data Management Team and Scheduler Team for making their software open-source. We thank Dave Young and Conor MacBride for initial help setting up the python project and repository. The authors also thank Michele Bannister and Rosemary Dorsey for conversations that helped improve the software's handling of interstellar objects. We also thank Aidan Berres, Ricardo Bánffy, and Brian Rogers for their contributions to coding, documentation, and/or beta testing.  We are additionally grateful to the members of the Rubin Observatory LSST Solar System Science Collaboration for useful feedback at the LSST Solar System Readiness Sprints. We also thank the contributors to Stack Overflow for their examples and advice on common \python challenges that provided guidance on solving some of the programming challenges we have encountered.

This material or work is supported in part by the National Science Foundation through Cooperative Agreement AST-1258333 and Cooperative Support Agreement AST1836783 managed by the Association of Universities for Research in Astronomy (AURA), and the Department of Energy under Contract No. DE-AC02-76SF00515 with the SLAC National Accelerator Laboratory managed by Stanford University.  

We are grateful for the use of the computing resources from the Northern Ireland High Performance Computing (NI-HPC) service funded by EPSRC (EP/T022175). We gratefully acknowledge the support of the Center for Advanced Computing and Modelling, University of Rijeka (Croatia), for providing supercomputing resources at HPC (High Performance Computing) Bura.

The authors wish to acknowledge the researchers who worked tirelessly to rapidly develop COVID-19 vaccines and subsequent boosters. Without all their efforts, we would not have been able to pursue this work.

We acknowledge the contribution of pets Isha Bernardinelli; Freddie and Millie Merritt; Stella Schwamb; Richard, Calcifer, and Buttons West; that, by keeping us awake at night, yowling during our meetings, or providing general emotional support, led to improvements in this software and manuscript.

# References

