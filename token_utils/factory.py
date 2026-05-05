from token_utils.registry import TokenizerRegistry
from token_utils.downloader import TokenizerDownloader
import os


def create_tokenizer(name: str):
    tokenizer_cls = TokenizerRegistry.get(name)

    # Handle different tokenizer initialization patterns
    if name == "hf":
        # HF tokenizer needs model_path
        base_dir = os.getenv("TOKENIZER_DIR", "/app/tokenizers")
        model_path = os.path.join(base_dir, "hf")
        # Try to download if not exists
        downloader = TokenizerDownloader()
        try:
            actual_path = downloader.get_tokenizer_path("hf")
            return tokenizer_cls(model_path=actual_path)
        except:
            # Fallback to original behavior
            return tokenizer_cls(model_path=model_path)
    elif name == "jina":
        # Jina tokenizer gets path
        base_dir = os.getenv("TOKENIZER_DIR", "/app/tokenizers")
        model_path = os.path.join(base_dir, "jina")
        downloader = TokenizerDownloader()
        try:
            actual_path = downloader.get_tokenizer_path("jina")
            return tokenizer_cls(model_path=actual_path)
        except:
            return tokenizer_cls(model_path=model_path)
    else:
        # For custom tokenizers, first check if it exists in standard location
        downloader = TokenizerDownloader()
        base_dir = os.getenv("TOKENIZER_DIR", "/app/tokenizers")
        standard_path = os.path.join(base_dir, name)

        if os.path.exists(standard_path):
            return tokenizer_cls(model_path=standard_path)

        # Try auto-detection
        detected_path = downloader.auto_detect_tokenizer(name)
        if detected_path:
            return tokenizer_cls(model_path=detected_path)

        # Try to download
        try:
            model_path = downloader.get_tokenizer_path(name)
            return tokenizer_cls(model_path=model_path)
        except Exception as e:
            raise ValueError(f"Tokenizer '{name}' not found locally, could not download, and auto-detection failed. "
                           f"Please specify the path manually or check your TOKENIZER_DIR. Error: {e}")