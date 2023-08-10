from abc import ABC, abstractmethod
from typing import List
import logging
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


class AbstractCometaryActivity(ABC):
    """Abstract base class for cometary activity models"""

    def __init__(self, required_column_names: List[str] = []) -> None:
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
        df : Pandas dataframe
            The ``observations`` dataframe provided by ``Sorcha``.
        """
        for colname in self.required_column_names:
            if colname not in df.columns:
                err_msg = f"Input dataframe is missing column %{colname}"
                self._log_error_message(error_msg=err_msg)
                raise (ValueError, err_msg)

    def _log_exception(self, exception: Exception) -> None:
        """Log an error message from an exception to the error log file

        Parameters
        ----------
        exception : Exception
            The exception with a value string to appended to the error log
        """
        self._log_error_message(str(exception.value))

    def _log_error_message(self, error_msg: str) -> None:
        """Log a specific error string to the error log file

        Parameters
        ----------
        error_msg : str
            The string to be appended to the error log
        """
        logger.error(error_msg)

    @staticmethod
    @abstractmethod
    def name_id() -> str:
        """This method will return the unique name of the LightCurve Model"""
        raise (NotImplementedError, "Must be implemented as a static method by the subclass")
