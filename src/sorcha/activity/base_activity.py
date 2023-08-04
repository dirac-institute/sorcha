from abc import ABC, abstractmethod
import pandas as pd
import numpy as np


class AbstractCometaryActivity(ABC):
    """Abstract base class for cometary activity models"""

    def __init__(self) -> None:
        """Abstract base class accepts a list of column names that are required
        to be present in the Pandas dataframe passed to the ``compute`` method.
        """
        self.required_column_names = []

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
        df : Pandas dataframe
            The ``observations`` dataframe provided by ``Sorcha``.
        """
        for colname in self.required_column_names:
            if colname not in df.columns:
                raise (ValueError, f"Input dataframe is missing column %{colname}")

    @staticmethod
    @abstractmethod
    def name_id() -> str:
        """This method will return the unique name of the LightCurve Model"""
        raise (NotImplementedError, "Must be implemented as a static method by the subclass")
