import timeit
import numpy as np
import pandas as pd

from metric_emitter import Emitter

from sorcha.modules.PPDetectionEfficiency import PPDetectionEfficiency


def setup_observations():
    return pd.DataFrame({"ObjID": np.arange(0, 1_000_000)})


def create_runtime_statement():
    return "PPDetectionEfficiency(observations, 0.5, rng)"


def create_setup_str():
    return f"""
observations = setup_observations()
rng = np.random.default_rng(2021)
"""


class TestBenchDetectionEfficiency:
    """Runtime benchmarking"""

    def test_bench_runtime(self):
        emitter = Emitter(
            namespace="lsst.lf",
            name="sspp.module_benchmarks",
            module=PPDetectionEfficiency.__name__,
            benchmark_type=f"run",
            benchmark_unit="s",
        )

        t = timeit.Timer(
            stmt=create_runtime_statement(),
            setup=create_setup_str(),
            globals=globals(),
        )

        output = t.repeat(repeat=11, number=1)

        # We take 11 samples, but we only emit the last 10.
        # The first sample is considered a warm up.
        for sample in output[1:]:
            emitter.set_value(sample)
            emitter.emit()
