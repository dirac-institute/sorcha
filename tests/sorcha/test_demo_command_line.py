# This test file checks to see if Sorcha runs correctly and produces output
# using the current demo command.
# It does not check the output for correctness. This is covered by test_demo_end2end.py.

import os
import pytest
import glob
from pathlib import Path


@pytest.fixture
def setup_and_teardown_for_demo_command_line():
    # Record initial working directory
    initial_wd = os.getcwd()

    # Find where the demo files are installed on this machine
    path_to_file = os.path.abspath(__file__)
    path_to_demo = os.path.join(str(Path(path_to_file).parents[2]), "demo")

    # Move to the demo directory
    os.chdir(path_to_demo)

    # Yield to pytest to run the test
    yield

    # After running the test, delete the created files...

    os.remove("sorcha-results.csv")
    os.remove("sorcha-results-stats.csv")
    os.remove("sorcha-results.log")

    # And move back to initial working directory.
    os.chdir(initial_wd)


def test_demo_command_line(setup_and_teardown_for_demo_command_line):
    """This checks to see if the current demo command-line command for Sorcha
    results in a successful run, i.e.: it runs without error and produces output.
    It does not check the actual output for correctness. This is done by
    test_demo_end2end.py.
    """

    from sorcha.utilities.sorcha_demo_command import get_demo_command

    current_demo_command = get_demo_command()

    # usually the ephemeris files have already been downloaded by the
    # ephemeris end-to-end test, but we can't rely on test order for this to
    # work! if the files already exist in the default location this will do nothing.
    os.system("sorcha bootstrap")

    os.system(current_demo_command)

    assert os.path.exists("sorcha-results.csv")

    # also check to make sure there are no errors in the log
    for line in open("sorcha-results.log"):
        assert " ERROR " not in line
