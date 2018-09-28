"""Contains commands related to GPG generation."""

import click
import os
import subprocess
import sys
import tempfile

# CLI COMMANDS


@click.command(name='gpg-pem', short_help='Create GPG key in PEM format.')
@click.pass_obj
def pem(ctx):
    """Generate an RSA pair and export it in PEM format."""
    click.echo(_get_pem(ctx().source))


@click.command(name='gpg-key', short_help='Create GPG key for import.')
@click.pass_obj
def key(ctx):
    """Generate an RSA pair and export it in GPG format.

    This command relies on pem2openpgp.
    """
    pem = _get_pem(ctx().source)
    click.echo(_get_gpg_key(pem, ctx().user, ctx().verbose))


@click.command(
    name='gpg-public', short_help='Create and print GPG public key.')
@click.pass_obj
def public(ctx):
    """Generate an (RSA) GPG key and export the public key in ASCII.

    This command relies on pem2openpgp and gpg.
    """
    gpg_key = _get_gpg_key(_get_pem(ctx().source), ctx().user, ctx().verbose)
    _run_gpg_with_key(
        gpg_key, ['--armor', '--export', ctx().user], None,
        click.get_binary_stream('stdin'), ctx().verbose)


@click.command(
    name='gpg-encrypt', short_help='Create GPG key and encrypt with it.')
@click.argument('input', type=click.File('rb'))
@click.argument('output', type=click.File('wb'))
@click.pass_obj
def encrypt(ctx, input, output):
    """
    Generate an (RSA) GPG key and use it to encrypt INPUT to OUTPUT.

    This command relies on pem2openpgp and gpg.
    """
    gpg_key = _get_gpg_key(_get_pem(ctx().source), ctx().user, ctx().verbose)
    _run_gpg_with_key(gpg_key, [
        '--encrypt', '--recipient',
        ctx().user, '--trust-model', 'always', '--armor'
    ], input, output, ctx().verbose)


@click.command(
    name='gpg-decrypt', short_help='Create GPG key and decrypt with it.')
@click.argument('input', type=click.File('rb'))
@click.argument('output', type=click.File('wb'))
@click.pass_obj
def decrypt(ctx, input, output):
    """
    Generate an (RSA) GPG key and use it to decrypt INPUT to OUTPUT.

    This command relies on pem2openpgp and gpg.
    """
    gpg_key = _get_gpg_key(_get_pem(ctx().source), ctx().user, ctx().verbose)
    _run_gpg_with_key(gpg_key, [
        '--decrypt', '--recipient',
        ctx().user, '--trust-model', 'always', '--armor'
    ], input, output, ctx().verbose)


# IMPLEMENTATION


def _get_pem(source):
    from Crypto.PublicKey import RSA
    return RSA.generate(4096, source).export_key(format='PEM')


def _get_gpg_key(pem, user_id, verbose):
    my_env = os.environ.copy()
    my_env['PEM2OPENPGP_TIMESTAMP'] = '0'
    my_env['PEM2OPENPGP_USAGE_FLAGS'] = 'certify,sign,encrypt,authenticate'
    return subprocess.run(
        ['pem2openpgp', user_id],
        env=my_env,
        check=True,
        input=pem,
        stdout=subprocess.PIPE,
        stderr=None if verbose else subprocess.DEVNULL).stdout


def _run_gpg_with_key(gpg_key, cmd, input, output, verbose):
    with tempfile.TemporaryDirectory() as tmpdirname:
        subprocess.run(['gpg', '--homedir', tmpdirname, '--import'],
                       input=gpg_key,
                       check=True,
                       stderr=None if verbose else subprocess.DEVNULL)
        result = subprocess.run(
            ['gpg', '--homedir', tmpdirname] + cmd,
            check=True,
            input=input.read() if input else None,
            stdout=subprocess.PIPE,
            stderr=None if verbose else subprocess.DEVNULL).stdout
        if output:
            output.write(result)
