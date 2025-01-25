---
title: 'Sorcha: A Solar System Survey Simulator for the Legacy Survey of Space and Time'
tags:
  - Python
  - astronomy
  - solar system
authors:
  - name: Stephanie R. Merritt
    orcid: 0000-0001-5930-2829
    affiliation: "1"
    corresponding: true
  - name: Grigori Fedorets
    orcid: 0000-0002-8418-4809
    affiliation: "1,2,3"
  - name: Megan E. Schwamb
    orcid: 0000-0003-4365-1455
    affiliation: "1"
  - name: Samuel Cornwall
    orcid: 0000-0002-0672-5104
    affiliation: "4"
  - name: Pedro H. Bernardinelli
    orcid:  0000-0003-0743-9422
    affiliation: "5"
  - name: Mario Jurić
    orcid:  0000-0003-1996-9252
    affiliation: "5"
  - name: Matthew J.Holman
    orcid:  0000-0002-1139-4880
    affiliation: "6"
  - name: Jacob A. Kurlander
    orcid: 0009-0005-5452-0671
    affiliation: "5"
  - name: Siegfried Eggl
    orcid:  0000-0002-1398-6302
    affiliation: "4,7,8"
  - name: Drew Oldag
    orcid:  0000-0001-6984-8411
    affiliation: "5,9"
  - name: Maxine West
    orcid: 0009-0003-3171-3118
    affiliation: "5,9"
  - name: Jeremy Kubica
    orcid: 0009-0009-2281-7031
    affiliation: "10,19"
  - name: Joseph Murtagh
    orcid: 0000-0001-9505-1131
    affiliation: "1"
  - name:  R. Lynne Jones
    orcid: 0000-0001-5916-0031
    affiliation: "11,12"
  - name: Peter Yoachim
    orcid: 0000-0003-2874-6464
    affiliation: "5"
  - name: Ryan R. Lyttle
    orcid:  0009-0007-8602-2954
    affiliation: "1"
  - name: Michael S. P. Kelley
    orcid:  0000-0002-6702-7676
    affiliation: "13"
  - name: Joachim Moeyens
    orcid: 0000-0001-5820-3925
    affiliation: "14,5"
  - name: Kathleen Kiker
    orcid: 
    affiliation: "14"
  - name: Shantanu P. Naidu
    orcid: 0000-0003-4439-7014
    affiliation: "15"
  - name: Colin Snodgrass
    orcid: 0000-0001-9328-2905
    affiliation: "16"
  - name: Shannon M. Matthews
    orcid: 0000-0001-8633-9141
    affiliation: "1"
  - name: Colin Orion Chandler
    orcid: 0000-0001-7335-1715
    affiliation: "5,9"
affiliations:
 - name: Astrophysics Research Centre, School of Mathematics and Physics, Queen’s University Belfast, Belfast BT7 1NN, UK
   index: 1
 - name: Finnish Centre for Astronomy with ESO, University of Turku, FI-20014 Turku, Finland
   index: 2
 - name: Department of Physics, University of Helsinki, P.O. Box 64, 00014 Helsinki, Finland
   index: 3
 - name: Department of Aerospace Engineering, Grainger College of Engineering, University of Illinois at Urbana-Champaign,Urbana, IL 61801, USA
   index: 4
 - name: DiRAC Institute and the Department of Astronomy, University of Washington, 3910 15th Ave NE, Seattle, WA 98195, USA
   index: 5
 - name: Center for Astrophysics | Harvard & Smithsonian, 60 Garden St., MS 51, Cambridge, MA 02138, USA
   index: 6
 - name: Department of Astronomy, University of Illinois at Urbana-Champaign, Urbana, IL 61801, USA
   index: 7
 - name: National Center for Supercomputing Applications, University of Illinois at Urbana-Champaign, Urbana, IL 61801, USA
   index: 8
 - name: LSST Interdisciplinary Network for Collaboration and Computing Frameworks, 933 N. Cherry Avenue, Tucson AZ 8572
   index: 9
 - name: McWilliams Center for Cosmology, Department of Physics, Carnegie Mellon University, Pittsburgh, PA 15213, USA
   index: 10
 - name: Rubin Observatory, 950 N. Cherry Ave., Tucson, AZ 85719, USA
   index: 11
 - name: Aston Carter, Suite 150, 4321 Still Creek Drive, Burnaby, BC V5C6S, Canada
   index: 12
 - name: Department of Astronomy, University of Maryland, College Park, MD 20742-0001, USA
   index: 13
 - name: Asteroid Institute, 20 Sunnyside Ave., Suite 427, Mill Valley, CA 94941, USA
   index: 14
 - name: Jet Propulsion Laboratory, California Institute of Technology, Pasadena, CA, USA
   index: 15
 - name: Institute for Astronomy, University of Edinburgh, Royal Observatory, Edinburgh, EH9 3HJ, UK
   index: 16

