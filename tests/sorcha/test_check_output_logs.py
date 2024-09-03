import os
import pytest
import pandas as pd
from sorcha.utilities.dataUtilitiesForTests import get_test_filepath


def test_find_and_check_all_log_files():
    from sorcha.utilities.check_output_logs import find_all_log_files
    from sorcha.utilities.check_output_logs import check_all_logs

    filepath = os.path.dirname(get_test_filepath("oiftestoutput.txt"))

    test_log = find_all_log_files(filepath)
    assert len(test_log) == 2

    good_log, last_lines = check_all_logs(test_log)

    assert good_log == [False, True]
    assert last_lines[1] == " "
    assert len(last_lines[0]) == 171


def test_check_output_logs(tmp_path):
    from sorcha.utilities.check_output_logs import check_output_logs

    filepath = os.path.dirname(get_test_filepath("oiftestoutput.txt"))

    output = os.path.join(tmp_path, "sorcha_logs.csv")
    check_output_logs(filepath, output)

    # check output matches
    written_output = pd.read_csv(output)
    expected_output = pd.read_csv(get_test_filepath("sorcha_logs_expected.csv"))
    pd.testing.assert_frame_equal(written_output, expected_output)

    # check no output on successful run
    single_filepath = os.path.join(os.path.dirname(get_test_filepath("oiftestoutput.txt")), "run_1")
    successful_output = os.path.join(tmp_path, "successful_sorcha_logs.csv")
    successful_run = check_output_logs(single_filepath, successful_output)

    assert os.path.exists(successful_output) == False

    # check error message when no files are found
    with pytest.raises(SystemExit) as e:
        failed_run = check_output_logs("dummy/path/")

    assert e.type == SystemExit
    assert (
        e.value.code
        == "ERROR: no Sorcha log files could be found in directories/subdirectories of supplied filepath."
    )
