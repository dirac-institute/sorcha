import hashlib
import numpy as np


def getModuleRNG(base_seed, module_name):
    """
    Return a random number generator that is based on a base seed
    and the current module name.

    Parameters:
    -----------
    base_seed (int): The base seed for a random number generator

    module_name (str): The name of the module (used as part of the seed)

    Returns:
    ----------
    rng (numpy Generator): The random number generator.

    """

    seed_offset = int(hashlib.md5(module_name.encode("utf-8")).hexdigest(), 16)
    module_seed = (base_seed + seed_offset) % (2**31)
    rng = np.random.default_rng(module_seed)

    return rng
