from src.token_utils .base

class Chunker:
    def __init__(self, tokenizer: BaseTokenizer) -> None:
        self._tokenizer = tokenizer

    def chunk(
        self, text: str, max_tokens: int, overlap: int = 0, return_ids: bool = False
    ) -> list[str] | list[list[int]]:
        """
        Split text into chunks of exactly `max_tokens`.
        Optional overlap for sliding-window processing.
        Args:
            text (str): The input text to chunk.
            max_tokens (int): The maximum number of tokens per chunk.
            overlap (int, optional): The number of overlapping tokens between chunks. Defaults to 0.
            return_ids (bool, optional): Whether to return token IDs instead of text. Defaults to False.
        Returns:
            list[str]: A list of text chunks.
        """

        if overlap >= max_tokens:
            raise ValueError("overlap must be strictly less than max_tokens")
        all_ids = self._tokenizer.encode(text)
        total = len(all_ids)
        stride = max_tokens - overlap
        id_chunks = [all_ids[i : i + max_tokens] for i in range(0, total, stride)]
        if return_ids:
            return id_chunks
        return [self._tokenizer.decode(chunk) for chunk in id_chunks]
