from registry import TokenizerRegistry


def create_tokenizer(name: str):
    tokenizer_cls = TokenizerRegistry.get(name)
    return tokenizer_cls()