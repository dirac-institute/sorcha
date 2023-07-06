def PPJoinEphemeridesAndParameters(padafr, padacl):
    """
    Joins the ephemerides pandas dataframe with the physical parameters pandas
    dataframe. Each database has to have same ObjIDs: NaNs will
    be populate the fields for the missing objects.

    Parameters:
    -----------
    padafr (Pandas dataframe): dataframe of ephemerides/OIF output.

    padacl (Pandas dataframe): dataframe of physical parameters information.

    Returns:
    ----------
    resdf (Pandas dataframe): joined dataframe.

    """

    resdf = padafr.join(padacl.set_index("ObjID"), on="ObjID")

    return resdf
