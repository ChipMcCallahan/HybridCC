import random


class RNG:
    _seed = random.randint(0, 0x7FFFFFFF)  # Class variable for the seed

    @classmethod
    def _check_seed(cls, seed):
        if seed is not None and seed < 0:
            raise ValueError("Seed must be nonnegative.")

    @classmethod
    def reset(cls, seed=None):
        cls._check_seed(seed)
        cls._seed = random.randint(0, 0x7FFFFFFF) if seed is None else seed

    @classmethod
    def next(cls):
        cls._seed = (cls._seed * 1103515245 + 12345) & 0x7FFFFFFF
        return cls._seed ^ (cls._seed >> 16)


# Initialize with a default seed
RNG.reset()