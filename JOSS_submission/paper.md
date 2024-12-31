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
    affiliation: "4,7,8,9"
  - name: Drew Oldag
    orcid:  0000-0001-6984-8411
    affiliation: "5,10"
  - name: Maxine West
    orcid: 0009-0003-3171-3118
    affiliation: "5,10"
  - name: Jeremy Kubica
    orcid: 0009-0009-2281-7031
    affiliation: "11,10"
  - name: Joseph Murtagh
    orcid: 0000-0001-9505-1131
    affiliation: "1"
  - name:  R. Lynne Jones
    orcid: 0000-0001-5916-0031
    affiliation: "12,13"
  - name: Peter Yoachim
    orcid: 0000-0003-2874-6464
    affiliation: "5"
  - name: Ryan R. Lyttle
    orcid:  0009-0007-8602-2954
    affiliation: "1"
  - name: Michael S. P. Kelley
    orcid:  0000-0002-6702-7676
    affiliation: "14"
  - name: Joachim Moeyens
    orcid: 0000-0001-5820-3925
    affiliation: "15,5"
  - name: Kathleen Kiker
    orcid: 
    affiliation: "15"
  - name: Shantanu P. Naidu
    orcid: 0000-0003-4439-7014
    affiliation: "16"
  - name: Colin Snodgrass
    orcid: 0000-0001-9328-2905
    affiliation: "17"
  - name: Shannon M. Matthews
    orcid: 0000-0001-8633-9141
    affiliation: "1"
  - name: Colin Orion Chandler
    orcid: 0000-0001-7335-1715
    affiliation: "5,10"
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
aas-doi: 10.3847/1538-4365/ad8b1f
aas-journal: Astrophysical Journal Supplement Series
---

# Summary

The upcoming Legacy Survey of Space and Time at the Vera C. Rubin Observatory is expected to revolutionize solar system astronomy. Unprecedented in scale, this ten-year wide-field survey will perform billions of observations and discover a predicted 5 million new solar system objects. This wealth of new information surpasses any solar system survey to date in its combination of depth, sky coverage and sheer number of observations, and this will allow us to probe the dynamics and formation history of the solar system on a scale never-before attempted. However, all astronomical surveys are affected by a complex set of intertwined observational biases caused by a number of factors, including observational strategy and cadence, limiting magnitude, instrumentation effects and poor weather/seeing. The detections from an astronomical survey therefore provide a biased and distorted view of the actual underlying population. To help address this, survey simulators have emerged as powerful tools for assessing the impact of observational biases and aiding in the study of the target population. Survey simulators have long been used in smaller population-specific surveys such as the Canada–France Ecliptic Plane Survey (CFEPS) [`@jones:2006’] and the Outer Solar System Origins Survey (OSSOS) `[@bannister:2016; @lawler:2018]` to forward-model the effects of biases on a given population, allowing for a direct comparison to real discoveries. However, the scale and tremendous scope of the LSST requires the development of a new tool capable of handling much larger data sets and all solar system small body populations.


# Statement of need

The majority of stars are born in binaries and multiple star systems [e.g., @Duchene+2013; @Moe+2017; @Offner+2023], a large subset of which will exchange mass at some point in their lives [e.g.,  @deMink+2014; @Podsiadlowski+1992; @Sana+2012]. These massive stars play a critical role in the formation and evolution of galaxies as a result of their feedback [e.g., @Dekel+1986; @Hopkins+2012; @Nomoto+2013; @Somerville+2015; @Naab+2017]. However, binary evolution remains uncertain, with many parameters such as common-envelope efficiency, mass transfer efficiency, angular momentum loss due to mass transfer and the mean magnitude of supernova natal kicks unconstrained over several orders of magnitude [e.g., @Ivanova+2020; @Janka+2012; @Ivanova+2013; @Katsuda+2018; @Ropke+2023; @Marchant2023].

Single massive stars are not expected to migrate far from their birth location before reaching core-collapse due to their short lifetimes [$\lesssim50$\,Myr, e.g., @zapartas:17]. However, binary stars may be disrupted after an initial supernova event, ejecting the secondary star from the system at its orbital velocity [e.g., @Blaauw+1961; @Eldridge+2011; @Renzo+2019]. Thus, close massive binaries that are disrupted can lead to the displacement of secondary stars significantly farther from star-forming regions. The present-day positions and kinematics of massive stars and binary products are therefore strongly impacted by changes in binary physics that alter the pre-supernova separation. This means that comparing simulations of positions and kinematics of stars and compact objects to observations will enable constraints on binary stellar evolution parameters.

The use of positions and kinematics as tracers of binary evolution has been considered in the past. Recent work has shown the importance of accounting for the galactic potential, which can change the velocity of kicked objects [e.g. @Disberg+2024]. It is also important to consider the inclination or timing of a supernova kick relative to the galactic orbit, since, for example, a kick out of the galactic plane at an object's highest galactic vertical position will have a strong effect on its final position. Failing to consider impacts from both a galactic potential and kicks (i.e. velocity impulses) will lead to misleading conclusions regarding the final spatial distributions of the population. Some studies have considered using the galactic potential at the present-day positions of objects to place a lower limit on the peculiar velocity at birth and constrain supernova kicks [@Repetto+2012; @Repetto+2015; @Repetto+2017; @atri:19], but the accuracy of this method is debated [@Mandel+2016]. Other works have considered the impact of the galactic potential for individual special cases, rather than at a population level. For example, @Evans+2020 considered the orbits of hyper-runaway candidates evolving through the Milky Way potential, while @Neuhauser+2020 developed software for tracing the motion of stars to investigate the recent nearby supernovae that ejected $\zeta$ Ophiuchi. @Andrews+2022 considered galactic orbits of synthetic populations to place constraints on black hole natal kicks based on observations of a microlensed black hole.

Additionally, there are several works that consider a full population of objects integrated through a galactic potential. @underworld and @Sweeney+2024 used a combination of `Galaxia` and `galpy` to predict the spatial distribution of black holes and neutron stars in the Milky Way. Similarly, several works have combined population synthesis with galactic orbit integration [e.g. using `COMPAS`, @COMPAS; and `NIGO`, @NIGO] to investigate binary neutron stars and pulsars [@Chattopadhyay+2020; @Chattopadhyay+2021; @Gaspari+2024a; @Disberg+2024b; @Song+2024], as well as binary neutron star mergers and short gamma-ray bursts [@Zevin+2020; @Mandhai+2022; @Gaspari+2024b].

There is a clear need for a unified open-source tool that provides the theoretical infrastructure for making predictions for the positions and kinematics of massive stars and compact objects, placing these systems in the context of their host galaxy and its gravitational potential. `cogsworth` fulfils this need, providing a framework for self-consistent population synthesis and galactic dynamics simulations. The code is applicable to a wide range of binary products, both common and rare, from walkaway and runaway stars to X-ray binaries, as well as gravitational-wave and gamma-ray burst progenitors.

# Acknowledgements

We gratefully acknowledge many fruitful discussions with Julianne Dalcanton and Eric Bellm that resulted in several helpful suggestions. TW acknowledges valuable conversations with Matt Orr and Chris Hayward regarding the FIRE simulations, and with Alyson Brooks and Akaxia Cruz regarding the ChaNGa simulations. TW thanks the Simons Foundation, Flatiron Institute and Center for Computational Astrophysics for running the pre-doctoral program during which much of this work was completed. The Flatiron Institute is supported by the Simons Foundation. TW and KB acknowledge support from NASA ATP grant 80NSSC24K0768.

# References
