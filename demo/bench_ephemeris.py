from sorcha.sorcha import runLSSTSimulation  # noqa: F401

if __name__ == '__main__':  # pragma: no cover

    cmd_args_dict = {
        "paramsinput": "../data_files/mpcorb_physical.csv",
        "orbinfile": "../data_files/mpcorb_orbits.csv",
        "oifoutput": "./mba_sample_1000_eph.csv",
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
