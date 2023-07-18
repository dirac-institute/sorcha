import timeit
import numpy as np
import pandas as pd

from memory_profiler import memory_usage
from metric_emitter import Emitter

from sorcha.modules.PPApplyColourOffsets import PPApplyColourOffsets


def setup_test_obs(num_copies=1):
    objects = np.array(["obj1", "obj1", "obj1", "obj1", "obj2", "obj2", "obj2", "obj2"] * num_copies)

    optfilter = np.array(["r", "g", "i", "z", "r", "g", "z", "i"] * num_copies)

    ur = np.array([0.1, 0.1, 0.1, 0.1, 0.2, 0.2, 0.2, 0.2] * num_copies)
    gr = np.array([0.3, 0.3, 0.3, 0.3, 0.4, 0.4, 0.4, 0.4] * num_copies)
    ir = np.array([0.5, 0.5, 0.5, 0.5, 0.6, 0.6, 0.6, 0.6] * num_copies)
    zr = np.array([0.7, 0.7, 0.7, 0.7, 0.8, 0.8, 0.8, 0.8] * num_copies)

    H = np.array([10.0, 10.0, 10.0, 10.0, 12.0, 12.0, 12.0, 12.0] * num_copies)
    G = np.array([0.15, 0.15, 0.15, 0.15, 0.12, 0.12, 0.12, 0.12] * num_copies)

    return pd.DataFrame(
        {
            "ObjID": objects,
            "optFilter": optfilter,
            "u-r": ur,
            "g-r": gr,
            "i-r": ir,
            "z-r": zr,
            "H_r": H,
            "GS": G,
        }
    )

    return pd.DataFrame(
        {
            "ObjID": objects,
            "optFilter": optfilter,
            "u-r": ur,
            "g-r": gr,
            "i-r": ir,
            "z-r": zr,
            "H_r": H,
            "GS": G,
        }
    )


def setup_other_colors():
    return ["u-r", "g-r", "i-r", "z-r"]


def setup_obs_filters():
    return ["r", "u", "g", "i", "z"]


def create_runtime_statement():
    return 'PPApplyColourOffsets(test_obs.copy(), "HG", othercolours, observing_filters, "r")'


def create_setup_str(num_copies=1):
    return f"""
test_obs = setup_test_obs({num_copies})
othercolours = setup_other_colors()
observing_filters = setup_obs_filters()
"""


class TestBenchApplyColourOffsets:
    """Runtime benchmarking"""

    def test_bench_runtime(self):
        num_copies = 1_000

        emitter = Emitter(
            namespace="lsst.lf",
            name="sspp.module_benchmarks",
            module=PPApplyColourOffsets.__name__,
            benchmark_type=f"run_{num_copies}",
            benchmark_unit="s",
        )

        t = timeit.Timer(
            stmt=create_runtime_statement(),
            setup=create_setup_str(num_copies),
            globals=globals(),
        )

        output = t.repeat(repeat=11, number=1)

        # We take 11 samples, but we only emit the last 10.
        # The first sample is considered a warm up.
        for sample in output[1:]:
            emitter.set_value(sample)
            emitter.emit()

    """Memory usage benchmarking"""

    def test_bench_memory(self):
        num_copies = 1_000
        emitter = Emitter(
            namespace="lsst.lf",
            name="sspp.module_benchmarks",
            module=PPApplyColourOffsets.__name__,
            benchmark_type=f"mem_{num_copies}",
            benchmark_unit="Mb",
        )

        max_mem_used = []

        for i in range(11):
            new_test_obs = setup_test_obs(num_copies)
            other_colours = setup_other_colors()
            obs_filters = setup_obs_filters()
            max_usage = memory_usage(
                (PPApplyColourOffsets, (new_test_obs.copy(), "HG", other_colours, obs_filters, "r"), {}),
                max_usage=True,
                interval=0.1,
                max_iterations=1,
            )

            max_mem_used.append(max_usage)

        # We take 11 samples, but we only emit the last 10.
        # The first sample is considered a warm up.
        for sample in max_mem_used[1:]:
            emitter.set_value(sample)
            emitter.emit()