date: 20 January 2025
bibliography: paper.bib

# Optional fields if submitting to a AAS journal too, see this blog post:
# https://blog.joss.theoj.org/2018/12/a-new-collaboration-with-aas-publishing
aas-doi: 
aas-journal: Astronomical Journal
---

# Statement of Need

The upcoming Legacy Survey of Space and Time (LSST)  at the Vera C. Rubin Observatory [@lsstsciencebook2009; @ivezic2019; @bianco2022] is expected to revolutionize solar system astronomy. Unprecedented in scale, this ten-year wide-field survey will take ~2 million exposures split between 6 filters while also discovering and monitoring millions more solar system objects than are currently known [@jones2009; @jones2018; @lsstsciencebook2009; @solontoi2010; @shannon2015; @grav2016; @silsbee2016; @veres2017; @schwamb2018; @ivezic2019; @fedorets2020; @hoover2022; @kurlander2025; @murtagh2025]. This wealth of new information surpasses any survey to date in its combination of depth, sky coverage and sheer number of observations, The LSST will enable planetary astronomers to probe the dynamics and formation history of the solar system on a scale never before attempted. However, all astronomical surveys are affected by a complex set of intertwined observational biases, including observational strategy and cadence, limiting magnitude, instrumentation effects and observing conditions. The small body discoveries from an astronomical survey therefore provide a biased and distorted view of the actual underlying population. To help address this, survey simulators have emerged as powerful tools for assessing the impact of observational biases and aiding in the study of the target population. Survey simulators have long been used in smaller population-specific surveys such as the Canada–France Ecliptic Plane Survey (CFEPS) [@jones2006; @kavelaars2009; @petit2011] and the Outer Solar System Origins Survey (OSSOS) [@bannister2016; @bannister2018; @lawler2018] to forward-model the effects of biases on a given population, allowing for a direct comparison to real discoveries. However, the scale and tremendous scope of the LSST requires the development of a new tool capable of handling the scale of the Rubin Observatory’s LSST and all solar system small body populations.

Probing the orbital/size/brightness distributions and surface composition in each of the solar system's small body reservoirs is the top science priority in the Rubin Observatory LSST Solar System Science Collaboration (SSSC) Science Roadmap [@schwamb2018]. In order to perform these detailed population studies, one must account for all the survey biases (the complex and often intertwined detection biases – brightness limits, pointing, cadence, on-sky motion limits, software detection efficiencies) in the discovery survey (see @lawler2018 for a more detailed discussion). The SSSC’s Software Roadmap has identified a solar system survey simulator as one of the key software tools that must be developed in order to achieve the collaboration’s top science goals [@Schwamb2019]. A survey simulator takes an input model small body population and outputs (biases the population to) what LSST should have detected by utilizing the LSST pointing history, observation metadata, and Rubin Observatory Solar System Processing (SSP) pipeline’s detection efficiency so one can compare those simulated LSST detections to what was actually found by Rubin Observatory.

# Summary

`Sorcha` is a multipurpose, open-source solar system survey simulator for the LSST. Its modular design and configuration file allows each simulation to be finely customized by the user for their specific needs.  `Sorcha` was designed to work at the large scale demanded by the large data rate from the LSST, and simulations can be run on  high-performance computing clusters or on a researcher's laptop/desktop machine. The simulator can be used to facilitate predictions before the LSST begins science operations and to achieve a wide range of science goals when the LSST solar system discoveries are available. 

