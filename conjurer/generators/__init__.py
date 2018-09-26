"""Contains all commands that are making use of the pseudorandom source."""

from . import gpg

import click

commands = [
    ('gpg-pem', gpg.pem),
    ('gpg-key', gpg.key),
    ('gpg-public', gpg.public),
    ('gpg-encrypt', gpg.encrypt),
    ('gpg-decrypt', gpg.decrypt),
]
