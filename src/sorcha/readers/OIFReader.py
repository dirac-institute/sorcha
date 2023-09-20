import numpy as np
import logging
import sys

from sorcha.readers.CSVReader import CSVDataReader
from sorcha.readers.HDF5Reader import HDF5DataReader
from sorcha.readers.ObjectDataReader import ObjectDataReader


class OIFDataReader(ObjectDataReader):
    """A class to read in ephemeris from a OIF file.

    Instead of subclassing the various readers (CSV, HDF5, etc.) individually, this class instantiates
    one of those classes in an internal ``reader`` attribute. As such all reading, validation, etc. is
    passed off to the ``reader`` object this object owns. While this adds a level of indirection, it
    allows us to support a cross product of N file types from M ephemeris generators with M + N readers
    instead of M * N.
    """

    def __init__(self, filename, inputformat, **kwargs):
        """A class for reading the object data from a CSV file.

        Parameters:
        -----------
        filename (string): location/name of the data file.

        inputformat (string): format of input file ("whitespace"/"comma"/"csv"/"h5"/"hdf5").
        """
        super().__init__(**kwargs)

        pplogger = logging.getLogger(__name__)
        self.reader = None
        if (inputformat == "whitespace") or (inputformat == "comma") or (inputformat == "csv"):
            self.reader = CSVDataReader(filename, sep=inputformat, **kwargs)
        elif (inputformat == "h5") or (inputformat == "hdf5") or (inputformat == "HDF5"):
            self.reader = HDF5DataReader(filename, **kwargs)
        else:
            pplogger.error(
                f"ERROR: OIFDataReader: unknown format for ephemeris simulation results ({inputformat})."
            )
            sys.exit(
                f"ERROR: OIFDataReader: unknown format for ephemeris simulation results ({inputformat})."
            )

    def get_reader_info(self):
        """Return a string identifying the current reader name
        and input information (for logging and output).

        Returns:
        --------
        name (str): The reader information.
        """
        return f"OIFDataReader|{self.reader.get_reader_info()}"

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

        Returns:
        -----------
        res_df (Pandas dataframe): dataframe of the object data.

        """
        res_df = self.reader.read_rows(block_start, block_size, **kwargs)
        return res_df

    def _read_objects_internal(self, obj_ids, **kwargs):
        """Read in a chunk of data corresponding to all rows for
        a given set of object IDs.

        Parameters:
        -----------
        obj_ids (list): A list of object IDs to use.

        Returns:
        -----------
        res_df (Pandas dataframe): The dataframe for the object data.
        """
        res_df = self.reader.read_objects(obj_ids, **kwargs)
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
        # We do not call reader.process_and_validate_input_table() or
        # super().process_and_validate_input_table() because reader's read functions have
        # already check the table.

        input_table = input_table.rename(columns=lambda x: x.strip())
        input_table = input_table.drop(["V", "V(H=0)"], axis=1, errors="ignore")

        oif_cols = [
            "ObjID",
            "FieldID",
            "FieldMJD_TAI",
            "AstRange(km)",
            "AstRangeRate(km/s)",
            "AstRA(deg)",
            "AstRARate(deg/day)",
            "AstDec(deg)",
            "AstDecRate(deg/day)",
            "Ast-Sun(J2000x)(km)",
            "Ast-Sun(J2000y)(km)",
            "Ast-Sun(J2000z)(km)",
            "Ast-Sun(J2000vx)(km/s)",
            "Ast-Sun(J2000vy)(km/s)",
            "Ast-Sun(J2000vz)(km/s)",
            "Obs-Sun(J2000x)(km)",
            "Obs-Sun(J2000y)(km)",
            "Obs-Sun(J2000z)(km)",
            "Obs-Sun(J2000vx)(km/s)",
            "Obs-Sun(J2000vy)(km/s)",
            "Obs-Sun(J2000vz)(km/s)",
            "Sun-Ast-Obs(deg)",
        ]

        optional_cols = ["JD_TDB"]

        if not set(input_table.columns.values) == set(oif_cols):
            for column in input_table.columns.values:
                if column not in oif_cols and column not in optional_cols:
                    pplogger = logging.getLogger(__name__)
                    pplogger.error(
                        "ERROR: OIFDataReader: column headings do not match expected OIF column headings. Check format of file."
                    )
                    sys.exit(
                        "ERROR: OIFDataReader: column headings do not match expected OIF column headings. Check format of file."
                    )

        # Return only the columns of interest.
        return input_table[oif_cols]


def read_full_oif_table(filename, inputformat):
    """A helper function for testing that reads and returns an entire OIF table.

    Parameters:
    -----------
    filename (string): location/name of the data file.

    inputformat (string): format of input file ("whitespace"/"comma"/"csv"/"h5"/"hdf5").

    Returns:
    -----------
    res_df (Pandas dataframe): dataframe of the object data.

    """
    reader = OIFDataReader(filename, inputformat)
    res_df = reader.read_rows()
    return res_df
