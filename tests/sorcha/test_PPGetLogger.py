import glob
import os
import pytest
import tempfile
import re


def test_PPGetLogger():
    from sorcha.modules.PPGetLogger import PPGetLogger

    with tempfile.TemporaryDirectory() as dir_name:
        logfn = os.path.join(dir_name, "sorcha-results.log")
        pplogger = PPGetLogger(logfn)

        # Check that the log file got created
        assert os.path.exists(logfn)

        # Log some information.
        pplogger.info("Test1")
        pplogger.info("Test2")
        pplogger.error("Error1")
        pplogger.info("Test3")

        # Check that all five lines exist in the INFO file.
        with open(logfn, "r") as fp:
            lines = fp.read()

        assert re.search(r".*INFO[^\n]*Test1.*", lines, re.MULTILINE) is not None
        assert re.search(r".*INFO[^\n]*Test2.*", lines, re.MULTILINE) is not None
        assert re.search(r".*INFO[^\n]*Test3.*", lines, re.MULTILINE) is not None
        assert re.search(r".*ERROR[^\n]*Error1.*", lines, re.MULTILINE) is not None
