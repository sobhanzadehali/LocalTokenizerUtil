from token_utils.factory import create_tokenizer
from token_utils.chunkers.token_chunker import TokenChunker


class TokenizationManager:
    def __init__(self, tokenizer_name: str):
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