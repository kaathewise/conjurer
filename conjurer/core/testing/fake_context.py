class FakeContextProvider:
    def __init__(self, **kwargs):
        self.verbose = False
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __call__(self):
        return self
