import logging
import sys

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

        pplogger = logging.getLogger(__name__)

        # Check for an H column (which should not be in the orbit file).
        if "H" in input_table.columns:
            pplogger.error(
                "ERROR: PPReadOrbitFile: H column present in orbits data file. H must be included in physical parameters file only."
            )
            sys.exit(
                "ERROR: PPReadOrbitFile: H column present in orbits data file. H must be included in physical parameters file only."
            )

        # rename i to incl to avoid confusion with the colour i
        input_table = input_table.rename(columns={"i": "incl"})
        input_table = input_table.drop(
            ["INDEX", "N_PAR", "MOID", "COMPCODE", "FORMAT"], axis=1, errors="ignore"
        )

        # Check if there is q in the resulting dataframe.
        if "q" not in input_table.columns:
            if "a" not in input_table.columns or "e" not in input_table.columns:
                pplogger.error(
                    "ERROR: OrbitAuxReader: unable to join ephemeris simulation and orbital parameters: no a or e in input."
                )
                sys.exit(
                    "ERROR: OrbitAuxReader: unable to join ephemeris simulation and orbital parameters: no a or e in input."
                )
            else:
                input_table["q"] = input_table["a"] * (1.0 - input_table["e"])

        return input_table
