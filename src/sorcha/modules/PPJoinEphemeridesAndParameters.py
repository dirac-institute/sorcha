def PPJoinEphemeridesAndParameters(padafr, padacl):
    """
    Joins the ephemerides pandas dataframe with the physical parameters pandas
    dataframe. Each database has to have same ObjIDs: NaNs will
    be populate the fields for the missing objects.

    Parameters
    -----------
    padafr : Pandas dataframe:
        Dataframe of ephemerides output.

    padacl : Pandas dataframe
        Dataframe of physical parameters information.

    Returns
    ----------
    resdf : Pandas dataframe
        Joined dataframe of "padafr" and "padacl"

    """

    resdf = padafr.join(padacl.set_index("ObjID"), on="ObjID")

    return resdf
