"""Contains commands related to GPG generation."""

import click
import os
import subprocess
import sys
import tempfile

# CLI COMMANDS


@click.command(short_help='Create GPG key in PEM format.')
@click.pass_obj
def pem(ctx):
    """Generate an RSA pair and export it in PEM format."""
    click.echo(_get_pem(ctx().source()))


@click.command(short_help='Create GPG key for import.')
@click.pass_obj
def key(ctx):
    """Generate an RSA pair and export it in GPG format.

    This command relies on pem2openpgp.
    """
    pem = _get_pem(ctx().source)
    click.echo(_get_gpg_key(pem, ctx().user))


@click.command(short_help='Create and print GPG public key.')
@click.pass_obj
def public(ctx):
    """Generate an (RSA) GPG key and export the public key in ASCII.

    This command relies on pem2openpgp and gpg.
    """
    gpg_key = _get_gpg_key(_get_pem(ctx().source), ctx().user)
    _run_gpg_with_key(
        gpg_key, ['--armor', '--export', ctx().user], None,
        click.get_binary_stream('stdin'))


@click.command(short_help='Create GPG key and encrypt with it.')
@click.argument('input', type=click.File('rb'))
@click.argument('output', type=click.File('wb'))
@click.pass_obj
def encrypt(ctx, input, output):
    """
    Generate an (RSA) GPG key and use it to encrypt INPUT to OUTPUT.

    This command relies on pem2openpgp and gpg.
    """
    gpg_key = _get_gpg_key(_get_pem(ctx().source), ctx().user)
    _run_gpg_with_key(gpg_key, [
        '--encrypt', '--recipient',
        ctx().id, '--trust-model', 'always', '--armor'
    ], input, output)


@click.command(short_help='Create GPG key and decrypt with it.')
@click.argument('input', type=click.File('rb'))
@click.argument('output', type=click.File('wb'))
@click.pass_obj
def decrypt(ctx, input, output):
    """
    Generate an (RSA) GPG key and use it to decrypt INPUT to OUTPUT.

    This command relies on pem2openpgp and gpg.
    """
    gpg_key = _get_gpg_key(_get_pem(ctx().source), ctx().user)
    _run_gpg_with_key(gpg_key, [
        '--decrypt', '--recipient',
        ctx().id, '--trust-model', 'always', '--armor'
    ], input, output)


# IMPLEMENTATION


def _get_pem(source):
    from Crypto.PublicKey import RSA
    return RSA.generate(4096, source).export_key(format='PEM')


def _get_gpg_key(pem, user_id):
    my_env = os.environ.copy()
    my_env['PEM2OPENPGP_TIMESTAMP'] = '0'
    my_env['PEM2OPENPGP_USAGE_FLAGS'] = 'certify,sign,encrypt,authenticate'
    pem2openpgp = subprocess.Popen(['pem2openpgp', user_id],
                                   env=my_env,
                                   stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE)
    return pem2openpgp.communicate(pem)[0]


def _run_gpg_with_key(gpg_key, cmd, input, output):
    inp = in_buf.read() if in_buf else None
    with tempfile.TemporaryDirectory() as tmpdirname:
        subprocess.run(['gpg', '--homedir', tmpdirname, '--import'],
                       input=gpg_key,
                       check=True)
        subprocess.run(
            ['gpg', '--homedir', tmpdirname] + cmd, stdin=input, stdout=output)
