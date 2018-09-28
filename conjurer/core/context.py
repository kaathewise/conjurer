from .pseudorandom_source import get_source

import click

class LazyContextProvider:
    """Lazy provider for command-line options needed to skip required options when calling --help."""

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.source = None

    def __call__(self):
        """Initialise the options."""
        if not self.source:
            passphrase = self.passphrase or click.prompt(
                'Passphrase', prompt_suffix=': 🔑', hide_input=True, err=True)
            self.user = self.user or click.prompt('User', err=True)
            self.source = get_source('%s$%s' % (passphrase, self.user))
            del self.passphrase
        return self
