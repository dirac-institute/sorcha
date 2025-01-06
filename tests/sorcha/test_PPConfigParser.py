#!/bin/python
import os
import shutil
import configparser
import pytest
import glob

from sorcha.utilities.dataUtilitiesForTests import get_test_filepath
from sorcha.utilities.sorchaArguments import sorchaArguments

def test_PPFindFileOrExit():
    from sorcha.modules.PPConfigParser import PPFindFileOrExit

    test_file = PPFindFileOrExit(get_test_filepath("test_PPConfig.ini"), "config file")

    with pytest.raises(SystemExit) as e:
        PPFindFileOrExit("totally_fake_file.txt", "test")

    assert test_file == get_test_filepath("test_PPConfig.ini")
    assert e.type == SystemExit
    assert e.value.code == "ERROR: filename totally_fake_file.txt supplied for test argument does not exist."

    return

def test_PPFindDirectoryOrExit():
    from sorcha.modules.PPConfigParser import PPFindDirectoryOrExit

    test_dir = PPFindDirectoryOrExit("./", "test")

    with pytest.raises(SystemExit) as e:
        PPFindDirectoryOrExit("./fake_dir/", "test")

    assert test_dir == "./"
    assert e.type == SystemExit
    assert e.value.code == "ERROR: filepath ./fake_dir/ supplied for test argument does not exist."

    return
