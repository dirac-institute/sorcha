import os
import astropy.table as tb
from multiprocessing import Pool
import pandas as pd
import sqlite3

def run_sorcha(i, args, path_inputs, pointings, instance,stats, config):
    print(f"sorcha run -c {config} --pd {pointings} -o {args.path}{instance}/ -t {instance}_{i} --ob  {args.path}{instance}/orbits_{i}.csv -p {args.path}{instance}/physical_{i}.csv --st {stats}_{i}", flush=True)
    os.system(f"sorcha run -c {config} --pd {pointings} -o {args.path}{instance}/ -t {instance}_{i} --ob  {args.path}{instance}/orbits_{i}.csv -p {args.path}{instance}/physical_{i}.csv --st {stats}_{i}")

if __name__ == '__main__':
        import argparse

        parser = argparse.ArgumentParser()
        parser.add_argument('--input_orbits', type=str)
        parser.add_argument('--input_physical', type=str)
        parser.add_argument('--path', type=str)
        parser.add_argument('--chunksize', type=int)
        parser.add_argument('--norbits', type=int)
        parser.add_argument('--cores', type=int)
        parser.add_argument('--instance', type=int)
        parser.add_argument('--cleanup',  action='store_true')
        parser.add_argument('--copy_inputs', action='store_true')
        parser.add_argument('--pointings', type=str)
        parser.add_argument('--stats', type=str)
        parser.add_argument('--config', type=str)
        args = parser.parse_args()
        chunk = args.chunksize
        instance = args.instance
        norbits = args.norbits
        pointings = args.pointings
        path = args.path
        config = args.config
        stats=args.stats

        orbits = tb.Table.read(args.input_orbits)
        orbits = orbits[instance*chunk:(instance+1)*chunk]
        physical = tb.Table.read(args.input_physical)
        physical = physical[instance*chunk:(instance+1)*chunk]

        os.system(f'mkdir {instance}')


        if args.copy_inputs:
                os.system(f'cp {pointings} {instance}/')
                path_inputs = f'{instance}'

        for i in range(args.cores):
                sub_orb = orbits[i*norbits:(i+1)*norbits]
                sub_phys = physical[i*norbits:(i+1)*norbits]
                sub_orb.write(f"{args.path}{instance}/orbits_{i}.csv", overwrite=True)
                sub_phys.write(f"{args.path}{instance}/physical_{i}.csv", overwrite=True)

        with Pool(processes=args.cores) as pool:
            pool.starmap(run_sorcha, [(i, args, path_inputs, pointings, instance, config, stats) for i in range(args.cores)])

        data = [] 
        for i in range(args.cores):
                data.append(pd.read_sql("select * from sorcha_results", sqlite3.connect(f"{args.path}{instance}/{instance}_{i}.db")))
        data = pd.concat(data)
        data.to_sql("sorcha_results", sqlite3.connect(f"{args.path}output_{instance}.db"))
        if args.cleanup:
               os.system(f"rm {args.path}{instance}/*")
               os.system(f"rmdir {args.path}{instance}")

