from sorcha.lightcurves.base_lightcurve import AbstractLightCurve
from typing import List
import numpy as np
import pandas as pd

"""
!!!!!!!!!!!!!!!!
FOR TESTING ONLY
!!!!!!!!!!!!!!!!
"""


class IdentityLightCurve(AbstractLightCurve):
    """
    !!! THIS SHOULD NEVER BE USED - FOR TESTING ONLY !!!

    Rudimentary lightcurve model that returns no shift. This class is explicitly
    created for testing purposes.
    """

    def __init__(self, required_column_names: List[str] = ["FieldMJD_TAI"]) -> None:
        super().__init__(required_column_names)

    def compute(self, df: pd.DataFrame) -> np.array:
        """Returns numpy array of 0's with shape equal to the input dataframe
        time column.

        Parameters
        ----------
        df : Pandas dataframe
            The ``observations`` dataframe provided by ``Sorcha``.

        Returns
        -------
        np.array
            Numpy array of 0's with shape equal to the input dataframe time column.
        """

        self._validate_column_names(df)

        return np.zeros_like(df["FieldMJD_TAI"])

    @staticmethod
    def name_id() -> str:
        """Returns the string identifier for this light curve method. It must be
        unique within all the subclasses of ``AbstractLightCurve``.

        We have chosen the name "identity" here because the input brightness will
        equal the output brightness if this model is applied.

        Returns
        -------
        str
            Unique identifier for this light curve calculator
        """
        return "identity"
