import hashlib
import numpy as np


class PerModuleRNG:
    """A collection of per-module random number generators."""

    def __init__(self, base_seed):
        """Parameters:
        --------------

        base_seed (int): The base seed for a random number generator
        """
        self._base_seed = base_seed
        self._rngs = {}

    def getModuleRNG(self, module_name):
        """
        Return a random number generator that is based on a base seed
        and the current module name.

        Parameters:
        -----------
        module_name (str): The name of the module

        Returns:
        ----------
        rng (numpy Generator): The random number generator.
        """
        if module_name in self._rngs:
            return self._rngs[module_name]

        seed_offset = int(hashlib.md5(module_name.encode("utf-8")).hexdigest(), 16)
        module_seed = (self._base_seed + seed_offset) % (2**31)
        new_rng = np.random.default_rng(module_seed)
        self._rngs[module_name] = new_rng

        return new_rng