Built in Python to be flexible, easy-to-use, and applicable to all solar system small body populations, 'Sorcha’ runs on the command-line, ingesting files which describe the input population and the input survey. To predict the position of millions of solar system objects over ten years and over ~billion observations in a reasonable timescale, `Sorcha` makes use of an ephemeris generator (described in @holman2025) powered by ASSIST [@holman2023], an open-source Python and C99 software package for producing ephemeris-quality integrations of solar system test particles using the the IAS15 (15th order Gauss-Radau) integrator [@rein2015] within the REBOUND N-body integrator package [@rein2012] to model the motion of the particles under the influence of gravity. `Sorcha` also makes use of a per-module randomization approach, as described in @schwamb2024, allowing for deterministic random number generation during testing regardless of the order in which modules are executed. Additionally, in order to facilitate the use of customisable, community-built classes to describe cometary activity or light-curve modulation effects, `Sorcha` provides abstract base classes from which custom implementations can inherit, allowing a high level of customisation of the code without requiring the user to modify the source code directly. 

`Sorcha` is expected to be a key community tool for solar system science with the LSST. The software package has already enabled predictive work to be made ahead of the start of the LSST, with predictions made of the overall yield of new the asteroid and trans-Neptunian object discoveries [@kurlander2025] and of Centaurs, a class of small, icy bodies that orbit the Sun on giant planet-crossing paths [@murtagh2025]. We expect that future upgrades to `Sorcha` will include adding the capability to simulate past well characterized wide-field discovery surveys in addition to the LSST.  

# Acknowledgements

This work was supported by a LSST Discovery Alliance LINCC Frameworks Incubator grant [2023-SFF-LFI-01-Schwamb]. Support was provided by Schmidt Sciences. S.R.M. and M.E.S. acknowledge support in part from UK Science and Technology Facilities Council (STFC) grants ST/V000691/1 and ST/X001253/1. G.F. acknowledges support in part from STFC grant ST/P000304/1. This project has received funding from the European Union’s Horizon 2020 research and innovation program under the Marie Skłodowska-Curie grant agreement No. 101032479. M.J. and P.H.B. acknowledge the support from the University of Washington College of Arts and Sciences, Department of Astronomy, and the DiRAC (Data-intensive Research in Astrophysics and Cosmology) Institute. The DiRAC Institute is supported through generous gifts from the Charles and Lisa Simonyi Fund for Arts and Sciences and the Washington Research Foundation. M.J. wishes to acknowledge the support of the Washington Research Foundation Data Science Term Chair fund, and the University of Washington Provost's Initiative in Data-Intensive Discovery. J. Murtagh acknowledges support from the Department for the Economy (DfE) Northern Ireland postgraduate studentship scheme and travel support from the STFC for UK participation in LSST through grant ST/S006206/1. S.E. and S.C. acknowledge support from the National Science Foundation through the following awards: Collaborative Research: SWIFT-SAT: Minimizing Science Impact on LSST and Observatories Worldwide through Accurate Predictions of Satellite Position and Optical Brightness NSF Award Number: 2332736 and Collaborative Research: Rubin Rocks: Enabling near-Earth asteroid science with LSST NSF Award Number: 2307570. RRL was supported by the UK STFC grant ST/V506990/1. Any opinions, findings, and conclusions or recommendations expressed in this material are those of the authors and do not necessarily reflect the views of the National Science Foundation.
 
This work was also supported via the Preparing for Astrophysics with LSST Program, funded by the Heising Simons Foundation through grant 2021-2975, and administered by Las Cumbres Observatory. This work was supported in part by the LSST Discovery Alliance Enabling Science grants program, the B612 Foundation, the University of Washington's DiRAC Institute, the Planetary Society, Karman+, and Adler Planetarium through generous support of the LSST Solar System Readiness Sprints.

This research has made use of NASA’s Astrophysics Data System Bibliographic Services. This research has made use of data and/or services provided by the International Astronomical Union's Minor Planet Center. The SPICE Resource files used in this work are described in [@acton1996; @acton2018]. Some of the results in this paper have been derived using the healpy and HEALPix packages [@gorski2005; @zonca2019]. This work made use of Astropy (http://www.astropy.org) a community-developed core \python package and an ecosystem of tools and resources for astronomy [@astropy2013; @astropy2018; @astropy2022]. We thank the Vera C. Rubin Observatory Data Management Team and Scheduler Team for making their software open-source. We thank Dave Young and Conor MacBride for initial help setting up the python project and repository. 

This material or work is supported in part by the National Science Foundation through Cooperative Agreement AST-1258333 and Cooperative Support Agreement AST1836783 managed by the Association of Universities for Research in Astronomy (AURA), and the Department of Energy under Contract No. DE-AC02-76SF00515 with the SLAC National Accelerator Laboratory managed by Stanford University.  


# References
