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

            error_raised = False
            for i in range(len(input_table["ObjID"])):

                # checking inc
                if 0 > input_table["inc"][i] or input_table["inc"][i] > 180:
                    pplogger.warning(
                        f"Warning: Object {input_table['ObjID'][i]}. inc < 0 or inc > 180. rotations are defined but will be silly -- orbit will probably be mirrored"
                    )

                # checking argPeri, node and ma are in same bounds
                if not (
                    (
                        0 <= input_table["argPeri"][i] <= 360
                        and 0 <= input_table["node"][i] <= 360
                        and 0 <= input_table["ma"][i] <= 360
                    )
                    or (
                        -180 <= input_table["argPeri"][i] <= 180
                        and -180 <= input_table["node"][i] <= 180
                        and -180 <= input_table["ma"][i] <= 180
                    )
                ):
                    pplogger.warning(
                        f"Warning: Object {input_table['ObjID'][i]} argPeri, node and ma not in same bounds (either [0 360] or [-180 180])"
                    )

                # checks all objects before a system exit
                try:
                    if input_table["e"][i] > 1 and input_table["a"][i] > 0:
                        error_raised = True
                        pplogger.error(
                            f"ERROR: Object {input_table['ObjID'][i]}. Unbound orbit (e > 1) with positive a is undefined"
                        )
                        raise ValueError(
                            f"ERROR: Object {input_table['ObjID'][i]}. Unbound orbit (e > 1) with positive a is undefined"
                        )
                    elif input_table["e"][i] < 1 and input_table["a"][i] < 0:
                        error_raised = True
                        pplogger.error(
                            f"ERROR: Object {input_table['ObjID'][i]}. Bound orbit (e < 1) is undefined with negative a"
                        )
                        raise ValueError(
                            f"ERROR: Object {input_table['ObjID'][i]}. Bound orbit (e < 1) is undefined with negative a"
                        )
                    elif input_table["e"][i] == 1:
                        error_raised = True
                        pplogger.error(
                            f"ERROR: Object {input_table['ObjID'][i]}. Parabolic orbit (e == 1) is undefined in Keplerian elemnets"
                        )
                        raise ValueError(
                            f"ERROR: Object {input_table['ObjID'][i]}. Parabolic orbit (e == 1) is undefined in Keplerian elemnets"
                        )
                    elif input_table["e"][i] < 0:
                        error_raised = True
                        pplogger.error(f"ERROR: Object {input_table['ObjID'][i]}. e < 0 is undefined")
                        raise ValueError(f"ERROR: Object {input_table['ObjID'][i]}. e < 0 is undefined")
                except ValueError:
                    continue

            if error_raised:
                sys.exit("Error: Errors found for keplerian elements of objects (check log for more details)")

        elif orb_format in ["COM", "BCOM"]:
            if not all(column in input_table.columns for column in cometary_elements):
                pplogger.error("ERROR: PPReadOrbitFile: Must provide all cometary orbital elements.")
                sys.exit("ERROR: PPReadOrbitFile: Must provide all cometary orbital elements.")
            if np.any(input_table["t_p_MJD_TDB"] > 2400000.5):
                pplogger.warning(
                    "WARNING: At least one t_p_MJD_TDB is above 2400000.5 - make sure your t_p are MJD and not in JD"
                )

            error_raised = False
            for i in range(len(input_table["ObjID"])):

                if input_table["q"][i] == 0:
                    pplogger.warning(
                        f"Warning: Object {input_table['ObjID'][i]}. q==0 is technically correct but weird"
                    )

                # checking inc
                if 0 > input_table["inc"][i] or input_table["inc"][i] > 180:
                    pplogger.warning(
                        f"Warning: Object {input_table['ObjID'][i]}. inc < 0 or inc > 180. rotations are defined but will be silly -- orbit will probably be mirrored"
                    )

                try:
                    if input_table["q"][i] < 0:
                        error_raised = True
                        pplogger.error(f"ERROR: Object {input_table['ObjID'][i]}. q < 0 is undefined")

                    if input_table["e"][i] < 0:
                        error_raised = True
                        pplogger.error(f"ERROR: e < 0 is undefined for object {input_table['ObjID'][i]}")

                except ValueError:
                    continue
            if error_raised:
                sys.exit("Error: Errors found for cometary elements of objects (check log for more details)")

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
