import click
import sys

from generators import commands
from core.context import LazyContextProvider


@click.group()
@click.option(
    '--passphrase',
    '-p',
    help='Passphrase for generation. It is the main source of enthropy.')
@click.option(
    '--user',
    '-u',
    help=
    'Username, UserId, or any kind of virtual identity. Used for generation, but also as the identity for certificates.'
)
@click.option('--verbose', '-v', is_flag=True, default=False)
@click.pass_context
def cli(ctx, passphrase, user, verbose):
    ctx.obj = LazyContextProvider(passphrase=passphrase, user=user, verbose=verbose)


for cmd in commands:
    cli.add_command(cmd)
