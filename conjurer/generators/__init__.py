"""Contains all commands that are making use of the pseudorandom source."""

from . import gpg

import click

commands = [
    gpg.pem,
    gpg.key,
    gpg.public,
    gpg.encrypt,
    gpg.decrypt,
]
