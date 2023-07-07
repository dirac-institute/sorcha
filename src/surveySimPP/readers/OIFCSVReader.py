import pandas as pd
import sqlite3
import logging
import sys

from surveySimPP.readers import EphemerisReader

class OIFCSVReader(EphemerisReader):

    def __init__(self, filename, sep="csv", *args, **kwargs):
        """A class for reading the ephemerides from a database.

        Parameters:
        -----------
        filename (string): location/name of the data file.

        sep (string, optional): format of input file ("whitespace"/"comma"/"csv").
        """
        super().__init__(*args, **kwargs)
        self.filename = filename
        self.sep = sep

        self.header_row = self._find_header()
        self.obj_id_map = None


    def _find_header(self):
        """Find the line number of the CSV header.

        Returns:
        --------
        i (int) : The line index of the header.

        """
        with open(self.filename) as fh:
            for i, line in enumerate(fh):
                if line.startswith("ObjID"):
                    return i
            if i > 100:  # because we don't want to scan infinitely - OIF headers are ~30 lines long.
                break

        pplogger = logging.getLogger(__name__)
        pplogger.error(
            "ERROR: OIFCSVReader: column headings not found. Ensure column headings exist in OIF output and first column is ObjID."
        )
        sys.exit(
            "ERROR: OIFCSVReader: column headings not found. Ensure column headings exist in OIF output and first column is ObjID."
        )


    def read_rows(self, begin_loc=0, chunk_size=None):
        """Reads in a set number of rows from the input file.

        Parameters:
        -----------
        begin_loc (int, optional): location in file where reading begins. This is the
           number of the line after the header, so 0 would be the first line of data
           [Default = 0].

        chunk_size (int, optional): length of chunk to be read in. Use None to read
            the entire file. [Default = None]

        Returns:
        -----------
        res_df (Pandas dataframe): dataframe of the auxilary data.

        """
        pplogger = logging.getLogger(__name__)

        # Skip the rows before the header and then begin_loc rows after the header.            
        skip_rows = []
        if self.header_row > 0:
            skip_rows = [i for i in range(0, self.header_row)]
        if begin_loc > 0:
            skip_rows.extend([i for i in range(self.header_row + 1, self.header_row + 1 + begin_loc)]

        # Read the rows.
        if self.sep == "whitespace":
            res_df = pd.read_csv(
                self.filename,
                delim_whitespace=True,
                skiprows=skip_rows
                nrows=chunk_size,
                header=self.header_row,
            )
        elif self.sep == "comma" or filesep == "csv":
            res_df = pd.read_csv(
                self.filename,
                delimiter=",",
                skiprows=skip_rows
                nrows=chunk_size,
                header=self.header_row,
            )
        else:
            pplogger.error(f"ERROR: Unrecognized delimiter ({filesep})")
            sys.exit(f"ERROR: Unrecognized delimiter ({filesep})")

        return res_df


    def _build_id_map(self):
        """Builds a table of just the object IDs"""
        if self.obj_id_map is not None:
            return

        if self.sep == "whitespace":
            self.obj_id_map = pd.read_csv(
                self.filename,
                delim_whitespace=True,
                header=self.header_row,
            )
        elif self.sep == "comma" or filesep == "csv":
            self.obj_id_map = pd.read_csv(
                self.filename,
                delimiter=",",
                header=self.header_row,
            )
        else:
            pplogger.error(f"ERROR: Unrecognized delimiter ({filesep})")
            sys.exit(f"ERROR: Unrecognized delimiter ({filesep})")


        # Maybe just save the values???
        self.obj_id_map = self.obj_id_map["ObjID"].values

            
    def read_objects(self, obj_ids=None):
        """Read in a chunk of data for given object IDs.

        Parameters:
        -----------
        obj_ids (list, optional): A list of object IDs to use.

        Returns:
        -----------
        res_df (Pandas dataframe): The dataframe for the ephemerides.
        """
        self._build_id_map()

        # Redo if we only save the values...
        goodrows = self.obj_id_map["ObjID"].isin(obj_ids).index
        goodrows = goodrows.insert(self.header_row, 0)

        # Read the rows.
        if self.sep == "whitespace":
            res_df = pd.read_csv(
                self.filename,
                delim_whitespace=True,
                skiprows=(lambda x: x not in goodrows),
            )
        elif self.sep == "comma" or filesep == "csv":
            res_df = pd.read_csv(
                self.filename,
                delimiter=",",
                skiprows=(lambda x: x not in goodrows),
            )
        else:
            pplogger.error(f"ERROR: Unrecognized delimiter ({filesep})")
            sys.exit(f"ERROR: Unrecognized delimiter ({filesep})")

        return res_df

