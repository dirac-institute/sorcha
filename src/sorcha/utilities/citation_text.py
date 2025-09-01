import rebound
import sys


def cite_sorcha(f=sys.stdout):
    """Providing the bibtex, AAS Journals software latex command, and acknowledgement
    statements for Sorcha and the associated packages that power it.

    Parameters
    -----------
    f: file-like object, default=sys.stdout
        The output for where the citation information will be written.

    Returns
    -----------
    None
    """

    f.write("\nSorcha: \n\n")
    f.write("@ARTICLE{2025AJ....170..100M,\n")
    f.write("author = {{Merritt}, Stephanie R. and {Fedorets}, Grigori and {Schwamb}, Megan E. and {Cornwall}, Samuel and {Bernardinelli}, Pedro H. and {Juri{\'c}}, Mario and {Holman}, Matthew J. and {Kurlander}, Jacob A. and {Eggl}, Siegfried and {Oldag}, Drew and {West}, Maxine and {Kubica}, Jeremy and {Murtagh}, Joseph and {Jones}, R. Lynne and {Yoachim}, Peter and {Lyttle}, Ryan R. and {Kelley}, Michael S.~P. and {Moeyens}, Joachim and {Kiker}, Kathleen and {Naidu}, Shantanu P. and {Snodgrass}, Colin and {Matthews}, Shannon M. and {Chandler}, Colin Orion},\n")
    f.write('title = "{Sorcha: A Solar System Survey Simulator for the Legacy Survey of Space and Time}"\n,')
    f.write("journal = {\\aj},\n")
    f.write("keywords = {Solar system astronomy, Small Solar System bodies, Astronomy software, Astronomical simulations, 1529, 1469, 1855, 1857, Earth and Planetary Astrophysics, Instrumentation and Methods for Astrophysics},\n")
    f.write("year = 2025,\n")
    f.write("month = aug,\n")
    f.write("volume = {170},\n")
    f.write("number = {2},\n")
    f.write("eid = {100},\n")
    f.write("pages = {100},\n")
    f.write("doi = {10.3847/1538-3881/add3ec},\n")
    f.write("archivePrefix = {arXiv},\n")
    f.write("eprint = {2506.02804},\n")
    f.write("primaryClass = {astro-ph.EP},\n")
    f.write("adsurl = {https://ui.adsabs.harvard.edu/abs/2025AJ....170..100M},\n")
    f.write("adsnote = {Provided by the SAO/NASA Astrophysics Data System}\n")
    f.write("}\n")


    f.write("\n\n")

    f.write("@ARTICLE{2025AJ....170...97H,\n")
    f.write("author = {{Holman}, Matthew J. and {Bernardinelli}, Pedro H. and {Schwamb}, Megan E. and {Juri{\'c}}, Mario and {Oldag}, Drew and {West}, Maxine and {Napier}, Kevin J. and {Merritt}, Stephanie R. and {Fedorets}, Grigori and {Cornwall}, Samuel and {Kurlander}, Jacob A. and {Eggl}, Siegfried and {Kubica}, Jeremy and {Kiker}, Kathleen and {Murtagh}, Joseph and {Naidu}, Shantanu P. and {Chandler}, Colin Orion},\n")
    f.write('title = "{Sorcha: Optimized Solar System Ephemeris Generation}",\n')
    f.write("journal = {\\aj},\n")
    f.write("keywords = {Ephemerides, Small Solar System bodies, N-body simulations, Sky surveys, 464, 1469, 1083, 1464, Earth and Planetary Astrophysics, Instrumentation and Methods for Astrophysics, Computational Physics},\n")
    f.write("year = 2025,\n")
    f.write("month = aug,\n")
    f.write("volume = {170},\n")
    f.write("number = {2},\n")
    f.write("eid = {97},\n")
    f.write("pages = {97},\n")
    f.write("doi = {10.3847/1538-3881/ade435},\n")
    f.write("archivePrefix = {arXiv},\n")
    f.write("eprint = {2506.02140},\n")
    f.write("primaryClass = {astro-ph.EP},\n")
    f.write(" adsurl = {https://ui.adsabs.harvard.edu/abs/2025AJ....170...97H},\n")
    f.write(" adsnote = {Provided by the SAO/NASA Astrophysics Data System}\n")
    f.write("}\n")



    f.write("\n\n")

    f.write("Please also cite the packages that are utilized by Sorcha:\n")

    f.write("\nASSIST:\n\n")

    f.write("@ARTICLE{2023PSJ.....4...69H,\n")
    f.write(
        "author = {{Holman}, Matthew J. and {Akmal}, Arya and {Farnocchia},"
        " Davide and {Rein}, Hanno and {Payne}, Matthew J. and {Weryk}, Robert"
        " and {Tamayo}, Daniel and {Hernandez}, David M.},\n"
    )
    f.write('title = "{ASSIST: An Ephemeris-quality Test-particle Integrator}",\n')
    f.write("journal = {\\psj},\n")
    f.write(
        "keywords = {Ephemerides, N-body simulations, Asteroid dynamics, "
        "Comet dynamics, 464, 1083, 2210, 2213, Astrophysics - Earth and Planetary Astrophysics,"
        "Astrophysics - Instrumentation and Methods for Astrophysics},\n"
    )
    f.write("year = 2023,\n")
    f.write("month = apr,\n")
    f.write("volume = {4},\n")
    f.write("number = {4},\n")
    f.write("eid = {69},\n")
    f.write("pages = {69},\n")
    f.write("doi = {10.3847/PSJ/acc9a9},\n")
    f.write("archivePrefix = {arXiv},\n")
    f.write("eprint = {2303.16246},\n")
    f.write("primaryClass = {astro-ph.EP},\n")
    f.write("adsurl = {https://ui.adsabs.harvard.edu/abs/2023PSJ.....4...69H},\n")
    f.write("adsnote = {Provided by the SAO/NASA Astrophysics Data System}\n")
    f.write("}\n")

    f.write("\n\n")

    f.write("@software{hanno_rein_2023_7778017,\n")
    f.write("author       = {Hanno Rein and matthewholman and Arya Akmal},\n")
    f.write("title        = {matthewholman/assist: v1.1.1},\n")
    f.write("month        = mar,\n")
    f.write("year         = 2023,\n")
    f.write("publisher    = {Zenodo},\n")
    f.write("version      = {v1.1.1},\n")
    f.write("doi          = {10.5281/zenodo.7778017},\n")
    f.write("url          = {https://doi.org/10.5281/zenodo.7778017}\n")
    f.write("}\n")

    f.write("\nAstropy:\n\n")
    f.write("@ARTICLE{2013A&A...558A..33A,\n")
    f.write(
        "author = {{Astropy Collaboration} and {Robitaille}, Thomas P. \n"
        "and {Tollerud}, Erik J. and {Greenfield}, Perry and {Droettboom}, \n"
        " Michael and {Bray}, Erik and {Aldcroft}, Tom and {Davis}, Matt \n"
        "and {Ginsburg}, Adam and {Price-Whelan}, Adrian M. and {Kerzendorf}, \n"
        " Wolfgang E. and {Conley}, Alexander and {Crighton}, Neil and \n"
        "{Barbary}, Kyle and {Muna}, Demitri and {Ferguson}, Henry \n"
        " and {Grollier}, Fr{\\'e}d{\\'e}ric and {Parikh}, Madhura M. \n"
        "and {Nair}, Prasanth H. and {Unther}, Hans M. and {Deil}, Christoph \n"
        " and {Woillez}, Julien and {Conseil}, Simon and {Kramer}, Roban \n"
        "and {Turner}, James E.~H. and {Singer}, Leo and {Fox}, Ryan and \n"
        "{Weaver}, Benjamin A. and {Zabalza}, Victor and {Edwards}, \n"
        "Zachary I. and {Azalee Bostroem}, K. and {Burke}, D.~J. and {Casey}, \n"
        "Andrew R. and {Crawford}, Steven M. and {Dencheva}, Nadia and {Ely},\n"
        "Justin and {Jenness}, Tim and {Labrie}, Kathleen and {Lim}, Pey Lian and \n"
        "{Pierfederici}, Francesco and {Pontzen}, Andrew and {Ptak}, Andy \n"
        " and {Refsdal}, Brian and {Servillat}, Mathieu and {Streicher}, Ole},\n"
    )
    f.write('title = "{Astropy: A community Python package for astronomy}",\n')
    f.write("journal = {\\aap},\n")
    f.write(
        "keywords = {methods: data analysis, methods: miscellaneous, "
        "virtual observatory tools, Astrophysics - Instrumentation and "
        "Methods for Astrophysics},\n"
    )
    f.write("year = 2013,\n")
    f.write("month = oct,\n")
    f.write("volume = {558},\n")
    f.write("eid = {A33},\n")
    f.write("pages = {A33},\n")
    f.write("doi = {10.1051/0004-6361/201322068},\n")
    f.write("archivePrefix = {arXiv},\n")
    f.write("eprint = {1307.6212},\n")
    f.write("primaryClass = {astro-ph.IM},\n")
    f.write("adsurl = {https://ui.adsabs.harvard.edu/abs/2013A&A...558A..33A},\n")
    f.write("adsnote = {Provided by the SAO/NASA Astrophysics Data System}\n")
    f.write("}\n")

    f.write("\n\n")
    f.write("@ARTICLE{2018AJ....156..123A,\n")
    f.write(
        "author = {{Astropy Collaboration} and {Price-Whelan}, A.~M. \n"
        'and {Sip{\\H{o}}cz}, B.~M. and {G{\\"u}nther}, H.~M. and {Lim}, P.~L. \n'
        "and {Crawford}, S.~M. and {Conseil}, S. and {Shupe}, D.~L. and \n"
        "{Craig}, M.~W. and {Dencheva}, N. and {Ginsburg}, A. and \n"
        "{VanderPlas}, J.~T. and {Bradley}, L.~D. and {P{'e}rez-Su{'a}rez}, D. \n"
        "and {de Val-Borro}, M. and {Aldcroft}, T.~L. and {Cruz}, K.~L. and \n"
        "{Robitaille}, T.~P. and {Tollerud}, E.~J. and {Ardelean}, C. and \n"
        "{Babej}, T. and {Bach}, Y.~P. and {Bachetti}, M. and {Bakanov}, \n"
        "A.~V. and {Bamford}, S.~P. and {Barentsen}, G. and {Barmby}, \n"
        " P. and {Baumbach}, A. and {Berry}, K.~L. and {Biscani}, F. and {Boquien}, \n"
        "M. and {Bostroem}, K.~A. and {Bouma}, L.~G. and {Brammer}, G.~B. and \n"
        " {Bray}, E.~M. and {Breytenbach}, H. and {Buddelmeijer}, H. and \n"
        "{Burke}, D.~J. and {Calderone}, G. and {Cano Rodr{\\'\\i}guez}, J.~L. \n"
        "and {Cara}, M. and {Cardoso}, J.~V.~M. and {Cheedella}, S. and {Copin}, \n"
        "Y. and {Corrales}, L. and {Crichton}, D. and {D'Avella}, D. and {Deil}, \n"
        "C. and {Depagne}, {'E}. and {Dietrich}, J.~P. and {Donath}, A. and \n"
        "{Droettboom}, M. and {Earl}, N. and {Erben}, T. and {Fabbro}, S. and \n"
        "{Ferreira}, L.~A. and {Finethy}, T. and {Fox}, R.~T. and {Garrison}, \n"
        "L.~H. and {Gibbons}, S.~L.~J. and {Goldstein}, D.~A. and {Gommers}, R. \n"
        "and {Greco}, J.~P. and {Greenfield}, P. and {Groener}, A.~M. and \n"
        "{Grollier}, F. and {Hagen}, A. and {Hirst}, P. and {Homeier}, D. \n"
        "and {Horton}, A.~J. and {Hosseinzadeh}, G. and {Hu}, L. and {Hunkeler}, \n"
        "J.~S. and {Ivezi{\\'c}}, {\\v{Z}}. and {Jain}, A. and {Jenness}, T. \n"
        "and {Kanarek}, G. and {Kendrew}, S. and {Kern}, N.~S. and {Kerzendorf}, \n"
        "W.~E. and {Khvalko}, A. and {King}, J. and {Kirkby}, D. and {Kulkarni}, \n"
        "A.~M. and {Kumar}, A. and {Lee}, A. and {Lenz}, D. and {Littlefair}, \n"
        "S.~P. and {Ma}, Z. and {Macleod}, D.~M. and {Mastropietro}, M. and \n"
        "{McCully}, C. and {Montagnac}, S. and {Morris}, B.~M. and {Mueller}, M. \n"
        " and {Mumford}, S.~J. and {Muna}, D. and {Murphy}, N.~A. and {Nelson}, S. \n"
        ' and {Nguyen}, G.~H. and {Ninan}, J.~P. and {N{"o}the}, M. and {Ogaz}, S. \n'
        "and {Oh}, S. and {Parejko}, J.~K. and {Parley}, N. and {Pascual}, S. and \n"
        "{Patil}, R. and {Patil}, A.~A. and {Plunkett}, A.~L. and {Prochaska}, J.~X. \n"
        "and {Rastogi}, T. and {Reddy Janga}, V. and {Sabater}, J. and {Sakurikar}, \n"
        "P. and {Seifert}, M. and {Sherbert}, L.~E. and {Sherwood-Taylor}, H. \n"
        " and {Shih}, A.~Y. and {Sick}, J. and {Silbiger}, M.~T. and \n"
        "{Singanamalla}, S. and {Singer}, L.~P. and {Sladen}, P.~H. and {Sooley}, \n"
        "K.~A. and {Sornarajah}, S. and {Streicher}, O. and {Teuben}, P. and \n"
        "{Thomas}, S.~W. and {Tremblay}, G.~R. and {Turner}, J.~E.~H. and \n"
        "{Terr{\\'o}n}, V. and {van Kerkwijk}, M.~H. and {de la Vega}, A. and \n"
        "{Watkins}, L.~L. and {Weaver}, B.~A. and {Whitmore}, J.~B. and {Woillez}, \n"
        "J. and {Zabalza}, V. and {Astropy Contributors}},\n"
    )
    f.write(
        'title = "{The Astropy Project: Building an Open-science Project '
        'and Status of the v2.0 Core Package}",\n'
    )
    f.write("journal = {\\aj},\n")
    f.write(
        "keywords = {methods: data analysis, methods: miscellaneous, "
        "methods: statistical, reference systems, Astrophysics - "
        "Instrumentation and Methods for Astrophysics},\n"
    )
    f.write("year = 2018,\n")
    f.write("month = sep,\n")
    f.write("volume = {156},\n")
    f.write("number = {3},\n")
    f.write("eid = {123},\n")
    f.write("pages = {123},\n")
    f.write("doi = {10.3847/1538-3881/aabc4f},\n")
    f.write("archivePrefix = {arXiv},\n")
    f.write("eprint = {1801.02634},\n")
    f.write("primaryClass = {astro-ph.IM},\n")
    f.write("adsurl = {https://ui.adsabs.harvard.edu/abs/2018AJ....156..123A},\n")
    f.write("adsnote = {Provided by the SAO/NASA Astrophysics Data System}\n")
    f.write("}\n")

    f.write("\n\n")
    f.write("@ARTICLE{2022ApJ...935..167A,\n")
    f.write(
        "author = {{Astropy Collaboration} and {Price-Whelan}, Adrian M. and \n"
        "{Lim}, Pey Lian and {Earl}, Nicholas and {Starkman}, Nathaniel and {Bradley}, \n"
        "Larry and {Shupe}, David L. and {Patil}, Aarya A. and {Corrales}, Lia and \n"
        '{Brasseur}, C.~E. and {N{\\"o}the}, Maximilian and {Donath}, Axel and \n'
        "{Tollerud}, Erik and {Morris}, Brett M. and {Ginsburg}, Adam and {Vaher}, \n"
        "Eero and {Weaver}, Benjamin A. and {Tocknell}, James and {Jamieson}, William \n"
        "and {van Kerkwijk}, Marten H. and {Robitaille}, Thomas P. and {Merry}, Bruce \n"
        'and {Bachetti}, Matteo and {G{\\"u}nther}, H. Moritz and {Aldcroft}, Thomas L. \n'
        "and {Alvarado-Montes}, Jaime A. and {Archibald}, Anne M. and {B{'o}di}, \n"
        "Attila and {Bapat}, Shreyas and {Barentsen}, Geert and {Baz{'a}n}, Juanjo \n"
        "and {Biswas}, Manish and {Boquien}, M{\\'e}d{\\'e}ric and {Burke}, D.~J. and \n"
        "{Cara}, Daria and {Cara}, Mihai and {Conroy}, Kyle E. and {Conseil}, Simon and \n"
        "{Craig}, Matthew W. and {Cross}, Robert M. and {Cruz}, Kelle L. and {D'Eugenio}, \n"
        'Francesco and {Dencheva}, Nadia and {Devillepoix}, Hadrien A.~R. and {Dietrich}, J{\\"o}rg P. \n'
        "and {Eigenbrot}, Arthur Davis and {Erben}, Thomas and {Ferreira}, Leonardo and \n"
        "{Foreman-Mackey}, Daniel and {Fox}, Ryan and {Freij}, Nabil and {Garg}, Suyog and {Geda}, \n"
        "Robel and {Glattly}, Lauren and {Gondhalekar}, Yash and {Gordon}, Karl D. and {Grant}, David \n"
        "and {Greenfield}, Perry and {Groener}, Austen M. and {Guest}, Steve and {Gurovich}, Sebastian \n"
        "and {Handberg}, Rasmus and {Hart}, Akeem and {Hatfield-Dodds}, Zac and {Homeier}, Derek and \n"
        "{Hosseinzadeh}, Griffin and {Jenness}, Tim and {Jones}, Craig K. and {Joseph}, Prajwel and \n"
        "{Kalmbach}, J. Bryce and {Karamehmetoglu}, Emir and {Ka{\\l}uszy{'n}ski}, Miko{\\l}aj and {Kelley}, \n"
        "Michael S.~P. and {Kern}, Nicholas and {Kerzendorf}, Wolfgang E. and {Koch}, Eric W. and \n"
        "{Kulumani}, Shankar and {Lee}, Antony and {Ly}, Chun and {Ma}, Zhiyuan and {MacBride}, Conor \n"
        "and {Maljaars}, Jakob M. and {Muna}, Demitri and {Murphy}, N.~A. and {Norman}, Henrik and {O'Steen}, Richard \n"
        "and {Oman}, Kyle A. and {Pacifici}, Camilla and {Pascual}, Sergio and {Pascual-Granado}, J. and \n"
        "{Patil}, Rohit R. and {Perren}, Gabriel I. and {Pickering}, Timothy E. and {Rastogi}, Tanuj and \n"
        "{Roulston}, Benjamin R. and {Ryan}, Daniel F. and {Rykoff}, Eli S. and {Sabater}, Jose and {Sakurikar}, \n"
        "Parikshit and {Salgado}, Jes{\\'u}s and {Sanghi}, Aniket and {Saunders}, Nicholas and {Savchenko}, \n"
        "Volodymyr and {Schwardt}, Ludwig and {Seifert-Eckert}, Michael and {Shih}, Albert Y. and {Jain}, \n"
        "Anany Shrey and {Shukla}, Gyanendra and {Sick}, Jonathan and {Simpson}, Chris and {Singanamalla}, \n"
        "Sudheesh and {Singer}, Leo P. and {Singhal}, Jaladh and {Sinha}, Manodeep and {Sip{\\H{o}}cz}, \n"
        "Brigitta M. and {Spitler}, Lee R. and {Stansby}, David and {Streicher}, Ole and {{\\v{S}}umak}, \n"
        "Jani and {Swinbank}, John D. and {Taranu}, Dan S. and {Tewary}, Nikita and {Tremblay}, Grant R. \n"
        "and {de Val-Borro}, Miguel and {Van Kooten}, Samuel J. and {Vasovi{\\'c}}, Zlatan and {Verma}, Shresth \n"
        "and {de Miranda Cardoso}, Jos{\\'e} Vin{\\'\\i}cius and {Williams}, Peter K.~G. and \n"
        "{Wilson}, Tom J. and {Winkel}, Benjamin and {Wood-Vasey}, W.~M. and {Xue}, \n"
        "Rui and {Yoachim}, Peter and {Zhang}, Chen and {Zonca}, Andrea and {Astropy Project Contributors}},\n"
    )
    f.write(
        'title = "{The Astropy Project: Sustaining and Growing a Community-oriented '
        'Open-source Project and the Latest Major Release (v5.0) of the Core Package}", \n'
    )
    f.write("journal = {\\apj},\n")
    f.write(
        "keywords = {Astronomy software, Open source software, Astronomy "
        "data analysis, 1855, 1866, 1858, Astrophysics - Instrumentation and "
        "Methods for Astrophysics},\n"
    )
    f.write("year = 2022,\n")
    f.write("month = aug,\n")
    f.write("volume = {935},\n")
    f.write("number = {2},\n")
    f.write("eid = {167},\n")
    f.write("pages = {167},\n")
    f.write("doi = {10.3847/1538-4357/ac7c74},\n")
    f.write("archivePrefix = {arXiv},\n")
    f.write("eprint = {2206.14220},\n")
    f.write("primaryClass = {astro-ph.IM},\n")
    f.write("adsurl = {https://ui.adsabs.harvard.edu/abs/2022ApJ...935..167A},\n")
    f.write("adsnote = {Provided by the SAO/NASA Astrophysics Data System}\n")
    f.write("}\n")

    f.write("\nHealpy:\n\n")
    f.write("@article{Zonca2019,\n")
    f.write("doi = {10.21105/joss.01298},\n")
    f.write("url = {https://doi.org/10.21105/joss.01298},\n")
    f.write("year = {2019},\n")
    f.write("month = mar,\n")
    f.write("publisher = {The Open Journal},\n")
    f.write("volume = {4},\n")
    f.write("number = {35},\n")
    f.write("pages = {1298},\n")
    f.write(
        "author = {Andrea Zonca and Leo Singer and Daniel Lenz and Martin Reinecke "
        "and Cyrille Rosset and Eric Hivon and Krzysztof Gorski},\n"
    )
    f.write(
        "title = {healpy: equal area pixelization and spherical harmonics transforms for data on the sphere in Python},\n"
    )
    f.write("journal = {Journal of Open Source Software}\n")
    f.write("}\n")

    f.write("\n\n")

    f.write("@ARTICLE{2005ApJ...622..759G,\n")
    f.write("author = {{G{'o}rski}, K.~M. and {Hivon}, E. and {Banday}, A.~J. and \n")
    f.write("{Wandelt}, B.~D. and {Hansen}, F.~K. and {Reinecke}, M. and \n")
    f.write("{Bartelmann}, M.},\n")
    f.write(
        'title = "{HEALPix: A Framework for High-Resolution Discretization '
        'and Fast Analysis of Data Distributed on the Sphere}",\n'
    )
    f.write("journal = {\\apj},\n")
    f.write("eprint = {arXiv:astro-ph/0409513},\n")
    f.write(
        "keywords = {Cosmology: Cosmic Microwave Background, Cosmology: Observations, Methods: Statistical},\n"
    )
    f.write("year = 2005,\n")
    f.write("month = apr,\n")
    f.write("volume = 622,\n")
    f.write("pages = {759-771},\n")
    f.write("doi = {10.1086/427976},\n")
    f.write("adsurl = {http://adsabs.harvard.edu/abs/2005ApJ...622..759G},\n")
    f.write("adsnote = {Provided by the SAO/NASA Astrophysics Data System}\n")
    f.write("}\n")

    f.write("\n\n")

    f.write(
        "Add an acknowledgment statement: “Some of the results in this "
        "paper have been derived using the healpy and HEALPix packages”.\n"
    )
    f.write("\n\n")

    f.write(
        "At the first use of the HEALPix acronym, a footnote placed in the"
        " main body of the paper referring to the HEALPix web site, "
        "currently http://healpix.sf.net \n"
    )

    f.write("\nJupyter Notebooks:\n\n")
    f.write("@inproceedings{soton403913,\n")
    f.write("booktitle = {Positioning and Power in Academic Publishing: Players, Agents and Agendas},\n")
    f.write("title = {Jupyter Notebooks ? a publishing format for reproducible computational workflows},\n")
    f.write(
        "author = {Thomas Kluyver and Benjamin Ragan-Kelley and Fernando P{\\'e}rez "
        "and Brian Granger and Matthias Bussonnier and Jonathan Frederic and Kyle Kelley "
        "and Jessica Hamrick and Jason Grout and Sylvain Corlay and Paul Ivanov "
        "and Dami{\\'a}n Avila and Safia Abdalla and Carol Willing and  Jupyter development team},\n"
    )
    f.write("publisher = {IOS Press},\n")
    f.write("year = {2016},\n")
    f.write("pages = {87--90},\n")
    f.write("url = {https://eprints.soton.ac.uk/403913/},\n")
    f.write("}\n")

    f.write("\nmatplotlib:\n\n")
    f.write("@Article{Hunter:2007,\n")
    f.write("Author    = {Hunter, J. D.},\n")
    f.write("Title     = {Matplotlib: A 2D graphics environment},\n")
    f.write("Journal   = {Computing in Science \\& Engineering},\n")
    f.write("Volume    = {9},\n")
    f.write("Number    = {3},\n")
    f.write("Pages     = {90--95},\n")
    f.write("abstract  = {Matplotlib is a 2D graphics package used for Python for \n")
    f.write("application development, interactive scripting, and publication-quality \n")
    f.write("image generation across user interfaces and operating systems.},\n")
    f.write("publisher = {IEEE COMPUTER SOC},\n")
    f.write("doi       = {10.1109/MCSE.2007.55},\n")
    f.write("year      = 2007\n")
    f.write("}\n")

    f.write("\nMinor Planet Center Resources:\n\n")

    f.write(
        "Add an acknowledgment statement: This research has made use of data and/or services provided by the International Astronomical Union's Minor Planet Center. \n"
    )

    f.write("\nNASA ADS:\n\n")
    f.write(
        "Add an acknowledgment statement: This research has made use of "
        "NASA’s Astrophysics Data System Bibliographic Services. \n"
    )

    f.write("\nNumba:\n\n")
    f.write("@INPROCEEDINGS{2015llvm.confE...1L,\n")
    f.write("author = {{Lam}, Siu Kwan and {Pitrou}, Antoine and {Seibert}, Stanley},\n")
    f.write('title = "{Numba: A LLVM-based Python JIT Compiler}",')
    f.write("keywords = {LLVM, Python, Compiler},\n")
    f.write("booktitle = {Proc. Second Workshop on the LLVM Compiler Infrastructure in HPC},\n")
    f.write(" year = 2015,\n")
    f.write("month = nov,\n")
    f.write("pages = {1-6},\n")
    f.write("doi = {10.1145/2833157.2833162},\n")
    f.write("adsurl = {https://ui.adsabs.harvard.edu/abs/2015llvm.confE...1L},\n")
    f.write("adsnote = {Provided by the SAO/NASA Astrophysics Data System}\n")
    f.write("}\n")

    f.write("\nNumpy:\n\n")
    f.write("@Article{         harris2020array,\n")
    f.write("title         = {Array programming with {NumPy}},\n")
    f.write(
        "author        = {Charles R. Harris and K. Jarrod Millman "
        "and St{\\'{e}}fan J. van der Walt and Ralf Gommers and "
        "Pauli Virtanen and David Cournapeau and Eric Wieser and "
        "Julian Taylor and Sebastian Berg and Nathaniel J. Smith and "
        "Robert Kern and Matti Picus and Stephan Hoyer and Marten H. "
        "van Kerkwijk and Matthew Brett and Allan Haldane and Jaime "
        "Fern{\\'{a}}ndez del R{\\'{i}}o and Mark Wiebe and "
        "Pearu Peterson and Pierre G{\\'{e}}rard-Marchant and Kevin "
        "Sheppard and Tyler Reddy and Warren Weckesser and Hameer Abbasi "
        "and Christoph Gohlke and Travis E. Oliphant},\n"
    )
    f.write("year          = {2020},\n")
    f.write("month         = sep,\n")
    f.write("journal       = {Nature},\n")
    f.write("volume        = {585},\n")
    f.write("number        = {7825},\n")
    f.write("pages         = {357--362},\n")
    f.write("doi           = {10.1038/s41586-020-2649-2},\n")
    f.write("publisher     = {Springer Science and Business Media {LLC}},\n")
    f.write("url           = {https://doi.org/10.1038/s41586-020-2649-2}\n")
    f.write("}\n")

    f.write("\nPandas:\n\n")
    f.write("@InProceedings{ mckinney-proc-scipy-2010,\n")
    f.write("author    = { {W}es {M}c{K}inney },\n")
    f.write("title     = { {D}ata {S}tructures for {S}tatistical {C}omputing in {P}ython },\n")
    f.write("booktitle = { {P}roceedings of the 9th {P}ython in {S}cience {C}onference },\n")
    f.write("pages     = { 56 - 61 },\n")
    f.write("year      = { 2010 },\n")
    f.write("editor    = { {S}t{\\'{e}}fan van der {W}alt and {J}arrod {M}illman },\n")
    f.write("doi       = { 10.25080/Majora-92bf1922-00a }\n")
    f.write("}\n")

    f.write("\n\n")
    f.write(
        "Update to the exact version you have installed. Below is the generic Zenodo link reference. \n\n"
    )
    f.write("@software{reback2020pandas,\n")
    f.write("author       = {The pandas development team},\n")
    f.write("title        = {pandas-dev/pandas: Pandas},\n")
    f.write("month        = feb,\n")
    f.write("year         = 2020,\n")
    f.write("publisher    = {Zenodo},\n")
    f.write("version      = {latest},\n")
    f.write("doi          = {10.5281/zenodo.3509134},\n")
    f.write("url          = {https://doi.org/10.5281/zenodo.3509134}\n")
    f.write("}\n")

    f.write("\nPooch:\n\n")
    f.write("@article{uieda2020,\n")
    f.write("title = {{Pooch}: {A} friend to fetch your data files},\n")
    f.write(
        "author = {Leonardo Uieda and Santiago Soler and R{\\'{e}}mi Rampin "
        "and Hugo van Kemenade and Matthew Turk and Daniel Shapero and "
        "Anderson Banihirwe and John Leeman},\n"
    )
    f.write("year = {2020},\n")
    f.write("doi = {10.21105/joss.01943},\n")
    f.write("url = {https://doi.org/10.21105/joss.01943},\n")
    f.write("month = jan,\n")
    f.write("publisher = {The Open Journal},\n")
    f.write("volume = {5},\n")
    f.write(" number = {45},\n")
    f.write("pages = {1943},\n")
    f.write("journal = {Journal of Open Source Software}\n")
    f.write("}\n")

    f.write("\nPytables\n\n")
    f.write("@Misc{pytables,\n")
    f.write("author = {PyTables Developers Team},\n")
    f.write("title = {{PyTables}: Hierarchical Datasets in {Python}},\n")
    f.write("year = {2002--},\n")
    f.write('url = "https://www.pytables.org/",\n')
    f.write("}\n")

    f.write("\nREBOUND:\n\n")
    _cite_rebound(f=f)

    f.write("\nAdapted Functions From rubin_sim:\n\n")

    f.write("@software{peter_yoachim_2022_7087823,\n")
    f.write("author       = {Peter Yoachim and ")
    f.write("R. Lynne Jones and ")
    f.write("Eric H. Neilsen and ")
    f.write("Tiago Ribeiro and ")
    f.write("Scott Daniel and ")
    f.write("Natasha Abrams and ")
    f.write("Husni Almoubayyed and ")
    f.write("Igor Andreoni and ")
    f.write("Humna Awan and ")
    f.write("Matthew R. Becker and ")
    f.write(" Keaton Bell and ")
    f.write("Eric Bellm and ")
    f.write("Federica Bianco and ")
    f.write("Johan Bregeon and ")
    f.write("Katja Bricman and ")
    f.write("Owen Boberg and ")
    f.write("Jeff Carlin and ")
    f.write("YuChia Chen and ")
    f.write("Will Clarkson and ")
    f.write("Andrew Connolly and ")
    f.write("Philippe Gris and ")
    f.write("Alina Hu and ")
    f.write("Michael Kelley and ")
    f.write("Somayeh Khakpash and ")
    f.write("Simon Krughoff and ")
    f.write("Xiaolong Li and ")
    f.write("Michael B. Lund and ")
    f.write("Phil Marshall and ")
    f.write("Josh Meyers and ")
    f.write("Loredana Prisinzano and ")
    f.write("Elahesadat Naghib and ")
    f.write("Meredith Rawls and ")
    f.write("Michael Reuter and ")
    f.write("Daniel Rothchild and ")
    f.write("Christian N. Setzer and ")
    f.write("Jonathan Sick and ")
    f.write(" Rachel Street},\n")
    f.write("title        = {lsst/rubin\\_sim: 0.12.1},\n")
    f.write("month        = sep,\n")
    f.write("year         = 2022,\n")
    f.write("publisher    = {Zenodo},\n")
    f.write("version      = {0.12.1},\n")
    f.write("doi          = {10.5281/zenodo.7087823},\n")
    f.write("url          = {https://doi.org/10.5281/zenodo.7087823}\n")
    f.write("}\n")

    f.write("\n\n")

    f.write("@ARTICLE{2018Icar..303..181J,\n")
    f.write(
        "author = {{Jones}, R. Lynne and {Slater}, Colin T. and {Moeyens}, "
        "Joachim and {Allen}, Lori and {Axelrod}, Tim and {Cook}, Kem and "
        "{Ivezi{\\'c}}, {\v{Z}}eljko and {Juri{\\'c}}, Mario and {Myers}, Jonathan "
        "and {Petry}, Catherine E.},\n"
    )
    f.write('title = "{The Large Synoptic Survey Telescope as a Near-Earth Object discovery machine}",\n')
    f.write("journal = {\\icarus},\n")
    f.write(
        "keywords = {Near-Earth objects, Image processing, Asteroids, "
        "Earth Science, Astrophysics - Earth and Planetary Astrophysics, "
        "Astrophysics - Instrumentation and Methods for Astrophysics},\n"
    )
    f.write("year = 2018,\n")
    f.write("month = mar,\n")
    f.write("volume = {303},\n")
    f.write("pages = {181-202},\n")
    f.write("doi = {10.1016/j.icarus.2017.11.033},\n")
    f.write("archivePrefix = {arXiv},\n")
    f.write("eprint = {1711.10621},\n")
    f.write(" primaryClass = {astro-ph.EP},\n")
    f.write("adsurl = {https://ui.adsabs.harvard.edu/abs/2018Icar..303..181J},\n")
    f.write(" adsnote = {Provided by the SAO/NASA Astrophysics Data System}\n")
    f.write("}\n")

    f.write("\nsbpy:\n\n")
    f.write("@ARTICLE{2019JOSS....4.1426M,\n")
    f.write(
        "author = {{Mommert}, Michael and {Kelley}, Michael and {de Val-Borro}, Miguel "
        "and {Li}, Jian-Yang and {Guzman}, Giannina and {Sip{\\H{o}}cz}, Brigitta and "
        "{{\\v{D}}urech}, Josef and {Granvik}, Mikael and {Grundy}, Will and {Moskovitz}, Nick "
        'and {Penttil{\\"a}}, Antti and {Samarasinha}, Nalin},\n'
    )
    f.write('title = "{sbpy: A Python module for small-body planetary astronomy}",\n')
    f.write("journal = {The Journal of Open Source Software},\n")
    f.write(
        "keywords = {comets, kuiper belt objects, Python, trans-neptunian objects, "
        "centaurs, planetary science, python, solar system, asteroids, meteoroids, "
        "trojans, astronomy, small bodies},\n"
    )
    f.write("year = 2019,\n")
    f.write("month = aug,\n")
    f.write("volume = {4},\n")
    f.write("number = {38},\n")
    f.write("eid = {1426},\n")
    f.write("pages = {1426},\n")
    f.write("doi = {10.21105/joss.01426},\n")
    f.write("adsurl = {https://ui.adsabs.harvard.edu/abs/2019JOSS....4.1426M},\n")
    f.write("adsnote = {Provided by the SAO/NASA Astrophysics Data System}\n")
    f.write("}\n")

    f.write("\nSciPy:\n\n")
    f.write("@ARTICLE{2020SciPy-NMeth,\n")
    f.write("author  = {Virtanen, Pauli and Gommers, Ralf and Oliphant, Travis E. and \n")
    f.write("Haberland, Matt and Reddy, Tyler and Cournapeau, David and \n")
    f.write("Burovski, Evgeni and Peterson, Pearu and Weckesser, Warren and \n")
    f.write("Bright, Jonathan and {van der Walt}, St{\\'{e}}fan J. and \n")
    f.write("Brett, Matthew and Wilson, Joshua and Millman, K. Jarrod and \n")
    f.write("Mayorov, Nikolay and Nelson, Andrew R. J. and Jones, Eric and \n")
    f.write("Kern, Robert and Larson, Eric and Carey, C J and \n")
    f.write("Polat, {\\.I}lhan and Feng, Yu and Moore, Eric W. and \n")
    f.write("{VanderPlas}, Jake and Laxalde, Denis and Perktold, Josef and \n")
    f.write("Cimrman, Robert and Henriksen, Ian and Quintero, E. A. and \n")
    f.write("Harris, Charles R. and Archibald, Anne M. and \n")
    f.write("Ribeiro, Ant{\\^o}nio H. and Pedregosa, Fabian and \n")
    f.write("{van Mulbregt}, Paul and {SciPy 1.0 Contributors}},\n")
    f.write("title   = {{{SciPy} 1.0: Fundamental Algorithms for Scientific \n")
    f.write("Computing in Python}},\n")
    f.write("journal = {Nature Methods},\n")
    f.write("year    = {2020},\n")
    f.write("volume  = {17},\n")
    f.write("pages   = {261--272},\n")
    f.write("adsurl  = {https://rdcu.be/b08Wh},\n")
    f.write("doi     = {10.1038/s41592-019-0686-2},\n")

    f.write("}\n")

    f.write("\nSpice Resources:\n\n")
    f.write(" @ARTICLE{1996P&SS...44...65A,\n")
    f.write("author = {{Acton}, Charles H.},\n")
    f.write(
        "title = {Ancillary data services of  " "NASA's Navigation and Ancillary Information Facility},\n"
    )
    f.write("journal = {\\planss},\n")
    f.write("year = 1996,\n")
    f.write("month = jan,\n")
    f.write("volume = {44},\n")
    f.write("number = {1},\n")
    f.write("pages = {65-70},\n")
    f.write("doi = {10.1016/0032-0633(95)00107-7},\n")
    f.write("adsurl = {https://ui.adsabs.harvard.edu/abs/1996P&SS...44...65A},\n")
    f.write("adsnote = {Provided by the SAO/NASA Astrophysics Data System}\n")
    f.write("}\n")

    f.write("\n\n")

    f.write("@ARTICLE{2018P&SS..150....9A,\n")
    f.write(
        "author = {{Acton}, Charles and {Bachman}, Nathaniel and {Semenov}, Boris and {Wright}, Edward},\n"
    )
    f.write('title = "{A look towards the future in the handling of space science mission geometry}",\n')
    f.write("journal = {\\planss},\n")
    f.write("year = 2018,\n")
    f.write("month = jan,\n")
    f.write("volume = {150},\n")
    f.write("pages = {9-12},\n")
    f.write("doi = {10.1016/j.pss.2017.02.013},\n")
    f.write("adsurl = {https://ui.adsabs.harvard.edu/abs/2018P&SS..150....9A},\n")
    f.write("adsnote = {Provided by the SAO/NASA Astrophysics Data System} \n")
    f.write("}\n")

    f.write(
        "\nAdd an acknowledgment statement:  The SPICE Resource files used in this work ere described in \\citep{1996P&SS...44...65A, 2018P&SS..150....9A}\n"
    )

    f.write("\nSpiceypy:\n\n")
    f.write("@ARTICLE{2020JOSS....5.2050A,\n")
    f.write(
        "author = {{Annex}, Andrew and {Pearson}, Ben and {Seignovert}, "
        "Beno{\\^\\i}t and {Carcich}, Brian and {Eichhorn}, Helge and {Mapel}, "
        "Jesse and {von Forstner}, Johan and {McAuliffe}, Jonathan and "
        "{del Rio}, Jorge and {Berry}, Kristin and {Aye}, K. -Michael and "
        "{Stefko}, Marcel and {de Val-Borro}, Miguel and {Kulumani}, Shankar "
        "and {Murakami}, Shin-ya}, \n"
    )
    f.write('title = "{SpiceyPy: a Pythonic Wrapper for the SPICE Toolkit}",\n')
    f.write("journal = {The Journal of Open Source Software},\n")
    f.write("keywords = {geometry, Python, spacecraft, Batchfile, planets, ephemeris, navigation, SPICE},\n")
    f.write("year = 2020,\n")
    f.write("month = feb,\n")
    f.write("volume = {5},\n")
    f.write("number = {46},\n")
    f.write(" eid = {2050},\n")
    f.write("pages = {2050},\n")
    f.write("doi = {10.21105/joss.02050},\n")
    f.write("adsurl = {https://ui.adsabs.harvard.edu/abs/2020JOSS....5.2050A},\n")
    f.write("adsnote = {Provided by the SAO/NASA Astrophysics Data System}\n")
    f.write("}\n")

    f.write("\ntqdm:\n\n")
    f.write("@software{casper_da_costa_luis_2023_8233425,\n")
    f.write("author       = {Casper da Costa-Luis and\n")
    f.write("Stephen Karl Larroque and\n")
    f.write("Kyle Altendorf and\n")
    f.write("Hadrien Mary and\n")
    f.write("richardsheridan and\n")
    f.write("Mikhail Korobov and\n")
    f.write("Noam Yorav-Raphael and\n")
    f.write("Ivan Ivanov and\n")
    f.write("Marcel Bargull and\n")
    f.write("Nishant Rodrigues and\n")
    f.write("Guangshuo Chen and\n")
    f.write("Antony Lee and\n")
    f.write("Charles Newey and\n")
    f.write("CrazyPython and\n")
    f.write("JC and\n")
    f.write("Martin Zugnoni and\n")
    f.write("Matthew D. Pagel and\n")
    f.write("mjstevens777 and\n")
    f.write("Mikhail Dektyarev and\n")
    f.write("Alex Rothberg and\n")
    f.write(" Alexander Plavin and\n")
    f.write("Fabian Dill and\n")
    f.write("FichteFoll and\n")
    f.write("Gregor Sturm and\n")
    f.write("HeoHeo and\n")
    f.write("Hugo van Kemenade and\n")
    f.write("Jack McCracken and\n")
    f.write("MapleCCC and\n")
    f.write("Max Nordlund and\n")
    f.write("Mike Boyle},\n")
    f.write("title        = {{tqdm: A fast, Extensible Progress Bar for Python \n")
    f.write("and CLI}},\n")
    f.write("month        = aug,\n")
    f.write("year         = 2023,\n")
    f.write(" publisher    = {Zenodo},\n")
    f.write(" version      = {v4.66.1},\n")
    f.write("doi          = {10.5281/zenodo.8233425},\n")
    f.write("url          = {https://doi.org/10.5281/zenodo.8233425}\n")
    f.write("}\n")

    f.write("\nIf using a rubin_sim simulated survey pointing database:\n\n")
    f.write(
        "Add an acknowledgment statement: This material or work is supported in part by the National Science  "
        "Foundation through Cooperative Agreement AST-1258333 and "
        "Cooperative Support Agreement AST1836783 managed by the Association "
        "of Universities for Research in Astronomy (AURA), and the Department "
        "of Energy under Contract No. DE-AC02-76SF00515 with the SLAC National "
        "Accelerator Laboratory managed by Stanford University.\n"
    )

    f.write("\n\n")
    f.write(
        "If you are submitting a paper to AAS Journals, here is"
        " the software citation latex command you will need once you have included "
        "all of the above  bibtex references above.\n"
    )

    f.write(
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


def _cite_rebound(f):
    """
    Function to output the print statements from rebound.Simulation.cite() into the file like object.
    Parameters
    -----------
    f: file-like object
        The output for where the citation information will be written. Default: sys.stdout

    Returns
    -----------
    None
    """
    # saving the default sys.stdout
    original_stdout = sys.stdout
    # making the sys.stdout output to f.
    sys.stdout = f
    sim = rebound.Simulation()
    sim.cite()
    # making the stdout default again
    sys.stdout = original_stdout
