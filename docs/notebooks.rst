.. _demonotebooks:

Demo Notebooks
========================================================================================

Below we provide Jupyter notebooks that demonstrate ``Sorcha``'s capabilities and validate various functions and components within ``Sorcha``.

.. note::
    You will need to install jupyter labs/notebooks into your environement to be able to run these Jupyter notebooks. 
 
In addition to installing ``Sorcha`` and its dependencies, you will need to install (through pip/conda/mamba) the following additional packages to run all of the demo notebooks:

* jupyter
* seaborn
* sorcha-addons
* rubin_sim (only required for demo_CalculateLSSTColours.ipynb) and the associated filter/optical system throughputs via (running ``scheduler_download_data`` on the command line)

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
