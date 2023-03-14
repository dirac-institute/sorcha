import glob
import os
import pytest

from surveySimPP.tests.data import get_test_filepath


@pytest.fixture
def setup_and_teardown_for_PPGetLogger():

    yield

    test_path = os.path.dirname(get_test_filepath('test_input_fullobs.csv'))

    errlog = glob.glob(os.path.join(test_path, '*-postprocessing.err'))
    datalog = glob.glob(os.path.join(test_path, '*-postprocessing.log'))

    os.remove(errlog[0])
    os.remove(datalog[0])


def test_PPGetLogger(setup_and_teardown_for_PPGetLogger):

    from surveySimPP.modules.PPGetLogger import PPGetLogger
    test_path = os.path.dirname(get_test_filepath('test_input_fullobs.csv'))

    PPGetLogger(test_path)

    errlog = glob.glob(os.path.join(test_path, '*-postprocessing.err'))
    datalog = glob.glob(os.path.join(test_path, '*-postprocessing.log'))

    assert os.path.exists(errlog[0])
    assert os.path.exists(datalog[0])

    return
