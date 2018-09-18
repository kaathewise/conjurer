from struct import pack

from Crypto.Hash import SHA3_512


def get_source(passphrase):
    seed = get_seed_argon2(passphrase)
    return FastPseudorandom(seed).read


def get_seed_argon2(passphrase):
    """
    Given a string passphrase, generates a 64-byte seed.

    The expectations from the seed are that it
    1. Is deterministic.
    2. Is statistically uniform.
    3. Is hard to compute.
    4. Preserves the enthropy given (up to 64 bytes).
    """
    from argon2 import argon2_hash
    return argon2_hash(passphrase, passphrase, t=4096, m=16, buflen=64)


class _FastPseudorandom:
    """
    Given a seed, creates a fast deterministic stream of bytes.

    If hash function is not provided, the iteration is simply
    block_{i+1} = sha3_512(block_i + i).

    Inspired by PBKDF2 but is deliberately simpler, because hardness is not a
    target.

    The expectations from the sequence are that it
    1. Is deterministic.
    2. Is statistically uniform.
    3. Is easy to compute.
    4. Preserves the enthropy given (up to 64 bytes).
    """

    def __init__(self, seed, hash=lambda x: SHA3_512.new(data=x).digest()):
        self.__seed = seed
        self.__buf = seed
        self.__hash = hash
        self.__iteration = 0

    def __next_block(self):
        assert 0 <= self.__iteration < 0xffffffff
        self.__seed = self.__hash(self.__seed + pack("!L", self.__iteration))
        self.__iteration += 1
        return self.__seed

    def read(self, bytes):
        """Read the specified number of key bytes."""
        while len(self.__buf) < bytes:
            self.__buf += self.__next_block()
        retval = self.__buf[:bytes]
        self.__buf = self.__buf[bytes:]
        return retval
