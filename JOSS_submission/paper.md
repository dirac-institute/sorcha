---
title: ‘Sorcha: A Solar System Survey Simulator for the Legacy Survey of Space and Time'
tags:
  - Python
  - astronomy
  - solar system
authors:
  - name: Stephanie R. Merritt
    orcid: 0000-0001-5930-2829
    affiliation: “1”
    corresponding: true
  - name: Grigori Fedorets
    orcid:0000-0002-8418-4809
    affiliation: “1,2,3”
  - name: Megan E. Schwamb
    orcid: 0000-0003-4365-1455
    affiliation: “1”
  - name: Samuel Cornwall
    orcid: 0000-0002-0672-5104
    affiliation: “4”
  - name: Pedro H. Bernardinelli
    orcid: 0000-0003-0743-9422
    affiliation: “5”
  - name: Mario Jurić
    orcid: 0000-0003-1996-9252
    affiliation: “5”
  - name: Matthew J.Holman
    orcid: 0000-0002-1139-4880
    affiliation: “6”
  - name: Jacob A. Kurlander
    orcid: 0000-0002-1139-4880
    affiliation: “5”
  - name: Jacob A. Kurlander
    orcid: 0009-0005-5452-0671
    affiliation: “5”
  - name: Siegfried Eggl
    orcid: 0000-0002-1398-6302
    affiliation: “4,7,8,9”
  - name: Drew Oldag
    orcid: 0000-0001-6984-8411
    affiliation: “5,10”
  - name: Maxine West
    orcid: 0009-0003-3171-3118
    affiliation: “5,10”
  - name: Jeremy Kubica
    orcid: 0009-0009-2281-7031
    affiliation: “11,10”
  - name: Joseph Murtagh
    orcid: 0000-0001-9505-1131
    affiliation: “1”
  - name: R. Lynne Jones
    orcid: 0000-0001-5916-0031
    affiliation: “12,13”
  - name: Peter Yoachim
    orcid: 0000-0003-2874-6464
    affiliation: “5”
- name: Ryan R. Lyttle
    orcid: 0009-0007-8602-2954
    affiliation: “1”
- name: Michael S. P. Kelley
    orcid: 0000-0002-6702-7676
    affiliation: “14”
- name: Joachim Moeyens
    orcid: 0000-0001-5820-3925
    affiliation: “15,5”
- name: Kathleen Kiker
    affiliation: “15”
- name: Shantanu P. Naidu
    orcid: 0000-0003-4439-7014
    affiliation: “16”
- name: Colin Snodgrass
    orcid: 0000-0001-9328-2905
    affiliation: “17”
- name: Shannon M. Matthews
    orcid: 0000-0001-8633-9141
    affiliation: “1”
- name: Colin Orion Chandler
    orcid: 0000-0001-7335-1715
    affiliation: “5,10”
affiliations:
 - name: Astrophysics Research Centre, School of Mathematics and Physics, Queen’s University Belfast, Belfast BT7 1NN, UK
   index: 1
 - name: Finnish Centre for Astronomy with ESO, University of Turku, FI-20014 Turku, Finland
   index: 2
 - name: Department of Physics, University of Helsinki, P.O. Box 64, 00014
Helsinki, Finland
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
 - name: IMCCE, Paris Observatory, 77 Avenue Denfert-Rochereau, 75014 Paris, France
   index: 9
 - name: LSST Interdisciplinary Network for Collaboration and Computing Frameworks, 933 N. Cherry Avenue, Tucson AZ 8572
   index: 10
 - name: McWilliams Center for Cosmology, Department of Physics, Carnegie Mellon University, Pittsburgh, PA 15213, USA
   index: 11
 - name: Rubin Observatory, 950 N. Cherry Ave., Tucson, AZ 85719, USA
   index: 12
 - name: Aston Carter, Suite 150, 4321 Still Creek Drive, Burnaby, BC V5C6S, Canada
   index: 13
 - name: Department of Astronomy, University of Maryland, College Park, MD 20742-0001, USA
   index: 14
 - name: Asteroid Institute, 20 Sunnyside Ave., Suite 427, Mill Valley, CA 94941, USA
   index: 15
 - name: Jet Propulsion Laboratory, California Institute of Technology, Pasadena, CA, USA
   index: 16
 - name: Institute for Astronomy, University of Edinburgh, Royal Observatory, Edinburgh, EH9 3HJ, UK
   index: 17
date: 15 January 2025
bibliography: paper.bib

# Optional fields if submitting to a AAS journal too, see this blog post:
# https://blog.joss.theoj.org/2018/12/a-new-collaboration-with-aas-publishing
aas-doi: 10.3847/xxxxx <- update this with the DOI from AAS once you know it.
aas-journal: Astrophysical Journal 

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

