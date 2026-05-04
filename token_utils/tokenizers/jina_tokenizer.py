import os
from token_utils.tokenizers.hf_tokenizer import HFTokenizer
from token_utils.registry import TokenizerRegistry


class JinaTokenizer(HFTokenizer):
    def __init__(self):
        base_dir = os.getenv("TOKENIZER_DIR", "/app/tokenizers")
        super().__init__(model_path=os.path.join(base_dir, "jina"))


TokenizerRegistry.register("jina", JinaTokenizer)
