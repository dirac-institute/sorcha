import logging
import sys


from sorcha.modules.PPLinkingFilter import PPLinkingFilter
from sorcha.modules.desDiscoveryFilter import desDiscoveryFilter
from sorcha.modules.desDistanceandMotionCuts import distance_cut, motion_cut


def Discovery_Filter(observations=None, sconfigs=None, verbose=None):
    """
    Wrapper function for PPLinkingFilter and desDiscoveryFilter linking filters.
    This checks whether to use the Rubin_sim or DES linking filters.

    Also checks for DES whether to include distance or motion cuts to the observations.

    Simulates the linking process of a survey, then drops rows where the
    objects are not discovered.

    Parameters
    -----------
    observations : Pandas dataframe
        Dataframe of observations.

    sconfigs: dataclass
        Dataclass of configuration file arguments.

    verbose : boolean, default=False
        Verbose logging flag.

    Returns
    -----------
    observations_drop : Pandas dataframe)
        Modified 'observations' dataframe without objects that could not be discovered.

    """
    pplogger = logging.getLogger(__name__)
    verboselog = pplogger.info if verbose else lambda *a, **k: None

    if sconfigs.linkingfilter.des_discovery_on:
        if sconfigs.linkingfilter.des_distance_cut_on:
            verboselog("Number of rows BEFORE applying distance cuts: " + str(len(observations.index)))
            observations = distance_cut(
                observations,
                sconfigs.linkingfilter.des_distance_cut_upper,
                sconfigs.linkingfilter.des_distance_cut_lower,
            )
            verboselog("Number of rows AFTER applying distance cuts: " + str(len(observations.index)))

        if sconfigs.linkingfilter.des_motion_cut_on:
            verboselog("Number of rows BEFORE applying motion cuts: " + str(len(observations.index)))
            observations = motion_cut(
                observations,
                sconfigs.linkingfilter.des_motion_cut_upper,
                sconfigs.linkingfilter.des_motion_cut_lower,
            )
            verboselog("Number of rows AFTER applying motion cuts: " + str(len(observations.index)))

        if len(observations.index) > 0:
            verboselog("Applying DES discovery filter...")
            verboselog("Number of rows BEFORE applying DES Discovery filter: " + str(len(observations.index)))
            observations = desDiscoveryFilter(observations)
            verboselog("Number of rows AFTER applying DES Discovery filter: " + str(len(observations.index)))
        return observations
    if sconfigs.linkingfilter.ssp_linking_on:
        verboselog("Applying SSP linking filter...")
        verboselog("Number of rows BEFORE applying SSP linking filter: " + str(len(observations.index)))
        observations = PPLinkingFilter(
            observations,
            sconfigs.linkingfilter.ssp_detection_efficiency,
            sconfigs.linkingfilter.ssp_number_observations,
            sconfigs.linkingfilter.ssp_number_tracklets,
            sconfigs.linkingfilter.ssp_track_window,
            sconfigs.linkingfilter.ssp_separation_threshold,
            sconfigs.linkingfilter.ssp_maximum_time,
            sconfigs.linkingfilter.ssp_night_start_utc,
            drop_unlinked=sconfigs.linkingfilter.drop_unlinked,
        )
        observations.reset_index(drop=True, inplace=True)
        verboselog("Number of rows AFTER applying SSP linking filter: " + str(len(observations.index)))
        return observations
    else:
        pplogger.error(f"ERROR: discovery_filter_on is true but no specfic linking is turned on.")
        sys.exit(f"ERROR: discovery_filter_on is true but no specfic linking is turned on.")
