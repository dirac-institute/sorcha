import os
import pytest


def test_sorcha_copy_configs(tmp_path):
    from sorcha.utilities.sorcha_copy_configs import copy_demo_configs

    # test that the Rubin files are successfully copied
    copy_demo_configs(tmp_path, "rubin")

    assert os.path.isfile(os.path.join(tmp_path, "Rubin_circular_approximation.ini"))
    assert os.path.isfile(os.path.join(tmp_path, "Rubin_full_footprint.ini"))

    # test that the demo config is successfully copied
    copy_demo_configs(tmp_path, "demo")

    assert os.path.isfile(os.path.join(tmp_path, "sorcha_config_demo.ini"))

    # remove those files
    os.remove(os.path.join(tmp_path, "Rubin_circular_approximation.ini"))
    os.remove(os.path.join(tmp_path, "Rubin_full_footprint.ini"))
    os.remove(os.path.join(tmp_path, "sorcha_config_demo.ini"))

    # test that all the configs are successfully copied
    copy_demo_configs(tmp_path, "all")

    assert os.path.isfile(os.path.join(tmp_path, "Rubin_circular_approximation.ini"))
    assert os.path.isfile(os.path.join(tmp_path, "Rubin_full_footprint.ini"))
    assert os.path.isfile(os.path.join(tmp_path, "sorcha_config_demo.ini"))

    # test the error message if user supplies non-existent directory
    dummy_folder = os.path.join(tmp_path, "dummy_folder")
    with pytest.raises(SystemExit) as e:
        copy_demo_configs(dummy_folder, "all")

    assert e.type == SystemExit
    assert e.value.code == "ERROR: filepath {} supplied for -f, --filepath argument does not exist.".format(
        dummy_folder
    )

    # test the error message if user supplies unrecognised keyword for which_configs variable
    with pytest.raises(SystemExit) as e2:
        copy_demo_configs(tmp_path, "laphroaig")

    assert e2.type == SystemExit
    assert (
        e2.value.code
        == "String 'laphroaig' not recognised for 'configs' variable. Must be 'rubin', 'demo' or 'all'."
    )
