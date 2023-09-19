"""The CombinedDataReader class supports loading the entire input data
for the simulator post processing by using individuals reader classes
to read individual input files and combining the data into a single table.

The CombinedDataReader object reads the data in blocks to limit memory usage.
For each blocks, it uses two stages:
1) It reads a range of individual rows from the ``primary_reader``. By default this
   reader is the first auxiliary data reader, but can be set to the ephemeris reader.
   This reader is used to extract a list of object IDs for this block.
2) For each of the readers (ephemeris and auxiliary data) load in all the rows
   corresponding to the object IDs extracted in stage 1.

For example, if the ephemeris file is used as the primary reader, the algorithm
will load data in blocks of the ephemeris rows and join in the auxiliary data
for just the object IDs on those rows. It is not guaranteed to include all
rows for the current objects.
"""
import logging
import pandas as pd
import sys


class CombinedDataReader:
    def __init__(self, ephem_primary=False, **kwargs):
        """
        Parameters
        ----------
        ephem_primary (bool, optional): Use the ephemeris reader as the primary
            reader. Otherwise uses the first auxiliary data reader.
        """
        self.ephem_reader = None
        self.aux_data_readers = []
        self.block_start = 0
        self.ephem_primary = ephem_primary

    def add_ephem_reader(self, new_reader):
        """Add a new reader for ephemeris data.

        Parameters
        ----------
        new_reader (ObjectDataReader): The reader for a specific input file.
        """
        pplogger = logging.getLogger(__name__)
        if self.ephem_reader is not None:
            pplogger.error("ERROR: Ephemeris reader already set.")
            sys.exit("ERROR: Ephemeris reader already set.")
        self.ephem_reader = new_reader

    def add_aux_data_reader(self, new_reader):
        """Add a new object reader that corresponds to an auxiliary input data type..

        Parameters
        ----------
        new_reader (ObjectDataReader): The reader for a specific input file.
        """
        self.aux_data_readers.append(new_reader)

    def read_block(self, block_size=None, verbose=False, **kwargs):
        """Reads in a set number of rows from the input, performs
        post-processing and validation, and returns a data frame.

        Parameters:
        -----------
        block_size (int, optional): the number of rows to read in.
            Use block_size=None to read in all available data.
            [Default = None]

        verbose (bool, optional): use verbose logging.

        Returns:
        -----------
        res_df (Pandas dataframe): dataframe of the combined object data.

        """
        pplogger = logging.getLogger(__name__)
        verboselog = pplogger.info if verbose else lambda *a, **k: None

        if self.ephem_reader is None:
            pplogger.error("ERROR: No ephemeris reader provided.")
            sys.exit("ERROR: No ephemeris reader provided.")
        if len(self.aux_data_readers) == 0:
            pplogger.error("ERROR: No auxiliary readers provided.")
            sys.exit("ERROR: No auxiliary readers provided.")

        # Load object IDs from the primary table.
        if self.ephem_primary:
            verboselog(f"Loading object IDs from: {self.ephem_reader.get_reader_info()}")
            ephem_df = self.ephem_reader.read_rows(self.block_start, block_size)
            self.block_start += len(ephem_df)

            if not "ObjID" in ephem_df.columns:
                pplogger.error("ERROR: No ObjID provided for ephemerides.")
                sys.exit("ERROR: No ObjID provided for ephemerides.")

            obj_ids = ephem_df["ObjID"].unique().tolist()
            primary_df = None
        else:
            verboselog(f"Loading object IDs from: {self.aux_data_readers[0].get_reader_info()}")
            primary_df = self.aux_data_readers[0].read_rows(self.block_start, block_size)
            self.block_start += len(primary_df)

            if not "ObjID" in primary_df.columns:
                pplogger.error("ERROR: No ObjID provided.")
                sys.exit("ERROR: No ObjID provided.")

            obj_ids = primary_df["ObjID"].unique().tolist()
            ephem_df = None

        # No more data to load.
        if len(obj_ids) == 0:
            return None

        # Load in the data for this block.
        if ephem_df is None:
            ephem_df = self.ephem_reader.read_objects(obj_ids)
        ephem_ids = set(ephem_df["ObjID"].unique().tolist())

        for i, reader in enumerate(self.aux_data_readers):
            # Skip reading the data from the first auxiliary file if we already read it.
            if i == 0 and primary_df is not None:
                current_df = primary_df
            else:
                verboselog(f"Reading input file: {reader.get_reader_info()}")
                current_df = reader.read_objects(obj_ids)

            # Check that the new dataframe has at least the object IDs matching
            # the ephemeris frame.
            verboselog("Checking Object IDs in auxiliary data")
            current_ids = set(pd.unique(current_df["ObjID"]).astype(str))
            if not ephem_ids.issubset(current_ids):  # pragma: no cover
                pplogger.error(f"ERROR: At least one missing ObjID in {reader.get_reader_info()}")
                sys.exit(f"ERROR: At least one missing ObjID {reader.get_reader_info()}")

            verboselog("Joining auxiliary data with ephemeris")
            ephem_df = ephem_df.join(current_df.set_index("ObjID"), on="ObjID")

        return ephem_df

    def read_aux_block(self, block_size=None, verbose=False, **kwargs):
        """Reads in a set number of rows from the input, performs
        post-processing and validation, and returns a data frame.

        This function DOES NOT include the ephemeris data in the returned data frame.
        It is to be used when generating the ephemeris during the execution of Sorcha.

        Parameters:
        -----------
        block_size (int, optional): the number of rows to read in.
            Use block_size=None to read in all available data.
            [Default = None]

        verbose (bool, optional): use verbose logging.

        Returns:
        -----------
        res_df (Pandas dataframe): dataframe of the combined object data, excluding
        any ephemeris data.

        """
        pplogger = logging.getLogger(__name__)
        verboselog = pplogger.info if verbose else lambda *a, **k: None

        if len(self.aux_data_readers) == 0:
            pplogger.error("ERROR: No auxiliary readers provided.")
            sys.exit("ERROR: No auxiliary readers provided.")

        # Load object IDs from the primary table.
        verboselog(f"Loading object IDs from: {self.aux_data_readers[0].get_reader_info()}")
        primary_df = self.aux_data_readers[0].read_rows(self.block_start, block_size)
        self.block_start += len(primary_df)

        if not "ObjID" in primary_df.columns:
            pplogger.error("ERROR: No ObjID provided.")
            sys.exit("ERROR: No ObjID provided.")

        obj_ids = primary_df["ObjID"].unique().tolist()

        # No more data to load.
        if len(obj_ids) == 0:
            return None

        aux_data_df = None
        for i, reader in enumerate(self.aux_data_readers):
            # Skip reading the data from the first auxiliary file if we already read it.
            if i == 0 and primary_df is not None:
                current_df = primary_df
            else:
                verboselog(f"Reading input file: {reader.get_reader_info()}")
                current_df = reader.read_objects(obj_ids)

            # Check that the new dataframe has at least the object IDs matching
            # the ephemeris frame.
            verboselog("Checking Object IDs in auxiliary data")
            current_ids = set(pd.unique(current_df["ObjID"]).astype(str))
            if not current_ids.issubset(obj_ids):  # pragma: no cover
                pplogger.error(f"ERROR: At least one missing ObjID in {reader.get_reader_info()}")
                sys.exit(f"ERROR: At least one missing ObjID {reader.get_reader_info()}")

            if i == 0:
                aux_data_df = current_df
            else:
                verboselog("Joining auxiliary data without ephemeris")
                aux_data_df = aux_data_df.join(current_df.set_index("ObjID"), on="ObjID")

        return aux_data_df
