import rebound


def cite_sorcha():
    """Providing the bibtex, AAS Journals software latex command, and acknowledgement
    statements for Sorcha and the associated packages that power it.
    """
    print("\nSorcha: \n")
    print("Merritt et al. (in prep)")

    print("\n")

    print("Please also cite the packages that are utilized by Sorcha:")

    print("\nASSIST:\n")

    print("@ARTICLE{2023PSJ.....4...69H,")
    print(
        "author = {{Holman}, Matthew J. and {Akmal}, Arya and {Farnocchia},"
        " Davide and {Rein}, Hanno and {Payne}, Matthew J. and {Weryk}, Robert"
        " and {Tamayo}, Daniel and {Hernandez}, David M.},"
    )
    print('title = "{ASSIST: An Ephemeris-quality Test-particle Integrator}",')
    print("journal = {\\psj},")
    print(
        "keywords = {Ephemerides, N-body simulations, Asteroid dynamics, "
        "Comet dynamics, 464, 1083, 2210, 2213, Astrophysics - Earth and Planetary Astrophysics,"
        "Astrophysics - Instrumentation and Methods for Astrophysics},"
    )
    print("year = 2023,")
    print("month = apr,")
    print("volume = {4},")
    print("number = {4},")
    print("eid = {69},")
    print("pages = {69},")
    print("doi = {10.3847/PSJ/acc9a9},")
    print("archivePrefix = {arXiv},")
    print("eprint = {2303.16246},")
    print("primaryClass = {astro-ph.EP},")
    print("adsurl = {https://ui.adsabs.harvard.edu/abs/2023PSJ.....4...69H},")
    print("adsnote = {Provided by the SAO/NASA Astrophysics Data System}")
    print("}")

    print("\n")

    print("@software{hanno_rein_2023_7778017,")
    print("author       = {Hanno Rein and matthewholman and Arya Akmal},")
    print("title        = {matthewholman/assist: v1.1.1},")
    print("month        = mar,")
    print("year         = 2023,")
    print("publisher    = {Zenodo},")
    print("version      = {v1.1.1},")
    print("doi          = {10.5281/zenodo.7778017},")
    print("url          = {https://doi.org/10.5281/zenodo.7778017}")
    print("}")

    print("\nAstropy:\n")
    print("@ARTICLE{2013A&A...558A..33A,")
    print(
        " author = {{Astropy Collaboration} and {Robitaille}, Thomas P. "
        "and {Tollerud}, Erik J. and {Greenfield}, Perry and {Droettboom}, "
        " Michael and {Bray}, Erik and {Aldcroft}, Tom and {Davis}, Matt "
        "and {Ginsburg}, Adam and {Price-Whelan}, Adrian M. and {Kerzendorf}, "
        " Wolfgang E. and {Conley}, Alexander and {Crighton}, Neil and "
        "{Barbary}, Kyle and {Muna}, Demitri and {Ferguson}, Henry "
        " and {Grollier}, Fr{\\'e}d{\\'e}ric and {Parikh}, Madhura M. "
        "and {Nair}, Prasanth H. and {Unther}, Hans M. and {Deil}, Christoph "
        " and {Woillez}, Julien and {Conseil}, Simon and {Kramer}, Roban "
        "and {Turner}, James E.~H. and {Singer}, Leo and {Fox}, Ryan and "
        "{Weaver}, Benjamin A. and {Zabalza}, Victor and {Edwards}, "
        "Zachary I. and {Azalee Bostroem}, K. and {Burke}, D.~J. and {Casey}, "
        "Andrew R. and {Crawford}, Steven M. and {Dencheva}, Nadia and {Ely},"
        "Justin and {Jenness}, Tim and {Labrie}, Kathleen and {Lim}, Pey Lian and "
        "{Pierfederici}, Francesco and {Pontzen}, Andrew and {Ptak}, Andy "
        " and {Refsdal}, Brian and {Servillat}, Mathieu and {Streicher}, Ole},"
    )
    print('title = "{Astropy: A community Python package for astronomy}",')
    print("journal = {\\aap},")
    print(
        "keywords = {methods: data analysis, methods: miscellaneous, "
        "virtual observatory tools, Astrophysics - Instrumentation and "
        "Methods for Astrophysics},"
    )
    print("year = 2013,")
    print("month = oct,")
    print("volume = {558},")
    print("eid = {A33},")
    print("pages = {A33},")
    print("doi = {10.1051/0004-6361/201322068},")
    print("archivePrefix = {arXiv},")
    print("eprint = {1307.6212},")
    print("primaryClass = {astro-ph.IM},")
    print("adsurl = {https://ui.adsabs.harvard.edu/abs/2013A&A...558A..33A},")
    print("adsnote = {Provided by the SAO/NASA Astrophysics Data System}")
    print("}")

    print("\n")
    print("@ARTICLE{2018AJ....156..123A,")
    print(
        "author = {{Astropy Collaboration} and {Price-Whelan}, A.~M. "
        'and {Sip{\\H{o}}cz}, B.~M. and {G{\\"u}nther}, H.~M. and {Lim}, P.~L. '
        "and {Crawford}, S.~M. and {Conseil}, S. and {Shupe}, D.~L. and "
        "{Craig}, M.~W. and {Dencheva}, N. and {Ginsburg}, A. and "
        "{VanderPlas}, J.~T. and {Bradley}, L.~D. and {P{'e}rez-Su{'a}rez}, D. "
        "and {de Val-Borro}, M. and {Aldcroft}, T.~L. and {Cruz}, K.~L. and "
        "{Robitaille}, T.~P. and {Tollerud}, E.~J. and {Ardelean}, C. and "
        "{Babej}, T. and {Bach}, Y.~P. and {Bachetti}, M. and {Bakanov}, "
        "A.~V. and {Bamford}, S.~P. and {Barentsen}, G. and {Barmby}, "
        " P. and {Baumbach}, A. and {Berry}, K.~L. and {Biscani}, F. and {Boquien}, "
        "M. and {Bostroem}, K.~A. and {Bouma}, L.~G. and {Brammer}, G.~B. and "
        " {Bray}, E.~M. and {Breytenbach}, H. and {Buddelmeijer}, H. and "
        "{Burke}, D.~J. and {Calderone}, G. and {Cano Rodr{\\'\\i}guez}, J.~L. "
        "and {Cara}, M. and {Cardoso}, J.~V.~M. and {Cheedella}, S. and {Copin}, "
        "Y. and {Corrales}, L. and {Crichton}, D. and {D'Avella}, D. and {Deil}, "
        "C. and {Depagne}, {'E}. and {Dietrich}, J.~P. and {Donath}, A. and "
        "{Droettboom}, M. and {Earl}, N. and {Erben}, T. and {Fabbro}, S. and "
        "{Ferreira}, L.~A. and {Finethy}, T. and {Fox}, R.~T. and {Garrison}, "
        "L.~H. and {Gibbons}, S.~L.~J. and {Goldstein}, D.~A. and {Gommers}, R. "
        "and {Greco}, J.~P. and {Greenfield}, P. and {Groener}, A.~M. and "
        "{Grollier}, F. and {Hagen}, A. and {Hirst}, P. and {Homeier}, D. "
        "and {Horton}, A.~J. and {Hosseinzadeh}, G. and {Hu}, L. and {Hunkeler}, "
        "J.~S. and {Ivezi{\\'c}}, {\\v{Z}}. and {Jain}, A. and {Jenness}, T. "
        "and {Kanarek}, G. and {Kendrew}, S. and {Kern}, N.~S. and {Kerzendorf}, "
        "W.~E. and {Khvalko}, A. and {King}, J. and {Kirkby}, D. and {Kulkarni}, "
        "A.~M. and {Kumar}, A. and {Lee}, A. and {Lenz}, D. and {Littlefair}, "
        "S.~P. and {Ma}, Z. and {Macleod}, D.~M. and {Mastropietro}, M. and "
        "{McCully}, C. and {Montagnac}, S. and {Morris}, B.~M. and {Mueller}, M. "
        " and {Mumford}, S.~J. and {Muna}, D. and {Murphy}, N.~A. and {Nelson}, S. "
        ' and {Nguyen}, G.~H. and {Ninan}, J.~P. and {N{"o}the}, M. and {Ogaz}, S. '
        "and {Oh}, S. and {Parejko}, J.~K. and {Parley}, N. and {Pascual}, S. and "
        "{Patil}, R. and {Patil}, A.~A. and {Plunkett}, A.~L. and {Prochaska}, J.~X. "
        "and {Rastogi}, T. and {Reddy Janga}, V. and {Sabater}, J. and {Sakurikar}, "
        "P. and {Seifert}, M. and {Sherbert}, L.~E. and {Sherwood-Taylor}, H. "
        " and {Shih}, A.~Y. and {Sick}, J. and {Silbiger}, M.~T. and "
        "{Singanamalla}, S. and {Singer}, L.~P. and {Sladen}, P.~H. and {Sooley}, "
        "K.~A. and {Sornarajah}, S. and {Streicher}, O. and {Teuben}, P. and "
        "{Thomas}, S.~W. and {Tremblay}, G.~R. and {Turner}, J.~E.~H. and "
        "{Terr{\\'o}n}, V. and {van Kerkwijk}, M.~H. and {de la Vega}, A. and "
        "{Watkins}, L.~L. and {Weaver}, B.~A. and {Whitmore}, J.~B. and {Woillez}, "
        "J. and {Zabalza}, V. and {Astropy Contributors}},"
    )
    print(
        'title = "{The Astropy Project: Building an Open-science Project '
        'and Status of the v2.0 Core Package}",'
    )
    print("journal = {\\aj},")
    print(
        "keywords = {methods: data analysis, methods: miscellaneous, "
        "methods: statistical, reference systems, Astrophysics - "
        "Instrumentation and Methods for Astrophysics},"
    )
    print("year = 2018,")
    print("month = sep,")
    print("volume = {156},")
    print("number = {3},")
    print("eid = {123},")
    print("pages = {123},")
    print("doi = {10.3847/1538-3881/aabc4f},")
    print("archivePrefix = {arXiv},")
    print("eprint = {1801.02634},")
    print("primaryClass = {astro-ph.IM},")
    print("adsurl = {https://ui.adsabs.harvard.edu/abs/2018AJ....156..123A},")
    print("adsnote = {Provided by the SAO/NASA Astrophysics Data System}")
    print("}")

    print("\n")
    print("@ARTICLE{2022ApJ...935..167A,")
    print(
        "author = {{Astropy Collaboration} and {Price-Whelan}, Adrian M. and "
        "{Lim}, Pey Lian and {Earl}, Nicholas and {Starkman}, Nathaniel and {Bradley}, "
        "Larry and {Shupe}, David L. and {Patil}, Aarya A. and {Corrales}, Lia and "
        '{Brasseur}, C.~E. and {N{\\"o}the}, Maximilian and {Donath}, Axel and '
        "{Tollerud}, Erik and {Morris}, Brett M. and {Ginsburg}, Adam and {Vaher}, "
        "Eero and {Weaver}, Benjamin A. and {Tocknell}, James and {Jamieson}, William "
        "and {van Kerkwijk}, Marten H. and {Robitaille}, Thomas P. and {Merry}, Bruce "
        'and {Bachetti}, Matteo and {G{\\"u}nther}, H. Moritz and {Aldcroft}, Thomas L. '
        "and {Alvarado-Montes}, Jaime A. and {Archibald}, Anne M. and {B{'o}di}, "
        "Attila and {Bapat}, Shreyas and {Barentsen}, Geert and {Baz{'a}n}, Juanjo "
        "and {Biswas}, Manish and {Boquien}, M{\\'e}d{\\'e}ric and {Burke}, D.~J. and "
        "{Cara}, Daria and {Cara}, Mihai and {Conroy}, Kyle E. and {Conseil}, Simon and "
        "{Craig}, Matthew W. and {Cross}, Robert M. and {Cruz}, Kelle L. and {D'Eugenio}, "
        'Francesco and {Dencheva}, Nadia and {Devillepoix}, Hadrien A.~R. and {Dietrich}, J{\\"o}rg P. '
        "and {Eigenbrot}, Arthur Davis and {Erben}, Thomas and {Ferreira}, Leonardo and "
        "{Foreman-Mackey}, Daniel and {Fox}, Ryan and {Freij}, Nabil and {Garg}, Suyog and {Geda}, "
        "Robel and {Glattly}, Lauren and {Gondhalekar}, Yash and {Gordon}, Karl D. and {Grant}, David "
        "and {Greenfield}, Perry and {Groener}, Austen M. and {Guest}, Steve and {Gurovich}, Sebastian "
        "and {Handberg}, Rasmus and {Hart}, Akeem and {Hatfield-Dodds}, Zac and {Homeier}, Derek and "
        "{Hosseinzadeh}, Griffin and {Jenness}, Tim and {Jones}, Craig K. and {Joseph}, Prajwel and "
        "{Kalmbach}, J. Bryce and {Karamehmetoglu}, Emir and {Ka{\\l}uszy{'n}ski}, Miko{\\l}aj and {Kelley}, "
        "Michael S.~P. and {Kern}, Nicholas and {Kerzendorf}, Wolfgang E. and {Koch}, Eric W. and "
        "{Kulumani}, Shankar and {Lee}, Antony and {Ly}, Chun and {Ma}, Zhiyuan and {MacBride}, Conor "
        "and {Maljaars}, Jakob M. and {Muna}, Demitri and {Murphy}, N.~A. and {Norman}, Henrik and {O'Steen}, Richard "
        "and {Oman}, Kyle A. and {Pacifici}, Camilla and {Pascual}, Sergio and {Pascual-Granado}, J. and "
        "{Patil}, Rohit R. and {Perren}, Gabriel I. and {Pickering}, Timothy E. and {Rastogi}, Tanuj and "
        "{Roulston}, Benjamin R. and {Ryan}, Daniel F. and {Rykoff}, Eli S. and {Sabater}, Jose and {Sakurikar}, "
        "Parikshit and {Salgado}, Jes{\\'u}s and {Sanghi}, Aniket and {Saunders}, Nicholas and {Savchenko}, "
        "Volodymyr and {Schwardt}, Ludwig and {Seifert-Eckert}, Michael and {Shih}, Albert Y. and {Jain}, "
        "Anany Shrey and {Shukla}, Gyanendra and {Sick}, Jonathan and {Simpson}, Chris and {Singanamalla}, "
        "Sudheesh and {Singer}, Leo P. and {Singhal}, Jaladh and {Sinha}, Manodeep and {Sip{\\H{o}}cz}, "
        "Brigitta M. and {Spitler}, Lee R. and {Stansby}, David and {Streicher}, Ole and {{\\v{S}}umak}, "
        "Jani and {Swinbank}, John D. and {Taranu}, Dan S. and {Tewary}, Nikita and {Tremblay}, Grant R. "
        "and {de Val-Borro}, Miguel and {Van Kooten}, Samuel J. and {Vasovi{\\'c}}, Zlatan and {Verma}, Shresth "
        "and {de Miranda Cardoso}, Jos{\\'e} Vin{\\'\\i}cius and {Williams}, Peter K.~G. and "
        "{Wilson}, Tom J. and {Winkel}, Benjamin and {Wood-Vasey}, W.~M. and {Xue}, "
        "Rui and {Yoachim}, Peter and {Zhang}, Chen and {Zonca}, Andrea and {Astropy Project Contributors}},"
    )
    print(
        'title = "{The Astropy Project: Sustaining and Growing a Community-oriented '
        'Open-source Project and the Latest Major Release (v5.0) of the Core Package}", '
    )
    print("journal = {\\apj},")
    print(
        "keywords = {Astronomy software, Open source software, Astronomy "
        "data analysis, 1855, 1866, 1858, Astrophysics - Instrumentation and "
        "Methods for Astrophysics},"
    )
    print("year = 2022,")
    print("month = aug,")
    print("volume = {935},")
    print("number = {2},")
    print("eid = {167},")
    print("pages = {167},")
    print("doi = {10.3847/1538-4357/ac7c74},")
    print("archivePrefix = {arXiv},")
    print("eprint = {2206.14220},")
    print("primaryClass = {astro-ph.IM},")
    print("adsurl = {https://ui.adsabs.harvard.edu/abs/2022ApJ...935..167A},")
    print("adsnote = {Provided by the SAO/NASA Astrophysics Data System}")
    print("}")

    print("\nHealpy:\n")
    print("@article{Zonca2019,")
    print("doi = {10.21105/joss.01298},")
    print("url = {https://doi.org/10.21105/joss.01298},")
    print("year = {2019},")
    print("month = mar,")
    print("publisher = {The Open Journal},")
    print("volume = {4},")
    print("number = {35},")
    print("pages = {1298},")
    print(
        "author = {Andrea Zonca and Leo Singer and Daniel Lenz and Martin Reinecke "
        "and Cyrille Rosset and Eric Hivon and Krzysztof Gorski},"
    )
    print(
        "title = {healpy: equal area pixelization and spherical harmonics transforms for data on the sphere in Python},"
    )
    print("journal = {Journal of Open Source Software}")
    print("}")

    print("\n")

    print("@ARTICLE{2005ApJ...622..759G,")
    print("author = {{G{'o}rski}, K.~M. and {Hivon}, E. and {Banday}, A.~J. and ")
    print("{Wandelt}, B.~D. and {Hansen}, F.~K. and {Reinecke}, M. and ")
    print("{Bartelmann}, M.},")
    print(
        'title = "{HEALPix: A Framework for High-Resolution Discretization '
        'and Fast Analysis of Data Distributed on the Sphere}",'
    )
    print("journal = {\\apj},")
    print("eprint = {arXiv:astro-ph/0409513},")
    print(
        "keywords = {Cosmology: Cosmic Microwave Background, Cosmology: Observations, Methods: Statistical},"
    )
    print("year = 2005,")
    print("month = apr,")
    print("volume = 622,")
    print("pages = {759-771},")
    print("doi = {10.1086/427976},")
    print("adsurl = {http://adsabs.harvard.edu/abs/2005ApJ...622..759G},")
    print("adsnote = {Provided by the SAO/NASA Astrophysics Data System}")
    print("}")

    print("\n")

    print(
        "Add an acknowledgment statement: “Some of the results in this "
        "paper have been derived using the healpy and HEALPix packages”."
    )
    print("\n")

    print(
        "At the first use of the HEALPix acronym, a footnote placed in the"
        " main body of the paper referring to the HEALPix web site, "
        "currently http://healpix.sf.net"
    )

    print("\nJupyter Notebooks:\n")
    print("@inproceedings{soton403913,")
    print("booktitle = {Positioning and Power in Academic Publishing: Players, Agents and Agendas},")
    print("title = {Jupyter Notebooks ? a publishing format for reproducible computational workflows},")
    print(
        "author = {Thomas Kluyver and Benjamin Ragan-Kelley and Fernando P{\\'e}rez "
        "and Brian Granger and Matthias Bussonnier and Jonathan Frederic and Kyle Kelley "
        "and Jessica Hamrick and Jason Grout and Sylvain Corlay and Paul Ivanov "
        "and Dami{\\'a}n Avila and Safia Abdalla and Carol Willing and  Jupyter development team},"
    )
    print("publisher = {IOS Press},")
    print("year = {2016},")
    print("pages = {87--90},")
    print("url = {https://eprints.soton.ac.uk/403913/},")
    print("}")

    print("\nmatplotlib:\n")
    print("@Article{Hunter:2007,")
    print("  Author    = {Hunter, J. D.},")
    print("Title     = {Matplotlib: A 2D graphics environment},")
    print("Journal   = {Computing in Science \\& Engineering},")
    print("Volume    = {9},")
    print("Number    = {3},")
    print("Pages     = {90--95},")
    print("abstract  = {Matplotlib is a 2D graphics package used for Python for ")
    print("application development, interactive scripting, and publication-quality ")
    print("image generation across user interfaces and operating systems.},")
    print("publisher = {IEEE COMPUTER SOC},")
    print("doi       = {10.1109/MCSE.2007.55},")
    print("year      = 2007")
    print("}")

    print("\nMinor Planet Center Resources:\n")

    print(
        "Add an acknowledgment statement: This research has made use of data and/or services provided by the International Astronomical Union's Minor Planet Center. "
    )

    print("\nNASA ADS:\n")
    print(
        "Add an acknowledgment statement: This research has made use of "
        "NASA’s Astrophysics Data System Bibliographic Services. "
    )

    print("\nNumba:\n")
    print("@INPROCEEDINGS{2015llvm.confE...1L,")
    print("author = {{Lam}, Siu Kwan and {Pitrou}, Antoine and {Seibert}, Stanley},")
    print('title = "{Numba: A LLVM-based Python JIT Compiler}",')
    print("keywords = {LLVM, Python, Compiler},")
    print("booktitle = {Proc. Second Workshop on the LLVM Compiler Infrastructure in HPC},")
    print(" year = 2015,")
    print("month = nov,")
    print("pages = {1-6},")
    print("doi = {10.1145/2833157.2833162},")
    print("adsurl = {https://ui.adsabs.harvard.edu/abs/2015llvm.confE...1L},")
    print("adsnote = {Provided by the SAO/NASA Astrophysics Data System}")
    print("}")

    print("\nNumpy:\n")
    print("@Article{         harris2020array,")
    print("title         = {Array programming with {NumPy}},")
    print(
        "author        = {Charles R. Harris and K. Jarrod Millman "
        "and St{\\'{e}}fan J. van der Walt and Ralf Gommers and "
        "Pauli Virtanen and David Cournapeau and Eric Wieser and "
        "Julian Taylor and Sebastian Berg and Nathaniel J. Smith and "
        "Robert Kern and Matti Picus and Stephan Hoyer and Marten H. "
        "van Kerkwijk and Matthew Brett and Allan Haldane and Jaime "
        "Fern{\\'{a}}ndez del R{\\'{i}}o and Mark Wiebe and "
        "Pearu Peterson and Pierre G{\\'{e}}rard-Marchant and Kevin "
        "Sheppard and Tyler Reddy and Warren Weckesser and Hameer Abbasi "
        "and Christoph Gohlke and Travis E. Oliphant},"
    )
    print("year          = {2020},")
    print("month         = sep,")
    print("journal       = {Nature},")
    print("volume        = {585},")
    print("number        = {7825},")
    print("pages         = {357--362},")
    print("doi           = {10.1038/s41586-020-2649-2},")
    print("publisher     = {Springer Science and Business Media {LLC}},")
    print("url           = {https://doi.org/10.1038/s41586-020-2649-2}")
    print("}")

    print("\nPandas:\n")
    print("@InProceedings{ mckinney-proc-scipy-2010,")
    print("author    = { {W}es {M}c{K}inney },")
    print("title     = { {D}ata {S}tructures for {S}tatistical {C}omputing in {P}ython },")
    print("booktitle = { {P}roceedings of the 9th {P}ython in {S}cience {C}onference },")
    print("pages     = { 56 - 61 },")
    print("year      = { 2010 },")
    print("editor    = { {S}t{\\'{e}}fan van der {W}alt and {J}arrod {M}illman },")
    print("doi       = { 10.25080/Majora-92bf1922-00a }")
    print("}")

    print("\n")
    print("Update to the exact version you have installed. Below is the generic Zenodo link reference. \n")
    print("@software{reback2020pandas,")
    print("author       = {The pandas development team},")
    print("title        = {pandas-dev/pandas: Pandas},")
    print("month        = feb,")
    print("year         = 2020,")
    print("publisher    = {Zenodo},")
    print("version      = {latest},")
    print("doi          = {10.5281/zenodo.3509134},")
    print("url          = {https://doi.org/10.5281/zenodo.3509134}")
    print("}")

    print("\nPooch:\n")
    print("@article{uieda2020,")
    print("title = {{Pooch}: {A} friend to fetch your data files},")
    print(
        "author = {Leonardo Uieda and Santiago Soler and R{\\'{e}}mi Rampin "
        "and Hugo van Kemenade and Matthew Turk and Daniel Shapero and "
        "Anderson Banihirwe and John Leeman},"
    )
    print("year = {2020},")
    print("doi = {10.21105/joss.01943},")
    print("url = {https://doi.org/10.21105/joss.01943},")
    print("month = jan,")
    print("publisher = {The Open Journal},")
    print("volume = {5},")
    print(" number = {45},")
    print("pages = {1943},")
    print("journal = {Journal of Open Source Software}")
    print("}")

    print("\nPytables\n")
    print("@Misc{pytables,")
    print("author = {PyTables Developers Team},")
    print("title = {{PyTables}: Hierarchical Datasets in {Python}},")
    print("year = {2002--},")
    print('url = "https://www.pytables.org/",')
    print("}")

    print("\nREBOUND:\n")
    sim = rebound.Simulation()
    sim.cite()

    print("\nAdapted Functions From rubin_sim:\n")

    print("@software{peter_yoachim_2022_7087823,")
    print("author       = {Peter Yoachim and")
    print("R. Lynne Jones and")
    print("Eric H. Neilsen and")
    print("Tiago Ribeiro and")
    print("Scott Daniel and")
    print("Natasha Abrams and")
    print("Husni Almoubayyed and")
    print("Igor Andreoni and")
    print("Humna Awan and")
    print("Matthew R. Becker and")
    print(" Keaton Bell and")
    print("Eric Bellm and")
    print("Federica Bianco and")
    print("Johan Bregeon and")
    print("Katja Bricman and")
    print("Owen Boberg and")
    print("Jeff Carlin and")
    print("YuChia Chen and")
    print("Will Clarkson and")
    print("Andrew Connolly and")
    print("Philippe Gris and")
    print("Alina Hu and")
    print("Michael Kelley and")
    print("Somayeh Khakpash and")
    print("Simon Krughoff and")
    print("Xiaolong Li and")
    print("Michael B. Lund and")
    print("Phil Marshall and")
    print("Josh Meyers and")
    print("Loredana Prisinzano and")
    print("Elahesadat Naghib and")
    print("Meredith Rawls and")
    print("Michael Reuter and")
    print("Daniel Rothchild and")
    print("Christian N. Setzer and")
    print("Jonathan Sick and")
    print(" Rachel Street},")
    print("title        = {lsst/rubin\\_sim: 0.12.1},")
    print("month        = sep,")
    print("year         = 2022,")
    print("publisher    = {Zenodo},")
    print("version      = {0.12.1},")
    print("doi          = {10.5281/zenodo.7087823},")
    print("url          = {https://doi.org/10.5281/zenodo.7087823}")
    print("}")

    print("\n")

    print("@ARTICLE{2018Icar..303..181J,")
    print(
        "author = {{Jones}, R. Lynne and {Slater}, Colin T. and {Moeyens}, "
        "Joachim and {Allen}, Lori and {Axelrod}, Tim and {Cook}, Kem and "
        "{Ivezi{\\'c}}, {\v{Z}}eljko and {Juri{\\'c}}, Mario and {Myers}, Jonathan "
        "and {Petry}, Catherine E.},"
    )
    print('title = "{The Large Synoptic Survey Telescope as a Near-Earth Object discovery machine}",')
    print("journal = {\\icarus},")
    print(
        "keywords = {Near-Earth objects, Image processing, Asteroids, "
        "Earth Science, Astrophysics - Earth and Planetary Astrophysics, "
        "Astrophysics - Instrumentation and Methods for Astrophysics},"
    )
    print("year = 2018,")
    print("month = mar,")
    print("volume = {303},")
    print("pages = {181-202},")
    print("doi = {10.1016/j.icarus.2017.11.033},")
    print("archivePrefix = {arXiv},")
    print("eprint = {1711.10621},")
    print(" primaryClass = {astro-ph.EP},")
    print("adsurl = {https://ui.adsabs.harvard.edu/abs/2018Icar..303..181J},")
    print(" adsnote = {Provided by the SAO/NASA Astrophysics Data System}")
    print("}")

    print("\nsbpy:\n")
    print("@ARTICLE{2019JOSS....4.1426M,")
    print(
        "author = {{Mommert}, Michael and {Kelley}, Michael and {de Val-Borro}, Miguel "
        "and {Li}, Jian-Yang and {Guzman}, Giannina and {Sip{\\H{o}}cz}, Brigitta and "
        "{{\\v{D}}urech}, Josef and {Granvik}, Mikael and {Grundy}, Will and {Moskovitz}, Nick "
        'and {Penttil{\\"a}}, Antti and {Samarasinha}, Nalin},'
    )
    print('title = "{sbpy: A Python module for small-body planetary astronomy}",')
    print("journal = {The Journal of Open Source Software},")
    print(
        "keywords = {comets, kuiper belt objects, Python, trans-neptunian objects, "
        "centaurs, planetary science, python, solar system, asteroids, meteoroids, "
        "trojans, astronomy, small bodies},"
    )
    print("year = 2019,")
    print("month = aug,")
    print("volume = {4},")
    print("number = {38},")
    print("eid = {1426},")
    print("pages = {1426},")
    print("doi = {10.21105/joss.01426},")
    print("adsurl = {https://ui.adsabs.harvard.edu/abs/2019JOSS....4.1426M},")
    print("adsnote = {Provided by the SAO/NASA Astrophysics Data System}")
    print("}")

    print("\nSciPy:\n")
    print("@ARTICLE{2020SciPy-NMeth,")
    print("author  = {Virtanen, Pauli and Gommers, Ralf and Oliphant, Travis E. and ")
    print("Haberland, Matt and Reddy, Tyler and Cournapeau, David and ")
    print("Burovski, Evgeni and Peterson, Pearu and Weckesser, Warren and ")
    print("Bright, Jonathan and {van der Walt}, St{\\'{e}}fan J. and ")
    print("Brett, Matthew and Wilson, Joshua and Millman, K. Jarrod and ")
    print("Mayorov, Nikolay and Nelson, Andrew R. J. and Jones, Eric and ")
    print("Kern, Robert and Larson, Eric and Carey, C J and ")
    print("Polat, {\\.I}lhan and Feng, Yu and Moore, Eric W. and ")
    print("{VanderPlas}, Jake and Laxalde, Denis and Perktold, Josef and ")
    print("Cimrman, Robert and Henriksen, Ian and Quintero, E. A. and ")
    print("Harris, Charles R. and Archibald, Anne M. and ")
    print("Ribeiro, Ant{\\^o}nio H. and Pedregosa, Fabian and ")
    print("{van Mulbregt}, Paul and {SciPy 1.0 Contributors}},")
    print("title   = {{{SciPy} 1.0: Fundamental Algorithms for Scientific ")
    print("Computing in Python}},")
    print("journal = {Nature Methods},")
    print("year    = {2020},")
    print("volume  = {17},")
    print("pages   = {261--272},")
    print("adsurl  = {https://rdcu.be/b08Wh},")
    print("doi     = {10.1038/s41592-019-0686-2},")

    print("}")

    print("\nSpice Resources:\n")
    print(" @ARTICLE{1996P&SS...44...65A,")
    print("author = {{Acton}, Charles H.},")
    print("title = {Ancillary data services of  " "NASA's Navigation and Ancillary Information Facility},")
    print("journal = {\\planss},")
    print("year = 1996,")
    print("month = jan,")
    print("volume = {44},")
    print("number = {1},")
    print("pages = {65-70},")
    print("doi = {10.1016/0032-0633(95)00107-7},")
    print("adsurl = {https://ui.adsabs.harvard.edu/abs/1996P&SS...44...65A},")
    print("adsnote = {Provided by the SAO/NASA Astrophysics Data System}")
    print("}")

    print("\n")

    print("@ARTICLE{2018P&SS..150....9A,")
    print("author = {{Acton}, Charles and {Bachman}, Nathaniel and {Semenov}, Boris and {Wright}, Edward},")
    print('title = "{A look towards the future in the handling of space science mission geometry}",')
    print("journal = {\\planss},")
    print("year = 2018,")
    print("month = jan,")
    print("volume = {150},")
    print("pages = {9-12},")
    print("doi = {10.1016/j.pss.2017.02.013},")
    print("adsurl = {https://ui.adsabs.harvard.edu/abs/2018P&SS..150....9A},")
    print("adsnote = {Provided by the SAO/NASA Astrophysics Data System} ")
    print("}")

    print(
        "\nAdd an acknowledgment statement:  The SPICE Resource files used in this work ere described in \\citep{1996P&SS...44...65A, 2018P&SS..150....9A}"
    )

    print("\nSpiceypy:\n")
    print("@ARTICLE{2020JOSS....5.2050A,")
    print(
        "author = {{Annex}, Andrew and {Pearson}, Ben and {Seignovert}, "
        "Beno{\\^\\i}t and {Carcich}, Brian and {Eichhorn}, Helge and {Mapel}, "
        "Jesse and {von Forstner}, Johan and {McAuliffe}, Jonathan and "
        "{del Rio}, Jorge and {Berry}, Kristin and {Aye}, K. -Michael and "
        "{Stefko}, Marcel and {de Val-Borro}, Miguel and {Kulumani}, Shankar "
        "and {Murakami}, Shin-ya}, "
    )
    print('title = "{SpiceyPy: a Pythonic Wrapper for the SPICE Toolkit}",')
    print("journal = {The Journal of Open Source Software},")
    print("keywords = {geometry, Python, spacecraft, Batchfile, planets, ephemeris, navigation, SPICE},")
    print("year = 2020,")
    print("month = feb,")
    print("volume = {5},")
    print("number = {46},")
    print(" eid = {2050},")
    print("pages = {2050},")
    print("doi = {10.21105/joss.02050},")
    print("adsurl = {https://ui.adsabs.harvard.edu/abs/2020JOSS....5.2050A},")
    print("adsnote = {Provided by the SAO/NASA Astrophysics Data System}")
    print("}")

    print("\ntqdm:\n")
    print("@software{casper_da_costa_luis_2023_8233425,")
    print("author       = {Casper da Costa-Luis and")
    print("Stephen Karl Larroque and")
    print("Kyle Altendorf and")
    print("Hadrien Mary and")
    print("richardsheridan and")
    print("Mikhail Korobov and")
    print("Noam Yorav-Raphael and")
    print("Ivan Ivanov and")
    print("Marcel Bargull and")
    print("Nishant Rodrigues and")
    print("Guangshuo Chen and")
    print("Antony Lee and")
    print("Charles Newey and")
    print("CrazyPython and")
    print("JC and")
    print("Martin Zugnoni and")
    print("Matthew D. Pagel and")
    print("mjstevens777 and")
    print("Mikhail Dektyarev and")
    print("Alex Rothberg and")
    print(" Alexander Plavin and")
    print("Fabian Dill and")
    print("FichteFoll and")
    print("Gregor Sturm and")
    print("HeoHeo and")
    print("Hugo van Kemenade and")
    print("Jack McCracken and")
    print("MapleCCC and")
    print("Max Nordlund and")
    print("Mike Boyle},")
    print("title        = {{tqdm: A fast, Extensible Progress Bar for Python ")
    print("and CLI}},")
    print("month        = aug,")
    print("year         = 2023,")
    print(" publisher    = {Zenodo},")
    print(" version      = {v4.66.1},")
    print("doi          = {10.5281/zenodo.8233425},")
    print("url          = {https://doi.org/10.5281/zenodo.8233425}")
    print("}")

    print("\nIf using a rubin_sim simulated survey pointing database:\n")
    print(
        "Add an acknowledgment statement: This material or work is supported in part by the National Science  "
        "Foundation through Cooperative Agreement AST-1258333 and "
        "Cooperative Support Agreement AST1836783 managed by the Association "
        "of Universities for Research in Astronomy (AURA), and the Department "
        "of Energy under Contract No. DE-AC02-76SF00515 with the SLAC National "
        "Accelerator Laboratory managed by Stanford University."
    )

    print("\n")
    print(
        "If you are submitting a paper to AAS Journals, here is"
        " the software citation latex command you will need once you have included "
        "all of the above  bibtex references above.\n"
    )

    print(
        "\\software{"
        "Sorcha,"
        "ASSIST \\citep{2023PSJ.....4...69H,hanno_rein_2023_7778017},"
        "Astropy \\citep{2013A&A...558A..33A,2018AJ....156..123A,2022ApJ...935..167A}, "
        "Healpy \\citep{Zonca2019,2005ApJ...622..759G}, "
        "Matplotlib \\citep{Hunter:2007}, "
        "Numba \\citep{2015llvm.confE...1L}, "
        "Numpy \\citep{harris2020array}, "
        "pandas \\citep{mckinney-proc-scipy-2010, reback2020pandas}, "
        "Pooch \\citep{uieda2020}, "
        "PyTables \\citep{pytables}, "
        "REBOUND \\citep{rebound,reboundias15}, "
        "rubin$\\_$sim \\citep{2018Icar..303..181J,peter_yoachim_2022_7087823}, "
        "sbpy \\citep{2019JOSS....4.1426M}, "
        "SciPy \\citep{2020SciPy-NMeth}, "
        "Spiceypy \\citep{2020JOSS....5.2050A}, "
        "sqlite (\\url{https://www.sqlite.org/index.html}), "
        "sqlite3 (\\url{https://docs.python.org/3/library/sqlite3.html}), "
        "tqdm \\citep{casper_da_costa_luis_2023_8233425}, "
        "Black (\\url{https://black.readthedocs.io/en/stable/faq.html}), "
        "Jupyter Notebooks \\citep{soton403913}}"
    )
