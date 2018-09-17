class GPGKey:
    def __init__(self, random_source):
        from Crypto.PublicKey import RSA
        self.key = RSA.generate(4096, random_source)

    def __str__(self):
        return self.key.export_key(format='PEM').decode('ascii')
