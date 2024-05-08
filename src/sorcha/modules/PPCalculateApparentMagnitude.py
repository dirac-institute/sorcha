from .PPCalculateApparentMagnitudeInFilter import PPCalculateApparentMagnitudeInFilter
from .PPCalculateSimpleCometaryMagnitude import PPCalculateSimpleCometaryMagnitude
from .PPApplyColourOffsets import PPApplyColourOffsets
import logging


def PPCalculateApparentMagnitude(
    observations,
    phasefunction,
    mainfilter,
    othercolours,
    observing_filters,
    cometary_activity_choice=None,
    lightcurve_choice=None,
    verbose=False,
):
    """This function applies the correct colour offset to H for the relevant filter, checks to make sure
    the correct columns are included (with additional functionality for colour-specific phase curves),
    then calculates the trailed source apparent magnitude including optional adjustments for
    cometary activity and rotational light curves.

    Adds the following columns to the observations dataframe:

    - H_filter
    - trailedSourceMagTrue
    - any columns created by the optional light curve and cometary activity models

    Removes the following columns from the observations dataframe:

    - Colour offset columns (i.e. u-r)
    - Colour-specific phase curve variables (if extant): the correct filter-specific value
    for each observation is located and stored instead. i.e. GS_r and GS_g columns will be deleted
    and replaced with a GS column containing either GS_r or GS_g depending on observation filter.

    Parameters
    -----------
    observations : Pandas dataframe
        dataframe of observations.

    phasefunction : string
        Desired phase function model. Options are HG, HG12, HG1G2, linear, none

    mainfilter : string
        The main filter in which H is given and all colour offsets are calculated against.

    othercolours : list of strings
        List of colour offsets present in input files.

    observing_filters : list of strings
        List of observation filters of interest.

    cometary_activity_choice : string
        Choice of cometary activity model.
        Default = None

    lc_choice : string
        Choice of lightcurve model. Default =  None

    verbose : boolean
        Flag for turning on verbose logging. Default = False

    Returns
    ----------
    observations : Pandas dataframe
        Modified observations pandas dataframe with calculated trailed source
        apparent magnitude column, H calculated in relevant filter (H_filter),
        renames the column for H in the main filter as H_original and
        adds a column for the light curve contribution to the trailed source
        apparent magnitude (if included)
    """

    pplogger = logging.getLogger(__name__)
    verboselog = pplogger.info if verbose else lambda *a, **k: None

    # apply correct colour offset to get H magnitude in observation filter
    # if user is only interested in one filter, we have no colour offsets to apply: assume H is in that filter
    if len(observing_filters) > 1:
        verboselog("Selecting and applying correct colour offset...")

        observations = PPApplyColourOffsets(
            observations, phasefunction, othercolours, observing_filters, mainfilter
        )
    else:
        observations["H_filter"] = observations["H_" + mainfilter].copy()

    # calculate main body apparent magnitude in observation filter
    verboselog("Calculating apparent magnitude in filter...")
    observations = PPCalculateApparentMagnitudeInFilter(
        observations,
        phasefunction,
        observing_filters,
        lightcurve_choice=lightcurve_choice,
        cometary_activity_choice=cometary_activity_choice,
    )

    return observations
