import os
import tempfile
import pandas as pd

from sorcha.utilities.dataUtilitiesForTests import get_demo_filepath
from sorcha.utilities.diffTestUtils import override_seed_and_run


def test_demo_process_subset():
    """This tests the --process-subset command line option, where only a chunk of
    the input files are run through Sorcha. It is a full end-to-end test
    with all randomised elements turned off for a quick test.
    """

    with tempfile.TemporaryDirectory() as dir_name:
        override_seed_and_run(dir_name, arg_set="subset")
        res_file = os.path.join(dir_name, "out_end2end_subset.csv")
        assert os.path.isfile(res_file)

        subset_data = pd.read_csv(res_file)

        assert len(subset_data["ObjID"].unique()) == 1
        assert subset_data["ObjID"].unique()[0] == "2010_TC209"
