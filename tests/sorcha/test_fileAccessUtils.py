#!/bin/python
import os
import shutil
import configparser
import pytest
import glob

from sorcha.utilities.dataUtilitiesForTests import get_test_filepath
from sorcha.utilities.sorchaArguments import sorchaArguments


def test_FindFileOrExit():
    from sorcha.utilities.fileAccessUtils import FindFileOrExit

    test_file = FindFileOrExit(get_test_filepath("test_PPConfig.ini"), "config file")

    with pytest.raises(SystemExit) as e:
        FindFileOrExit("totally_fake_file.txt", "test")

    assert test_file == get_test_filepath("test_PPConfig.ini")
    assert e.type == SystemExit
    assert e.value.code == "ERROR: filename totally_fake_file.txt supplied for test argument does not exist."

    return


def test_FindDirectoryOrExit():
    from sorcha.utilities.fileAccessUtils import FindDirectoryOrExit

    test_dir = FindDirectoryOrExit("./", "test")

    with pytest.raises(SystemExit) as e:
        FindDirectoryOrExit("./fake_dir/", "test")

    assert test_dir == "./"
    assert e.type == SystemExit
    assert e.value.code == "ERROR: filepath ./fake_dir/ supplied for test argument does not exist."

    return
