import glob
import os


def test_PPGetLogger(tmp_path):
    from sorcha.modules.PPGetLogger import PPGetLogger

    PPGetLogger(tmp_path)

    errlog = glob.glob(os.path.join(tmp_path, "*-sorcha.err"))
    datalog = glob.glob(os.path.join(tmp_path, "*-sorcha.log"))

    assert os.path.exists(errlog[0])
    assert os.path.exists(datalog[0])

    return
