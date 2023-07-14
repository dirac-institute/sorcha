import pandas as pd
import logging
import sys

from surveySimPP.readers.ObjectDataReader import ObjectDataReader


class HDF5Reader(ObjectDataReader):
    """A class to read in object data files stored as HDF5 files."""

    def __init__(self, filename, *args, **kwargs):
        """A class for reading the object data from an HDF5 file.

        Parameters:
        -----------
        filename (string): location/name of the data file.
        """
        super().__init__(*args, **kwargs)
        self.filename = filename

    def read_rows(self, block_start=0, block_size=None, **kwargs):
        """Reads in a set number of rows from the input.

        Parameters:
        -----------
        block_start (int, optional): The 0-indexed row number from which
            to start reading the data. For example in a CSV file
            block_start=2 would skip the first two lines after the header
            and return data starting on row=2. [Default=0]

        block_size (int, optional): the number of rows to read in.
            Use block_size=None to read in all available data.
            [Default = None]

        validate_data (bool, optional): if True then checks the data for
            NaNs or nulls.

        Returns:
        -----------
        res_df (Pandas dataframe): dataframe of the auxilary data.
        """
        if block_size is None:
            res_df = pd.read_hdf(
                self.filename,
                start=block_start,
            )
        else:
            res_df = pd.read_hdf(
                self.filename,
                start=block_start,
                stop=block_start + block_size,
            )
        res_df = self.process_and_validate_input_table(res_df, **kwargs)
        return res_df

    def read_objects(self, obj_ids, **kwargs):
        """Read in a chunk of data for given object IDs.

        Parameters:
        -----------
        obj_ids (list): A list of object IDs to use.

        Returns:
        -----------
        res_df (Pandas dataframe): The dataframe for the ephemerides.
        """
        res_df = pd.read_hdf(self.filename, where="ObjID=obj_ids")

        res_df = self.process_and_validate_input_table(res_df, **kwargs)
        return res_df

    def process_and_validate_input_table(self, input_table, **kwargs):
        """Perform any input-specific processing and validation on the input table.
        Modifies the input dataframe in place.

        Note
        ----
        The base implementation includes filtering that is common to most
        input types. Subclasses should call super.process_and_validate()
        to ensure that the ancestor’s validation is also applied.

        Parameters:
        -----------
        input_table (Pandas dataframe): A loaded table.

        Returns:
        -----------
        input_table (Pandas dataframe): Returns the input dataframe modified in-place.
        """
        # Perform the parent class's validation.
        input_table = super().process_and_validate_input_table(input_table, **kwargs)
        return input_table
