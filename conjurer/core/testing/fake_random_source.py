"""Module providing a deterministic pseudorandom source."""

import random

def get_source():
    random.seed(1543)
    return lambda count: bytes(random.randrange(0, 256) for _ in range(count))
