from abc import ABC, abstractmethod
import numpy as np
import pandas as pd


class AbstractLightCurve(ABC):
    """Abstract base class for lightcurve models"""

    def __init__(self, required_column_names: list[str] = []) -> None:
        """Abstract base class accepts a list of column names that are required
        to be present in the Pandas dataframe passed to the ``compute`` method.

        Parameters
        ----------
        required_column_names : list, optional
            The list of columns in ``observations`` dataframe that are required
            for the model calculation, by default []
        """
        self.required_column_names = required_column_names

    @abstractmethod
    def compute(self, df: pd.DataFrame) -> np.array:
        """User implemented calculation based on the input provided by the
        pandas dataframe ``df``.

        Parameters
        ----------
        df : Pandas dataframe
            The ``observations`` dataframe provided by ``Sorcha``.
        """
        raise (NotImplementedError, "Must be implemented by the subclass")

    def _validate_column_names(self, df: pd.DataFrame) -> None:
        """Private method that checks that the provided pandas dataframe contains
           the required columns defined in ``self.required_column_names``.

        Parameters
        ----------
        df : _type_
            _description_
        """
        for colname in self.required_column_names:
            if colname not in df.columns:
                raise (ValueError, f"Input dataframe is missing column %{colname}")

    @staticmethod
    @abstractmethod
    def name_id() -> str:
        """This method will return the unique name of the LightCurve Model"""
        raise (NotImplementedError, "Must be implemented as a static method by the subclass")


# ! The code below will be moved to the `sorcha_community_utils` repository soon
TIME_COLUMN = "FieldMJD"


class SinusoidalLightCurve(AbstractLightCurve):
    """
    Note: assuming sinusoidal in magnitude instead of flux. Maybe not call LCA?
    """

    def __init__(self, required_column_names: list[str] = [TIME_COLUMN, "LCA", "Period", "Time0"]) -> None:
        super().__init__(required_column_names)

    def compute(self, df: pd.DataFrame) -> np.array:
        """
        Computes a sinusoidal light curve given the input dataframe
        """

        self._validate_column_names(df)

        modtime = np.mod(df[TIME_COLUMN] / df["Period"] + df["Time0"], 2 * np.pi)
        return df["LCA"] * np.sin(modtime)

    @staticmethod
    def name_id() -> str:
        return "sinusoidal"
