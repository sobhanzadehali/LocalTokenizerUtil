from token_utils.registry import TokenizerRegistry
import os


def create_tokenizer(name: str):
    tokenizer_cls = TokenizerRegistry.get(name)
    
    # Handle different tokenizer initialization patterns
    if name == "hf":
        # HF tokenizer needs model_path
        base_dir = os.getenv("TOKENIZER_DIR", "/app/tokenizers")
        model_path = os.path.join(base_dir, "hf")
        return tokenizer_cls(model_path=model_path)
    elif name == "jina":
        # Jina tokenizer gets path from base class
        return tokenizer_cls()
    else:
        # Default case - try with no arguments
        return tokenizer_cls()