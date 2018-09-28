import json

from generators.testing.fingerprints import fingerprint_generators
from core.pseudorandom_source import get_source

PASSPHRASE = 'Nobody expects deterministic conjuration.'

source = get_source(PASSPHRASE)
fprints = dict(
    (cmd.name, gen(source)) for cmd, gen in fingerprint_generators.items())
print(json.dumps(fprints, sort_keys=True, indent=2))
