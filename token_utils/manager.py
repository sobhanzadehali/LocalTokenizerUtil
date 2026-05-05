from token_utils.factory import create_tokenizer
from token_utils.chunkers.token_chunker import TokenChunker


class TokenizationManager:
    def __init__(self, tokenizer_name: str, model_path: str = None):
        if model_path:
            # Use custom path - assume HF tokenizer
            from token_utils.tokenizers.hf_tokenizer import HFTokenizer
            self.tokenizer = HFTokenizer(model_path)
        else:
            self.tokenizer = create_tokenizer(tokenizer_name)

    def tokenize(self, text: str):
        return self.tokenizer.encode(text)

    def count_tokens(self, text: str):
        return self.tokenizer.count_tokens(text)

    def chunk_text(self, text: str, chunk_size: int, overlap: int = 0):
        chunker = TokenChunker(
            tokenizer=self.tokenizer,
            chunk_size=chunk_size,
            overlap=overlap
        )
        return chunker.chunk(text)