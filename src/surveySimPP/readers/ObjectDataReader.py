"""Classes for reading object-related data from a variety of sources.
Each data source needs to have a column ObjID that identifies the object and
can be used for joining and filtering.
"""
import abc


class ObjectDataReader(abc.ABC):
    """The base class for reading in the object data."""

    def __init__(self, *args, **kwargs):
        pass

    @abc.abstractmethod
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

        Returns:
        -----------
        res_df (Pandas dataframe): dataframe of the object data.

        """
        pass  # pragma: no cover

    @abc.abstractmethod
    def read_objects(self, obj_ids, **kwargs):
        """Read in a chunk of data corresponding to all rows for
        a given set of object IDs.

        Parameters:
        -----------
        obj_ids (list): A list of object IDs to use.

        Returns:
        -----------
        res_df (Pandas dataframe): The dataframe for the object data.
        """
        pass  # pragma: no cover

    def process_and_validate_input_table(self, input_table, **kwargs):
        """Perform any input-specific processing and validation on the input table.
        Modifies the input dataframe in place.

        Parameters:
        -----------
        input_table (Pandas dataframe): A loaded table.

        Returns:
        -----------
        res_df (Pandas dataframe): Returns the input dataframe modified in-place.
        """
        return input_table
