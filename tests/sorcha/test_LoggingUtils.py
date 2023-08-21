import glob
import os
import pytest

from sorcha.modules.LoggingUtils import logErrorAndExit, GetLogger


def test_logErrorAndExit():
    with pytest.raises(SystemExit) as err:
        logErrorAndExit("Test Message")
    assert err.value.args[0] == "Test Message"


def test_PPGetLogger(tmp_path):
    GetLogger(tmp_path)

    errlog = glob.glob(os.path.join(tmp_path, "*-postprocessing.err"))
    datalog = glob.glob(os.path.join(tmp_path, "*-postprocessing.log"))

    assert os.path.exists(errlog[0])
    assert os.path.exists(datalog[0])

    return
