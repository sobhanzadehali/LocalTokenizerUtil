import os
from .hf_tokenizer import HFTokenizer
from ..registry import TokenizerRegistry


class JinaTokenizer(HFTokenizer):
    def __init__(self, model_path: str = None):
        if model_path is None:
            base_dir = os.getenv("TOKENIZER_DIR", "/app/tokenizers")
            model_path = os.path.join(base_dir, "jina")
        super().__init__(model_path=model_path)


TokenizerRegistry.register("jina", JinaTokenizer)
