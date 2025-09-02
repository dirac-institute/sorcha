.. _demonotebooks:

Demo Notebooks
========================================================================================


Below we provide Jupyter notebooks that demonstrate ``Sorcha``'s capabilities and validate various functions and components within ``Sorcha``. These notebooks are automatically generated in the online documentation so you can view the contents and output of the notebooks by clicking on the link to each notebook. 

In addition to installing ``Sorcha`` and its dependencies, you will need to install (through pip/conda/mamba) the following additional packages to run all of the demo notebooks:

* jupyter
* seaborn
* sorcha-addons
* rubin_sim (only required for demo_CalculateLSSTColours.ipynb) and the associated filter/optical system throughputs via (running ``scheduler_download_data`` on the command line)

.. note::

   These packages are installed (except for ``rubin_sim``) if you install ``Sorcha`` from the source code via pip in editable development mode as described in the :ref:`dev_mode` page.

.. tip::

    The easiest way to run the notebooks is to clone the repository and install ``Sorcha`` from the source code via pip in editable development mode as described in the :ref:`dev_mode` page. Then move to the docs/notebooks directory and run the notebooks from the there. We also provide the data files used below so you can try individual notebooks out without running them all or cloning the full repository. 


Demo Notebooks
------------------------
.. toctree::
    :maxdepth: 1

    LSST Camera Footprint and Various Other Sorcha Related Fields-of-View <notebooks/demo_PlotLSSTCamCornersFOVs> 
    Apparent Magnitude Validation <notebooks/demo_ApparentMagnitudeValidation>
    Calculate LSST Colours <notebooks/demo_CalculateLSSTColours>
    Circle Footprint Filter <notebooks/demo_CircleFootprint>
    LSST Camera Footprint Filter <notebooks/demo_FootprintFilter>
    Coordinate Transformation Example <notebooks/demo_CoordinateTransformations.ipynb>
    Detection Efficiency (Fading Function) Validation <notebooks/demo_DetectionEfficiencyValidation>
    Estimating Colors in LSST Filters From Optical/NIR Spectra <notebooks/demo_CalculateLSSTColours.ipynb>
    SSP Linking Filter <notebooks/demo_LinkingFilter>
    Magnitude and SNR Cuts <notebooks/demo_MagnitudeAndSNRCuts>
    Trailing Losses Validation <notebooks/demo_TrailingLossesValidation>
    Trailed Source Magnitude Versus PSF Magnitude <notebooks/demo_TrailingLossPhasecurve>
    Uncertainties and Randomization <notebooks/demo_UncertaintiesAndRandomization>
    Vignetting Demo <notebooks/demo_Vignetting>
    Light curve Demo <notebooks/demo_Lightcurve>
    Cometary Activity Demo <notebooks/demo_Cometary_Activity> 
    miniDifi Validation <notebooks/demo_miniDifiValidation>
    Sorcha End-to-End Verification <notebooks/demo_Verification>

Files to Download To Run the Notebooks Individually
------------------------------------------------------

* LSST Camera Footprint and Various Other Sorcha Related Fields-of-View 

    * :download:`LSSTCam detector configuration file <../src/sorcha/modules/data/LSST_detector_corners_100123.csv>`

* Calculate LSST Colours

    * :download:`2002PN34_highres.spec <./2002PN34_highres.spec>`

* Circle Footprint Filter

    * :download:`oneline_v2.0.db <./notebooks/oneline_v2.0.db>`
    * :download:`footprintFilterValidationObservations.csv <./notebooks/footprintFilterValidationObservations.csv>`


