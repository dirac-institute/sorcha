import pooch


def make_retriever(auxconfigs, directory_path: str = None) -> pooch.Pooch:
    """Helper function that will create a Pooch object to track and retrieve files.

    Parameters
    ----------
    auxconfigs: dataclass
        Dataclass of auxiliary configuration file arguments.

    directory_path : string, default=None
        The base directory to place all downloaded files. 

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
        urls=auxconfigs.urls,
        registry=auxconfigs.registry,
        retry_if_failed=25,
    )
