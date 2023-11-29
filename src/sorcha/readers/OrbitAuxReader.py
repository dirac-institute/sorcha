import logging
import sys
import numpy as np

from sorcha.readers.CSVReader import CSVDataReader


class OrbitAuxReader(CSVDataReader):
    """A class to read in the auxiliary orbit data files."""

    def __init__(self, filename, sep="csv", header=-1, **kwargs):
        """A class for reading the object data from a CSV file.

        Parameters:
        -----------
        filename (string): location/name of the data file.

        sep (string, optional): format of input file ("whitespace"/"csv").

        header (int): The row number of the header. If not provided, does an automatic search.
        """
        super().__init__(filename, sep, header, **kwargs)

    def get_reader_info(self):
        """Return a string identifying the current reader name
        and input information (for logging and output).

        Returns:
        --------
        name (str): The reader information.
        """
        return f"OrbitAuxReader:{self.filename}"

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
        res_df (Pandas dataframe): Returns the input dataframe modified in-place.
        """
        # Do standard CSV file processing
        super()._process_and_validate_input_table(input_table, **kwargs)

        if len(input_table) == 0:
            return input_table

        pplogger = logging.getLogger(__name__)

        if "FORMAT" not in input_table.columns:
            pplogger.error("ERROR: PPReadOrbitFile: Orbit format must be provided.")
            sys.exit("ERROR: PPReadOrbitFile: Orbit format must be provided.")

        if len(input_table.columns) != 9:
            pplogger.error("ERROR: Please only provide the required columns in your orbits file.")
            sys.exit("ERROR: Please only provide the required columns in your orbits file.")

        orb_format = input_table["FORMAT"].iloc[0]
        if len(input_table["FORMAT"].unique()) != 1:
            pplogger.error("ERROR: Orbit file must have a consistent FORMAT (COM, KEP, or CART).")
            sys.exit("ERROR: Orbit file must have a consistent FORMAT (COM, KEP, or CART).")

        keplerian_elements = ["ObjID", "a", "e", "inc", "node", "argPeri", "ma", "epochMJD_TDB"]
        cometary_elements = ["ObjID", "q", "e", "inc", "node", "argPeri", "t_p_MJD_TDB", "epochMJD_TDB"]
        cartesian_elements = ["ObjID", "x", "y", "z", "xdot", "ydot", "zdot", "epochMJD_TDB"]

        if orb_format in ["KEP", "BKEP"]:
            if not all(column in input_table.columns for column in keplerian_elements):
                pplogger.error("ERROR: PPReadOrbitFile: Must provide all keplerian orbital elements.")
                sys.exit("ERROR: PPReadOrbitFile: Must provide all keplerian orbital elements.")
        elif orb_format in ["COM", "BCOM"]:
            if not all(column in input_table.columns for column in cometary_elements):
                pplogger.error("ERROR: PPReadOrbitFile: Must provide all cometary orbital elements.")
                sys.exit("ERROR: PPReadOrbitFile: Must provide all cometary orbital elements.")
            if np.any(input_table["t_p_MJD_TDB"] > 2400000.5):
                pplogger.warning(
                    "WARNING: At least one t_p_MJD_TDB is above 2400000.5 - make sure your t_p are MJD and not in JD"
                )
        elif orb_format in ["CART", "BCART"]:
            if not all(column in input_table.columns for column in cartesian_elements):
                pplogger.error("ERROR: PPReadOrbitFile: Must provide all cartesian coordinate values.")
                sys.exit("ERROR: PPReadOrbitFile: Must provide all cartesian coordinate values.")
        else:
            pplogger.error(
                "ERROR: PPReadOrbitFile: Orbit format must be one of cometary (COM), keplerian (KEP), cartesian (CART),"
                "barycentric cometary (BCOM), barycentric keplerian (BKEP), or barycentric cartesian (BCART)."
            )
            sys.exit(
                "ERROR: PPReadOrbitFile: Orbit format must be one of cometary (COM), keplerian (KEP), cartesian (CART),"
                "barycentric cometary (BCOM), barycentric keplerian (BKEP), or barycentric cartesian (BCART)."
            )

        return input_table
