"""The CombinedDataReader class supports loading the entire input data
for the simulator post processing by using individuals reader classes
to read individual input files and combining the data into a single table.

The CombinedDataReader object reads the data in blocks to limit memory usage.
For each blocks, it uses two stages:
1) It reads a range of individual rows from the ``primary_reader``. This reader
   can be any of the individual data files as long as reading it in a row-wise
   fashion produces valid results. It uses the data from the primary_reader to
   assemble a list of object IDs that it will read in stage 2.
2) For each of the other readers (``object_readers``) load in all the rows
   corresponding to the object IDs extracted in stage 1.

For example, if the ephemeris file is used as the primary reader, the algorithm
will load data in blocks of the ephemeris rows and load the auxiliary data
for just the object IDs on those rows. Alternatively if the orbit file
is used, the algorithm will load data in blocks of object ids and load *all*
ephemeris for those objects.
"""
import logging
import sys


class CombinedDataReader:
    def __init__(self, **kwargs):
        self.primary_reader = None
        self.object_readers = []
        self.block_start = 0

    def add_primary_reader(self, new_reader):
        """Add a new reader that corresponds to an input data type..

        Parameters
        ----------
        new_reader (ObjectDataReader): The reader for a specific input file.
        """
        pplogger = logging.getLogger(__name__)
        if self.primary_reader is not None:
            pplogger.error("ERROR: Primary reader already set.")
            sys.exit("ERROR: Primary reader already set.")

        self.primary_reader = new_reader

    def add_reader(self, new_reader):
        """Add a new object reader that corresponds to an input data type..

        Parameters
        ----------
        new_reader (ObjectDataReader): The reader for a specific input file.
        """
        self.object_readers.append(new_reader)

    def reset_block_start(self, new_start=0):
        """Reset the starting row for reading blocks of data.

        Parameters
        ----------
        new_reader (ObjectDataReader): The reader for a specific input file.
        """
        pplogger = logging.getLogger(__name__)
        if new_start < 0:
            pplogger.error(f"ERROR: Invalid block start ({new_start}).")
            sys.exit(f"ERROR: Invalid block start ({new_start}).")
        self.block_start = new_start

    def read_block(self, block_size=None, **kwargs):
        """Reads in a set number of rows from the input, performs
        post-processing and validation, and returns a data frame.

        Parameters:
        -----------
        block_size (int, optional): the number of rows to read in.
            Use block_size=None to read in all available data.
            [Default = None]

        Returns:
        -----------
        res_df (Pandas dataframe): dataframe of the combined object data.

        """
        pplogger = logging.getLogger(__name__)
        verboselog = pplogger.info if verbose else lambda *a, **k: None

        if self.primary_reader is None:
            pplogger.error("ERROR: No primary reader provided.")
            sys.exit("ERROR: No primary reader provided.")

        # Load data from the primary table.
        verboselog(f"Reading primary input file: {primary_reader.get_reader_info()}")
        primary_df = self.primary_reader.read_rows(self.block_start, block_size)
        objid_list = primary_df["ObjID"].unique().tolist()

        # Load and join in the other data frames.
        for reader in self.object_readers:
            verboselog(f"Reading input file: {reader.get_reader_info()}")
            current_df = reader.read_objects(objid_list)

            # Check that the new dataframe has the correct object IDs.
            current_objs = pd.unique(current_df["ObjID"]).astype(str)
            if set(current_objs) != set(objid_list):
                pplogger.error("ERROR: ObjectIDs do not match primary table.")
                sys.exit("ERROR: ObjectIDs do not match primary table.")

            primary_df = primary_df.join(current_df.set_index("ObjID"), on="ObjID")

        return primary_df
