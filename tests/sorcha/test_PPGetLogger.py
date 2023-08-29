import glob
import os
import pytest
import tempfile


def test_PPGetLogger():
    from sorcha.modules.PPGetLogger import PPGetLogger

    with tempfile.TemporaryDirectory() as dir_name:
        pplogger = PPGetLogger(dir_name)

        # Check that the files get created.
        errlog = glob.glob(os.path.join(dir_name, "*-sorcha.err"))
        datalog = glob.glob(os.path.join(dir_name, "*-sorcha.log"))

        assert os.path.exists(errlog[0])
        assert os.path.exists(datalog[0])

        # Log some information.
        pplogger.info("Test1")
        pplogger.info("Test2")
        pplogger.error("Error1")
        pplogger.info("Test3")

        # Check that all five lines exist in the INFO file.
        with open(datalog[0], "r") as f_info:
            log_data = f_info.read()
            assert "Test1" in log_data
            assert "Test2" in log_data
            assert "Error1" in log_data
            assert "Test3" in log_data

        # Check that only error and critical lines exist in the ERROR file.
        with open(errlog[0], "r") as f_err:
            log_data = f_err.read()
            assert "Test1" not in log_data
            assert "Test2" not in log_data
            assert "Error1" in log_data
            assert "Test3" not in log_data
