import hashlib

from struct import pack

def get_pseudorandom_stream(passphrase):
    seed = get_seed_argon2(passphrase)
    return FastPseudorandom(seed)

'''
Given a string passphrase, generates a 64-byte seed.

The expectations from the seed are that it
1. Is deterministic.
2. Is statistically uniform.
3. Is hard to compute.
4. Preserves the enthropy given (up to 64 bytes).
'''
def get_seed_argon2(passphrase):
    from argon2 import argon2_hash
    return argon2_hash(passphrase, passphrase, t=4096, m=16, buflen=64)

class FastPseudorandom:
    '''
    Given a 64-byte seed, creates a fast deterministic stream of
    bytes. If hash function is not provided, the iteration is simply
    next_block = sha3_512(prev_block).

    Inspired by PBKDF2 but is deliberately simpler, because hardness is not a
    target.

    The expectations from the sequence are that it
    1. Is deterministic.
    2. Is statistically uniform.
    3. Is easy to compute.
    4. Preserves the enthropy given (up to 64 bytes).
    '''
    def __init__(self, seed, hash=lambda x: hashlib.sha3_512(x).digest()):
        self.__seed = seed
        self.__buf = seed
        self.__hash = hash
        self.__iteration = 0

    def __next_block(self):
        assert 0 <= self.__iteration < 0xffffffff
        self.__seed = self.__hash(self.__seed + pack("!L", self.__iteration))
        self.__iteration += 1
        return self.__seed

    '''Read the specified number of key bytes.'''
    def read(self, bytes):
        while len(self.__buf) < bytes:
            self.__buf += self.__next_block()
        retval = self.__buf[:bytes]
        self.__buf = self.__buf[bytes:]
        return retval
