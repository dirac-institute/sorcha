sorcha.modules.PPCalculateSimpleCometaryMagnitude
=================================================

.. py:module:: sorcha.modules.PPCalculateSimpleCometaryMagnitude


Functions
---------

.. autoapisummary::

   sorcha.modules.PPCalculateSimpleCometaryMagnitude.PPCalculateSimpleCometaryMagnitude


Module Contents
---------------

.. py:function:: PPCalculateSimpleCometaryMagnitude(padain: pandas.DataFrame, observing_filters: List[str], rho: List[float], delta: List[float], alpha: List[float], activity_choice: str = None) -> pandas.DataFrame

   Adjusts the  observations' trailed source apparent magnitude for cometary activity
   using the model specified by `activity_choice` added by the user

   :param padain: The input ``observations`` dataframe
   :type padain: pd.DataFrame
   :param observing_filters: The photometric filters the observation is taken in (the filter
                             requested that the coma magnitude be calculated for)
   :type observing_filters: List[str]
   :param rho: Heliocentric distance [units au]
   :type rho: List[float]
   :param delta: Distance to Earth [units au]
   :type delta: List[float]
   :param alpha: Phase angle [units degrees]
   :type alpha: List[float]
   :param activity_choice: The activity model to use, by default None
   :type activity_choice: string, optional

   :returns: The ``observations`` dataframe with updated trailed
             source apparent magnitude values.
   :rtype: pd.DataFrame


