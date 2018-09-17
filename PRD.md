# Project Conjurer
###### (a.k.a. Transient Identity)

## Goals

The goal of Project Conjurer is to create transient identities (passwords and
cryptographic keys) on the fly in a deterministic fashion. It should be
especially useful for amnesic systems, such as TAILS.

The idea is to create a simple tool that, when seeded by a passphrase, will
deterministically generate an authentication token of the specified format.

### Rationale

The common setup for an amnesic system implies that the user may persist their
passwords, keys and certificates on an encrypted drive next to the system.

It is, however, almost impossible to hide the existence of such drive
(especially on a USB stick, which doesn't work well with VeraCrypt hidden
volumes).

Due to the fact that in some jurisdictions or circumstances you might be forced
to give away the password to any encrypted data, the only way to be able to
plausibly alienate yourself from the secret identity markers is not to store
them at all.

### Requirements

1. *Provable security.* The amount of crypto done by the tool itself must be
strictly minimal. The security should be provided by a choice of the passphrase
and well-known and proofed implementations of the respective algorithms.

2. *Proof of work.* The tool must have a way to configure the amount of
pre-computation done with a given passphrase to defend against brute force.

3. *Simplicity.* While having multiple formats/outputs and modes is feasible,
the primary goal is to make the code extremely easy to analyse and trust.

## Prior work

1. https://dankaminsky.com/2012/01/03/phidelius/ -- a simple C program that
mocks /dev/random and some other sources of randomness for other generators.
Pros: works with many other generators without modification. Cons: since it is
a wrapper, you need to know where exactly the wrapped generator takes its
randomness.

2. https://ritter.vg/blog-non_persistent_pgp.html -- a simple C program that
generates specifically GPG keys in a deterministic fashion. Pros: it works (?)
Cons: it implements the key generation afaict, which makes it harder to analyse.

3. https://github.com/arttukasvio/deterministic -- a tool for deterministic
GPG creation. Pros: it can generate a phrase for you. It is supposed to be some
kind of a plugin (?) Cons: dependency on electrum, the code is a bit hard to
analyse and to extend.

4. https://github.com/dcc4e/cckeytools -- the closest thing to what this Project
aims to do. Pros: it seems to be able to do everything listed above. It also
can generate a passphrase for you. Cons: it seems to be doing too many things
at once, which makes the code hard to trust (req. 3 -- Simplicity).
