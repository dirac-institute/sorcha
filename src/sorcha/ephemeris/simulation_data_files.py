import pooch


def make_retriever(sconfigs, directory_path: str = None) -> pooch.Pooch:
    """Helper function that will create a Pooch object to track and retrieve files.

    Parameters
    ----------
    directory_path : string, optional
        The base directory to place all downloaded files. Default = None
    registry : dictionary, optional
        A dictionary of file names to SHA hashes. Generally we'll not use SHA=None
        because the files we're tracking change frequently. Default = REGISTRY
    sconfigs: dataclass
        Dataclass of configuration file arguments.
    Returns
    -------
    : pooch
        The instance of a Pooch object used to track and retrieve files.
    """
    dir_path = pooch.os_cache("sorcha")
    if directory_path:
        dir_path = directory_path

    return pooch.create(
        path=dir_path,
        base_url="",
        urls=sconfigs.auxiliary.urls,
        registry=sconfigs.auxiliary.registry,
        retry_if_failed=25,
    )
