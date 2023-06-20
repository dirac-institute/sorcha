import datetime
import json
import timeit
import numpy as np
import pandas as pd

from memory_profiler import memory_usage

from surveySimPP.modules.PPApplyColourOffsets import PPApplyColourOffsets

def setup_test_obs(num_copies=1):
    objects = np.array(['obj1', 'obj1', 'obj1', 'obj1', 'obj2', 'obj2', 'obj2', 'obj2']*num_copies)

    optfilter = np.array(['r', 'g', 'i', 'z', 'r', 'g', 'z', 'i']*num_copies)

    ur = np.array([0.1, 0.1, 0.1, 0.1, 0.2, 0.2, 0.2, 0.2]*num_copies)
    gr = np.array([0.3, 0.3, 0.3, 0.3, 0.4, 0.4, 0.4, 0.4]*num_copies)
    ir = np.array([0.5, 0.5, 0.5, 0.5, 0.6, 0.6, 0.6, 0.6]*num_copies)
    zr = np.array([0.7, 0.7, 0.7, 0.7, 0.8, 0.8, 0.8, 0.8]*num_copies)

    H = np.array([10.0, 10.0, 10.0, 10.0, 12.0, 12.0, 12.0, 12.0]*num_copies)
    G = np.array([0.15, 0.15, 0.15, 0.15, 0.12, 0.12, 0.12, 0.12]*num_copies)

    return pd.DataFrame({'ObjID': objects, 'optFilter': optfilter,
                                    'u-r': ur, 'g-r': gr, 'i-r': ir, 'z-r': zr,
                                    'H_r': H, 'GS': G})

def setup_other_colors():
    return ['u-r', 'g-r', 'i-r', 'z-r']

def setup_obs_filters():
    return ['r', 'u', 'g', 'i', 'z']

statement = 'PPApplyColourOffsets(test_obs.copy(), "HG", othercolours, observing_filters, "r")'

def create_setup_str(num_copies=1):
    return f'''
test_obs = setup_test_obs({num_copies})
othercolours = setup_other_colors()
observing_filters = setup_obs_filters()
'''

'''Runtime benchmarking'''

benchmarks = []

for n in [1_000, 10_000, 100_000]:

    t = timeit.Timer(
        stmt=statement,
        setup=create_setup_str(n),
        globals={
            'PPApplyColourOffsets': PPApplyColourOffsets,
            'setup_other_colors': setup_other_colors,
            'setup_test_obs': setup_test_obs,
            'setup_obs_filters': setup_obs_filters,
            },
        )

    output = t.repeat(repeat=10, number=1)

    print("repetitions:", len(output), "avg:", np.mean(output), "std:", np.std(output))

    bench_dict = {
        'timestamp': str(datetime.datetime.now()),
        'name': f'ApplyColourOffsets_{n}',
        'repetitions': len(output),
        'avg_run_time_of_repetitions': np.mean(output),
        'std_of_repetitions': np.std(output),
        'all_run_times': output
    }

    benchmarks.append(bench_dict)

'''Memory usage benchmarking'''

mem_usage = []

for i in range(10):
    new_test_obs = setup_test_obs(1_000)
    other_colours = setup_other_colors()
    obs_filters = setup_obs_filters()
    max_usage = memory_usage(
        (PPApplyColourOffsets, (new_test_obs.copy(), "HG", other_colours, obs_filters, "r"), {}),
        max_usage=True,
        interval=0.1, max_iterations=1)

    mem_usage.append(max_usage)

bench_dict = {
        'timestamp': str(datetime.datetime.now()),
        'name': f'ApplyColourOffsets_{n}',
        'repetitions': len(mem_usage),
        'avg_max_memory_usage': np.mean(mem_usage),
        'std_of_repetitions': np.std(mem_usage),
        'all_max_memory_measurements': mem_usage
    }

benchmarks.append(bench_dict)

print("repetitions:", len(mem_usage), "avg:", np.mean(mem_usage), "std:", np.std(mem_usage))


output_dict = {
    'benchmarks': benchmarks
}

with open('bench_ApplyColourOffset.json', 'w') as output_file:
    json.dump(output_dict, output_file)