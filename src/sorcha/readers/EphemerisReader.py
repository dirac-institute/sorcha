import logging
import sys

from sorcha.readers.CSVReader import CSVDataReader
from sorcha.readers.HDF5Reader import HDF5DataReader
from sorcha.readers.ObjectDataReader import ObjectDataReader


class EphemerisDataReader(ObjectDataReader):
    """A class to read in ephemeris from an external ephemeris file.

    Instead of subclassing the various readers (CSV, HDF5, etc.) individually, this class instantiates
    one of those classes in an internal ``reader`` attribute. As such all reading, validation, etc. is
    passed off to the ``reader`` object this object owns. While this adds a level of indirection, it
    allows us to support a cross product of N file types from M ephemeris generators with M + N readers
    instead of M * N.
    """

    def __init__(self, filename, inputformat, **kwargs):
        """A class for reading the object data from a CSV file.

        Parameters
        -----------
        filename : string
            location/name of the data file.

        inputformat : string
            format of input file ("whitespace"/"comma"/"csv"/"h5"/"hdf5").

        **kwargs : dictionary, optional
            Extra arguments

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
                f"ERROR: EphemerisDataReader: unknown format for ephemeris simulation results ({inputformat})."
            )
            sys.exit(
                f"ERROR: EphemerisDataReader: unknown format for ephemeris simulation results ({inputformat})."
            )

    def get_reader_info(self):
        """Return a string identifying the current reader name
        and input information (for logging and output).

        Returns
        --------
        : string
            The reader information.
        """
        return f"EphemerisDataReader|{self.reader.get_reader_info()}"

    def _read_rows_internal(self, block_start=0, block_size=None, **kwargs):
        """Reads in a set number of rows from the input.

        Parameters
        -----------
        block_start : int, optional
            The 0-indexed row number from which
            to start reading the data. For example in a CSV file
            block_start=2 would skip the first two lines after the header
            and return data starting on row=2. Default =0

        block_size : int, optional
            the number of rows to read in.
            Use block_size=None to read in all available data.
            Default = None

        **kwargs : dictionary, optional
            Extra arguments

        Returns
        -----------
        res_df : Pandas dataframe
            dataframe of the object data.

        """
        res_df = self.reader.read_rows(block_start, block_size, **kwargs)
        return res_df

    def _read_objects_internal(self, obj_ids, **kwargs):
        """Read in a chunk of data corresponding to all rows for
        a given set of object IDs.

        Parameters
        -----------
        obj_ids : list
            A list of object IDs to use.

        **kwargs : dictionary, optional
            Extra arguments

        Returns
        -----------
        res_df : pandas dataframe
            The dataframe for the object data.
        """
        res_df = self.reader.read_objects(obj_ids, **kwargs)
        return res_df

    def _process_and_validate_input_table(self, input_table, **kwargs):
        """Perform any input-specific processing and validation on the input table.
        Modifies the input dataframe in place.

        Parameters
        -----------
        input_table : Pandas dataframe
            A loaded table.

        **kwargs : dictionary, optional
            Extra arguments

        Returns
        -----------
        input_table : Pandas dataframe
            Returns the input dataframe modified in-place.

        Notes
        -----
        The base implementation includes filtering that is common to most
        input types. Subclasses should call super.process_and_validate()
        to ensure that the ancestor’s validation is also applied.

        """
        # We do not call reader.process_and_validate_input_table() or
        # super().process_and_validate_input_table() because reader's read functions have
        # already check the table.

        input_table = input_table.rename(columns=lambda x: x.strip())
        input_table = input_table.drop(["V", "V(H=0)"], axis=1, errors="ignore")

        ephem_cols = [
            "ObjID",
            "FieldID",
            "fieldMJD_TAI",
            "Range_LTC_km",
            "RangeRate_LTC_km_s",
            "RA_deg",
            "RARateCosDec_deg_day",
            "Dec_deg",
            "DecRate_deg_day",
            "Obj_Sun_x_LTC_km",
            "Obj_Sun_y_LTC_km",
            "Obj_Sun_z_LTC_km",
            "Obj_Sun_vx_LTC_km_s",
            "Obj_Sun_vy_LTC_km_s",
            "Obj_Sun_vz_LTC_km_s",
            "Obs_Sun_x_km",
            "Obs_Sun_y_km",
            "Obs_Sun_z_km",
            "Obs_Sun_vx_km_s",
            "Obs_Sun_vy_km_s",
            "Obs_Sun_vz_km_s",
            "phase_deg",
        ]

        optional_cols = ["fieldJD_TDB"]

        if not set(input_table.columns.values) == set(ephem_cols):
            for column in input_table.columns.values:
                if column not in ephem_cols and column not in optional_cols:
                    pplogger = logging.getLogger(__name__)
                    pplogger.error(
                        "ERROR: EphemerisDataReader: column headings do not match expected ephemeris column headings. Check format of file."
                    )
                    sys.exit(
                        "ERROR: EphemerisDataReader: column headings do not match expected ephemeris column headings. Check format of file."
                    )

        # Return only the columns of interest.
        return input_table[ephem_cols]


def read_full_ephemeris_table(filename, inputformat):
    """A helper function for testing that reads and returns an entire ephemeris table.

    Parameters
    -----------
    filename : string
        location/name of the data file.

    inputformat : string
        format of input file ("whitespace"/"comma"/"csv"/"h5"/"hdf5").

    Returns
    -----------
    res_df : pandas dataframe
        dataframe of the object data.

    """
    reader = EphemerisDataReader(filename, inputformat)
    res_df = reader.read_rows()
    return res_df
