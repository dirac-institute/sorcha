import os
import sys
import pytest

from sorcha.utilities.dataUtilitiesForTests import get_test_filepath

# These tests won't work on Windows because Windows uses backslashes for paths.
# Hence, the asserts will always fail.
if sys.platform.startswith("win"):
    pytest.skip("These tests do not work on Windows.", allow_module_level=True)


class args:
    def __init__(self, filename, oss, sss, dc, dr=False, dw=False, dl=False):
        abspath = os.path.dirname(get_test_filepath("oiftestoutput.txt"))

        args.filename = filename
        args.inputs = os.path.relpath(abspath)
        args.deletecache = True
        args.os = oss
        args.ss = sss
        args.ssppcon = os.path.join(os.path.relpath(abspath), "test_PPConfig.ini")
        args.oifout = os.path.relpath(abspath)
        args.allout = os.path.relpath(abspath)
        args.comet = False
        args.dr = dr
        args.dc = dc
        args.dw = dw
        args.dl = dl
        args.ncores = 0
        args.jobname = "test"


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
    file5 = "testSLURMout_5.sh"

    os.remove(os.path.join(temp_path, file1))
    os.remove(os.path.join(temp_path, file2))
    os.remove(os.path.join(temp_path, file3))
    os.remove(os.path.join(temp_path, file4))
    os.remove(os.path.join(temp_path, file5))


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

    temp_path = os.path.dirname(get_test_filepath("oiftestoutput.txt"))

    # testing OIF+SSPP, no temporary databases
    test_args1 = args(os.path.join(temp_path, "testSLURMout_1.sh"), False, False, False)

    makeSLURM(test_args1)

    testfile1 = open(get_test_filepath("testSLURMout_1.sh"), mode="r")
    newfile1 = open(get_test_filepath("makeSLURMscript_1.sh"), mode="r")

    alltest1 = testfile1.readlines()
    allnew1 = newfile1.readlines()

    testfile1.close()
    newfile1.close()

    assert alltest1 == allnew1

    # testing OIF-only
    test_args2 = args(os.path.join(temp_path, "testSLURMout_2.sh"), True, False, False)

    makeSLURM(test_args2)

    testfile2 = open(get_test_filepath("testSLURMout_2.sh"), mode="r")
    newfile2 = open(get_test_filepath("makeSLURMscript_2.sh"), mode="r")

    alltest2 = testfile2.readlines()
    allnew2 = newfile2.readlines()

    testfile2.close()
    newfile2.close()

    assert alltest2 == allnew2

    # testing SSPP-only
    test_args3 = args(os.path.join(temp_path, "testSLURMout_3.sh"), False, True, False)

    makeSLURM(test_args3)

    testfile3 = open(get_test_filepath("testSLURMout_3.sh"), mode="r")
    newfile3 = open(get_test_filepath("makeSLURMscript_3.sh"), mode="r")

    alltest3 = testfile3.readlines()
    allnew3 = newfile3.readlines()

    testfile3.close()
    newfile3.close()

    assert alltest3 == allnew3

    # testing creating temporary databases with utility script, plus dr and dl flags
    test_args4 = args(os.path.join(temp_path, "testSLURMout_4.sh"), False, False, True, dr=True, dl=True)

    makeSLURM(test_args4)

    testfile4 = open(get_test_filepath("testSLURMout_4.sh"), mode="r")
    newfile4 = open(get_test_filepath("makeSLURMscript_4.sh"), mode="r")

    alltest4 = testfile4.readlines()
    allnew4 = newfile4.readlines()

    testfile4.close()
    newfile4.close()

    assert alltest4 == allnew4

    # testing dw flag
    test_args5 = args(os.path.join(temp_path, "testSLURMout_5.sh"), False, False, False, dw=True, dl=True)

    makeSLURM(test_args5)

    testfile5 = open(get_test_filepath("testSLURMout_5.sh"), mode="r")
    newfile5 = open(get_test_filepath("makeSLURMscript_5.sh"), mode="r")

    alltest5 = testfile5.readlines()
    allnew5 = newfile5.readlines()

    testfile5.close()
    newfile5.close()

    assert alltest5 == allnew5


def test_convert_args_to_absolute_paths(setup_for_convert_args_to_absolute_paths):
    from sorcha.utilities.makeSLURMscript import convert_args_to_absolute_paths

    temp_path = os.path.dirname(get_test_filepath("oiftestoutput.txt"))
    test_args = args(os.path.join(temp_path, "makeSLURMscript_5.sh"), False, False, False, dw=True, dl=True)

    convargs = convert_args_to_absolute_paths(test_args)

    assert convargs.filename == get_test_filepath("makeSLURMscript_5.sh")
    assert convargs.inputs == temp_path
    assert convargs.ssppcon == get_test_filepath("test_PPConfig.ini")
    assert convargs.oifout == temp_path
    assert convargs.allout == temp_path
