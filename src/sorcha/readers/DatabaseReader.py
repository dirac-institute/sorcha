import pandas as pd
import sqlite3
import logging
import sys

from sorcha.readers.ObjectDataReader import ObjectDataReader

# NOTE: this was written for a now-defunct functionality, but has been left
# in the code as a database reader class may be useful later.


class DatabaseReader(ObjectDataReader):
    """A class to read in object data stored in a sqlite database."""

    def __init__(self, intermdb, **kwargs):
        """A class for reading the object data from a sqlite database.

        Parameters:
        -----------
        intermdb (string): filepath/name of temporary database.
        """
        super().__init__(**kwargs)
        self.intermdb = intermdb

    def get_reader_info(self):
        """Return a string identifying the current reader name
        and input information (for logging and output).

        Returns:
        --------
        name (str): The reader information.
        """
        return f"DatabaseReader:{self.intermdb}"

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
            A non-None block size must be provided if block_start > 0.

        validate_data (bool, optional): if True then checks the data for
            NaNs or nulls.

        Returns:
        ----------
        res_df (Pandas dataframe): dataframe of the object data.


        Notes:
        ------
        A non-None block size must be provided if block_start > 0.
        """
        if block_start > 0 and block_size is None:
            pplogger = logging.getLogger(__name__)
            pplogger.error("ERROR: DatabaseReader requires a block_size when block_start > 0.")
            sys.exit("ERROR: DatabaseReader requires a block_size when block_start > 0.")

        con = sqlite3.connect(self.intermdb)
        if block_size is not None:
            sql = f"SELECT * FROM interm ORDER BY ObjID LIMIT {block_start}, {block_size}"
        else:
            sql = "SELECT * FROM interm ORDER BY ObjID"
        res_df = pd.read_sql(sql, con=con)
        return res_df

    def _read_objects_internal(self, obj_ids, **kwargs):
        """Read in a chunk of data for given object IDs.

        Parameters:
        -----------
        obj_ids (list): A list of object IDs to use.

        Returns:
        -----------
        res_df (Pandas dataframe): The dataframe for the object data.
        """
        con = sqlite3.connect(self.intermdb)
        prm_list = ", ".join("?" for _ in obj_ids)
        sql = "SELECT * FROM interm WHERE ObjID IN ({})".format(prm_list)

        res_df = pd.read_sql(sql, con=con, params=obj_ids)
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
