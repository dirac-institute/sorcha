import sys
import logging


def PPGetMainFilterAndColourOffsets(filename, observing_filters, filesep):
    """
    Function to obtain the main filter (i.e. the filter in which H is
    defined) from the header of the physical parameters file and then generate
    the expected colour offsets. Also makes sure that columns exist for all
    the expected colour offsets in the physical parameters file.

    The main filter should be found as a column heading of H_[mainfilter]. If
    this format isn't followed, this function will error out.

    Parameters:
    -----------
    filename (string): the filename of the physical parameters file.

    observing_filters (list of strings): the observation filters requested
    in the config file.

    filesep (string): the format of the physical parameters file. Should be "csv"/"comma"
    or "whitespace".

    Returns:
    ----------
    mainfilter (string): the main filter in which H is defined.

    colour_offsets (list of strings): a list of the colour offsets present in the
    physical parameters file.

    """

    pplogger = logging.getLogger(__name__)

    with open(filename) as f:
        first_line = f.readline()

    H_loc = first_line.find("H_")

    if H_loc == -1:
        pplogger.error(
            "ERROR: PPGetMainFilterAndColourOffsets: cannot find column of H_{main filter} format in physical parameters file."
        )
        sys.exit(
            "ERROR: PPGetMainFilterAndColourOffsets: cannot find column of H_{main filter} format in physical parameters file."
        )

    mainfilter = first_line[H_loc + 2]

    if mainfilter not in observing_filters:
        pplogger.error(
            "ERROR: PPGetMainFilterAndColourOffsets: H is given as {}, but {} is not listed as a requested observation filter in config file.".format(
                mainfilter, mainfilter
            )
        )
        sys.exit(
            "ERROR: PPGetMainFilterAndColourOffsets: H is given as {}, but {} is not listed as a requested observation filter in config file.".format(
                mainfilter, mainfilter
            )
        )

    if len(observing_filters) > 1:
        colour_offsets = [x + "-" + mainfilter for x in observing_filters[1:]]
    elif len(observing_filters) == 1:
        colour_offsets = None
    else:
        pplogger.error(
            "ERROR: PPGetMainFilterAndColourOffsets: could not parse filters supplied for observing_filters keyword. Check formatting and try again."
        )
        sys.exit(
            "ERROR: PPGetMainFilterAndColourOffsets: could not parse filters supplied for observing_filters keyword. Check formatting and try again."
        )

    # check that the columns match up with the othercolours calculated from observing_filters config variable

    if filesep == "whitespace":
        sep = " "
    elif filesep == "comma" or filesep == "csv":
        sep = ","
    else:
        pplogger.error(
            "ERROR: PPGetMainFilterAndColourOffsets: unexpected valye for auxFormat keyword in configs."
        )
        sys.exit("ERROR: PPGetMainFilterAndColourOffsets: unexpected valye for auxFormat keyword in configs.")

    if colour_offsets and not all(colour in first_line[:-1].split(sep) for colour in colour_offsets):
        pplogger.error(
            "ERROR: PPGetMainFilterAndColourOffsets: colour offset columns in physical parameters file do not match with observing filters specified in config file."
        )
        sys.exit(
            "ERROR: PPGetMainFilterAndColourOffsets: colour offset columns in physical parameters file do not match with observing filters specified in config file."
        )

    return mainfilter, colour_offsets
