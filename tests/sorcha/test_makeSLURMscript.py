import os
import sys
import pytest

from sorcha.utilities.dataUtilitiesForTests import get_test_filepath

# These tests won't work on Windows because Windows uses backslashes for paths.
# Hence, the asserts will always fail.
if sys.platform.startswith("win"):
    pytest.skip("These tests do not work on Windows.", allow_module_level=True)


class args:
    def __init__(self, filename, er, ew, com):
        abspath = os.path.dirname(get_test_filepath("oiftestoutput.txt"))

        args.filename = filename
        args.inputs = os.path.relpath(abspath)
        args.config = os.path.join(os.path.relpath(abspath), "test_PPConfig.ini")
        args.outfile = os.path.relpath(abspath)
        args.pointing_database = os.path.join(os.path.relpath(abspath), "baseline_10klines_2.0.db")
        args.params_stem = "params*"
        args.orbits_stem = "orbits*"
        args.ephem_read_stem = er
        args.ephem_write_stem = ew
        args.ar_data_path = os.path.relpath(abspath)
        args.ncores = 0
        args.jobname = "test"
        args.force = False
        args.complex_stem = com
        args.output_stem = "SorchaOutput"


@pytest.fixture
def setup_and_teardown_for_makeSLURM():
    # for relative paths to work correctly, we must move to a
    # known directory. there's no real reason it has to be the
    # directory this script is in other than this is how I wrote
    # the test and now I'm tired and don't want to change it.

    # get current directory
    initial_wd = os.getcwd()

    # get location of this file
    test_dir = os.path.dirname(os.path.realpath(__file__))

    # move to directory containing this file
    os.chdir(test_dir)

    yield

    # head back to the original directory
    os.chdir(initial_wd)

    # delete things
    temp_path = os.path.dirname(get_test_filepath("oiftestoutput.txt"))
    file1 = "testSLURMout_1.sh"
    file2 = "testSLURMout_2.sh"
    file3 = "testSLURMout_3.sh"
    file4 = "testSLURMout_4.sh"

    os.remove(os.path.join(temp_path, file1))
    os.remove(os.path.join(temp_path, file2))
    os.remove(os.path.join(temp_path, file3))
    os.remove(os.path.join(temp_path, file4))


@pytest.fixture
def setup_for_convert_args_to_absolute_paths():
    # get current directory
    initial_wd = os.getcwd()

    # get location of this file
    test_dir = os.path.dirname(os.path.realpath(__file__))

    # move to directory containing this file
    os.chdir(test_dir)

    yield

    # head back to the original directory
    os.chdir(initial_wd)


def test_makeSLURM(setup_and_teardown_for_makeSLURM):
    from sorcha.utilities.makeSLURMscript import makeSLURM
    from sorcha.utilities.makeSLURMscript import convert_args_to_absolute_paths

    temp_path = os.path.dirname(get_test_filepath("oiftestoutput.txt"))

    # testing OIF+SSPP, no temporary databases
    test_args1 = args(os.path.join(temp_path, "testSLURMout_1.sh"), None, None, None)

    makeSLURM(test_args1)

    testfile1 = open(get_test_filepath("testSLURMout_1.sh"), mode="r")
    newfile1 = open(get_test_filepath("makeSLURMscript_1.sh"), mode="r")

    alltest1 = testfile1.readlines()
    allnew1 = newfile1.readlines()

    testfile1.close()
    newfile1.close()

    assert alltest1 == allnew1

    # testing OIF-only
    test_args2 = args(os.path.join(temp_path, "testSLURMout_2.sh"), "orbits*", None, None)

    makeSLURM(test_args2)

    testfile2 = open(get_test_filepath("testSLURMout_2.sh"), mode="r")
    newfile2 = open(get_test_filepath("makeSLURMscript_2.sh"), mode="r")

    alltest2 = testfile2.readlines()
    allnew2 = newfile2.readlines()

    testfile2.close()
    newfile2.close()

    assert alltest2 == allnew2

    # testing SSPP-only
    test_args3 = args(os.path.join(temp_path, "testSLURMout_3.sh"), None, "ephem", None)
    makeSLURM(test_args3)

    testfile3 = open(get_test_filepath("testSLURMout_3.sh"), mode="r")
    newfile3 = open(get_test_filepath("makeSLURMscript_3.sh"), mode="r")

    alltest3 = testfile3.readlines()
    allnew3 = newfile3.readlines()

    testfile3.close()
    newfile3.close()

    assert alltest3 == allnew3

    # testing creating temporary databases with utility script, plus dr and dl flags
    test_args4 = args(os.path.join(temp_path, "testSLURMout_4.sh"), None, None, "params*")
    makeSLURM(test_args4)

    testfile4 = open(get_test_filepath("testSLURMout_4.sh"), mode="r")
    newfile4 = open(get_test_filepath("makeSLURMscript_4.sh"), mode="r")

    alltest4 = testfile4.readlines()
    allnew4 = newfile4.readlines()

    testfile4.close()
    newfile4.close()

    assert alltest4 == allnew4


def test_convert_args_to_absolute_paths(setup_for_convert_args_to_absolute_paths):
    from sorcha.utilities.makeSLURMscript import convert_args_to_absolute_paths

    temp_path = os.path.dirname(get_test_filepath("oiftestoutput.txt"))
    test_args = args(os.path.join(temp_path, "makeSLURMscript_4.sh"), None, None, None)

    convargs = convert_args_to_absolute_paths(test_args)

    assert convargs.filename == get_test_filepath("makeSLURMscript_4.sh")
    assert convargs.inputs == temp_path
    assert convargs.config == get_test_filepath("test_PPConfig.ini")
    assert convargs.outfile == temp_path
    assert convargs.pointing_database == get_test_filepath("baseline_10klines_2.0.db")
    assert convargs.ar_data_path == temp_path


def test_get_sorted_list_of_files():
    from sorcha.utilities.makeSLURMscript import get_sorted_list_of_files

    temp_path = os.path.dirname(get_test_filepath("oiftestoutput.txt"))
    test_list = get_sorted_list_of_files(temp_path, "orbits*")

    comp_list = [os.path.join(temp_path, "orbits_test1.txt"), os.path.join(temp_path, "orbits_test2.txt")]

    assert test_list == comp_list
