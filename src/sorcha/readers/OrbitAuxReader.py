import logging
import sys
import numpy as np

from sorcha.readers.CSVReader import CSVDataReader


class OrbitAuxReader(CSVDataReader):
    """A class to read in the auxiliary orbit data files."""

    def __init__(self, filename, sep="csv", header=-1, **kwargs):
        """A class for reading the object data from a CSV file.

        Parameters
        -----------
        filename : string
            location/name of the data file.

        sep : string, optional
            format of input file ("whitespace"/"csv").
            Default = "csv"

        header : int
            The row number of the header. If not provided, does an automatic search.
            Default = -1

        **kwargs : dictionary, optional
            Extra arguments
        """
        super().__init__(filename, sep, header, **kwargs)

    def get_reader_info(self):
        """Return a string identifying the current reader name
        and input information (for logging and output).

        Returns
        --------
        : string
            The reader information.
        """
        return f"OrbitAuxReader:{self.filename}"

    def _process_and_validate_input_table(self, input_table, **kwargs):
        """Perform any input-specific processing and validation on the input table.
        Modifies the input dataframe in place.

        Parameters
        -----------
        input_table : pandas dataframe
            A loaded table.

        **kwargs : dictionary, optional

        Returns
        -----------
        res_df : pandas dataframe
            Returns the input dataframe modified in-place.

        Notes
        ------
        The base implementation includes filtering that is common to most
        input types. Subclasses should call super.process_and_validate()
        to ensure that the ancestor’s validation is also applied.

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

            filtered_df = input_table.loc[(input_table["inc"] < 0) | (input_table["inc"] > 180), ["ObjID"]]
            if not filtered_df.empty:
                pplogger.warning(
                    f"WARNING: For Object(s) {', '.join(filtered_df['ObjID'].astype(str))}. Inclination (inc) is outside the valid range (0 180 degrees), which may cause the orbits to be mirrored affecting orbital calculations."
                )
            filtered_df = input_table.loc[
                ~(
                    (
                        (input_table["argPeri"] >= 0)
                        & (input_table["argPeri"] <= 360)
                        & (input_table["node"] >= 0)
                        & (input_table["node"] <= 360)
                        & (input_table["ma"] >= 0)
                        & (input_table["ma"] <= 360)
                    )
                    | (
                        (input_table["argPeri"] >= -180)
                        & (input_table["argPeri"] <= 180)
                        & (input_table["node"] >= -180)
                        & (input_table["node"] <= 180)
                        & (input_table["ma"] >= -180)
                        & (input_table["ma"] <= 180)
                    )
                ),
                ["ObjID"],
            ]
            if not filtered_df.empty:
                pplogger.warning(
                    f"WARNING: For Object(s) {', '.join(filtered_df['ObjID'].astype(str))}. The argument of Perihelion (argPeri), the Longitude of the Ascending Node (node), and the Mean Anomaly (ma) are not in the same bounds (either [0 360] or [-180 180] degrees), which may lead to incorrect orbital calculations."
                )
            error_raised = False
            # checks all objects before a system exit
            filtered_df = input_table.loc[(input_table["e"] == 1), ["ObjID"]]
            if not filtered_df.empty:
                error_raised = True
                pplogger.error(
                    f"ERROR: For Object(s) {', '.join(filtered_df['ObjID'].astype(str))}. Parabolic orbit (e == 1) is undefined in Keplerian elements."
                )
            filtered_df = input_table.loc[(input_table["e"] < 0), ["ObjID"]]
            if not filtered_df.empty:
                error_raised = True
                pplogger.error(
                    f"ERROR: For Object(s) {', '.join(filtered_df['ObjID'].astype(str))}. Eccentricity (e) cannot be less than 0."
                )
            filtered_df = input_table.loc[(input_table["e"] > 1), ["ObjID"]]
            if not filtered_df.empty:
                error_raised = True
                pplogger.error(
                    f"ERROR: For Object(s) {', '.join(filtered_df['ObjID'].astype(str))}. Hyperbolic orbit (e > 1) is not supported for Keplerian elements."
                )
            filtered_df = input_table.loc[(input_table["e"] < 1) & (input_table["a"] < 0), ["ObjID"]]
            if not filtered_df.empty:
                error_raised = True
                pplogger.error(
                    f"ERROR: For Object(s) {', '.join(filtered_df['ObjID'].astype(str))}. Bound orbit (e < 1) with negative semi-major axis (a < 0) is not physical."
                )

            if error_raised:
                pplogger.error("ERROR: Invalid Keplerian elements detected for one or more objects.")
                sys.exit(
                    "ERROR: Invalid Keplerian elements detected for one or more objects (check log for information)"
                )

        elif orb_format in ["COM", "BCOM"]:
            if not all(column in input_table.columns for column in cometary_elements):
                pplogger.error("ERROR: PPReadOrbitFile: Must provide all cometary orbital elements.")
                sys.exit("ERROR: PPReadOrbitFile: Must provide all cometary orbital elements.")
            if np.any(input_table["t_p_MJD_TDB"] > 2400000.5):
                pplogger.warning(
                    "WARNING: At least one t_p_MJD_TDB is above 2400000.5 - make sure your t_p are MJD and not in JD"
                )

            error_raised = False
            filtered_df = input_table.loc[(input_table["q"] == 1), ["ObjID"]]
            if not filtered_df.empty:
                pplogger.warning(
                    f"WARNING: For Object(s) {', '.join(filtered_df['ObjID'].astype(str))}. q==0 is technically correct but suggests a collisional path with an object instead of an orbital path."
                )

            filtered_df = input_table.loc[(input_table["inc"] < 0) | (input_table["inc"] > 180), ["ObjID"]]
            if not filtered_df.empty:
                pplogger.warning(
                    f"WARNING: For Object(s) {', '.join(filtered_df['ObjID'].astype(str))}. Inclination (inc) is outside the valid range (0 180 degrees), which may cause the orbits to be mirrored affecting orbital calculations."
                )
            filtered_df = input_table.loc[(input_table["q"] < 0), ["ObjID"]]
            if not filtered_df.empty:
                error_raised = True
                pplogger.error(
                    f"ERROR: For Object(s) {', '.join(filtered_df['ObjID'].astype(str))}. Perihelion distance (q) cannot be less than 0."
                )
            filtered_df = input_table.loc[(input_table["e"] < 0), ["ObjID"]]
            if not filtered_df.empty:
                error_raised = True
                pplogger.error(
                    f"ERROR: For Object(s) {', '.join(filtered_df['ObjID'].astype(str))}. Eccentricity (e) cannot be less than 0."
                )

            if error_raised:
                pplogger.error("ERROR: Invalid cometary elements detected for one or more objects")
                sys.exit(
                    "ERROR: Invalid cometary elements detected for one or more objects (check log for information)"
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
