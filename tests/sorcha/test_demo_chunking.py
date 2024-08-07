import os
import tempfile
import pandas as pd

from sorcha.utilities.diffTestUtils import override_seed_and_run


def test_demo_chunking():
    """This tests chunked vs. unchunked Sorcha. It is a full end-to-end test
    with all randomised elements turned off to enable a one-to-one comparison
    between the chunked and unchunked results.
    """

    with tempfile.TemporaryDirectory() as dir_name:
        override_seed_and_run(dir_name, arg_set="chunked")
        override_seed_and_run(dir_name, arg_set="unchunked")
        res_file_chunked = os.path.join(dir_name, "out_end2end_chunked.csv")
        res_file_unchunked = os.path.join(dir_name, "out_end2end_unchunked.csv")
        assert os.path.isfile(res_file_chunked)
        assert os.path.isfile(res_file_unchunked)

        chunked_data = pd.read_csv(res_file_chunked)
        unchunked_data = pd.read_csv(res_file_unchunked)

        if chunked_data.shape != unchunked_data.shape:
            return False

        chunked_sorted = chunked_data.sort_values(["ObjID", "fieldMJD_TAI"]).reset_index(drop=True)
        unchunked_sorted = unchunked_data.sort_values(["ObjID", "fieldMJD_TAI"]).reset_index(drop=True)

        pd.testing.assert_frame_equal(chunked_sorted, unchunked_sorted)
