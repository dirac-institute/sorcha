import logging
import sys

from surveySimPP.readers.CSVReader import CSVDataReader


class OrbitAuxReader(CSVDataReader):
    """A class to read in the auxiliary orbit data files."""

    def __init__(self, filename, sep="csv", header=-1, *args, **kwargs):
        """A class for reading the object data from a CSV file.

        Parameters:
        -----------
        filename (string): location/name of the data file.

        sep (string, optional): format of input file ("whitespace"/"comma"/"csv").

        header (int): The row number of the header. If not provided, does an automatic search.
        """
        super().__init__(filename, sep, header, *args, **kwargs)

    def process_and_validate_input_table(self, input_table, **kwargs):
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

        disallow_nan (bool, optional): if True then checks the data for
            NaNs or nulls.

        Returns:
        -----------
        res_df (Pandas dataframe): Returns the input dataframe modified in-place.
        """
        # Do standard CSV file processing
        super().process_and_validate_input_table(input_table, **kwargs)

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

        return input_table
