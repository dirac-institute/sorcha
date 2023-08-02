from sorcha.activity.base_activity import AbstractCometaryActivity
import pandas as pd

"""
!!!!!!!!!!!!!!!!
FOR TESTING ONLY
!!!!!!!!!!!!!!!!
"""


class IdentityCometaryActivity(AbstractCometaryActivity):
    """
    !!! THIS SHOULD NEVER BE USED - FOR TESTING ONLY !!!

    Rudimentary cometary activity model that returns no change to the input ``observation``
    dataframe.
    This class is explicitly created for testing purposes.
    """

    def __init__(self) -> None:
        super().__init__()

    def compute(self, df: pd.DataFrame) -> pd.DataFrame:
        """Returns numpy array of 0's with shape equal to the input dataframe
        time column.

        Parameters
        ----------
        df : pd.DataFrame
            The ``observations`` dataframe provided by ``Sorcha``.

        Returns
        -------
        pd.DataFrame
            The original ``observations`` dataframe, unchanged.
        """

        self._validate_column_names(df)

        return df

    @staticmethod
    def name_id() -> str:
        """Returns the string identifier for this cometary activity method. It
        must be unique within all the subclasses of ``AbstractCometaryActivity``.

        We have chosen the name "identity" here because the input dataframe is
        returned unchanged.

        Returns
        -------
        str
            Unique identifier for this cometary activity model
        """
        return "identity"
