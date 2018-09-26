import click
import sys

from generators import *
from pseudorandom_source import get_source


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
@click.pass_context
def cli(ctx, passphrase, user):
    ctx.obj = LazyOptionProvider(passphrase, user)


for name, cmd in commands:
    cli.add_command(cmd, name=name)


class LazyOptionProvider:
    def __init__(self, passphrase, user):
        self.passphrase = passphrase
        self.user = user
        self.source = None

    def __call__(self):
        if not self.source:
            passphrase = self.passphrase or click.prompt(
                'Passphrase', prompt_suffix=': 🔑', hide_input=True, err=True)
            self.user = self.user or click.prompt('User', err=True)
            self.source = get_source('%s$%s' % (passphrase, self.user))
            del self.passphrase
        return self
