from sorcha.sorcha import runLSSTSimulation  # noqa: F401

"""How to use this:
There are two files that need to be downloaded from here: 
https://drive.google.com/drive/u/0/folders/1oDwA6Vd3jz8vJa0EJ0OZt4lI-WwfyOmO
1) mpcorb_physical.csv
2) mpcorb_orbits.csv

For this script I have saved them in `../data_files` directory.

Run this script from the command line using: 
> python bench_ephemeris

Look for output files in the `../data/out/` directory.
There should be an `ephemeris_output.csv` as well as .log and .err files.
"""

if __name__ == '__main__':  # pragma: no cover

    cmd_args_dict = {
        # paramsinput and orbinfile are both downloaded from here: 
        # https://drive.google.com/drive/u/0/folders/1oDwA6Vd3jz8vJa0EJ0OZt4lI-WwfyOmO
        "paramsinput": "../data_files/mpcorb_physical.csv",
        "orbinfile": "../data_files/mpcorb_orbits.csv",
        "oifoutput": "./mba_sample_1000_eph.csv", # this shouldn't be used at all, but an existing file is required.
        "configfile": "./ARconfig_benchmark.ini",
        "pointing_database": "./baseline_v2.0_1yr.db",
        "outpath": "../data/out",
        "makeTemporaryEphemerisDatabase": False,
        "readTemporaryEphemerisDatabase": False,
        "deleteTemporaryEphemerisDatabase": False,
        "surveyname": "LSST",
        "outfilestem": "out_mba",
        "verbose": False,
    }

    runLSSTSimulation(cmd_args_dict)
