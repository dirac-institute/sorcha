import pandas as pd
import logging
import sys

from surveySimPP.readers.ObjectDataReader import ObjectDataReader


class HDF5DataReader(ObjectDataReader):
    """A class to read in object data files stored as HDF5 files."""

    def __init__(self, filename, *args, **kwargs):
        """A class for reading the object data from an HDF5 file.

        Parameters:
        -----------
        filename (string): location/name of the data file.
        """
        super().__init__(*args, **kwargs)
        self.filename = filename

        # A table holding just the object ID for each row. Only populated
        # if we try to read data for specific object IDs.
        self.obj_id_table = None

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

    def _build_id_map(self):
        """Builds a table of just the object IDs"""
        if self.obj_id_table is not None:
            return
        self.obj_id_table = pd.read_hdf(self.filename, columns=["ObjID"])
        self.obj_id_table = self._validate_object_id_column(self.obj_id_table)

    def read_objects(self, obj_ids, **kwargs):
        """Read in a chunk of data for given object IDs.

        Parameters:
        -----------
        obj_ids (list): A list of object IDs to use.

        Returns:
        -----------
        res_df (Pandas dataframe): The dataframe for the ephemerides.
        """
        self._build_id_map()
        row_match = self.obj_id_table["ObjID"].isin(obj_ids)
        read_rows = self.obj_id_table[row_match].index

        res_df = pd.read_hdf(self.filename, where="index=read_rows")
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

        disallow_nan (bool, optional): if True then checks the data for
            NaNs or nulls.

        Returns:
        -----------
        input_table (Pandas dataframe): Returns the input dataframe modified in-place.
        """
        # Perform the parent class's validation (checking object ID column).
        input_table = super().process_and_validate_input_table(input_table, **kwargs)

        # Check for NaNs or nulls.
        if "disallow_nan" in kwargs and kwargs["disallow_nan"]:  # pragma: no cover
            if input_table.isnull().values.any():
                pdt = input_table[input_table.isna().any(axis=1)]
                inds = str(pdt["ObjID"].values)
                outstr = f"ERROR: While reading table {self.filename} found uninitialised values ObjID: {str(inds)}."

                pplogger = logging.getLogger(__name__)
                pplogger.error(outstr)
                sys.exit(outstr)

        return input_table
