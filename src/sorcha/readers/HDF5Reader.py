import pandas as pd

from sorcha.readers.ObjectDataReader import ObjectDataReader


class HDF5DataReader(ObjectDataReader):
    """A class to read in object data files stored as HDF5 files."""

    def __init__(self, filename, **kwargs):
        """A class for reading the object data from an HDF5 file.

        Parameters:
        -----------
        filename (string): location/name of the data file.
        """
        super().__init__(**kwargs)
        self.filename = filename

        # A table holding just the object ID for each row. Only populated
        # if we try to read data for specific object IDs.
        self.obj_id_table = None

    def get_reader_info(self):
        """Return a string identifying the current reader name
        and input information (for logging and output).

        Returns:
        --------
        name (str): The reader information.
        """
        return f"HDF5DataReader:{self.filename}"

    def _read_rows_internal(self, block_start=0, block_size=None, **kwargs):
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
        res_df (Pandas dataframe): dataframe of the object data.
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
        return res_df

    def _build_id_map(self):
        """Builds a table of just the object IDs"""
        if self.obj_id_table is not None:
            return
        self.obj_id_table = pd.read_hdf(self.filename, columns=["ObjID"])
        self.obj_id_table = self._validate_object_id_column(self.obj_id_table)

    def _read_objects_internal(self, obj_ids, **kwargs):
        """Read in a chunk of data for given object IDs.

        Parameters:
        -----------
        obj_ids (list): A list of object IDs to use.

        Returns:
        -----------
        res_df (Pandas dataframe): The dataframe for the object data.
        """
        self._build_id_map()
        row_match = self.obj_id_table["ObjID"].isin(obj_ids)
        match_inds = self.obj_id_table[row_match].index
        res_df = pd.read_hdf(self.filename, where="index=match_inds")  # noqa: F841
        return res_df

    def _process_and_validate_input_table(self, input_table, **kwargs):
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
        # Perform the parent class's validation (checking object ID column).
        input_table = super()._process_and_validate_input_table(input_table, **kwargs)

        return input_table
