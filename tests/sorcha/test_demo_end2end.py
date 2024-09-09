import os
import tempfile

from sorcha.utilities.dataUtilitiesForTests import get_test_filepath
from sorcha.utilities.diffTestUtils import compare_result_files, override_seed_and_run


def test_demo_end2end():
    """run the full rubin sim to ensure there are no errors."""
    golden_dir = get_test_filepath("goldens")
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
    golden_dir = get_test_filepath("goldens")
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


def test_demo_verification():
    """verification independently derived by Pedro - should match the results of Sorcha really really well."""
    import numpy as np
    import astropy.table as tb

    golden_dir = get_test_filepath("goldens")
    golden_fn = os.path.join(golden_dir, "verification_truth.csv")
    truth = tb.Table.read(golden_fn)
    t = {}
    t["2011 OB60"] = truth[truth["ObjID"] == "2011 OB60"]
    t["2010 TU149"] = truth[truth["ObjID"] == "2010 TU149"]

    print(f"Golden File: {golden_fn}")

    with tempfile.TemporaryDirectory() as dir_name:
        override_seed_and_run(dir_name, arg_set="truth")
        res_file = os.path.join(dir_name, "verification_output.csv")
        out = tb.Table.read(res_file)
        print(f"Res File: {res_file}")

        v = {}
        v["2011 OB60"] = out[out["ObjID"] == "2011_OB60"]
        v["2010 TU149"] = out[out["ObjID"] == "2010_TU149"]

        for i in v:
            v[i].sort("fieldMJD_TAI")
            t[i].sort("observationStartMJD_TAI")
            for j, k in zip(
                ["RA_deg", "Dec_deg", "trailedSourceMag"], ["RA_INTERP", "DEC_INTERP", "mag"]
            ):
                m = np.abs(np.mean(v[i][j] - t[i][k]))
                if k == "mag":
                    assert np.isclose(np.max(m), 0, atol=1e-3)  # 1 mmag - should be much better than that
                else:
                    assert np.isclose(np.max(m), 0, atol=0.005 / 3600)  # 5 mas - mean is 0 but std is ~1 mas
