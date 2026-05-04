class TokenizerRegistry:
    _registry = {}

    @classmethod
    def register(cls, name: str, tokenizer_cls):
        cls._registry[name] = tokenizer_cls

    @classmethod
    def get(cls, name: str):
        if name not in cls._registry:
            raise ValueError(f"Tokenizer '{name}' not registered")
        return cls._registry[name]