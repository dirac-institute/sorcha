import os
import tempfile

from sorcha.utilities.dataUtilitiesForTests import get_demo_filepath
from sorcha.utilities.diffTestUtils import compare_result_files, override_seed_and_run


def test_demo_end2end():
    """run the full rubin sim to ensure there are no errors."""
    golden_dir = get_demo_filepath("goldens")
    golden_fn = os.path.join(golden_dir, "out_end2end.csv")
    print(f"Golden File: {golden_fn}")
    if not os.path.isdir(golden_dir) or not os.path.isfile(golden_fn):
        print("ERROR: No goldens generated. You must first run:")
        print("  python src/sorcha/utilities/generateGoldens.py")
        assert False

    with tempfile.TemporaryDirectory() as dir_name:
        override_seed_and_run(dir_name, arg_set="baseline")
        res_file = os.path.join(dir_name, "out_end2end.csv")
        assert os.path.isfile(res_file)
        print(f"Res File: {res_file}")

        if not compare_result_files(res_file, golden_fn):
            print("Result files do not match. There may be an error in the code, or you may need")
            print("to regenerate the goldens with 'python src/sorcha/utilities/generateGoldens.py'")
            assert False


def test_demo_ephemeris_generation():
    """run the ephemeris generation to ensure there are no errors."""
    golden_dir = get_demo_filepath("goldens")
    golden_fn = os.path.join(golden_dir, "sorcha_ephemeris.csv")
    print(f"Golden File: {golden_fn}")
    if not os.path.isdir(golden_dir) or not os.path.isfile(golden_fn):
        print("ERROR: No goldens generated. You must first run:")
        print("  python src/sorcha/utilities/generateGoldens.py")
        assert False

    with tempfile.TemporaryDirectory() as dir_name:
        override_seed_and_run(dir_name, arg_set="with_ephemeris")
        res_file = os.path.join(dir_name, "sorcha_ephemeris.csv")
        assert os.path.isfile(res_file)
        print(f"Res File: {res_file}")

        if not compare_result_files(res_file, golden_fn):
            print("Result files do not match. There may be an error in the code, or you may need")
            print("to regenerate the goldens with 'python src/sorcha/utilities/generateGoldens.py'")
            assert False
