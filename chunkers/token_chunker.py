from typing import List
from base import BaseTokenizer
from chunkers.base_chunker import BaseChunker


class TokenChunker(BaseChunker):
    def __init__(self, tokenizer: BaseTokenizer, chunk_size: int, overlap: int = 0):
        self.tokenizer = tokenizer
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(self, text: str) -> List[str]:
        tokens = self.tokenizer.encode(text)

        chunks = []
        start = 0

        while start < len(tokens):
            end = start + self.chunk_size
            chunk_tokens = tokens[start:end]
            chunks.append(self.tokenizer.decode(chunk_tokens))
            start += self.chunk_size - self.overlap

        return chunks