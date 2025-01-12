sorcha.modules.PPApplyFOVFilter
===============================

.. py:module:: sorcha.modules.PPApplyFOVFilter


Functions
---------

.. autoapisummary::

   sorcha.modules.PPApplyFOVFilter.PPApplyFOVFilter
   sorcha.modules.PPApplyFOVFilter.PPGetSeparation
   sorcha.modules.PPApplyFOVFilter.PPCircleFootprint
   sorcha.modules.PPApplyFOVFilter.PPSimpleSensorArea


Module Contents
---------------

.. py:function:: PPApplyFOVFilter(observations, sconfigs, module_rngs, footprint=None, verbose=False)

   Wrapper function for PPFootprintFilter and PPFilterDetectionEfficiency that checks to see
   whether a camera footprint filter should be applied or if a simple fraction of the
   circular footprint should be used, then applies the required filter where rows are
    are removed from the inputted pandas dataframevfor moving objects that land outside of
    their associated observation's footprint.

   Adds the following columns to the observations dataframe:

   - detectorId (if full camera footprint is used)

   :param observations:
   :type observations: Pandas dataframe
   :param dataframe of observations.:
   :param sconfigs: Dataclass of configuration file arguments.
   :type sconfigs: dataclass
   :param module_rngs: A collection of random number generators (per module).
   :type module_rngs: PerModuleRNG
   :param footprint: A Footprint class object that represents the boundaries of the detector(s).
                     Default: None.
   :type footprint: Footprint
   :param verbose: Controls whether logging in verbose mode is on or off.
                   Default: False
   :type verbose: boolean

   :returns: **observations** -- dataframe of observations updated after field-of-view filters have been applied.
   :rtype: Pandas dataframe


.. py:function:: PPGetSeparation(obj_RA, obj_Dec, cen_RA, cen_Dec)

   Function to calculate the distance of an object from the field centre.

   :param obj_RA: RA of object in decimal degrees.
   :type obj_RA: float
   :param obj_Dec: Dec of object in decimal degrees.
   :type obj_Dec: float
   :param cen_RA: RA of field centre in decimal degrees.
   :type cen_RA: float
   :param cen_Dec: Dec of field centre in decimal degrees.
   :type cen_Dec: float

   :returns: **sep_degree** -- The separation of the object from the centre of the field, in decimal
             degrees.
   :rtype: float


.. py:function:: PPCircleFootprint(observations, circle_radius)

   Simple function which removes objects which lay outside of a circle
   of given radius centred on the field centre.

   :param observations: dataframe of observations.
   :type observations: Pandas dataframe
   :param circle_radius: radius of circle footprint in degrees.
   :type circle_radius: float

   :returns: **new_observations** -- dataframe of observations with all lying beyond the circle radius dropped.
   :rtype: Pandas dataframe


.. py:function:: PPSimpleSensorArea(ephemsdf, module_rngs, fillfactor=0.9)

   Randomly removes a number of observations proportional to the
   fraction of the field not covered by the detector.

   :param ephemsdf: Dataframe containing observations.
   :type ephemsdf: Pandas dataframe
   :param module_rngs: A collection of random number generators (per module).
   :type module_rngs: PerModuleRNG
   :param fillfactor: fraction of FOV covered by the sensor.
                      Default = 0.9
   :type fillfactor: float

   :returns: **ephemsOut** -- Dataframe of observations with 1- fillfactor fraction of objects
             removed per on-sky observation pointing.
   :rtype: Pandas dataframe


