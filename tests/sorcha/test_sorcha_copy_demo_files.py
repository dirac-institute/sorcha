import os
import pytest


def test_sorcha_copy_demo_files(tmp_path):
    from sorcha.utilities.sorcha_copy_demo_files import copy_demo_files

    copy_demo_files(tmp_path, False)

    demo_files = [
        "sorcha_config_demo.ini",
        "sspp_testset_colours.txt",
        "sspp_testset_orbits.des",
        "baseline_v2.0_1yr.db",
    ]

    # test that the files are created
    for filename in demo_files:
        assert os.path.isfile(os.path.join(tmp_path, filename))

    # test that files are successfully overwritten if -f flag used
    copy_demo_files(tmp_path, True)

    # test that the correct error is triggered if force overwrite not used
    with pytest.raises(SystemExit) as e:
        copy_demo_files(tmp_path, False)

    assert (
        e.value.code
        == "Identically named file exists at location. Re-run with -f or --force to force overwrite."
    )

    # test the error message if user supplies non-existent directory
    dummy_folder = os.path.join(tmp_path, "dummy_folder")

    with pytest.raises(SystemExit) as e2:
        copy_demo_files(dummy_folder, True)

    assert e2.value.code == "ERROR: filepath {} supplied for filepath argument does not exist.".format(
        dummy_folder
    )
