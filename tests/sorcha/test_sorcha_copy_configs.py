import os
import pytest


def test_sorcha_copy_configs(tmp_path):
    from sorcha.utilities.sorcha_copy_configs import copy_demo_configs

    # test that the Rubin files are successfully copied
    copy_demo_configs(tmp_path, "rubin_circle", False)

    assert os.path.isfile(os.path.join(tmp_path, "Rubin_circular_approximation.ini"))

    copy_demo_configs(tmp_path, "rubin_footprint", False)

    assert os.path.isfile(os.path.join(tmp_path, "Rubin_full_footprint.ini"))

    copy_demo_configs(tmp_path, "rubin_known", False)
    assert os.path.isfile(os.path.join(tmp_path, "Rubin_known_object_prediction.ini"))

    # remove those files
    os.remove(os.path.join(tmp_path, "Rubin_circular_approximation.ini"))
    os.remove(os.path.join(tmp_path, "Rubin_full_footprint.ini"))
    os.remove(os.path.join(tmp_path, "Rubin_known_object_prediction.ini"))

    # test that all the configs are successfully copied
    copy_demo_configs(tmp_path, "all", False)

    assert os.path.isfile(os.path.join(tmp_path, "Rubin_circular_approximation.ini"))
    assert os.path.isfile(os.path.join(tmp_path, "Rubin_full_footprint.ini"))
    assert os.path.isfile(os.path.join(tmp_path, "Rubin_known_object_prediction.ini"))

    # test that files are successfully overwritten if -f flag used
    copy_demo_configs(tmp_path, "all", True)

    # test the error message if user supplies non-existent directory
    dummy_folder = os.path.join(tmp_path, "dummy_folder")
    with pytest.raises(SystemExit) as e:
        copy_demo_configs(dummy_folder, "all", False)

    assert e.value.code == "ERROR: filepath {} supplied for filepath argument does not exist.".format(
        dummy_folder
    )

    # test the error message if user supplies unrecognised keyword for which_configs variable
    with pytest.raises(SystemExit) as e2:
        copy_demo_configs(tmp_path, "laphroaig", True)

    assert (
        e2.value.code
        == "String 'laphroaig' not recognised for 'configs' variable. Must be 'rubin_circle', 'rubin_footprint', 'rubin_known' or 'all'."
    )

    # test the error message if file exists and overwrite isn't forced

    with pytest.raises(SystemExit) as e3:
        copy_demo_configs(tmp_path, "rubin_footprint", False)

    assert (
        e3.value.code
        == "Identically named file exists at location. Re-run with -f or --force to force overwrite."
    )


def test_parse_file_selection():
    from sorcha_cmdline.init import parse_file_selection

    # test to make sure the inputs align with the correct options
    test_rubin_circle = parse_file_selection("1")
    test_rubin_footprint = parse_file_selection("2")
    test_rubin_known = parse_file_selection("3")
    test_all = parse_file_selection("4")

    assert test_rubin_circle == "rubin_circle"
    assert test_rubin_footprint == "rubin_footprint"
    assert test_rubin_known == "rubin_known"
    assert test_all == "all"

    # test error messages

    with pytest.raises(SystemExit) as e:
        test_string = parse_file_selection("not_an_integer")

    assert e.value.code == "Input could not be converted to a valid integer. Please try again."

    with pytest.raises(SystemExit) as e2:
        test_wrong_integer = parse_file_selection("500")

    assert (
        e2.value.code
        == "Input could not be converted to a valid integer. Please input an integer between 1 and 4."
    )
