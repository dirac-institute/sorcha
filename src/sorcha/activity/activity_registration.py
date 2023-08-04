from sorcha.activity.base_activity import AbstractCometaryActivity
from typing import Callable, Dict


def register_activity_subclasses() -> Dict[str, Callable]:
    """This method will identify all of the subclasses of ``AbstractCometaryActivity``
    and build a dictionary that maps ``name : subclass``.

    Returns
    -------
    dict
        A dictionary of all of subclasses of ``AbstractCometaryActivity``. Where
        the string returned from ``subclass.name_id()`` is the key, and the
        subclass is the value.

    Raises
    ------
    ValueError
        If a duplicate key is found, a ``ValueError`` is raised. This would
        likely occur if a user copy/pasted an existing subclass but failed to
        update the string returned from ``name_id()``.
    """
    subclass_dict = {}
    for subcls in AbstractCometaryActivity.__subclasses__():
        if subcls.name_id() in subclass_dict:
            raise ValueError(
                "Attempted to add duplicate cometary activity calculator name to CA_METHODS: "
                + str(subcls.name_id())
            )

        subclass_dict[subcls.name_id()] = subcls

    return subclass_dict


def update_activity_subclasses() -> None:
    """This function is used to register newly created subclasses of the
    `AbstractCometaryActivity`.
    """
    for subcls in AbstractCometaryActivity.__subclasses__():
        if subcls.name_id() not in CA_METHODS.keys():
            CA_METHODS[subcls.name_id()] = subcls


# The dictionary of all available subclasses of the AbstractCometaryActivity.
CA_METHODS = register_activity_subclasses()
