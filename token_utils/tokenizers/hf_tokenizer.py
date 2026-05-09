import os
from transformers import AutoTokenizer
from ..base import BaseTokenizer
from ..registry import TokenizerRegistry


class HFTokenizer(BaseTokenizer):
    def __init__(self, model_path: str, **kwargs):
        if not os.path.exists(model_path):
            raise ValueError(f"Tokenizer path does not exist: {model_path}")

        self.tokenizer = AutoTokenizer.from_pretrained(
            model_path,
            local_files_only=True,
            **kwargs
        )

    def encode(self, text: str):
        return self.tokenizer.encode(text, add_special_tokens=False)

    def decode(self, tokens):
        return self.tokenizer.decode(tokens)

    def count_tokens(self, text: str):
        return len(self.encode(text))


TokenizerRegistry.register("hf", HFTokenizer)