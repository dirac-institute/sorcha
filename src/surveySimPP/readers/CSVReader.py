import pandas as pd
import logging
import sys

from surveySimPP.readers.ObjectDataReader import ObjectDataReader


class CSVDataReader(ObjectDataReader):
    """A class to read in object data files stores as CSV or whitespace
    separated values.

    Requires that the file's first column is ObjID.
    """

    def __init__(self, filename, sep="csv", header=-1, *args, **kwargs):
        """A class for reading the object data from a CSV file.

        Parameters:
        -----------
        filename (string): location/name of the data file.

        sep (string, optional): format of input file ("whitespace"/"comma"/"csv").

        header (int): The row number of the header. If not provided, does an automatic search.
        """
        super().__init__(*args, **kwargs)
        self.filename = filename
        self.sep = sep

        if header < 0:
            self.header_row = self._find_header_line()
        else:
            self.header_row = header

        # A table holding just the object ID for each row. Only populated
        # if we try to read data for specific object IDs.
        self.obj_id_table = None

    def _find_header_line(self):
        """Find the line number of the CSV header. Used for cases
        where the header is not the first line and we want to skip down.

        Returns:
        --------
        i (int) : The line index of the header.

        """
        with open(self.filename) as fh:
            for i, line in enumerate(fh):
                if line.startswith("ObjID"):
                    return i
                if i > 100:  # because we don't want to scan infinitely
                    break

        pplogger = logging.getLogger(__name__)
        pplogger.error(
            "ERROR: OIFCSVReader: column headings not found. Ensure column headings exist in OIF output and first column is ObjID."
        )
        sys.exit(
            "ERROR: OIFCSVReader: column headings not found. Ensure column headings exist in OIF output and first column is ObjID."
        )
        return 0

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
        pplogger = logging.getLogger(__name__)

        # Skip the rows before the header and then begin_loc rows after the header.
        skip_rows = []
        if self.header_row > 0:
            skip_rows = [i for i in range(0, self.header_row)]
        if block_start > 0:
            skip_rows.extend([i for i in range(self.header_row + 1, self.header_row + 1 + block_start)])

        # Read the rows.
        if self.sep == "whitespace":
            res_df = pd.read_csv(
                self.filename,
                delim_whitespace=True,
                skiprows=skip_rows,
                nrows=block_size,
            )
        elif self.sep == "comma" or self.sep == "csv":
            res_df = pd.read_csv(
                self.filename,
                delimiter=",",
                skiprows=skip_rows,
                nrows=block_size,
            )
        else:
            pplogger.error(f"ERROR: Unrecognized delimiter ({self.sep})")
            sys.exit(f"ERROR: Unrecognized delimiter ({self.sep})")

        # Strip out the whitespace from the column names.
        res_df = res_df.rename(columns=lambda x: x.strip())

        # Check that the ObjID column exists and convert it to a string.
        try:
            res_df["ObjID"] = res_df["ObjID"].astype(str)
        except KeyError:
            err_str = f"ERROR: Unable to find ObjID column headings in {self.filename}."
            pplogger.error(err_str)
            sys.exit(err_str)

        # Check for NaNs or nulls.
        if "validate_data" in kwargs and kwargs["validate_data"]:
            if res_df.isnull().values.any():
                pdt = res_df[res_df.isna().any(axis=1)]
                inds = str(pdt["ObjID"].values)
                outstr = (
                    f"ERROR: While reading {self.filename} found uninitialised values ObjID: {str(inds)}."
                )
                pplogger.error(outstr)
                sys.exit(outstr)

        return res_df

    def _build_id_map(self):
        """Builds a table of just the object IDs"""
        if self.obj_id_table is not None:
            return

        if self.sep == "whitespace":
            self.obj_id_table = pd.read_csv(
                self.filename,
                delim_whitespace=True,
                header=self.header_row,
            )
        elif self.sep == "comma" or self.sep == "csv":
            self.obj_id_table = pd.read_csv(
                self.filename,
                delimiter=",",
                header=self.header_row,
            )
        else:
            pplogger = logging.getLogger(__name__)
            pplogger.error(f"ERROR: Unrecognized delimiter ({self.sep})")
            sys.exit(f"ERROR: Unrecognized delimiter ({self.sep})")

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

        # Create list of only the matching rows for these object IDs and the header row.
        row_good = [False] * self.header_row  # pre-header
        row_good = [True]  # the header
        row_good.extend(self.obj_id_table["ObjID"].isin(obj_ids).values)

        # Read the rows.
        if self.sep == "whitespace":
            res_df = pd.read_csv(
                self.filename,
                delim_whitespace=True,
                skiprows=(lambda x: not row_good[x]),
            )
        elif self.sep == "comma" or self.sep == "csv":
            res_df = pd.read_csv(
                self.filename,
                delimiter=",",
                skiprows=(lambda x: not row_good[x]),
            )
        else:
            pplogger = logging.getLogger(__name__)
            pplogger.error(f"ERROR: Unrecognized delimiter ({self.sep})")
            sys.exit(f"ERROR: Unrecognized delimiter ({self.sep})")

        return res_df
